FROM odoo:15.0
MAINTAINER jeffery <jeffery9@gmail.com>

USER root
RUN echo "root:Docker!" | chpasswd

RUN set -x;\
    usermod odoo -s /bin/bash

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
    && apt-get install -y procps build-essential libjpeg-dev libxslt-dev libzip-dev libldap2-dev libsasl2-dev git python3-dev \
            python3-setuptools \
            python3-pip \
            python3-wheel \
            python3-babel \
            python3-decorator \
            python3-docutils \
            python3-freezegun \
            python3-gevent \
            python3-greenlet \
            python3-idna \
            python3-jinja2 \
            python3-ldap \ 
            python3-lxml \
            python3-libsass \
            python3-markupsafe \
            python3-mock \
            python3-num2words \
            python3-ofxparse \
            python3-passlib \
            python3-pillow \
            python3-psutil \
            python3-psycopg2 \
            python3-polib \
            python3-pydot \
            python3-dateutil \
            python3-qrcode \
            python3-reportlab \
            python3-requests \
            python3-six \
            python3-stdnum \
            python3-vobject \
            python3-werkzeug \
            python3-xlwt \
            python3-xlrd \
            python3-zeep \
            python3-num2words \
    && pip3 install -r requirements.txt -i https://mirror.sjtu.edu.cn/pypi/web/simple/ \
    && pip3 install debugpy -i https://mirror.sjtu.edu.cn/pypi/web/simple/ \
    && rm -rf /root/.cache  /var/lib/apt/lists/*


# Expose Odoo services and debugpy port
EXPOSE 8069 8071 5678

USER odoo

CMD [ "/bin/sh","-c","while sleep 1000; do :; done" ]