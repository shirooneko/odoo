import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

class ClientOnboarding(models.Model):
    _name = 'proper.client.onboarding'
    _description = 'Client Onboarding'
    _order = 'id'
    
    _logger = logging.getLogger(__name__)

    display_name = fields.Char(string="Display Name", compute='_compute_display_name', store=True)
    actual_date = fields.Date(string='Actual End Date')
    attachment = fields.Binary(string='Attachment')
    completed_task_ids = fields.One2many('proper.client.onboarding.task', 'onboarding_id')
    is_completed = fields.Boolean(string='Completed?')
    is_final = fields.Boolean(string='Final State?')
    is_initial = fields.Boolean(string='Initial State?')
    notes = fields.Html(string='Notes')
    onboarding_type = fields.Selection(selection=[
        ('onboarding', 'Onboarding'),
        ('offboarding', 'Offboarding')
        ], string='Onboarding Type') 
    partner_id = fields.Many2one('res.partner', string='Partners', default=lambda self: self.env.user.partner_id.id)
    state_id = fields.Many2one('proper.client.onboarding.state', string='State')
    target_date = fields.Date(string='Target End Date')
    todo_task_ids = fields.One2many('proper.client.onboarding.task', 'onboarding_id')
    
    @api.depends('partner_id', 'state_id')
    def _compute_display_name(self):
        for record in self:
            if record.partner_id and record.state_id:
                record.display_name = f"{record.partner_id.name} - {record.state_id.name}"
            elif record.partner_id:
                record.display_name = record.partner_id.name
            else:
                record.display_name = ""
                
    @api.model
    def create(self, vals):
        if not vals.get('state_id'):
            # Ambil status yang memiliki is_initial True
            initial_state = self.env['proper.client.onboarding.state'].search([('is_initial', '=', True)], limit=1)
            if not initial_state:
                raise UserError("No initial state found. Please set at least one state as initial state.")
            else:
                vals['state_id'] = initial_state.id
        elif not self.env['proper.client.onboarding.state'].search([]):
            raise UserError("No state records found. Please add states before creating an onboarding.")
        
        # Panggil metode untuk membuat task dari onboarding
        task_vals = {
            'state_id': vals.get('state_id'),  # Gunakan state_id dari vals
            'onboarding_id': self.id,  # Gunakan id onboarding saat ini
        }
        print("Task Vals:", task_vals)
        # Panggil metode create_task_from_onboarding
        self.create_task_from_onboarding(task_vals)
        
        return super(ClientOnboarding, self).create(vals)

    @api.model
    def create_task_from_onboarding(self, vals):
        try:
            # Tambahkan state_id dari onboarding ke task yang dibuat
            task = self.env['proper.client.onboarding.task'].sudo().create(vals)
            print("Task Created:", task)
            # Lakukan pengecekan jika nilai state_id sudah disimpan dengan benar di task yang baru dibuat
            if task.state_id.id != vals.get('state_id'):
                raise UserError("Failed to save state_id to the task.")
            return task
        except Exception as e:
            print("Error:", e)
            raise UserError("Failed to create task from onboarding: %s" % e)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ClientOnboarding, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            # Ambil status default dari model onboarding
            default_state = self.env['proper.client.onboarding.state'].search([('is_initial', '=', True)], limit=1)
            if default_state:
                default_state_id = default_state.id
            else:
                default_state_id = False
            
            if default_state_id:
                # Ambil task berdasarkan status default
                todo_tasks = self.env['proper.client.onboarding.task'].search([('state_id', '=', default_state_id)])
                
                # Ubah domain untuk todo_task_ids
                res['fields']['todo_task_ids']['domain'] = [('id', 'in', todo_tasks.ids)]
        return res
    
