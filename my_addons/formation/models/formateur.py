# -*- coding: utf-8 -*-

from odoo import models, fields, api


class formateur(models.Model):
     _name = 'formation.formateur'
     _description = 'formation.formateur'
     _inherit = ['mail.thread', 'mail.activity.mixin']
     _rec_name = 'name_formateur'

     id_formateur = fields.Char('Id Formateur')
     name_formateur = fields.Char('Name Formateur')
     niveau_etude = fields.Integer('Niveau Etude')
     cin = fields.Integer('carte identité')
     sexe = fields.Selection([('homme', 'Homme'), ('femme', 'Femme')], string="Sexe")
     email = fields.Char('Email')
     phone = fields.Char('Phone')
     image_1920 = fields.Image("Image")
     id = fields.Integer()
     color = fields.Integer()

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

     def send_sms(self):
         from twilio.rest import Client

         #Your ACCOUNT SID from twilio
         account_sid = "ACaf4c43b3d27215fb913a5bef6b0b841b"
         #Your Auth Token from twilio.com
         auth_token = "1a086d15ad22a4bd9015cd871a3c2969"

         client = Client(account_sid, auth_token)

         message = client.messages.create(
              body="Cher Nous vous invitons à être présent à la Formation de la semaine prochaine.Meilleures salutations,",
              from_="+19403988751",
              to=self.phone)

     @api.model
     def default_get(self, fields):
          res = super(formateur, self).default_get(fields)

          res['session_formation_id'] = self._context.get('active_id')

          return res
