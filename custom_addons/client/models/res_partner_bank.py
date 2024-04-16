from odoo import models, fields

class ResPartnerBank(models.Model):
    _name = 'res.partner.bank'
    _description = 'Parner Bank'
    _inherit = 'res.partner.bank'


    # Add your new fields here
    sequence = fields.Integer('Sequence')