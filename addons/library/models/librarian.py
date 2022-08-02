from odoo import _, api, fields, models

class Librarian(models.Model):
    _name = 'librarian'
    _description = 'Librarian'
    
    _inherits = {'user': 'user_id'}

    user_id = fields.Many2one('user', string='user')