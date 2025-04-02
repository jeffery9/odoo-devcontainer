from mcp.server.fastmcp import FastMCP
import subprocess
import os
import asyncio
import yaml
from flask import Response
import time
import shutil
import zipfile
import io
import base64

import logging

# 读取 YAML 配置文件
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

DOCKER_COMPOSE_PATH = config['odoo']['docker_compose_path']
ODOO_SERVICE_NAME = config['odoo']['odoo_service_name']
ODOO_MODULE_PATH = config['odoo']['odoo_module_path']
ODOO_TEST_MODULE = config['odoo']['odoo_test_module']
MCP_SERVER_PORT = config['mcp']['mcp_server_port']

try:
    mcp = FastMCP("OdooMCP", port=MCP_SERVER_PORT)
    logging.info(f"MCP Server running on port {MCP_SERVER_PORT}")
except Exception as e:
    logging.error(f"Failed to start MCP Server: {e}")
    exit(1)

def generate_prompt(user_story: str, acceptance_criteria: list) -> str:
    """根据用户故事和验收条件动态生成提示词"""
    
    # 将验收条件转化为列表形式
    criteria = "\n".join([f"{i+1}. {criterion}" for i, criterion in enumerate(acceptance_criteria)])

    prompt_template = """
任务：你是一位精通 Odoo 开发的 AI 助手，负责根据产品负责人提供的用户故事和验收条件，生成符合要求的 Odoo 代码，并编写完整的 Odoo 测试用例。

用户故事：
{user_story}

验收条件：
{acceptance_criteria}

步骤：

1. **分析用户故事和验收条件：**
   * 仔细阅读并理解产品负责人提供的用户故事和验收条件。
   * 明确需求的具体功能、业务逻辑和预期行为。

2. **生成 Odoo 后端代码：**
   * 根据分析结果，编写符合 Odoo 开发规范的模型、视图、报表等后端代码。
   * 包括业务模型的创建、数据字段的定义，视图（如表单视图、树形视图）和报表的开发。

3. **开发 Web 端功能：**
   * 为前端功能开发提供支持，例如：
      - 创建自定义的 Web 控制器（如 REST API、Web 表单处理）。
      - 开发动态的 **Web 表单**，并将其与后端模型进行绑定。
      - 定义 Odoo Web 客户端所需的 **JavaScript** 交互功能，如表单验证、动态加载等。
      - 设计和实现自定义的菜单项和页面视图。

4. **编写 Odoo 测试用例：**
   * 基于验收条件，编写完整、细致的测试用例。
   * 测试用例应覆盖所有可能的场景，包括正常情况、边界情况和异常情况。
   * 测试用例应符合 Odoo 的测试框架（unittest），并以 `test_` 开头。

5. **执行测试用例：**
   * 使用 MCP 自动化测试工具在 Odoo 测试环境中运行测试用例。
   * 记录测试结果，包括通过的测试用例和失败的测试用例。

6. **代码改进和测试用例调整：**
   * 如果测试用例未能全部通过，则分析失败原因，并对代码进行改进。
   * 根据代码的修改，相应地调整测试用例。
   * 重复步骤 4 和 5，直到所有测试用例均通过。

7. **输出结果：**
   * 提供最终的 Odoo 后端代码和 Web 端功能代码。
   * 提供测试结果报告，包括通过的测试用例和失败的测试用例（如果存在）。
   * 给出代码的改进说明。

要求：

* 代码必须符合 Odoo 开发规范。
* 测试用例必须覆盖所有验收条件。
* 通过所有测试用例意味着代码符合需求。
* 使用 python unittest 标准库进行编写测试用例。

    """ # 返回根据用户故事和验收条件动态生成的提示词 
    return prompt_template.format(user_story=user_story, acceptance_criteria=criteria)

@mcp.tool()
def generate_code(user_story: str, acceptance_criteria: list) -> str:
    """根据用户故事和验收条件，采取 reAct 模式生成 Odoo 代码的提示词"""
    # 动态生成提示词
    prompt = generate_prompt(user_story, acceptance_criteria)

    return prompt

@mcp.tool()
def deploy_code(zip_content: str) -> str:
    """接收 ZIP 压缩包内容，解压并部署到 Docker 容器"""
    try:
        # 1. 解析 ZIP 数据（Base64 解码）
        zip_bytes = base64.b64decode(zip_content)
        zip_stream = io.BytesIO(zip_bytes)

        # 2. 确保目标目录干净
        generated_dir = os.path.join(os.getcwd(), ODOO_TEST_MODULE)
        if os.path.exists(generated_dir):
            shutil.rmtree(generated_dir)
        os.makedirs(generated_dir, exist_ok=True)

        # 3. 解压 ZIP 到指定目录
        with zipfile.ZipFile(zip_stream, 'r') as zip_ref:
            zip_ref.extractall(generated_dir)

        logging.info(f"Extracted module '{ODOO_TEST_MODULE}' to {generated_dir}")

        # 4. 复制解压后的模块到 Odoo 模块路径
        odoo_module_dest = os.path.join(ODOO_MODULE_PATH, ODOO_TEST_MODULE)
        if os.path.exists(odoo_module_dest):
            shutil.rmtree(odoo_module_dest)
        shutil.copytree(generated_dir, odoo_module_dest)

        logging.info(f"Copied module to Odoo path: {odoo_module_dest}")

        # 5. 重启 Odoo 容器
        subprocess.run(['docker-compose', '-f', DOCKER_COMPOSE_PATH, 'restart', ODOO_SERVICE_NAME], check=True)

        return f"Module '{ODOO_TEST_MODULE}' deployed successfully"
    except zipfile.BadZipFile:
        return "Error: Invalid ZIP file format"
    except subprocess.CalledProcessError as e:
        logging.error(f"Deployment failed: {e.stderr}")
        return f"Error: {e.stderr}"
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"Unexpected error: {e}"

@mcp.tool()
def start_instance() -> str:
    """启动 Odoo Docker 实例"""
    try:
        subprocess.run(['docker-compose', '-f', DOCKER_COMPOSE_PATH, 'up', '-d', ODOO_SERVICE_NAME])
        return "Odoo instance started successfully"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def stop_instance() -> str:
    """停止 Odoo Docker 实例"""
    try:
        subprocess.run(['docker-compose', '-f', DOCKER_COMPOSE_PATH, 'down'])
        return "Odoo instance stopped successfully"
    except Exception as e:
        return f"Error: {e}"
    
@mcp.tool()
def update_container() -> str:
    """更新 Odoo Docker 容器"""
    try:
        logging.info("Pulling the latest Odoo image...")
        subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_PATH, "pull"], check=True)

        logging.info("Rebuilding and restarting the Odoo container...")
        subprocess.run(["docker-compose", "-f", DOCKER_COMPOSE_PATH, "up", "--build", "-d"], check=True)

        logging.info("Removing unused Docker images...")
        subprocess.run(["docker", "image", "prune", "-f"], check=True)

        return "Odoo container updated successfully"
    except subprocess.CalledProcessError as e:
        logging.error(f"Container update failed: {e.stderr}")
        return f"Error updating container: {e.stderr}"
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"Unexpected error: {e}"


@mcp.tool()
def install_module(module_name: str) -> str:
    """在 Odoo Docker 容器中安装指定模块"""
    try:
        logging.info(f"Installing module: {module_name}")
        
        # 进入 Odoo 容器并安装模块
        result = subprocess.run(
            [
                "docker-compose", "-f", DOCKER_COMPOSE_PATH, "exec", 
                ODOO_SERVICE_NAME, "odoo", "-u", module_name, "--stop-after-init"
            ], 
            capture_output=True, text=True, check=True
        )
        
        return f"Module '{module_name}' installed successfully\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        logging.error(f"Module installation failed: {e.stderr}")
        return f"Error installing module '{module_name}': {e.stderr}"
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"Unexpected error: {e}"

@mcp.tool()
def run_all_tests() -> str:
    """在 Odoo Docker 容器中运行测试用例"""
    try:
        result = subprocess.run(['docker-compose', '-f', DOCKER_COMPOSE_PATH, 'exec', ODOO_SERVICE_NAME, 'odoo', '-i', ODOO_TEST_MODULE, '--test-enable'], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def run_tests(module_name: str) -> str:
    """在 Odoo Docker 容器中运行指定模块的测试用例"""
    try:
        logging.info(f"Running tests for module: {module_name}")

        # 在 Odoo 容器中运行测试
        result = subprocess.run(
            [
                "docker-compose", "-f", DOCKER_COMPOSE_PATH, "exec",
                ODOO_SERVICE_NAME, "odoo", "-i", module_name, "--test-enable", "--stop-after-init"
            ],
            capture_output=True, text=True, check=True
        )

        return f"Tests for module '{module_name}' completed successfully:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        logging.error(f"Module test failed: {e.stderr}")
        return f"Error running tests for '{module_name}': {e.stderr}"
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return f"Unexpected error: {e}"


if __name__ == "__main__":
    mcp.run()