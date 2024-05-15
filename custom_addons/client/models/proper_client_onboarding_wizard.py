from odoo import models, fields, api
from odoo.exceptions import UserError


class PartnerOnboardingWizard(models.TransientModel):
    _name = 'proper.client.onboarding.wizard'
    _description = 'Partner Onboarding Wizard'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True, default=lambda self: self._context.get('default_partner_id'))
    onboarding_id = fields.Many2one('proper.client.onboarding', string='Onboarding')
    state_id = fields.Many2one('res.country.state', string='State')
    actual_date = fields.Date(string='Actual End Date')
    target_date = fields.Date(string='Target End Date')
    notes = fields.Html(string='Notes')
    attachment = fields.Binary(string='Attachment')
    
    def generate_onboarding(self):
        if self.target_date:
            vals = {
                'partner_id': self.partner_id.id,
                'target_date': self.target_date,
                'notes': self.notes,
                'attachment': self.attachment,
            }
            onboarding = self.env['proper.client.onboarding'].create(vals)

            # Copy tasks from task templates
            if onboarding.task_template_id:
                task_template = onboarding.task_template_id
                for task in task_template.task_ids:
                    task_vals = {
                        'name': task.name,
                        'planned_completion_date': task.planned_completion_date,
                        'attachment': task.attachment,
                        'state_id': task.state_id.id,
                        'is_optional': task.is_optional,
                        'task_template_id': task_template.id,
                        'onboarding_id': onboarding.id,
                    }
                    self.env['proper.client.onboarding.task'].create(task_vals)

            self.partner_id.write({'onboarding_id': onboarding.id})
        else:
            raise UserError("Target End Date is required.")

