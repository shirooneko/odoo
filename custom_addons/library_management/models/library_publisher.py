from odoo import models, fields

class LibraryPublisher(models.Model):
    _name = 'library.publisher'
    _description = 'Penerbit'

    name = fields.Char('Nama Penerbit', required=True)
    address = fields.Text('Alamat')
    phone = fields.Char('Telepon')
    email = fields.Char('Email')