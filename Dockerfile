FROM odoo:15.0
MAINTAINER jeffery <jeffery9@gmail.com>

USER root

RUN set -x;\
    usermod odoo -s /bin/sh

RUN set -x;\
 sed -i "s/deb.debian.org/mirror.sjtu.edu.cn/"  /etc/apt/sources.list  \ 
 && sed -i "s/security.debian.org/mirror.sjtu.edu.cn/"  /etc/apt/sources.list 

# Run Odoo in workspace instead of Odoo offical release.
RUN set -x; \
    rm /usr/bin/odoo  \
    && rm -rf /etc/odoo  \
    && rm -rf  /usr/lib/python3/dist-packages/odoo 

COPY ./requirements.txt ./requirements.txt 

RUN set -x; \
    apt-get update \
    && apt-get install -y build-essential git python3-dev python3-setuptools python3-wheel python3-ldap \
    && pip3 install -r requirements.txt -i https://mirror.sjtu.edu.cn/pypi/web/simple/ \
    && pip3 install debugpy -i https://mirror.sjtu.edu.cn/pypi/web/simple/ \
    && rm -rf /root/.cache  /var/lib/apt/lists/*


# Expose Odoo services and debugpy port
EXPOSE 8069 8071 5678

USER odoo
