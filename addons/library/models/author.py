from odoo import _, api, fields, models

class Author(models.Model):
    _name = 'open.library.author'
    _description = 'Author'
    
    author_ids = fields.Many2many('open.library.book', relation='author_book_rel', column1='author_id', column2='book_id', string='author')