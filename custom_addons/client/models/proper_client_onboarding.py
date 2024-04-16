from odoo import models, fields

class ClientOnboarding(models.Model):
    _name = 'proper.client.onboarding'
    _description = 'Client Onboarding'
    _order = 'id'

    actual_date = fields.Date(string='Actual End Date')
    attachment = fields.Binary(string='Attachment')
    completed_task_ids = fields.One2many('proper.client.onboarding.task', 'onboarding_id')
    is_completed = fields.Boolean(string='Completed?')
    is_final = fields.Boolean(string='Final State?')
    is_initial = fields.Boolean(string='Initial State?')
    notes = fields.Html(string='Notes')
    onboarding_type = fields.Selection(selection=[
        ('onboarding', 'Onboarding'),
        ('offboarding', 'Offboarding')
        ], string='Onboarding Type') 
    partner_id = fields.Many2one('res.partner', string='Partner')
    state_id = fields.Many2one('proper.client.onboarding.state', string='State')
    target_date = fields.Date(string='Target End Date')
    todo_task_ids = fields.One2many('proper.client.onboarding.task', 'onboarding_id')