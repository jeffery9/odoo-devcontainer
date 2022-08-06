from odoo import _, api, fields, models


class User(models.Model):
    _name = 'open.library.user'
    _description = 'User'

    _inherit = 'res.partner'

    card_number = fields.Char('Card Number')