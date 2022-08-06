from odoo import _, api, fields, models

class BookLending(models.Model):
    _name = 'open.library.book.lending'
    _description = 'Book Lending'
    
    book_item_id = fields.Many2one('open.library.book.item', string='Book Item')

    member_id = fields.Many2one('open.library.member', string='member')