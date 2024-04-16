from odoo import models, fields

class CrmLead(models.Model):
    _name = 'crm.lead'
    _description = 'CRM'
    _inherit = 'crm.lead'
