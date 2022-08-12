from odoo import _, api, fields, models


class Publisher(models.Model):
    _name = 'open.library.publisher'
    _description = 'Publisher'

    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner',
                                 string='partner',
                                 required=True,
                                 ondelete="restrict")

    book_ids = fields.One2many('open.library.book',
                               'publisher_id',
                               string='publisher')
