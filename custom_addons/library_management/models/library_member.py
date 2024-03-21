from odoo import models, fields

class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Anggota Perpustakaan'

    name = fields.Char('Nama', required=True)
    membership_date = fields.Date('Tanggal Keanggotaan')
    address = fields.Text('Alamat')
    email = fields.Char('Email')
