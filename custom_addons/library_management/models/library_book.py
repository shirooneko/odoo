from odoo import models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Buku Perpustakaan'

    name = fields.Char('Judul', required=True)
    author = fields.Char('Penulis')
    isbn = fields.Char('ISBN')
    copies = fields.Integer('Jumlah Salinan')
    publisher_id = fields.Many2one('library.publisher', 'Penerbit')
    genre_id = fields.Many2one('library.genre', 'Genre')
    description = fields.Text('Deskripsi')
