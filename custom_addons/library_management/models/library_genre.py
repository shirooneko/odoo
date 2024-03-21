from odoo import models, fields, api

class LibraryGenre(models.Model):
    _name = 'library.genre'
    _description = 'Genre Buku'

    name = fields.Char('Genre', required=True)
    book_ids = fields.One2many('library.book', 'genre_id', 'Buku')
    book_names = fields.Char('Daftar Buku', compute='_compute_book_names')

    @api.depends('book_ids.name')
    def _compute_book_names(self):
        for record in self:
            record.book_names = ', '.join(book.name for book in record.book_ids)