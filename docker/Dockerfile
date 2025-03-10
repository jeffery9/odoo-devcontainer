FROM odoo:18.0
USER root

RUN set -x;\
 sed -i "s/deb.ubuntu.com/mirrors.aliyun.com/"  /etc/apt/sources.list && \ 
 sed -i "s/archive.ubuntu.com/mirrors.aliyun.com/"  /etc/apt/sources.list && \ 
 sed -i "s/security.ubuntu.com/mirrors.aliyun.com/"  /etc/apt/sources.list 

RUN set -x; \
        apt-get update \
        && apt-get install -y procps sudo git git-lfs \
        && rm -rf /var/lib/apt/lists/*

# override odoo source codes
# COPY odoo18/odoo  /usr/lib/python3/dist-packages/odoo

RUN set -x; \
        pip3 install -i https://mirrors.aliyun.com/pypi/simple  --upgrade pip 

COPY  requirements.txt  ./
RUN set -x; \
        pip3 install -i https://mirrors.aliyun.com/pypi/simple  -r ./requirements.txt

RUN usermod -aG sudo odoo
RUN usermod -s /bin/bash  odoo
RUN echo "odoo:odoo" | chpasswd
# Set default user when running the container
USER odoo
