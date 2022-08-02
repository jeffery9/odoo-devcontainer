from odoo import _, api, fields, models

class Member(models.Model):
    _name = 'member'
    _description = 'Member'
    
    _inherits = {'user': 'user_id'}

    user_id = fields.Many2one('user', string='user')