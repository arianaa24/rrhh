# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import datetime

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        for slip in self:
            if slip.move_id:
                slip.move_id.button_cancel()
                for line in slip.move_id.line_ids:
                    line.analytic_account_id = slip.contract_id.analytic_account_id.id
                slip.move_id.post()
        return res

    @api.multi
    def compute_sheet(self):
        res =  super(HrPayslip, self).compute_sheet()
        for nomina in self:
            mes_nomina = int(datetime.datetime.strptime(nomina.date_from, '%Y-%m-%d').date().strftime('%m'))
            dia_nomina = int(datetime.datetime.strptime(nomina.date_to, '%Y-%m-%d').date().strftime('%d'))
            anio_nomina = int(datetime.datetime.strptime(nomina.date_from, '%Y-%m-%d').date().strftime('%Y'))
            if dia_nomina > 20:
                for entrada in nomina.input_line_ids:
                    for prestamo in nomina.employee_id.prestamo_ids:
                        anio_prestamo = int(datetime.datetime.strptime(prestamo.fecha_inicio, '%Y-%m-%d').date().strftime('%Y'))
                        if (prestamo.codigo == entrada.code) and ((prestamo.estado == 'nuevo') or (prestamo.estado == 'proceso')):
                            for plan in prestamo.plan_ids:
                                if mes_nomina == plan.mes and anio_nomina == plan.anio:
                                    plan.nomina_id = nomina.id
                            cantidad_pagos = prestamo.numero_descuentos
                            cantidad_pagados = 0
                            for pago in prestamo.plan_ids:
                                if pago.nomina_id:
                                    cantidad_pagados +=1
                            logging.warn(cantidad_pagados)
                            if cantidad_pagados > 0 and cantidad_pagados < cantidad_pagos:
                                prestamo.estado = "proceso"
                            if cantidad_pagados == cantidad_pagos and cantidad_pagos > 0:
                                prestamo.estado = "pagado"
        return res

    def get_inputs(self, contracts, date_from, date_to):
        res = super(HrPayslip, self).get_inputs(contracts, date_from, date_to)
        for contract in contracts:
            mes_nomina = int(datetime.datetime.strptime(date_from, '%Y-%m-%d').date().strftime('%m'))
            anio_nomina = int(datetime.datetime.strptime(date_from, '%Y-%m-%d').date().strftime('%Y'))
            dia_nomina = int(datetime.datetime.strptime(date_to, '%Y-%m-%d').date().strftime('%d'))
            monto_prestamo = 0
            if dia_nomina > 20:
                for prestamo in contract.employee_id.prestamo_ids:
                    for r in res:
                        anio_prestamo = int(datetime.datetime.strptime(prestamo.fecha_inicio, '%Y-%m-%d').date().strftime('%Y'))
                        if (prestamo.codigo == r['code']) and (prestamo.estado == 'nuevo') :
                            for plan in prestamo.plan_ids:
                                if mes_nomina == plan.mes and anio_nomina == plan.anio:
                                    r['amount'] = plan.monto
        return res
