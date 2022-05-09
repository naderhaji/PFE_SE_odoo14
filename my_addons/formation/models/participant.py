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
     payment = fields.Float()
     session_formation_id = fields.Many2one('formation.formation', "Session")
     payment_id = fields.One2many('formation.payment', 'participant_id')
     borrower_id = fields.Many2one('res.partner', 'Borrower', required=True)

     state = fields.Selection([('ongoing', 'Ongoing'), ('returned', 'Returned')],
                              'State', default='ongoing', required=True)

     color = fields.Integer()
     popularity = fields.Selection(
          [('no', 'No Demand'), ('low', 'Low Demand'), ('medium', 'Average Demand'), ('high', 'High Demand'), ])
     tag_ids = fields.Many2many('participant.tag')

     stage_id = fields.Many2one(
          'participant.stage',

          group_expand='_group_expand_stages'
     )

     @api.model
     def _default_rent_stage(self):
          Stage = self.env['participant.stage']
          return Stage.search([], limit=1)

     @api.model
     def _group_expand_stages(self, stages, domain, order):
          return stages.search([], order=order)


class ParticipantStage(models.Model):
     _name = 'participant.stage'
     _order = 'sequence,name'

     name = fields.Char()
     sequence = fields.Integer()
     fold = fields.Boolean()
     payment_state = fields.Selection(
          [('available', 'Available'),
           ('borrowed', 'Borrowed'),
           ('lost', 'Lost')],
          'State', default="available")



class ParticipantTags(models.Model):
    _name = 'participant.tag'

    name = fields.Char()
    color = fields.Integer()


class ResPartner(models.Model):
    _inherit = 'res.partner'

    participant_ids = fields.One2many('formation.participant', 'borrower_id')





class payment(models.Model):

     _name = 'formation.payment'
     _description = 'formation.payment'

     payment_id = fields.Char('Id Payment')
     mode_paiement = fields.Selection([('especes','Especes'), ('cheque', 'Cheque'), ('bancaires', 'Bancaires')])
     montant_paye = fields.Char('Montant Paye')
     montant_restant = fields.Char('Montant Restant')
     expected_to_be_payed = fields.Char('Expected to be payed')

     participant_id = fields.Many2one('formation.participant', "Participant")










