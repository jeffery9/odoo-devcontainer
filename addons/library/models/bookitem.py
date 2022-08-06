from odoo import _, api, fields, models


class BookItem(models.Model):
    _name = 'open.library.book.item'
    _description = 'Book Item'
    

    book_id = fields.Many2one('open.library.book', string='book')

    lending_ids = fields.One2many('open.library.book.lending', 'book_item_id', string='lending')

