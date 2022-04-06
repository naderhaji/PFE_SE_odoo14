# -*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api


class sessionformation(models.Model):
     _name = 'formation.formation'
     _inherit = ['mail.thread', 'mail.activity.mixin']
     _description = 'formation.formation'
     _rec_name = 'nom_session_formation'

     id_session_formation = fields.Integer('Id Session Formation')
     nom_session_formation = fields.Char('Nom Session Formation', required=True, tracking=True)
     niveau_session_formation = fields.Integer('Niveau Session Formation')
     nombre_participant = fields.Integer('Nombre Participant')
     objectif_global = fields.Char('Objectif Global')
     date_debut = fields.Datetime('Date Debut Session', default=fields.Date.today())
     periode = fields.Float(digits=(6, 2), help="Duration in days")
     date_fin = fields.Datetime(string="Date Fin Session", store=True, compute='_get_end_date', inverse='_set_end_date')
     prix = fields.Integer('prix session Formation')
     color = fields.Integer()



     state = fields.Selection([('En Cours', 'en cours'), ('Done', 'done'), ('Terminé', 'terminé'), ('Prochainement', 'prochainement')], string="Status", tracking=True)

     active = fields.Boolean(string="Active", default=True)

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


