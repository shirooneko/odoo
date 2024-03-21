from odoo import models, fields

class LibraryBookLoan(models.Model):
    _name = 'library.book.loan'
    _description = 'Peminjaman Buku Perpustakaan'

    book_id = fields.Many2one('library.book', 'Buku', required=True)
    member_id = fields.Many2one('library.member', 'Peminjam', required=True)
    date_borrowed = fields.Date('Tanggal Pinjam', required=True, default=fields.Date.context_today)
    date_return = fields.Date('Tanggal Pengembalian')
    state = fields.Selection([
        ('borrowed', 'Dipinjam'),
        ('returned', 'Dikembalikan'),
    ], default='borrowed', string='Status')
