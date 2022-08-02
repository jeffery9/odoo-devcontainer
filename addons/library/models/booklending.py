from odoo import _, api, fields, models

class BookLending(models.Model):
    _name = 'book.lending'
    _description = 'Book Lending'
    
    book_item_id = fields.Many2one('book.item', string='Book Item')

    member_id = fields.Many2one('member', string='member')