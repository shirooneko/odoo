from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class ClientOnboardingTask(models.Model):
    _name = 'proper.client.onboarding.task'
    _description = 'Client Onboarding Task'
    _order = 'id'

    # Fields
    actual_completion_date = fields.Datetime(string='Actual Completion Date', compute='_compute_actual_completion_date', store=True)
    attachment = fields.Binary(string='Attachment')
    completed_by = fields.Many2one('res.users', string='Completed By', default=lambda self: self.env.user.id)
    delta_completion_days = fields.Integer(string='Days Late', compute='_compute_delta_completion_days', store=True)
    is_completed = fields.Boolean(string='Completed?', default=False, store=True)
    is_optional = fields.Boolean(string='Optional Task?', store=True, required=False)
    name = fields.Char(string='Name', compute='_compute_task_name', inverse='_set_task_name', required=True, store=True)
    notes = fields.Html(string='Notes')
    onboarding_id = fields.Many2one('proper.client.onboarding', string='Onboarding')
    pic_ids = fields.Many2many('res.users', string='PICs')
    planned_completion_date = fields.Datetime(string='Planned Completion Date', required=False, store=True)
    sequence = fields.Integer(string='Sequence')
    state_id = fields.Many2one('proper.client.onboarding.state', string='State')
    target_days_completed = fields.Integer(string='Target Days')
    task_template_id = fields.Many2one('proper.client.onboarding.task.template', string='Task')
    
    # Compute Methods
    @api.depends('task_template_id')
    def _compute_task_name(self):
        for task in self:
            task.name = task.task_template_id.name if task.task_template_id else False

    def _set_task_name(self):
        for task in self:
            if task.task_template_id:
                task.task_template_id.name = task.name

    @api.depends('is_completed')
    def _compute_actual_completion_date(self):
        for task in self:
            if task.is_completed:
                task.actual_completion_date = fields.Datetime.now()
            else:
                task.actual_completion_date = False

    @api.depends('planned_completion_date', 'actual_completion_date')
    def _compute_delta_completion_days(self):
        for task in self:
            if task.actual_completion_date and task.planned_completion_date:
                planned_date = task.planned_completion_date
                actual_date = task.actual_completion_date
                delta = actual_date - planned_date
                task.delta_completion_days = delta.days if delta.days > 0 else 0
            else:
                task.delta_completion_days = 0

    # Onchange Methods
    @api.onchange('state_id')
    def _onchange_state_id(self):
        for task in self:
            if task.onboarding_id:
                task.state_id = task.onboarding_id.state_id.id

    @api.onchange('onboarding_id')
    def _onchange_onboarding_id(self):
        if self.onboarding_id and not self.state_id:
            self.state_id = self.onboarding_id.state_id

