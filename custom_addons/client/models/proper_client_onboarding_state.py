from odoo import models, fields

class ClientOnboardingState(models.Model):
    _name = 'proper.client.onboarding.state'
    _description = 'Client Onboarding State'
    _order = 'sequence asc'

    allowed_next_state_ids = fields.Many2many(
        'proper.client.onboarding.state',
        relation='onboarding_state_relation',
        column1='state_id', 
        column2='next_state_id',  
        string='Allowed Next State'
    )
    is_final = fields.Boolean(string='Final State?')
    is_initial = fields.Boolean(string='Initial State?')
    name = fields.Char(string='Name')
    sequence = fields.Integer(string='Sequence')
    task_ids = fields.One2many('proper.client.onboarding.task.template', 'state_id')