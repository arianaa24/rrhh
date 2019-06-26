# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
import datetime
import time
import dateutil.parser
from dateutil.relativedelta import relativedelta
from odoo.fields import Date, Datetime

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    porcentaje_prestamo = fields.Float(related="payslip_run_id.porcentaje_prestamo",string='Prestamo (%)',store=True)

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
            mes_nomina = int(datetime.datetime.strptime(str(nomina.date_from), '%Y-%m-%d').date().strftime('%m'))
            dia_nomina = int(datetime.datetime.strptime(str(nomina.date_to), '%Y-%m-%d').date().strftime('%d'))
            anio_nomina = int(datetime.datetime.strptime(str(nomina.date_from), '%Y-%m-%d').date().strftime('%Y'))
            # tipos_ausencias_ids = self.env['hr.holidays.status'].search([])
            # tipos_ausencias = {
            #     'ausencias_sumar': [],
            #     'ausencias_restar': []
            # }
            # dias_ausentados_sumar = 0
            # dias_ausentados_restar = 0
            # for ausencia in tipos_ausencias_ids:
            #     if ausencia.descontar_nomina == False:
            #         tipos_ausencias['ausencias_sumar'].append(ausencia.name)
            #     else:
            #         tipos_ausencias['ausencias_restar'].append(ausencia.name)
            valor_pago = 0
            porcentaje_pagar = 0
            # for dias in nomina.worked_days_line_ids:
            #     if dias.code in tipos_ausencias['ausencias_sumar']:
            #         dias_ausentados_sumar += dias.number_of_days
            #     if dias.code in tipos_ausencias['ausencias_restar']:
            #         dias_ausentados_restar += dias.number_of_days
            # if nomina.date_from <= nomina.employee_id.contract_id.date_start <= nomina.date_to:
            #     dias_laborados = nomina.employee_id.get_work_days_data(Datetime.from_string(nomina.employee_id.contract_id.date_start), Datetime.from_string(nomina.date_to), calendar=nomina.employee_id.contract_id.resource_calendar_id)
            #     nomina.worked_days_line_ids = [(0, 0, {'name': 'Dias trabajados', 'sequence': 10,'code': 'TRABAJO100', 'number_of_days': (dias_laborados['days'] + dias_ausentados_sumar), 'contract_id': nomina.employee_id.contract_id.id})]
            # else:
            #     if nomina.employee_id.contract_id.schedule_pay == 'monthly':
            #         nomina.worked_days_line_ids = [(0, 0, {'name': 'Dias trabajados','sequence': 10,'code': 'TRABAJO100','number_of_days': 30 - dias_ausentados_restar, 'contract_id': nomina.employee_id.contract_id.id})]
            #     if nomina.employee_id.contract_id.schedule_pay == 'bi-monthly':
            #         nomina.worked_days_line_ids = [(0, 0, {'name': 'Dias trabajados','sequence': 10,'code': 'TRABAJO100','number_of_days': 15 - dias_ausentados_restar, 'contract_id': nomina.employee_id.contract_id.id})]
            # logging.warn(nomina.worked_days_line_ids)
            for entrada in nomina.input_line_ids:
                for prestamo in nomina.employee_id.prestamo_ids:
                    anio_prestamo = int(datetime.datetime.strptime(str(prestamo.fecha_inicio), '%Y-%m-%d').date().strftime('%Y'))
                    if (prestamo.codigo == entrada.code) and ((prestamo.estado == 'nuevo') or (prestamo.estado == 'proceso')):
                        lista = []
                        for lineas in prestamo.prestamo_ids:
                            if mes_nomina == lineas.mes and anio_nomina == lineas.anio:
                                lista = lineas.nomina_id.ids
                                lista.append(nomina.id)
                                lineas.nomina_id = [(6, 0, lista)]
                                valor_pago = lineas.monto
                                porcentaje_pagar =(valor_pago * (nomina.porcentaje_prestamo/100))
                                entrada.amount = porcentaje_pagar
                        cantidad_pagos = prestamo.numero_descuentos
                        cantidad_pagados = 0
                        for lineas in prestamo.prestamo_ids:
                            if lineas.nomina_id:
                                cantidad_pagados +=1
                        if cantidad_pagados > 0 and cantidad_pagados < cantidad_pagos:
                            prestamo.estado = "proceso"
                        if cantidad_pagados == cantidad_pagos and cantidad_pagos > 0:
                            prestamo.estado = "pagado"
        return res

    def salario_promedio(self, empleado_id, reglas):
        fecha_hoy = datetime.datetime.now()
        salario = 0
        nomina_ids = self.env['hr.payslip'].search([['employee_id', '=', empleado_id.id]])
        nominas = []
        contador = 1
        meses_nominas = []
        while contador <= 12:
            mes = relativedelta(months=contador)
            resta_mes = fecha_hoy - mes
            for nomina in nomina_ids:
                nomina_mes = datetime.datetime.strptime(nomina.date_from,"%Y-%m-%d")
                if nomina_mes.month == resta_mes.month and nomina_mes.year == resta_mes.year:
                    if resta_mes not in meses_nominas:
                        meses_nominas.append({resta_mes.month: resta_mes.month})
                    else:
                        meses_nominas[resta_mes.month] = resta_mes.month
                    nominas.append(nomina)
                    for linea in nomina.line_ids:
                        if linea.salary_rule_id.id in reglas:
                            salario += linea.total
            contador += 1
        return salario / len(meses_nominas)

    def get_inputs(self, contracts, date_from, date_to):
        res = super(HrPayslip, self).get_inputs(contracts, date_from, date_to)
        for contract in contracts:
            mes_nomina = int(datetime.datetime.strptime(str(date_from), '%Y-%m-%d').date().strftime('%m'))
            anio_nomina = int(datetime.datetime.strptime(str(date_from), '%Y-%m-%d').date().strftime('%Y'))
            dia_nomina = int(datetime.datetime.strptime(str(date_to), '%Y-%m-%d').date().strftime('%d'))
            monto_prestamo = 0
            for prestamo in contract.employee_id.prestamo_ids:
                for r in res:
                    anio_prestamo = int(datetime.datetime.strptime(str(prestamo.fecha_inicio), '%Y-%m-%d').date().strftime('%Y'))
                    if (prestamo.codigo == r['code']) and ((prestamo.estado == 'nuevo') or (prestamo.estado == 'proceso')):
                        for lineas in prestamo.prestamo_ids:
                            if mes_nomina == lineas.mes and anio_nomina == lineas.anio:
                                if self:
                                    r['amount'] = lineas.monto*(self.porcentaje_prestamo/100)
                                else:
                                    active_id = self.env.context.get('active_id')
                                    if active_id:
                                        [data] = self.env['hr.payslip.run'].browse(active_id).read(['porcentaje_prestamo'])
                                        r['amount'] = lineas.monto*(data.get('porcentaje_prestamo')/100)
            salario = self.salario_promedio(contract.employee_id,contract.company_id.salario_promedio_ids.ids)
            res.append({'name': 'Salario promedio', 'code': 'SalarioPromedio','amount': salario,'contract_id': contract.id})
        return res

    @api.onchange('employee_id', 'date_from', 'date_to','porcentaje_prestamo')
    def onchange_employee(self):
        res = super(HrPayslip, self).onchange_employee()
        mes_nomina = int(datetime.datetime.strptime(str(self.date_from), '%Y-%m-%d').date().strftime('%m'))
        anio_nomina = int(datetime.datetime.strptime(str(self.date_from), '%Y-%m-%d').date().strftime('%Y'))
        dia_nomina = int(datetime.datetime.strptime(str(self.date_to), '%Y-%m-%d').date().strftime('%d'))
        for prestamo in self.employee_id.prestamo_ids:
            anio_prestamo = int(datetime.datetime.strptime(str(prestamo.fecha_inicio), '%Y-%m-%d').date().strftime('%Y'))
            for inmput in self.input_line_ids:
                if (prestamo.codigo == inmput.code) and ((prestamo.estado == 'nuevo') or (prestamo.estado == 'proceso')):
                    for lineas in prestamo.prestamo_ids:
                        if mes_nomina == lineas.mes and anio_nomina == lineas.anio:
                            inmput.amount = lineas.monto*(self.porcentaje_prestamo/100)
        return res


    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        res = super(HrPayslip, self).get_worked_day_lines(contracts,date_from,date_to)
        if self.employee_id.contract_id:
            contracts = self.employee_id.contract_id
        tipos_ausencias_ids = self.env['hr.holidays.status'].search([])
        ausencias_restar = []
        dias_ausentados_restar = 0
        for ausencia in tipos_ausencias_ids:
            if ausencia.descontar_nomina:
                ausencias_restar.append(ausencia.name)
        for dias in res:
            if dias['code'] in ausencias_restar:
                dias_ausentados_restar += dias['number_of_days']
        if contracts.date_start and date_from <= contracts.date_start <= date_to:
            dias_laborados = self.employee_id.get_work_days_data(Datetime.from_string(contracts.date_start), Datetime.from_string(date_to), calendar=contracts.resource_calendar_id)
            res.append({'name': 'Dias trabajados', 'sequence': 10,'code': 'TRABAJO100', 'number_of_days': (dias_laborados['days'] + 1 - dias_ausentados_restar ), 'contract_id': contracts.id})
        elif contracts.date_end and date_from <= contracts.date_end <= date_to:
            dias_laborados = self.employee_id.get_work_days_data(Datetime.from_string(date_from), Datetime.from_string(contracts.date_end), calendar=contracts.resource_calendar_id)
            res.append({'name': 'Dias trabajados', 'sequence': 10,'code': 'TRABAJO100', 'number_of_days': ( dias_laborados['days'] + 1 - dias_ausentados_restar), 'contract_id': contracts.id})
        else:
            if contracts.schedule_pay == 'monthly':
                res.append({'name': 'Dias trabajados','sequence': 10,'code': 'TRABAJO100','number_of_days': 30 - dias_ausentados_restar, 'contract_id': contracts.id})
            if contracts.schedule_pay == 'bi-monthly':
                res.append({'name': 'Dias trabajados','sequence': 10,'code': 'TRABAJO100','number_of_days': 15 - dias_ausentados_restar, 'contract_id': contracts.id})
        return res

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    porcentaje_prestamo = fields.Float('Prestamo (%)')

    def generar_pagos(self):
        pagos = self.env['account.payment'].search([('nomina_id', '!=', False)])
        nominas_pagadas = []
        for pago in pagos:
            nominas_pagadas.append(pago.nomina_id.id)
        for nomina in self.slip_ids:
            if nomina.id not in nominas_pagadas:
                total_nomina = 0
                if nomina.employee_id.diario_pago_id and nomina.employee_id.address_home_id and nomina.state == 'done':
                    res = self.env['report.rrhh.recibo'].lineas(nomina)
                    total_nomina = res['totales'][0] + res['totales'][1]
                    pago = {
                        'payment_type': 'outbound',
                        'partner_type': 'supplier',
                        'payment_method_id': 2,
                        'partner_id': nomina.employee_id.address_home_id.id,
                        'amount': total_nomina,
                        'journal_id': nomina.employee_id.diario_pago_id.id,
                        'nomina_id': nomina.id
                    }
                    pago_id = self.env['account.payment'].create(pago)
                    #pago_id.post()
        return True

    @api.multi
    def close_payslip_run(self):
        for slip in self.slip_ids:
            if slip.state == 'draft':
                slip.action_payslip_done()

        res = super(HrPayslipRun, self).close_payslip_run()
        return res
