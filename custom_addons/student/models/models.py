# -*- coding: utf-8 -*-

from odoo import models, fields

class Student(models.Model):
    _name = "wb.student"
    _description = "This is student profile"

    name = fields.Char(string="Nama Lengkap", required=True)
    nis = fields.Integer(string="NIS", required=True)
    alamat = fields.Text(string="Alamat", required=True)
    kota = fields.Char(string="Kota", required=True)
    provinsi = fields.Char(string="Provinsi", required=True)
    negara = fields.Char(string="Negara", required=True)