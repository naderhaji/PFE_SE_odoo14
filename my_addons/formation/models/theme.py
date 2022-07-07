# -*- coding: utf-8 -*-

from odoo import models, fields, api


class theme(models.Model):
     _name = 'formation.theme'
     _inherit = ['mail.thread', 'mail.activity.mixin']
     _description = 'formation.theme'

     id_theme = fields.Char('Id Theme')
     designation = fields.Char('Designation')
     description = fields.Char('Description')
     id = fields.Integer()
     image_1920 = fields.Image("Image")
     color = fields.Integer()

     formateur_id = fields.One2many('formation.formateur', 'Theme_id')