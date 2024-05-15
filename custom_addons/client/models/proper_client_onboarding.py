import logging
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

class ClientOnboarding(models.Model):
    _name = 'proper.client.onboarding'
    _description = 'Client Onboarding'
    _order = 'id'

    # Fields
    display_name = fields.Char(string="Display Name", compute='_compute_display_name', store=True)
    actual_date = fields.Date(string='Actual End Date', compute='_compute_actual_date', store=True)
    is_completed = fields.Boolean(string='Completed?', compute='_compute_actual_date', default=False, store=True)
    attachment = fields.Binary(string='Attachment')
    notes = fields.Html(string='Notes')
    onboarding_type = fields.Selection(selection=[
        ('onboarding', 'Onboarding'),
        ('offboarding', 'Offboarding')
        ], string='Onboarding Type') 
    partner_id = fields.Many2one('res.partner', string='Partners', default=lambda self: self.env.user.partner_id.id)
    state_id = fields.Many2one('proper.client.onboarding.state', string='State', readonly=False)
    allowed_next_state_ids = fields.Many2many(
        'proper.client.onboarding.state',
        relation='onboarding_allowed_next_state_relation',
        column1='onboarding_id',
        column2='next_state_id',
        string='Allowed Next State',
        compute='_compute_allowed_next_state_ids'
    )
    previous_state_id = fields.Many2one('proper.client.onboarding.state', string='Previous State', readonly=True, copy=False)
    target_date = fields.Date(string='Target End Date')
    task_template_id = fields.Many2one('proper.client.onboarding.task.template', string='Task', help='Properties Access Rights Miscellaneous BASE PROPERTIES')
    todo_task_ids = fields.One2many('proper.client.onboarding.task', 'onboarding_id')
    task_id_completed = fields.One2many(
        'proper.client.onboarding.task',
        'onboarding_id',
        domain=lambda self: [('onboarding_id', '=', self.id), ('state_id', '=', self.state_id.id), ('is_completed', '=', True)]
    )
    task_id_ongoing = fields.One2many(
        'proper.client.onboarding.task',
        'onboarding_id',
        domain=lambda self: [('onboarding_id', '=', self.id), ('state_id', '=', self.state_id.id), ('is_completed', '!=', True)]
    )

    # Computed Fields
    @api.depends('state_id')
    def _compute_allowed_next_state_ids(self):
        for record in self:
            if record.state_id:
                record.allowed_next_state_ids = record.state_id.allowed_next_state_ids
            else:
                record.allowed_next_state_ids = False

    @api.depends('partner_id', 'state_id')
    def _compute_display_name(self):
        for record in self:
            if record.partner_id and record.state_id:
                record.display_name = f"{record.partner_id.name} - {record.state_id.name}"
            elif record.partner_id:
                record.display_name = record.partner_id.name
            else:
                record.display_name = ""

    @api.depends('todo_task_ids.is_completed')
    def _compute_actual_date(self):
        for onboarding in self:
            # Filter tugas yang belum selesai pada state final
            unfinished_tasks = onboarding.todo_task_ids.filtered(lambda task: not task.is_completed and task.state_id.is_final)

            if unfinished_tasks:
                # Jika masih ada tugas yang belum selesai pada state final, set actual_date dan is_completed menjadi False
                onboarding.actual_date = False
                onboarding.is_completed = False
            else:
                # Jika tidak ada tugas yang belum selesai pada state final, lanjutkan dengan logika sebelumnya
                final_completed_tasks = onboarding.todo_task_ids.filtered(lambda task: task.is_completed and task.state_id.is_final)
                if final_completed_tasks:
                    min_completion_date = min(final_completed_tasks.mapped('actual_completion_date'))
                    onboarding.actual_date = min_completion_date
                    onboarding.is_completed = True
                else:
                    onboarding.actual_date = False
                    onboarding.is_completed = False

    @api.model
    def create(self, vals):
        # Menambahkan logika untuk menentukan nilai state_id dan previous_state_id jika tidak disediakan
        if not vals.get('state_id'):
            initial_state = self.env['proper.client.onboarding.state'].search([('is_initial', '=', True)], limit=1)
            if not initial_state:
                raise UserError("No initial state found. Please set at least one state as initial state.")
            else:
                vals['state_id'] = initial_state.id
        
        if not vals.get('previous_state_id'):
            vals['previous_state_id'] = False

        # Membuat record onboarding
        onboarding = super(ClientOnboarding, self).create(vals)
        
        # Mengambil task template berdasarkan state_id
        task_templates = self.env['proper.client.onboarding.task.template'].search([('state_id', '=', onboarding.state_id.id)])
        
        # Membuat tugas secara otomatis untuk onboarding ini
        for template in task_templates:
            task_vals = {
                'name': template.name,
                'onboarding_id': onboarding.id,
                'state_id': onboarding.state_id.id,
                'task_template_id': template.id,
                'is_optional': template.is_optional,
                'target_days_completed': template.target_days_completed
            }
            self.env['proper.client.onboarding.task'].create(task_vals)

        return onboarding

    @api.model
    def write(self, values):
        validation_errors = []

        if 'state_id' in values:
            current_state_id = self.state_id.id

            for record in self:
                new_state_id = values.get('state_id') if 'state_id' in values else record.previous_state_id.id
                
                if record.previous_state_id and new_state_id == record.previous_state_id.id:
                    validation_errors.append('Cannot revert to the previous state.')

                if new_state_id:
                    new_state = self.env['proper.client.onboarding.state'].browse(new_state_id)
                    
                    if new_state_id not in record.allowed_next_state_ids.ids and not new_state.is_final:
                        # Ambil nama state yang tidak diizinkan
                        disallowed_state_name = new_state.name
                        current_state_name = record.state_id.name
                        validation_errors.append(f'Cannot change state from "{current_state_name}" to "{disallowed_state_name}". The selected state "{disallowed_state_name}" is not allowed.')
                        
                    if record.todo_task_ids:
                        # Filter tugas yang sedang berlangsung dan belum selesai
                        ongoing_tasks = record.todo_task_ids.filtered(lambda task: task.state_id == record.state_id and not task.is_completed and not task.is_optional)
                        # Ambil nama dari tugas yang belum selesai
                        ongoing_task_names = ", ".join(task.name for task in ongoing_tasks)
                        # Jika ada tugas yang belum selesai, tambahkan pesan kesalahan dengan nama tugas
                        if ongoing_task_names:
                            validation_errors.append(f'Cannot change state while the following tasks are ongoing: {ongoing_task_names}.')

                if not record.todo_task_ids.filtered(lambda task: task.state_id == record.state_id):
                    validation_errors.append('Cannot change state because there are no tasks for the current state.')

            if validation_errors:
                raise ValidationError('\n'.join(validation_errors))

            result = super(ClientOnboarding, self).write(values)
            self.previous_state_id = current_state_id

            # Mengambil task template berdasarkan state_id
            task_templates = self.env['proper.client.onboarding.task.template'].search([('state_id', '=', record.state_id.id)])
            
            # Membuat tugas secara otomatis untuk onboarding ini
            for template in task_templates:
                task_vals = {
                        'name': template.name,
                        'onboarding_id': record.id,
                        'state_id': record.state_id.id,
                        'task_template_id': template.id,
                        'is_optional': template.is_optional,
                        'target_days_completed': template.target_days_completed
                    }
                self.env['proper.client.onboarding.task'].create(task_vals)


        else:
            result = super(ClientOnboarding, self).write(values)

        return result
