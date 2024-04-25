from odoo import models, fields

class ResPartnerBank(models.Model):
    _name = 'res.users'
    _description = 'User'
    _inherit = 'res.users'


    # Add your new fields here
    sequence = fields.Integer('Sequence')