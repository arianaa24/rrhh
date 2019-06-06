# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HolidaysStatus(models.Model):
    _inherit = "hr.holidays.status"

    descontar_nomina = fields.Boolean('Descontar en nómina')
