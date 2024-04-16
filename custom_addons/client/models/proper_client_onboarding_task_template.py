from odoo import models, fields

class ClientOnboardingTaskTemplate(models.Model):
    _name = 'proper.client.onboarding.task.template'
    _description = 'Client Onboarding Task Template'
    _order = 'sequence asc'

    is_optional = fields.Boolean(string='Optional Task?')
    name = fields.Char(string='Name')
    notes = fields.Html(string='Notes')
    sequence = fields.Integer(string='Sequence')
    state_id = fields.Many2one('proper.client.onboarding.state', string='State')
    target_days_completed = fields.Integer(string='Target Days')
    task_ids = fields.One2many('proper.client.onboarding.task', 'task_template_id')