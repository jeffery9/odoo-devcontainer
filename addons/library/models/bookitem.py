from odoo import _, api, fields, models


class BookItem(models.Model):
    _name = 'book.item'
    _description = 'Book Item'
    

    book_id = fields.Many2one('book', string='book')

    lending_ids = fields.One2many('book.lending', 'book_item_id', string='lending')

