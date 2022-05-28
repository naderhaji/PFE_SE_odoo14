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

     session_formation_id = fields.Many2one('formation.formation', "Session")

     Theme_id = fields.Many2one('formation.theme', "Theme")


     def action_send_mail(self):
          self.ensure_one()
          template_id = self.env.ref('formation.email_template_formateur').id
          ctx = {
               'default_model': 'formation.formateur',
               'default_res_id': self.id,
               'default_use_template': bool(template_id),
               'default_template_id': template_id,
               'default_composition_mode': 'comment',
               'email_to': self.email,
          }
          return {
               'type': 'ir.actions.act_window',
               'view_type': 'form',
               'view_mode': 'form',
               'res_model': 'mail.compose.message',
               'target': 'new',
               'context': ctx,
          }




