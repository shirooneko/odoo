from odoo import models, fields, api
from odoo.tools.translate import _

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
    
    contract_number = fields.Char(string='Contract Number', help='Contract Number')
    current_contract_state = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('expired', 'Expired'), ('terminated', 'Terminated')], 
                                              compute='_compute_current_contract_state', string='Current Contract State', store=True)
    
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
        
    @api.depends('is_company', 'client_contract_ids.state')
    def _compute_current_contract_state(self):
        for record in self:
            active_contract = record.client_contract_ids.filtered(lambda c: c.state in ['active', 'terminated']).sorted('date', reverse=True)[:1]
            if active_contract:
                record.current_contract_state = active_contract.state
            else:
                record.current_contract_state = False
    
