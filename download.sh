#!/bin/bash

wget https://nightly.odoo.com/18.0/nightly/src/odoo_18.0.latest.zip
unzip -oqq odoo_18.0.latest.zip  -d docker/ && mv docker/odoo-18*  docker/odoo18
