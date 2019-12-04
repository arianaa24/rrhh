# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
import datetime
from datetime import date, datetime
import time
import dateutil.parser
from dateutil.relativedelta import relativedelta
from dateutil import relativedelta as rdelta
from odoo.fields import Date, Datetime
import logging
from odoo.release import version_info

class rrhh_vacaciones_wizard(models.TransientModel):
    _name = 'rrhh.vacaciones.wizard'

    dias = fields.Float('Cantidad de dias')

    def generar_vacaciones(self):
        if self.env.context.get('active_ids', []):
            fecha_actual = date.today()
            anio_actual = datetime.strptime(str(fecha_actual), '%Y-%m-%d').strftime('%Y')
            for empleado in self.env['hr.employee'].browse(self.env.context.get('active_ids', [])):
                if version_info[0] == 12:
                    ausencias = self.env['hr.leave'].search([('state', '=', 'validate'), ('employee_id', '=', empleado.id),('number_of_days','>',0)])
                else:
                    ausencias = self.env['hr.holidays'].search([('state', '=', 'validate'), ('employee_id', '=', empleado.id),('number_of_days','>',0)])
                asusencia_anio = []
                if empleado.contract_ids:
                    for contrato in empleado.contract_ids:
                        dias_trabajados = datetime.strptime(str(fecha_actual),'%Y-%m-%d') -  datetime.strptime(str(contrato.date_start),'%Y-%m-%d')
                        if ausencias:
                            anio_ausencia = 0
                            for ausencia in ausencias:
                                anio_ausencia = int(datetime.strptime(str(ausencia.create_date), '%Y-%m-%d %H:%M:%S').date().strftime('%Y'))
                                if contrato.state == 'open' and ausencia.number_of_days > 0 and int(anio_ausencia) == int(anio_actual):
                                    asusencia_anio.append(ausencia)
                            if len(asusencia_anio) == 0 and dias_trabajados.days >= 365:
                                empleado.remaining_leaves += self.dias
                        else:
                            if contrato.state == 'open' and dias_trabajados.days >= 365:
                                empleado.remaining_leaves += self.dias
        return {'type': 'ir.actions.act_window_close'}
