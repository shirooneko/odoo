from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ClientOnboardingState(models.Model):
    _name = 'proper.client.onboarding.state'
    _description = 'Client Onboarding State'
    _order = 'sequence asc'

    allowed_next_state_ids = fields.Many2many(
        'proper.client.onboarding.state',
        relation='allowed_next_state_relation',  # change this to a unique name
        column1='state_id', 
        column2='next_state_id',  
        string='Allowed Next State'
    )
    is_final = fields.Boolean(string='Final State?')
    is_initial = fields.Boolean(string='Initial State?')
    name = fields.Char(string='Name')
    sequence = fields.Integer(string='Sequence')
    task_template_id = fields.One2many('proper.client.onboarding.task.template', 'state_id')

    @api.constrains('is_final', 'is_initial')
    def _check_state(self):
        for record in self:
            if record.is_final and record.is_initial:
                raise ValidationError("A state cannot be both an initial and final state.")

    @api.constrains('is_initial')
    def _check_initial_state(self):
        initial_states = self.search([('is_initial', '=', True)])
        if len(initial_states) > 1:
            raise ValidationError("There can only be one initial state.")

    @api.constrains('is_final')
    def _check_final_state(self):
        final_states = self.search([('is_final', '=', True)])
        if len(final_states) > 1:
            raise ValidationError("There can only be one final state.")
        
    
    

