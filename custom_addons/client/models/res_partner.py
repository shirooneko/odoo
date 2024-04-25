from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _name = 'res.partner'
    _description = 'Partner'
    _order = 'complete_name ASC, id DESC'
    _inherit = 'res.partner'

    is_client = fields.Boolean(string='Is a client', compute='_compute_is_client')
    client_contract_ids = fields.One2many('proper.client.contract', 'partner_id', string='Client Contracts')
    
    bank_ids = fields.One2many(
        comodel_name='res.partner.bank',
        inverse_name='partner_id',
        string='Banks',
        help='Properties'
    )
    
    onboarding_id = fields.Many2one('proper.client.onboarding', string='Onboarding', inverse_name='partner_id')
    
    latest_contract = fields.Char(string='Latest Contract',compute="_compute_latest_contract", help='Contract Number')
    
    current_contract_state = fields.Selection([
        ('draft', 'Draft'), 
        ('active', 'Active'), 
        ('expired', 'Expired'), 
        ('terminated', 'Terminated')], 
        compute='_compute_current_contract_state', string='Contract State', store=True)
    
    @api.depends('is_company')
    def _compute_is_client(self):
        for record in self:
            record.is_client = record.is_company
            
    def action_contract(self):
        self.ensure_one()
        active_contracts = self.client_contract_ids.filtered(lambda c: c.state == 'active')
        contract_numbers = active_contracts.mapped('contract_number')
        return {
            'name': _('Confirm Termination of Contract for %s' % ', '.join(contract_numbers)),
            'type': 'ir.actions.act_window',
            'res_model': 'terminate.contract.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
            'default_company_name': self.name,
            },
        }
        
    def action_target_onboarding(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Target Onboarding',
            'res_model': 'proper.client.onboarding.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_partner_id': self.id,
            },
        }
        
    def action_view_onboarding(self):
        self.ensure_one()
        if self.onboarding_id:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Onboarding',
                'res_model': 'proper.client.onboarding',
                'view_mode': 'form',
                'res_id': self.onboarding_id.id,
            }
        else:
            raise UserError("No onboarding found for this partner.")

    @api.depends('is_company', 'client_contract_ids.state')
    def _compute_current_contract_state(self):
        for record in self:
            contracts_with_date = record.client_contract_ids.filtered(lambda r: r.create_date)
            latest_contract = contracts_with_date.sorted('create_date', reverse=True)[:1]
            if latest_contract:
                record.current_contract_state = latest_contract.state
            else:
                record.current_contract_state = False
    
    @api.depends('client_contract_ids')
    def _compute_latest_contract(self):
        for record in self:
            contracts_with_date = record.client_contract_ids.filtered(lambda r: r.create_date)
            latest_contract = contracts_with_date.sorted('create_date', reverse=True)[:1]
            record.latest_contract = latest_contract.contract_number if latest_contract else ''
    