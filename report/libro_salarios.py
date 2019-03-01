# -*- encoding: utf-8 -*-

from odoo import api, models, fields
import time
import datetime
from datetime import date
from datetime import datetime, date, time
import logging

class ReportLibroSalarios(models.AbstractModel):
    _name = 'report.rrhh.libro_salarios'

    def _get_contrato(self,id):
        contrato_id = self.env['hr.contract'].search([['employee_id', '=', id]])
        return {'fecha_ingreso':contrato_id.date_start,'fecha_finalizacion': contrato_id.date_end}

    def _get_empleado(self,id):
        empleado_id = self.env['hr.employee'].search([['id', '=', id]])
        return empleado_id

    def _get_nominas(self,id,anio):
        nomina_id = self.env['hr.payslip'].search([['employee_id', '=', id]],order="date_from asc")
        nominas_lista = []
        for nomina in nomina_id:
            nomina_anio = datetime.strptime(nomina.date_from, "%Y-%m-%d").year
            if anio == nomina_anio:
                salario = 0
                dias_trabajados = 0
                ordinarias = 0
                extra_ordinarias = 0
                ordinario = 0
                extra_ordinario = 0
                igss = 0
                isr = 0
                anticipos = 0
                bonificacion = 0
                bono = 0
                aguinaldo = 0
                indemnizacion = 0
                for linea in nomina.line_ids:
                    if linea.salary_rule_id in nomina.company_id.salario_ids:
                        salario += linea.total
                    if linea.salary_rule_id in nomina.company_id.ordinarias_ids:
                        ordinarias += linea.total
                    if linea.salary_rule_id in nomina.company_id.extras_ordinarias_ids:
                        extra_ordinarias += linea.total
                    if linea.salary_rule_id in nomina.company_id.ordinario_ids:
                        ordinario += linea.total
                    if linea.salary_rule_id in nomina.company_id.extra_ordinario_ids:
                        extra_ordinario += linea.total
                    if linea.salary_rule_id in nomina.company_id.igss_ids:
                        igss += linea.total
                    if linea.salary_rule_id in nomina.company_id.isr_ids:
                        isr += linea.total
                    if linea.salary_rule_id in nomina.company_id.anticipos_ids:
                        anticipos += linea.total
                    if linea.salary_rule_id in nomina.company_id.bonificacion_ids:
                        bonificacion += linea.total
                    if linea.salary_rule_id in nomina.company_id.bono_ids:
                        bono += linea.total
                    if linea.salary_rule_id in nomina.company_id.aguinaldo_ids:
                        aguinaldo += linea.total
                    if linea.salary_rule_id in nomina.company_id.indemnizacion_ids:
                        indemnizacion += linea.total
                for linea in nomina.worked_days_line_ids:
                    dias_trabajados += linea.number_of_days
                total_salario_devengado = ordinarias + extra_ordinarias + ordinario + extra_ordinario
                total_descuentos = igss + isr + anticipos
                bono_agui_indem = bono + aguinaldo + indemnizacion
                nominas_lista.append({
                    'fecha_inicio': nomina.date_from,
                    'fecha_fin': nomina.date_to,
                    'moneda_id': nomina.journal_id.currency_id,
                    'salario': salario,
                    'dias_trabajados': dias_trabajados,
                    'ordinarias': ordinarias,
                    'extra_ordinarias': extra_ordinarias,
                    'ordinario': ordinario,
                    'extra_ordinario': extra_ordinario,
                    'total_salario_devengado': total_salario_devengado,
                    'igss': igss,
                    'isr': isr,
                    'anticipos': anticipos,
                    'total_descuentos': total_descuentos,
                    'bonificacion_id': bonificacion,
                    'bono_agui_indem': bono_agui_indem,
                    'liquido_recibir': total_salario_devengado + total_descuentos + bonificacion + bono_agui_indem

                })
        return nominas_lista

    @api.model
    def get_report_values(self, docids, data=None):
        data = data if data is not None else {}
        self.model = 'hr.employee'
        docs = data.get('ids', data.get('active_ids'))
        anio = data.get('form', {}).get('anio', False)
        logging.warn(anio)
        return {
            'doc_ids': docids,
            'doc_model': self.model,
            'docs': docs,
            'anio': anio,
            '_get_empleado': self._get_empleado,
            '_get_contrato': self._get_contrato,
            '_get_nominas': self._get_nominas,
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
