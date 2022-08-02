from odoo import _, api, fields, models


class Catalog(models.Model):
    _name = 'catalog'
    _description = 'Catalog'
    

    lib_id = fields.Many2one('library', string='library')

    book_ids = fields.One2many('book', 'cat_id', string='book')