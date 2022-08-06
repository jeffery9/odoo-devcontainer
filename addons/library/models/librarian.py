from odoo import _, api, fields, models

class Librarian(models.Model):
    _name = 'open.library.librarian'
    _description = 'Librarian'
    
    _inherits = {'open.library.user': 'user_id'}

    user_id = fields.Many2one('open.library.user', string='user', required=True, ondelete="restrict")

    lib_id = fields.Many2one('open.library.library', string='library')
