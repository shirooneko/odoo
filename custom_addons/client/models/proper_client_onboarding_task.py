from odoo import models, fields

class ClientOnboardingTask(models.Model):
    _name = 'proper.client.onboarding.task'
    _description = 'Client Onboarding Task'
    _order = 'id'

    actual_completion_date = fields.Datetime(string='Actual Completion Date')
    attachment = fields.Binary(string='Attachment')
    completed_by = fields.Many2one('res.users', string='Completed By')
    delta_completion_days = fields.Integer(string='Days Late')
    is_completed = fields.Boolean(string='Completed?')
    is_optional = fields.Boolean(string='Optional Task?')
    name = fields.Char(string='Name')
    notes = fields.Html(string='Notes')
    onboarding_id = fields.Many2one('proper.client.onboarding', string='Onboarding')
    pic_ids = fields.Many2many('res.users', string='PICs')
    planned_completion_date = fields.Datetime(string='Planned Completion Date')
    sequence = fields.Integer(string='Sequence')
    state_id = fields.Many2one('proper.client.onboarding.state', string='State')
    target_days_completed = fields.Integer(string='Target Days')
    task_template_id = fields.Many2one('proper.client.onboarding.task.template', string='Task')