# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import _,models, fields, api


class sessionformation(models.Model):
     _name = 'formation.formation'
     _inherit = ['mail.thread', 'mail.activity.mixin']
     _description = 'formation.formation'
     _rec_name = 'nom_session_formation'

     session_formation_id = fields.Char('Id Session Formation')
     nom_session_formation = fields.Char('Nom Session Formation', required=True, tracking=True)
     niveau_session_formation = fields.Integer('Niveau Session Formation')
     objectif_global = fields.Char('Objectif Global')
     participants_number = fields.Integer('Nombre de Participants attendu')
     date_debut = fields.Datetime('Date Debut Session', default=fields.Date.today())
     periode = fields.Float(digits=(6, 2), help="Duration in days")
     date_fin = fields.Datetime(string="Date Fin Session", store=True, compute='_get_end_date', inverse='_set_end_date')
     prix = fields.Integer('prix session Formation')
     color = fields.Integer()
     address = fields.Char('Adresse')
     nombre_participant = fields.Integer(string='Nombre Participant', compute='_compute_nombre_participant')
     priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string="Priority")
     description = fields.Char('Description')


     participant_id = fields.One2many('formation.participant', 'session_formation_id')

     depense_id = fields.One2many('formation.depense', 'session_formation_id')

     revenu_id = fields.One2many('formation.revenu', 'session_formation_id')

     formateur_id = fields.One2many('formation.formateur', 'session_formation_id')




     def _compute_nombre_participant(self):
          for rec in self:
               nombre_participant = self.env['formation.participant'].search_count([('session_formation_id', '=', rec.id)])
               rec.nombre_participant = nombre_participant

     #@api.multi
     def action_open_participants(self):
          return {
               'type': 'ir.actions.act_window',
               'name': 'Participants',
               'res_model': 'formation.participant',
               'domain': [('session_formation_id', '=', self.id)],
               'view_mode': 'tree,form',
               'target': 'current',
          }

     def action_open_deponses(self):
          return {
               'type': 'ir.actions.act_window',
               'name': 'Deponses',
               'res_model': 'formation.depense',
               'domain': [('session_formation_id', '=', self.id)],
               'view_mode': 'tree,form',
               'target': 'current',
          }

     def action_open_revenues(self):
          return {
               'type': 'ir.actions.act_window',
               'name': 'Revenues',
               'res_model': 'formation.revenu',
               'domain': [('session_formation_id', '=', self.id)],
               'view_mode': 'tree,form',
               'target': 'current',
          }







     kanban_state = fields.Selection([('En Cours', 'en cours'), ('Done', 'done'), ('Terminé', 'terminé'), ('Prochainement', 'prochainement')], default='Done')#string="Status", tracking=True)


     legend_Prochainement = fields.Char(related='session_formation_id.legend_Prochainement', string='Kanban prochainement Explanation', readonly=True)
     legend_Done = fields.Char(related='session_formation_id.legend_Done', string='Kanban Valid Explanation', readonly=True)
     legend_Terminé = fields.Char(related='session_formation_id.legend_Terminé', legend_donestring='Kanban Ongoing Explanation', readonly=True)



     fold = fields.Boolean(string='Folded in Kanban', default=False)

     legend_Terminé = fields.Char(
          'Red Kanban Label', default=lambda s: _('terminé'), translate=True, required=True,
          help='Override the default value displayed for the blocked state for kanban selection.')
     legend_Done = fields.Char(
          'Green Kanban Label', default=lambda s: _('done'), translate=True, required=True,
          help='Override the default value displayed for the done state for kanban selection.')
     legend_Prochainement = fields.Char(
          'Grey Kanban Label', default=lambda s: _('prochainement'), translate=True, required=True,
          help='Override the default value displayed for the normal state for kanban selection.')

     kanban_state_label = fields.Char(string='Kanban State Label', compute='_compute_kanban_state_label',
                                      store=True, tracking=True)


     state = fields.Selection([('En Cours', 'en cours'), ('Done', 'done'), ('Terminé', 'terminé'), ('Prochainement', 'prochainement')], string="Status", tracking=True)

     active = fields.Boolean(string="Active", default=True)


     @api.depends('session_formation_id','kanban_state')
     def _compute_kanban_state_label(self):
          for formation in self:
               if formation.kanban_state == 'Done':
                    formation.kanban_state_label = formation.session_formation_id.legend_Done
               elif formation.kanban_state == 'Terminé':
                    formation.kanban_state_label = formation.session_formation_id.legend_Terminé
               else:
                    formation.kanban_state_label = formation.session_formation_id.legend_Prochainement



     @api.depends('date_debut','periode')
     def _get_end_date(self):
          for r in self:
               if not (r.date_debut and r.periode):
                    r.date_fin = r.date_debut
                    continue

                    periode = timedelta(days=r.periode, seconde=-1)
                    r.date_fin = r.date_debut + periode




     def _set_end_date(self):
          for r in self:
               if not (r.date_debut and r.date_fin):
                    continue


               r.periode = (r.date_fin - r.date_debut).days + 1


class depenseformation(models.Model):
     _name = 'formation.depense'
     _description = 'formation.depense'

     depense_id = fields.Char('Id Depense')
     depense_equipement = fields.Integer('Depense Equipement')
     depense_aliments_boissons = fields.Integer('Depense Aliments Boissons')
     depense_formateur = fields.Integer('Depense Formateur')
     depense_totale = fields.Integer('depense totale')



     session_formation_id = fields.Many2one('formation.formation', "Session")



class Revenuformation(models.Model):
     _name = 'formation.revenu'
     _description = 'formation.revenu'
     _rec_name = 'revenu_id'

     revenu_id = fields.Char('Id Revenu')
     revenu_total = fields.Integer('Revenu Total')
     revenu_net = fields.Integer('Revenu Net')
     payment_total_participant = fields.Integer('Payment Total Participant')
     deponse_total = fields.Integer('Deponse Total')
     expected_revenue = fields.Integer('Expected Revenu')
     color = fields.Integer()
     user_id = fields.Integer()
     tag_ids = fields.Integer()

     #tag_ids = fields.Integer('Tags')

     #priority = fields.Char('periority')


     #activity_date_deadline = fields.Char('Activity ')


     #activity_summary = fields.Char('Activity Summary')

     #active = fields.Char('Active')

     #company_currency = fields.Char('Company')

     #activity_ids = fields.Char('Activity id')

     #name = fields.Char('Name')

     session_formation_id = fields.Many2one('formation.formation', "Session")






