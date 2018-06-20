# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    dia_del_mes = fields.Integer('Dia del Mes')
    dias_totales_mes = fields.Integer('Dias totales') 