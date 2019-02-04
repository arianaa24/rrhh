# -*- coding: utf-8 -*-

from odoo import models, fields, api


class res_company(models.Model):
    _inherit = 'res.company'

    version_mensaje = fields.Char('Version del mensaje')
    numero_patronal = fields.Char('Numero patronal')
    tipo_planilla = fields.Selection([('0', 'Produccion'),
                                       ('1', 'Pruebas')], 'Tipo de planilla')
    codigo_centro_trabajo = fields.Char('Codigo del centro de trabajo')
    nombre_centro_trabajo = fields.Char('Nombre del centro de trabajo')
    direccion_centro_trabajo = fields.Char('Direccion del centro de trabajo')
    zona_centro_trabajo = fields.Char('Zona donde se ubica el centro de trabajo')
    telefonos = fields.Char('Telefonos (separados por guiones o diagonales)')
    fax = fields.Char('Fax')
    nombre_contacto = fields.Char('Nombre del contacto en centro de trabajo')
    correo_electronico = fields.Char('correo_electronico')
    codigo_departamento = fields.Char('Codigo departamento de la Republica')
    codigo_municipio = fields.Char('Codigo municipio de la Republica')
    codigo_actividad_economica = fields.Char('Codigo actividad economica')
    identificacion_tipo_planilla = fields.Char('Identificacion de tipo de planilla')
    nombre_tipo_planilla = fields.Char('Nombre del tipo de planilla')
    tipo_afiliados = fields.Selection([('S', 'Sin IVS'),
                                        ('C', 'Con IVS')], 'Tipo de afiliados')
    periodo_planilla = fields.Selection([('M', 'Mensual'),
                                          ('C', 'Catorcenal'),
                                          ('S', 'Semanal')], 'Periodo de planilla')
    departamento_republica = fields.Char('Depto. de la Rep. donde laboran los empleados')
    actividad_economica = fields.Char('Actividad economica')
    clase_planilla = fields.Selection([('N', 'Normal'),
                                        ('V', 'Sin movimiento')], 'Clase de planilla')
    representante_legal_id = fields.Many2one('hr.employee','Representante legal')
    ordinarias_id = fields.Many2one('hr.salary.rule','Ordinarias')
    extras_ordinarias_id = fields.Many2one('hr.salary.rule','Extras ordinarias')
    ordinario_id = fields.Many2one('hr.salary.rule','Ordinario')
    extra_ordinario_id = fields.Many2one('hr.salary.rule','Extra ordinario')
    igss_id = fields.Many2one('hr.salary.rule','IGGS')
    isr_id = fields.Many2one('hr.salary.rule','ISR')
    anticipos_id = fields.Many2one('hr.salary.rule','Anticipos')
    bonificacion_id = fields.Many2one('hr.salary.rule','Bonificacion incentivo')
    bono_id = fields.Many2one('hr.salary.rule','Bono 14')
    aguinaldo_id = fields.Many2one('hr.salary.rule','Aguinaldo')
    indemnizacion_id = fields.Many2one('hr.salary.rule','Indemnizacion')
    salario_id = fields.Many2one('hr.salary.rule','Salario')
    origen_compania = fields.Selection([('nacional', 'Nacional'),
                                    ('extranjero', 'Extranjero')], 'Nacional o Extranjero')
    barrio_colonia = fields.Char('Barrio o Colonia')
    nomenclatura = fields.Char('Nomenclatura')
    sindicato = fields.Selection([('si', 'Si'),
                                    ('no', 'No')], 'Existe sindicato')
    contratar_personal = fields.Selection([('si', 'Si'),
                                    ('no', 'No')], 'Contratar nuevo personal')
    contabilidad_completa = fields.Selection([('si', 'Si'),
                                    ('no', 'No')], 'Contabilidad completa')
    rango_ingresos = fields.Selection([('si', 'Si'),
                                    ('no', 'No')], 'Rango ingresos anual')
    jefe_recursos_humanos_id = fields.Many2one('hr.employee','Jefe de recursos humanos')
