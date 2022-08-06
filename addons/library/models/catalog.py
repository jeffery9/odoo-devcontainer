from odoo import _, api, fields, models


class Catalog(models.Model):
    _name = 'open.library.catalog'
    _description = 'Catalog'
    

    lib_id = fields.Many2one('open.library.library', string='library')

    book_ids = fields.One2many('open.library.book', 'cat_id', string='book')