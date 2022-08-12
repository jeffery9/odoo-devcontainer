from odoo import _, api, fields, models


class Library(models.Model):
    _name = 'open.library.library'
    _description = 'Library'

    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner',
                                 string='partner',
                                 required=True,
                                 ondelete="restrict")

    book_item_ids = fields.One2many('open.library.book.item',
                                    'lib_id',
                                    string='book item')

    member_ids = fields.One2many('open.library.member',
                                 'lib_id',
                                 string='member')

    librarian_ids = fields.One2many('open.library.librarian',
                                    'lib_id',
                                    string='librarian')

    book_ids = fields.Many2many('open.library.book', string='book')

    catalog_ids = fields.Many2many('open.library.catalog', string='catalog')
