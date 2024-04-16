from odoo import models, fields

class MailActivity(models.Model):
    _name = 'mail.activity'
    _description = 'Activity'
    _order = 'date_deadline ASC, id ASC'
    _inherit = 'mail.activity'

    

