from odoo import _, api, fields, models


class User(models.Model):
    _name = 'open.library.user'
    _description = 'User'

    _inherits = {'res.users': 'user_id'}

    user_id = fields.Many2one('res.users',
                              string='user',
                              required=True,
                              ondelete='restrict')

    card_number = fields.Char('Card Number')
