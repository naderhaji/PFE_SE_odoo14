# -*- coding: utf-8 -*-

from odoo import models, fields, api


class theme(models.Model):
     _name = 'formation.theme'
     _description = 'formation.theme'

     id_theme = fields.Integer('Id Theme')
     designation = fields.Char('Designation')
     description = fields.Char('Description')

     formateur_id = fields.One2many('formation.formateur', 'Theme_id')