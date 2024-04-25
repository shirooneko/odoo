from odoo import api, fields, models, exceptions, _
from dateutil.relativedelta import relativedelta
from datetime import date

class ProperClientContract(models.Model):
    _name = 'proper.client.contract'
    _description = 'Propertek Client Contract'
    _order = 'write_date desc'
    

    active = fields.Boolean('Active', default=True)
    attachment = fields.Binary('Contract Attachment')
    contract_number = fields.Char('Contract Number', default=lambda self: self._default_contract_number())
    contract_type = fields.Selection([
        ('initial', 'Initial Contract'),
        ('renewal', 'Renewal Contract'),
        ('addendum', 'Addendum')
    ], 'Contract Type', default='initial')
    create_date = fields.Datetime('Created on')
    create_uid = fields.Many2one('res.users', 'Created by')
    currency_id = fields.Many2one('res.currency', 'Contract Currency', default=lambda self: self.env.ref('base.IDR'))
    date = fields.Date('Contract Date', default=fields.Date.today())
    display_name = fields.Char('Display Name')
    duration = fields.Integer('Contract Duration', default=1)
    duration_unit = fields.Selection([
        ('month', 'Month'),
        ('years', 'Year')
    ], 'Contract Duration Unit', default='years')
    end_date = fields.Date('Contract End Date', compute='_compute_end_date', inverse='_inverse_end_date', store=True)
    notes = fields.Html('Contract Notes')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated')
    ], 'Contract State', compute='_compute_state', store=True, default='draft')
    value = fields.Float('Contract Value')
    write_date = fields.Datetime('Last Updated on')
    write_uid = fields.Many2one('res.users', 'Last Updated by')
    partner_id = fields.Many2one('res.partner', string='Partner')

    @api.depends('date', 'duration', 'duration_unit')
    def _compute_end_date(self):
        for record in self:
            if record.date and record.duration and record.duration_unit:
                if record.duration_unit == 'years':
                    record.end_date = record.date + relativedelta(years=record.duration)
                else:  # duration_unit == 'month'
                    record.end_date = record.date + relativedelta(months=record.duration)

    def _inverse_end_date(self):
        pass  # make the field readonly

    @api.depends('date', 'end_date')
    def _compute_state(self):
        for record in self:
            if record.date and record.end_date:
                today = date.today()
                if record.date <= today <= record.end_date:
                    record.state = 'active'
                elif today < record.date:
                    record.state = 'draft'
                else:  # today > record.end_date
                    record.state = 'expired'

    @api.model
    def _default_contract_number(self):
        # Get the number of existing contracts
        contract_count = self.search_count([])

        # The new contract number is the existing count plus one
        new_contract_number = contract_count + 1

        # Format the new contract number
        formatted_contract_number = "CONT/PROP/{:03d}".format(new_contract_number)

        return formatted_contract_number
    
    @api.constrains('state', 'partner_id')
    def _check_active_contract(self):
        for record in self:
            active_contracts = self.search([
                ('state', '=', 'active'), 
                ('partner_id', '=', record.partner_id.id),  # check for the same partner_id
                ('id', '!=', record.id)
            ])
            if active_contracts:
                if record.state == 'active':
                    raise exceptions.UserError("There is already an active contract for this partner. You cannot create another active contract.")
                elif record.state == 'draft':
                    raise exceptions.UserError("There is already an active contract for this partner. You cannot create a draft contract.")
