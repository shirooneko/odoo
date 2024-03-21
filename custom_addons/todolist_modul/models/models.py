from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class TodoTask(models.Model):
    _name = 'todo.task'
    _description = 'To-do Task'
    _inherit = ['mail.thread']


    name = fields.Char(string='Nama Tugas', required=True)
    description = fields.Html(string='Deskripsi')
    deadline = fields.Date(string='Deadline')
    status = fields.Selection([
        ('draft','Draft'),
        ('in_progress', 'Proses'),
        ('done', 'Selesai')], string='Status', default="draft",track_visibility='onchange', group_expand='_read_group_status_ids')

    message_ids = fields.One2many('mail.message', 'res_id', domain=lambda self: [('model', '=', 'todo.task')],string='Messages', copy=False)
    
    @api.model
    def _read_group_status_ids(self, stages, domain, order):
        return ['draft','in_progress', 'done']

    def create(self, vals):
        task = super(TodoTask, self).create(vals)
        task.with_context(mail_create_nosubscribe=True).message_post(body="Tugas dibuat")
        return task

    
    def write(self, vals):
        # Mengambil nilai-nilai sebelum perubahan dilakukan
        old_values = {field: getattr(self, field) for field in vals.keys()}

        # Memanggil metode write dari superclass untuk melakukan perubahan
        result = super(TodoTask, self).write(vals)

        # Membandingkan nilai-nilai sebelum dan sesudah perubahan
        for task in self:
            for field, new_value in vals.items():
                old_value = old_values.get(field)
                if old_value != new_value:
                    if field == 'status':
                        if new_value == 'in_progress':
                            task.message_post(body='Tugas sedang diproses', message_type='comment')
                        elif new_value == 'draft':
                            task.message_post(body='Tugas dikembalikan ke draft', message_type='comment')
                        elif new_value == 'done':
                            task.message_post(body='Tugas telah diselesaikan', message_type='comment')
                    else:
                        task.message_post(body=f'Data tugas diperbarui', message_type='comment')

        return result



    def action_edit(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'todo.task',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
            'flags': {'form': {'action_buttons': True, 'options': {'mode': 'edit'}}}
        }

    def action_delete(self):
        self.ensure_one()
        return {
            'name': 'Yakin Hapus?',
            'type': 'ir.actions.act_window',
            'res_model': 'todo.task.delete',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_task_id': self.id},
        }
    
    def action_in_progress(self):
        if "done" in self.mapped("status"):
            raise UserError("Tugas yang sudah selesai tidak dapat diubah menjadi dalam proses.")
        self.write({'status': 'in_progress'})

    def action_draft(self):
        self.write({'status': 'draft'})

    def action_done(self):
        self.write({'status': 'done'})
    

class TodoTaskDelete(models.TransientModel):
    _name = 'todo.task.delete'
    _description = 'Confirm Deletion of Todo Task'

    task_id = fields.Many2one('todo.task', string='Task')
    confirmation_message = fields.Text(string='Confirmation Message', default='Apa anda yakin ingin menghapus task ini?')

    def confirm(self):
        self.task_id.unlink()
        return {'type': 'ir.actions.act_window_close'}