from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _name = 'res.partner'
    _description = 'Partner'
    _order = 'complete_name ASC, id DESC'
    _inherit = 'res.partner'

    # Fields
    is_client = fields.Boolean(string='Is a client', compute='_compute_is_client')
    client_contract_ids = fields.One2many('proper.client.contract', 'partner_id', string='Client Contracts')
    has_completed_onboarding = fields.Boolean(string='Has Completed Onboarding', compute='_compute_has_completed_onboarding')
    bank_ids = fields.One2many(comodel_name='res.partner.bank', inverse_name='partner_id', string='Banks', help='Properties')
    onboarding_id = fields.Many2one('proper.client.onboarding', string='Onboarding', inverse_name='partner_id')
    latest_contract = fields.Char(string='Latest Contract', compute="_compute_latest_contract", help='Contract Number')
    current_contract_state = fields.Selection([
        ('draft', 'Draft'), 
        ('active', 'Active'), 
        ('expired', 'Expired'), 
        ('terminated', 'Terminated')
    ], compute='_compute_current_contract_state', string='Contract State', store=True)

    # Computed Fields
    @api.depends('onboarding_id.is_completed')
    def _compute_has_completed_onboarding(self):
        for partner in self:
            partner.has_completed_onboarding = partner.onboarding_id.is_completed if partner.onboarding_id else False

    @api.depends('client_contract_ids')
    def _compute_is_client(self):
        for partner in self:
            partner.is_client = bool(partner.client_contract_ids)

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

    # Actions
    def action_terminate(self):
        self.ensure_one()
        active_contracts = self.env['proper.client.contract'].search([('partner_id', '=', self.id), ('state', '=', 'active')], limit=1)
        if active_contracts:
            return {
                'name': _('Confirm Termination of Contract for %s' % active_contracts.contract_number),
                'type': 'ir.actions.act_window',
                'res_model': 'terminate.contract.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_company_name': self.name,
                    'default_partner_id': self.id,
                },
            }
        else:
            raise UserError("No active contract found for this partner.")

    def action_contract(self):
        # Logika untuk membuka tampilan kontrak
        # Anda dapat menyesuaikan logika ini sesuai kebutuhan Anda
        return {
            'name': 'Create Contract',
            'type': 'ir.actions.act_window',
            'res_model': 'proper.client.contract',
            'view_mode': 'form',
            'view_id': False,
            'target': 'new',
            'context': {'default_partner_id': self.id}
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
