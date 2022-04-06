# -*- coding: utf-8 -*-

from odoo import models, fields, api


class formateur(models.Model):
     _name = 'formation.formateur'
     _description = 'formation.formateur'
     _rec_name = 'nom_formateur'

     id_formateur = fields.Integer('Id Formateur')
     nom_formateur = fields.Char('Nom Formateur')
     prenom_formateur = fields.Char('Prenom Formateur')
     niveau_etude = fields.Integer('Niveau Etude')
     cin = fields.Integer('carte identité')
     sexe = fields.Selection([('homme', 'Homme'), ('femme', 'Femme')])
     email = fields.Char('Email')
     phone = fields.Char('Phone')




