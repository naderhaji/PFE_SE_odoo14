# -*- coding: utf-8 -*-

from odoo import models, fields, api


class formateur(models.Model):
     _name = 'formation.formateur'
     _description = 'formation.formateur'
     _rec_name = 'name_formateur'

     id_formateur = fields.Char('Id Formateur')
     name_formateur = fields.Char('Name Formateur')
     niveau_etude = fields.Integer('Niveau Etude')
     cin = fields.Integer('carte identité')
     sexe = fields.Selection([('homme', 'Homme'), ('femme', 'Femme')])
     email = fields.Char('Email')
     phone = fields.Char('Phone')
     image_1920 = fields.Image("Image")
     id = fields.Integer()
     color = fields.Integer()

     color = fields.Integer()

     session_formation_id = fields.Many2one('formation.formation', "Session")

     Theme_id = fields.Many2one('formation.theme', "Theme")

<<<<<<< HEAD
=======

>>>>>>> 15ac6b326fc22bbfc6ed2d17110567d0395a3cf2
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

     @api.model
     def default_get(self, fields):
          res = super(formateur, self).default_get(fields)

          res['session_formation_id'] = self._context.get('active_id')

          return res
