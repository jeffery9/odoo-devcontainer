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

    name = fields.Char('name')
    isbn = fields.Char('isbn')
    summary = fields.Html('summary')
    cover = fields.Image('cover', max_width=1024, max_height=1204)
    price = fields.Float('price')
    publish_date = fields.Date('Publish Date')
    publisher_id = fields.Many2one('open.library.publisher', string='publiser')