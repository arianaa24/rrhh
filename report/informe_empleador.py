# -*- encoding: utf-8 -*-

from odoo import api, models, fields
import time
import datetime
from datetime import date
from datetime import datetime, date, time
import logging

class ReportInformeEmpleador(models.AbstractModel):
    _name = 'report.rrhh.informe_empleador'

    def datos_compania(self,data=None):
        data = data if data is not None else {}
        logging.warn(data)
        empleados = data.get('ids', data.get('active_ids'))
        logging.warn(empleados)
        empleado_id = self.env['hr.employee'].search([['id', '=', empleados[0]]])
        compania = self.env['res.company'].search([['id', '=', empleado_id.company_id.id]])
        return compania

    @api.model
    def get_report_values(self, docids, data=None):
        data = data if data is not None else {}
        self.model = 'hr.employee'
        docs = data.get('ids', data.get('active_ids'))
        anio = data.get('form', {}).get('anio', False)

        return {
            'doc_ids': docids,
            'doc_model': self.model,
            'docs': docs,
            'anio': anio,
            'datos_compania': datos_compania,
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
