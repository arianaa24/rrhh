# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Holidays(models.Model):
    _inherit = "hr.holidays"

    descontar_nomina = fields.Boolean('Descontar en nómina')
