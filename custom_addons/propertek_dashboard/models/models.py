# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class propertek_dashboard(models.Model):
#     _name = 'propertek_dashboard.propertek_dashboard'
#     _description = 'propertek_dashboard.propertek_dashboard'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

