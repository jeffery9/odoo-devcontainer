from odoo import _, api, fields, models

class Library(models.Model):
    _name = 'library'
    _description = 'Library'
    
    _inherit = 'res.partner'

    catalog_ids = fields.One2many('catalog', 'lib_id', string='catalog')    

    member_ids = fields.One2many('member', 'lib_id', string='member')   

    librarian_ids = fields.One2many('librarian', 'lib_id', string='librarian')

    