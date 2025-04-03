import yaml
import os
import subprocess
import requests
import json
from langgraph import Graph, Node

# Qwen API 配置
QWEN_API_URL = "https://api.qwen.com/v1/chat"  # 替换为实际 API 地址
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "your_api_key_here")  # 使用环境变量存储密钥

# 调用 Qwen API
def call_qwen(prompt):
    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 500
    }
    try:
        response = requests.post(QWEN_API_URL, headers=headers, json=data)
        response.raise_for_status()  # 检查 HTTP 错误
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error calling Qwen API: {str(e)}")

# 辅助函数：安全加载 YAML 文件
def load_yaml(file_path):
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise Exception(f"Error loading YAML file: {str(e)}")

# 辅助函数：写入文件
def write_file(file_path, content):
    try:
        with open(file_path, "w") as file:
            file.write(content)
    except Exception as e:
        raise Exception(f"Error writing to file: {str(e)}")

# 定义 LangGraph
graph = Graph()

# Step 1: 解析环境配置模块
def parse_environment_config(state):
    config_file = state["config_file"]  # 假设用户提供了 YAML 配置文件路径
    config = load_yaml(config_file)
    odoo_version = config.get("odoo_version", "16.0")
    base_modules = config.get("base_modules", [])
    compose_dir = config.get("compose_directory", "./test_env")
    test_database_name = config.get("test_database_name", "test_db")  # 从配置中读取测试数据库名称
    return {
        "odoo_version": odoo_version,
        "base_modules": base_modules,
        "compose_directory": compose_dir,
        "test_database_name": test_database_name
    }

graph.add_node("ParseEnvironmentConfig", parse_environment_config)

# Step 2: 动态生成或更新 Docker Compose 文件
def generate_or_update_docker_compose_files(state):
    odoo_version = state["odoo_version"]
    base_modules = state["base_modules"]
    compose_dir = state["compose_directory"]
    compose_file_path = os.path.join(compose_dir, "docker-compose.yml")
    os.makedirs(compose_dir, exist_ok=True)

    if os.path.exists(compose_file_path):
        existing_compose = load_yaml(compose_file_path)
        current_odoo_version = existing_compose["services"]["web"]["image"].split(":")[1]
        if current_odoo_version != odoo_version:
            print(f"Updating Odoo version from {current_odoo_version} to {odoo_version}")
            existing_compose["services"]["web"]["image"] = f"odoo:{odoo_version}"
            write_file(compose_file_path, yaml.dump(existing_compose, default_flow_style=False))
        else:
            print(f"Using existing Odoo version: {odoo_version}")
    else:
        docker_compose_content = f"""
version: '3.8'
services:
  web:
    image: odoo:{odoo_version}
    depends_on:
      - db
    ports:
      - "8069:8069"
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
    volumes:
      - ./addons:/mnt/extra-addons
      - ./tests:/mnt/tests
    command: -- --dev=all
  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_PASSWORD=odoo
      - POSTGRES_USER=odoo
    volumes:
      - ./data:/var/lib/postgresql/data
"""
        write_file(compose_file_path, docker_compose_content)

    env_content = f"""
ODOO_VERSION={odoo_version}
BASE_MODULES={",".join(base_modules)}
"""
    write_file(os.path.join(compose_dir, ".env"), env_content)
    return {"compose_directory": compose_dir}

graph.add_node("GenerateOrUpdateDockerComposeFiles", generate_or_update_docker_compose_files)

# Step 3: 启动或更新测试环境
def start_or_update_test_environment(state):
    compose_dir = state["compose_directory"]
    compose_file_path = os.path.join(compose_dir, "docker-compose.yml")
    try:
        if os.path.exists(compose_file_path):
            print("Pulling latest images and updating containers...")
            subprocess.run(["docker-compose", "pull"], cwd=compose_dir, check=True)
            subprocess.run(["docker-compose", "up", "-d"], cwd=compose_dir, check=True)
            return {"environment_status": "updated"}
        else:
            print("Starting new test environment...")
            subprocess.run(["docker-compose", "up", "-d"], cwd=compose_dir, check=True)
            return {"environment_status": "started"}
    except subprocess.CalledProcessError as e:
        return {"environment_status": "failed", "error": str(e)}

graph.add_node("StartOrUpdateTestEnvironment", start_or_update_test_environment)

# Step 4: 分析现有功能并保存分析结果
def analyze_existing_features(state):
    compose_directory = state["compose_directory"]
    analysis_file = os.path.join(compose_directory, "feature_analysis.json")
    
    # 加载已有的功能分析结果（如果存在）
    if os.path.exists(analysis_file):
        with open(analysis_file, "r") as file:
            feature_analysis = json.load(file)
    else:
        feature_analysis = {}

    # 调用 LLM 分析现有功能
    prompt = f"""
You are an AI agent following the Odoo Framework, Odoo App, and Business Flow.
Your task is to analyze the existing features of the system.
Current Feature Analysis: {feature_analysis}
Instructions:
- Identify all models in the system.
- For each model, extract the following information:
  - Fields: List all fields (e.g., name, price, image).
  - Related Models: List related models (e.g., Many2one, One2many relationships).
  - Business Rules: Describe any constraints or validation rules (e.g., price must be positive).
  - Business Logic: Explain the functionality (e.g., sorting products by price).
- Organize the analysis result by model and include business rules and logic.
Output:
- Return the updated feature analysis as a dictionary with the following structure:
  {{
    "models": {{
      "model_name_1": {{
        "fields": [list of fields],
        "related_models": [list of related models],
        "business_rules": [list of business rules],
        "business_logic": [description of business logic]
      }}
    }}
  }}
"""
    result = call_qwen(prompt)
    
    # 保存更新后的功能分析结果
    with open(analysis_file, "w") as file:
        json.dump(result, file, indent=4)
    return {"feature_analysis": result["models"]}

graph.add_node("AnalyzeExistingFeatures", analyze_existing_features)

# Step 5: 汇聚环境准备结果
def join_environment_preparation(state):
    return {
        "compose_directory": state["GenerateOrUpdateDockerComposeFiles"]["compose_directory"],
        "environment_status": state["StartOrUpdateTestEnvironment"]["environment_status"],
        "feature_analysis": state["AnalyzeExistingFeatures"]
    }

graph.add_node("JoinEnvironmentPreparation", join_environment_preparation)

# Step 6: 解析需求并生成 BDD 测试用例
def parse_requirements(state):
    user_story = state["user_story"]
    acceptance_criteria = state["acceptance_criteria"]
    module_name = state["module_name"]  # 新增字段
    feature_analysis = state["feature_analysis"]

    relevant_analysis = {
        model: details for model, details in feature_analysis.items()
        if model.lower() in user_story.lower()
    }

    prompt = f"""
You are an AI agent following the Odoo Framework, Odoo App, and Business Flow.
Your task is to analyze the user story and acceptance criteria.
### User Story:
{user_story}
### Acceptance Criteria:
{acceptance_criteria}
### Relevant Feature Analysis:
{relevant_analysis}
Instructions:
- Extract the following information:
  - Models: List all models and their fields.
  - Views: Describe the UI components (e.g., form view, tree view).
  - Business Rules: Include any constraints or validation rules.
  - Business Logic: Explain the functionality.
- Convert acceptance criteria into BDD test cases using Gherkin syntax.
Output:
- Return the extracted requirements and BDD test cases as a dictionary with the following structure:
  {{
    "requirements": {{
      "models": [list of models and fields],
      "views": [list of views and their descriptions],
      "business_rules": [list of business rules],
      "business_logic": [description of business logic]
    }},
    "bdd_test_cases": {{
      "test_case_1.feature": "Gherkin syntax for test case 1",
      "test_case_2.feature": "Gherkin syntax for test case 2"
    }}
  }}
"""
    result = call_qwen(prompt)
    return {
        "requirements": result["requirements"],
        "bdd_test_cases": result["bdd_test_cases"],
        "module_name": module_name
    }

graph.add_node("ParseRequirements", parse_requirements)

# Step 7: 根据 BDD 测试用例生成测试代码
def generate_test_code(state):
    bdd_test_cases = state["bdd_test_cases"]
    compose_directory = state["compose_directory"]
    module_name = state["module_name"]

    prompt = f"""
You are an AI agent following the Odoo Framework, Odoo App, and Business Flow.
Your task is to generate Python test code based on the given BDD test cases.
BDD Test Cases:
{bdd_test_cases}
Instructions:
- Write Python test code using the Odoo testing framework.
- Ensure the test code covers all scenarios described in the BDD test cases.
Output:
- Return the generated test code as a dictionary with filenames as keys and code as values.
"""
    result = call_qwen(prompt)
    tests_dir = os.path.join(compose_directory, "tests", module_name)  # 使用 module 名称作为子目录
    os.makedirs(tests_dir, exist_ok=True)
    for filename, content in result.items():
        write_file(os.path.join(tests_dir, filename), content)
    return {"test_code_generated": True, "module_name": module_name}

graph.add_node("GenerateTestCode", generate_test_code)

# Step 8: 根据需求分析生成业务代码
def generate_business_code(state):
    requirements = state["requirements"]
    compose_directory = state["compose_directory"]
    module_name = state["module_name"]

    prompt = f"""
You are an AI agent following the Odoo Framework, Odoo App, and Business Flow.
Your task is to generate business code based on the given requirements.
Requirements:
- Models: {requirements["models"]}
- Views: {requirements["views"]}
- Business Rules: {requirements["business_rules"]}
- Business Logic: {requirements["business_logic"]}
Instructions:
- Generate Python code for models.
- Design XML views.
- Implement business rules and logic.
- Ensure the code satisfies the requirements.
Output:
- Return the generated business code as a dictionary with filenames as keys and code as values.
"""
    result = call_qwen(prompt)
    addons_dir = os.path.join(compose_directory, "addons", module_name)  # 使用 module 名称作为子目录
    os.makedirs(addons_dir, exist_ok=True)
    for filename, content in result.items():
        write_file(os.path.join(addons_dir, filename), content)
    return {"business_code_generated": True, "module_name": module_name}

graph.add_node("GenerateBusinessCode", generate_business_code)

# Step 9: 运行测试代码
def run_tests(state):
    compose_directory = state["compose_directory"]
    test_database_name = state.get("test_database_name")
    module_name = state.get("module_name")
    if not test_database_name or not module_name:
        return {"test_results": "failed", "error": "Missing test_database_name or module_name in state."}

    try:
        print(f"Installing module '{module_name}' and running tests on database '{test_database_name}'...")
        install_command = [
            "docker-compose", "exec", "web",
            "odoo-bin", "-d", test_database_name, "-i", module_name
        ]
        subprocess.run(install_command, cwd=compose_directory, check=True)

        test_command = [
            "docker-compose", "exec", "web",
            "odoo-bin", "-d", test_database_name, "--test-enable"
        ]
        result = subprocess.run(
            test_command,
            cwd=compose_directory,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return {"test_results": "All tests passed!"}
        else:
            return {"test_results": "Some tests failed.", "error": result.stderr}
    except subprocess.CalledProcessError as e:
        return {"test_results": "Some tests failed.", "error": str(e)}

graph.add_node("RunTests", run_tests)

# Step 10: 修复代码
def fix_code(state):
    error_log = state["test_results"]["error"]
    module_name = state["module_name"]

    prompt = f"""
You are an AI agent following the Odoo Framework, Odoo App, and Business Flow.
Your task is to analyze the error log and suggest fixes.
Error Log: {error_log}
Instructions:
- Identify the root cause of the error.
- Suggest a fix for the issue.
- Validate the fix against the original requirements.
- Apply the fix and update the code.
Output:
- Return the fixed code as a dictionary with filenames as keys and code as values.
"""
    fixed_code = call_qwen(prompt)
    addons_dir = os.path.join(state["compose_directory"], "addons", module_name)
    for filename, content in fixed_code.items():
        write_file(os.path.join(addons_dir, filename), content)
    return {"fixed_code": True, "module_name": module_name}

graph.add_node("FixCode", fix_code)

# Step 11: 重启容器以加载新代码
def restart_containers(state):
    compose_directory = state["compose_directory"]
    try:
        print("Restarting containers to apply new code...")
        subprocess.run(["docker-compose", "restart"], cwd=compose_directory, check=True)
        return {"restart_status": "success"}
    except subprocess.CalledProcessError as e:
        return {"restart_status": "failed", "error": str(e)}

graph.add_node("RestartContainers", restart_containers)

# 定义节点之间的连接
graph.add_edge("ParseEnvironmentConfig", "GenerateOrUpdateDockerComposeFiles")
graph.add_edge("ParseEnvironmentConfig", "StartOrUpdateTestEnvironment")
graph.add_edge("ParseEnvironmentConfig", "AnalyzeExistingFeatures")

graph.add_edge("GenerateOrUpdateDockerComposeFiles", "JoinEnvironmentPreparation")
graph.add_edge("StartOrUpdateTestEnvironment", "JoinEnvironmentPreparation")
graph.add_edge("AnalyzeExistingFeatures", "JoinEnvironmentPreparation")

graph.add_edge("JoinEnvironmentPreparation", "ParseRequirements")
graph.add_edge("ParseRequirements", "GenerateTestCode")
graph.add_edge("ParseRequirements", "GenerateBusinessCode")
graph.add_edge("GenerateTestCode", "RunTests")
graph.add_edge("GenerateBusinessCode", "RunTests")

graph.add_conditional_edge(
    "RunTests",
    lambda state: "FixCode" if "error" in state["test_results"] else "RestartContainers"
)
graph.add_edge("FixCode", "GenerateBusinessCode")

# 执行 LangGraph
def run_langgraph(user_story, acceptance_criteria, module_name, config_file):
    initial_state = {
        "config_file": config_file,
        "user_story": user_story,
        "acceptance_criteria": acceptance_criteria,
        "module_name": module_name
    }
    return graph.run(initial_state)

# 支持批量处理
def batch_process(stories_and_criteria, config_file):
    results = []
    for item in stories_and_criteria:
        user_story = item.get("user_story")
        acceptance_criteria = item.get("acceptance_criteria")
        module_name = item.get("module")  # 获取模块名称
        print(f"Processing user story: {user_story}")
        result = run_langgraph(user_story, acceptance_criteria, module_name, config_file)
        results.append({
            "user_story": user_story,
            "acceptance_criteria": acceptance_criteria,
            "module_name": module_name,
            "result": result
        })
    return results

# 后端入口点
if __name__ == "__main__":
    # 示例输入
    stories_and_criteria = [
        {
            "user_story": "As a user, I want to see a list of products.",
            "acceptance_criteria": [
                "The product list should display name, price, and image.",
                "The product list should be sortable by price."
            ],
            "module": "product_list_module"  # 模块名称
        },
        {
            "user_story": "As a user, I want to add products to my cart.",
            "acceptance_criteria": [
                "The user can select a product and add it to the cart.",
                "The cart should display the total price."
            ],
            "module": "shopping_cart_module"  # 模块名称
        }
    ]
    config_file = "./config.yaml"
    # 批量处理
    results = batch_process(stories_and_criteria, config_file)
    print("Batch Processing Results:")
    for idx, result in enumerate(results):
        print(f"Result {idx + 1}:")
        print(result)