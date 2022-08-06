from odoo import _, api, fields, models


class Book(models.Model):
    _name = 'open.library.book'
    _description = 'Book'

    cat_id = fields.Many2one('open.library.catalog', string='catalog')

    book_item_ids = fields.One2many('open.library.book.item',
                                    'book_id',
                                    string='book item')

    author_ids = fields.Many2many('open.library.author',
                                  relation='author_book_rel',
                                  column1='book_id',
                                  column2='author_id',
                                  string='author')
