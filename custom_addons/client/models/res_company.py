from odoo import models, fields

class ResCompany(models.Model):
    _name = 'res.company'
    _description = 'Companies'
    _order = 'sequence, name'
    _inherit = 'res.company'


    # Add your new fields here
    sequence = fields.Integer('Sequence')