FROM odoo:16.0
MAINTAINER Odoo S.A. <info@odoo.com>
USER root

RUN set -x;\
 sed -i "s/deb.debian.org/mirrors.aliyun.com/"  /etc/apt/sources.list && \ 
 sed -i "s/security.debian.org/mirrors.aliyun.com/"  /etc/apt/sources.list 

RUN set -x; \
        apt-get update \
        && apt-get install -y procps sudo git git-lfs \
                python3 \
                python3-babel \
                python3-dateutil \
                python3-decorator \
                python3-docutils \
                python3-gevent \
                python3-jinja2 \
                python3-libsass \
                python3-lxml \
                python3-magic \
                python3-num2words \
                python3-odf \
                python3-ofxparse \
                python3-openssl \
                python3-passlib \
                python3-pdfminer \
                python3-phonenumbers \
                python3-pil \
                python3-pip \
                python3-polib \
                python3-psutil \
                python3-psycopg2 \
                python3-pydot \
                python3-pyldap \
                python3-pypdf2 \
                python3-qrcode \
                python3-renderpm \
                python3-reportlab \
                python3-requests \
                python3-serial \
                python3-setuptools \
                python3-slugify \
                python3-stdnum \
                python3-tz \
                python3-usb \
                python3-vobject \
                python3-watchdog \
                python3-werkzeug \
                python3-xlrd \
                python3-xlsxwriter \
                python3-xlwt \
                python3-zeep \
        && rm -rf /var/lib/apt/lists/*

# override odoo source codes
# COPY odoo16/odoo  /usr/lib/python3/dist-packages/odoo

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
