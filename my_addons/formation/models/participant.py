# -*- coding: utf-8 -*-

from odoo import models, fields, api


class participant(models.Model):
     _name = 'formation.participant'
     _inherit = ['mail.thread', 'mail.activity.mixin']
     _description = 'formation.participant'
     _rec_name = 'nom_participant'

     participant_id = fields.Char('Id Participant')
     nom_participant = fields.Char('Nom Participant')
     prenom_participant = fields.Char('Prenom Participant')
     niveau_etude = fields.Char('Niveau Etude')
     email = fields.Char('Email')
     phone = fields.Integer('Phone')
     sexe = fields.Selection([('homme', 'Homme'), ('femme', 'Femme')])
     type = fields.Selection([('individuel', 'Individuel'), ('etudiant', 'Etudiant'), ('société','Société')])
     nom_société = fields.Char('Nom Société')
     session_formation_id = fields.Many2one('formation.formation', "Session")
     payment_id = fields.One2many('formation.payment', 'participant_id')





class payment(models.Model):

     _name = 'formation.payment'
     _description = 'formation.payment'

     payment_id = fields.Char('Id Payment')
     mode_paiement = fields.Selection([('especes','Especes'), ('cheque', 'Cheque'), ('bancaires', 'Bancaires')])
     montant_paye = fields.Char('Montant Paye')
     montant_restant = fields.Char('Montant Restant')
     expected_to_be_payed = fields.Char('Expected to be payed')

     participant_id = fields.Many2one('formation.participant', "Participant")










