from odoo import models, fields, api
from odoo.exceptions import UserError

class TerminateContractWizard(models.TransientModel):
    _name = 'terminate.contract.wizard'
    _description = 'Terminate Contract Wizard'

    company_name_repeat = fields.Char()
    company_name = fields.Char(string='Company Name', readonly=True)
    company_name_match = fields.Boolean(string='Company Name Match', compute='_compute_company_name_match', readonly=True, store=False)
    client_contract_ids = fields.Many2one('proper.client.contract', string='Contract', required=True)
    reason_for_termination = fields.Text(string='Reason for Termination')

    @api.depends('company_name', 'company_name_repeat')
    def _compute_company_name_match(self):
        for record in self:
            record.company_name_match = record.company_name == record.company_name_repeat


    def terminate_contract(self):
        if self.company_name != self.company_name_repeat:
            raise UserError("The entered company name does not match the actual company name.")
        
        active_contracts = self.env['proper.client.contract'].search([('state', '=', 'active')])

        fields = self.env['proper.client.contract'].fields_get()
        if 'reason_for_termination' in fields:
            active_contracts.write({'state': 'terminated', 'reason_for_termination': self.reason_for_termination})
        else:
            active_contracts.write({'state': 'terminated'})

        for contract in active_contracts:
            contract.partner_id._compute_current_contract_state()
            
