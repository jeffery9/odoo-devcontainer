from odoo import _, api, fields, models

class Member(models.Model):
    _name = 'open.library.member'
    _description = 'Member'
    
    _inherits = {'open.library.user': 'user_id'}

    user_id = fields.Many2one('open.library.user', string='user', required=True, ondelete="restrict")

    lib_id = fields.Many2one('open.library.library', string='library')
