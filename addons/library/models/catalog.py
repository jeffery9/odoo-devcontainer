from odoo import _, api, fields, models


class Catalog(models.Model):
    _name = 'open.library.catalog'
    _description = 'Catalog'

    _parent_store = True

    name = fields.Char('name')

    child_id = fields.One2many('open.library.catalog',
                               'parent_id',
                               string='Child IDs')
    parent_id = fields.Many2one('open.library.catalog',
                                string='Parent Catalog',
                                index=True,
                                ondelete="restrict")

    lib_id = fields.Many2one('open.library.library', string='library')

    book_ids = fields.One2many('open.library.book', 'cat_id', string='book')