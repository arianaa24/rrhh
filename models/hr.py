# -*- coding: utf-8 -*-

from odoo import models, fields, api


class hr_employee(models.Model):
    _inherit = 'hr.employee'

#    promedio_salario = fields.function(_promedio_salario, string='Promedio Salario', digits_compute=dp.get_precision('Account')),
    numero_liquidacion = fields.Char('Numero o identificacion de liquidacion')
    codigo_centro_trabajo = fields.Char('Codigo de centro de trabajo asignado')
    codigo_ocupacion = fields.Char('Codigo ocupacion')
    condicion_laboral = fields.Selection([('P', 'Permanente'), ('T', 'Temporal')], 'Condicion laboral')
    
    job_id = fields.Many2one('hr.job', 'Job Title', track_visibility='onchange')
    department_id = fields.Many2one('hr.department', 'Department', track_visibility='onchange')
    diario_pago_id = fields.Many2one('account.journal', 'Diario de Pago')
    igss = fields.Char('IGSS')
    irtra = fields.Char('IRTRA')
    nit = fields.Char('NIT')
    recibo_id = fields.Many2one('rrhh.recibo', 'Formato de recibo')
    nivel_academico = fields.Char('Nivel Academico')
    profesion = fields.Char('Profesion')
    etnia = fields.Char('Etnia')
    idioma = fields.Char('Idioma')
    pais_origen = fields.Many2one('res.country','Pais Origen')
    trabajado_extranjero = fields.Boolean('A trabajado en el extranjero')
    motivo_finalizacion = fields.Char('Motivo de finalizacion')
    jornada_trabajo = fields.Char('Jornada de Trabajo')
    permiso_trabajo = fields.Char('Permiso de Trabajo')
    contacto_emergencia = fields.Many2one('res.partner','Contacto de Emergencia')

