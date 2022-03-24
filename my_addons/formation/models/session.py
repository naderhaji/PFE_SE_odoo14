# -*- coding: utf-8 -*-

from odoo import models, fields, api


class sessionformation(models.Model):
     _name = 'formation.formation'
     _inherit = 'mail.thread'
     _description = 'formation.formation'

     id_session_formation = fields.Integer('Id Session Formation')
     nom_session_formation = fields.Char('Nom Session Formation')
     niveau_session_formation = fields.Integer('Niveau Session Formation')
     nombre_participant = fields.Integer('Nombre Participant')
     objectif_global = fields.Char('Objectif Global')
     date_debut = fields.Datetime('Date Debut Session')
     date_fin = fields.Datetime('Date Fin Session')
     prix = fields.Integer('prix session Formation')




