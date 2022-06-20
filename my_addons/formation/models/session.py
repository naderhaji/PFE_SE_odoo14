# -*- coding: utf-8 -*-

from datetime import timedelta


from odoo import _,models, fields, api



class sessionformation(models.Model):
     _name = 'formation.formation'
     _inherit = ['mail.thread', 'mail.activity.mixin']
     _description = 'formation.formation'
     _rec_name = 'nom_session_formation'

     def _get_default_stage_id(self):
          session_stages = self.env['session.stage'].search([])
          return session_stages[0] if session_stages else False

     session_formation_id = fields.Char(string="Id Session")
     nom_session_formation = fields.Char('Nom Session', required=True, tracking=True)
     niveau_session_formation = fields.Integer('Niveau Session')
     objectif_global = fields.Char('Objectif Global')
     participants_number = fields.Integer('Nombre de Participants attendu')
     date_debut = fields.Datetime('Date Debut Session', default=fields.Date.today())
     periode = fields.Float(digits=(6, 2), help="Duration in days")
     date_fin = fields.Datetime(string="Date Fin Session", store=True, compute='_get_end_date', inverse='_set_end_date')
     prix = fields.Float(string="Prix Session")
     color = fields.Integer()
     address = fields.Char('Adresse')
     type_formation = fields.Selection([('intra', 'Intra'), ('interne', 'Interne')], string="Type Formation")
     catégorie_formation = fields.Selection([('enligne', 'EnLigne'), ('présentielle', 'Présentielle'), ('hybride', 'Hybride')], string="Catégorie Formation")
     nombre_participant = fields.Integer(string='Nombre Participant', compute='_compute_nombre_participant')
     priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string="Priority")
     note = fields.Text(string='Note')
     id = fields.Integer()
     image_1920 = fields.Image("Image")
     website = fields.Char("WebSite")







     participant_id = fields.One2many('formation.participant', 'session_formation_id')

     depense_id = fields.One2many('formation.depense', 'session_formation_id')

     revenu_id = fields.One2many('formation.revenu', 'session_formation_id')

     formateur_id = fields.One2many('formation.formateur', 'session_formation_id')

     payment_id = fields.One2many('formation.payment', 'session_formation_id')


     @api.model
     def _default_currency_id(self):
          value = self.env['res.currency'].search([('name', '=', 'COP')],limit=1)
          return value and value.id or False

     currency_id = fields.Many2one("res.currency", string="Currency", default=_default_currency_id)

     def _compute_nombre_participant(self):
          for rec in self:
               nombre_participant = self.env['formation.participant'].search_count([('session_formation_id', '=', rec.id)])
               rec.nombre_participant = nombre_participant


     def action_open_participants(self):
          return {
               'type': 'ir.actions.act_window',
               'name': 'Participants',
               'res_model': 'formation.participant',
               'domain': [('session_formation_id', '=', self.id)],
               'context': {'default_session_formation_id': self.id},
               'view_mode': 'tree,form',
               'target': 'current',
          }


     def action_open_formateurs(self):
          return {
               'type': 'ir.actions.act_window',
               'name': 'Formateurs',
               'res_model': 'formation.formateur',
               'domain': [('session_formation_id', '=', self.id)],
               'context': {'default_session_formation_id': self.id},
               'view_mode': 'tree,form',
               'target': 'current',
          }

     def action_open_deponses(self):
          return {
               'type': 'ir.actions.act_window',
               'name': 'Deponses',
               'res_model': 'formation.depense',
               'domain': [('session_formation_id', '=', self.id)],
               'context': {'default_session_formation_id': self.id},
               'view_mode': 'tree,form',
               'target': 'current',
          }

     def action_open_payment(self):
          return {
               'type': 'ir.actions.act_window',
               'name': 'Pyaments',
               'res_model': 'formation.payment',
               'view_type': 'form',
               'domain': [('session_formation_id', '=', self.id)],
               'context': {'default_session_formation_id': self.id},
               'view_mode': 'tree,form',
               'target': 'current',
          }







     def action_open_revenues(self):
          return {
               'type': 'ir.actions.act_window',
               'name': 'Revenues',
               'res_model': 'formation.revenu',
               'domain': [('session_formation_id', '=', self.id)],
               'context': {'default_session_formation_id': self.id},
               'view_mode': 'tree,form',
               'target': 'current',
          }

     kanban_state = fields.Selection([('normal', 'In Progress'), ('done', 'Done'), ('blocked', 'Blocked')],
                                     default='normal')

     kanban_state_label = fields.Char(
          string='Kanban State Label', compute='_compute_kanban_state_label',
          store=True, tracking=True)

     stage_id = fields.Many2one(
          'session.stage', string="Formation" , group_expand='_group_expand_stages')

     @api.model
     def _group_expand_stages(self, stages, domain, order):
          return stages.search([], order=order)

     legend_blocked = fields.Char(related='stage_id.legend_blocked', string='Kanban Blocked Explanation', readonly=True)
     legend_done = fields.Char(related='stage_id.legend_done', string='Kanban Valid Explanation', readonly=True)
     legend_normal = fields.Char(related='stage_id.legend_normal', string='Kanban Ongoing Explanation', readonly=True)




     #kanban_state_label = fields.Char(string='Kanban State Label', compute='_compute_kanban_state_label', store=True, tracking=True)


     state = fields.Selection([('Prochainement', 'prochainement'), ('En Cours', 'en cours'), ('Done', 'done'), ('Terminé', 'terminé')], string="Status", tracking=True)

     def action_en_cours(self):
          self.state = 'en cours'

     def action_done(self):
          self.state = 'done'

     def action_terminé(self):
          self.state = 'terminé'

     def action_prochainement(self):
          self.state = 'prochainement'

     def etape_suivante(self):
          self.ensure_one()
          if self.state == 'Prochainement':
               return self.write({'state': 'En Cours'})
          elif self.state == 'En Cours':
               return self.write({'state': 'Done'})
          elif self.state == 'Done':
               return self.write({'state': 'Terminé'})
          #else:
           #    raise ValidationError('Session Déjà Terminé !')
          #else:
               #from quorum.exceptions import ValidationError
               #raise ValidationError('Session Déjà Terminé !')

     active = fields.Boolean(string="Active", default=True)

     @api.depends('stage_id', 'kanban_state')
     def _compute_kanban_state_label(self):
          for formation in self:
               if formation.kanban_state == 'normal':
                    formation.kanban_state_label = formation.stage_id.legend_normal
               elif formation.kanban_state == 'blocked':
                    formation.kanban_state_label = formation.stage_id.legend_blocked
               else:
                    formation.kanban_state_label = formation.stage_id.legend_done



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



class SessionStage(models.Model):
    _name = 'session.stage'
    _description = 'Session Stage'
    _order = 'sequence, name'

    name = fields.Char(string='Stage Name', required=True, translate=True)
    description = fields.Text(string='Stage description', translate=True)
    sequence = fields.Integer('Sequence', default=1)
    fold = fields.Boolean(string='Folded in Kanban', default=False)
    pipe_end = fields.Boolean(
        string='End Stage', default=False,
        help='Events will automatically be moved into this stage when they are finished. The event moved into this stage will automatically be set as green.')
    legend_blocked = fields.Char(
         'Red Kanban Label', default=lambda s: _('Blocked'), translate=True, required=True,
         help='Override the default value displayed for the blocked state for kanban selection.')
    legend_done = fields.Char(
         'Green Kanban Label', default=lambda s: _('Done'), translate=True, required=True,
         help='Override the default value displayed for the done state for kanban selection.')
    legend_normal = fields.Char(
         'Grey Kanban Label', default=lambda s: _('In Progress'), translate=True, required=True,
         help='Override the default value displayed for the normal state for kanban selection.')

    session_formation_id = fields.One2many('formation.formation', 'stage_id')


class depenseformation(models.Model):
     _name = 'formation.depense'
     _description = 'formation.depense'
     _rec_name = 'depense_id'

     depense_id = fields.Char('Id Depense')
     depense_loyer = fields.Float('Depense Loyer')
     depense_aliments_boissons = fields.Float('Depense Aliments Boissons')
     facture_electrcité_eau = fields.Float('Depense Eau et Electricité')
     facture_telecom = fields.Float('Facture Telecom')
     depense_support_cours = fields.Float('Depense Support Cours')
     depense_location_voiture = fields.Float('Depense Location Voiture')
     depense_parking_voiture = fields.Float('Depense Parking Voiture')
     depenses_personnelles = fields.Float('Depense Personnelles')
     depense_formateur = fields.Float('Depense Formateur')
     depense_totale = fields.Float(string="Depense Total")
     session_formation_id = fields.Many2one('formation.formation', "Session")
     priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string="Priority")
     date = fields.Datetime(string="Date")
     color = fields.Integer()
     active = fields.Boolean(string="Active", default=True)

     @api.onchange('depense_loyer', 'depense_aliments_boissons', 'facture_electrcité_eau', 'facture_telecom', 'depense_formateur', 'depense_support_cours', 'depense_location_voiture', 'dpense_parking_voiture', 'depenses_personnelles')
     def onchange_function(self):
          self.depense_totale = self.depense_loyer + self.depense_aliments_boissons + self.facture_electrcité_eau + self.facture_telecom + self.depense_formateur + self.depense_support_cours + self.depense_location_voiture + self.depense_parking_voiture + self.depenses_personnelles










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
     priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Very High')], string="Priority")
     user_id = fields.Integer()
     tag_ids = fields.Integer()
     date = fields.Datetime(string="Date")
     active = fields.Boolean(string="Active", default=True)

     #tag_ids = fields.Integer('Tags')

     #priority = fields.Char('periority')


     #activity_date_deadline = fields.Char('Activity ')


     #activity_summary = fields.Char('Activity Summary')

     #active = fields.Char('Active')

     #company_currency = fields.Char('Company')

     #activity_ids = fields.Char('Activity id')

     #name = fields.Char('Name')

     session_formation_id = fields.Many2one('formation.formation', "Session")