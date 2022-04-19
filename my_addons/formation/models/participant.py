# -*- coding: utf-8 -*-

from odoo import models, fields, api


class participant(models.Model):
     _name = 'formation.participant'
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
     mode_paiement = fields.Selection([('especes','Especes'), ('cheque','Cheque'), ('bancaires','Bancaires')])
     session_formation_id = fields.Many2one('formation.formation', "Session")







