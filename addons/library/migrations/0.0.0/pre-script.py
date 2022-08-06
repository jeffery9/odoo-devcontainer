from odoo import api, SUPERUSER_ID

import logging
__logger = logging.getLogger(__name__)

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    __logger.warning(' >>>> pre')