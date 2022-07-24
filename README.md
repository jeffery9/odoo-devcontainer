# develop Odoo in docker

### 介绍
coding debugging Odoo in Docker

### 安装运行环境

#### Ubuntu
- 安装 docker 

ref. https://docs.docker.com/engine/install/ubuntu/

- 安装 docker compose

#### MAC 
- 安装 docker for desktop

ref. https://docs.docker.com/desktop/mac/install/

- 安装 docker compose


#### Windows 
- 安装 docker for desktop

ref. https://docs.docker.com/desktop/windows/install/

- 安装 docker compose


 **重要说明**

. 根目录下 放置 Odoo 源代码， 即 包含 `odoo-bin 的 Odoo 源代码整个目录

. 非官方 Addons 存放在根目录 addons 下


### 运行odoo

1. 克隆本仓库到本地目录，例如 `odoo-docker`
1. 执行下面的命令运行 Odoo

```bash

cd odoo-docker
docker-compose -p odoo15 up -d

```
3. docker将会拉取相关的镜像，然后运行项目
4. 浏览器打开 http://localhost:8000



### FAQ

1. #### Docker 报错 `Get https://registry-1.docker.io/v2/: unable to connect to HTTP proxy 127.0.0.1:1080` , 此时你需要使用 Docker 镜像注册中心
 
  调整 docker 配置增加中国本地注册器镜像，
  ```
  {
    "registry-mirrors": [
      "https://registry.docker-cn.com",
      "https://docker.mirrors.ustc.edu.cn"
    ]
  }
  ```


