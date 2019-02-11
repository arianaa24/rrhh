# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import xlwt
import base64
import io
import logging
import time
import datetime
from datetime import date
from datetime import datetime, date, time
import itertools

class rrhh_informe_empleador(models.TransientModel):
    _name = 'rrhh.informe_empleador'

    anio = fields.Integer('Año', required=True)
    name = fields.Char('Nombre archivo', size=32)
    archivo = fields.Binary('Archivo', filters='.xls')

    def empleados_inicio_anio(self,company_id,anio):
        empleados = 0
        empleado_ids = self.env['hr.employee'].search([['company_id', '=', company_id]])
        for empleado in empleado_ids:
            if empleado.contract_ids:
                anio_fin_contrato = 0
                anio_inicio_contrato = datetime.strptime(empleado.contract_ids.date_start, "%Y-%m-%d").year
                if empleado.contract_ids.date_end:
                    anio_fin_contrato = datetime.strptime(empleado.contract_ids.date_end, "%Y-%m-%d").year
                if anio_inicio_contrato < anio and (empleado.contract_ids.date_end == False or anio_fin_contrato < anio) :
                    empleados += 1
        return empleados

    def empleados_fin_anio(self,company_id,anio):
        empleados = 0
        empleado_ids = self.env['hr.employee'].search([['company_id', '=', company_id]])
        for empleado in empleado_ids:
            if empleado.contract_ids:
                anio_fin_contrato = 0
                anio_inicio_contrato = datetime.strptime(empleado.contract_ids.date_start, "%Y-%m-%d").year
                if empleado.contract_ids.date_end:
                    anio_fin_contrato = datetime.strptime(empleado.contract_ids.date_end, "%Y-%m-%d").year
                if anio_inicio_contrato <= anio and (empleado.contract_ids.date_end == False or anio_fin_contrato <= anio) :
                    empleados += 1
        return empleados

    @api.multi
    def print_report(self):
        datas = {'ids': self.env.context.get('active_ids', [])}
        res = self.read(['anio'])
        res = res and res[0] or {}
        res['anio'] = res['anio']
        datas['form'] = res
        return self.env.ref('rrhh.action_informe_empleador').report_action([], data=datas)

    def print_report_excel(self):
        for w in self:
            dict = {}
            empleados_id = self.env.context.get('active_ids', [])
            datos_compania = self.env['hr.employee'].search([['id', '=', empleados_id[0]]]).company_id
            libro = xlwt.Workbook()
            dict['anio'] = w['anio']
            empleados = self.env['hr.employee'].search([['id', 'in', empleados_id]])
            responsable_id = self.env['hr.employee'].search([['id', '=', self.env.user.id]])

            # ESTILOS
            estilo_borde = xlwt.easyxf('border: bottom thin, left thin,right thin, top thin')
            xlwt.add_palette_colour("custom_colour", 0x21)
            libro.set_colour_RGB(0x21, 58, 137, 255)
            estilo = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour;border: bottom thin, left thin,right thin, top thin;align: wrap on, vert centre, horiz center')

            hoja_patrono = libro.add_sheet('Patrono')
            empleados_inicio_anio = self.empleados_inicio_anio(datos_compania.id,w['anio'])
            empleados_fin_anio = self.empleados_fin_anio(datos_compania.id,w['anio'])
            col_width = 100 * 20
            row_height = 35 * 30

            lista = [0,1]
            try:
                for i in lista:
                    hoja_patrono.col(i).width = col_width
                    hoja_patrono.row(i).height = row_height
            except ValueError:
                pass

            default_book_style = libro.default_style
            default_book_style.font.height = 20 * 36    # 36pt

            hoja_patrono.write(1, 0, 'Nombre, Denominación  o Razón Social del Patrono', estilo)
            hoja_patrono.write(1, 1, 'Nacional o Extranjero',estilo)
            hoja_patrono.write(1, 2, 'Número  Patronal IGSS',estilo)
            hoja_patrono.write(1, 3, 'Nit',estilo)
            hoja_patrono.write(1, 4, 'Nombre Empresa',estilo)
            hoja_patrono.write(1, 5, 'Actividad Economica ',estilo)
            hoja_patrono.write(1, 6, 'Teléfono',estilo)
            hoja_patrono.write(1, 7, 'Email ',estilo)
            hoja_patrono.write(1, 8, 'Sitio Web',estilo)
            hoja_patrono.write(1, 9, 'Ubicación Geográfica',estilo)

            hoja_patrono.write_merge(0, 0,10,14, 'Dirección',estilo)
            hoja_patrono.write(1, 10, 'Zona',estilo)
            hoja_patrono.write(1, 11, 'Barrio o colonia',estilo)
            hoja_patrono.write(1, 12, 'Avenida',estilo)
            hoja_patrono.write(1, 13, 'Calle',estilo)
            hoja_patrono.write(1, 14, 'Nomenclatura',estilo)

            xlwt.add_palette_colour("custom_colour_purp", 0x22)
            libro.set_colour_RGB(0x22, 107, 54, 250)
            estilo_morado = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour_purp;border: bottom thin, left thin,right thin, top thin;align: wrap on, vert centre, horiz center')

            hoja_patrono.write(1, 15, 'Persona Responsable de elaborar el informe',estilo_morado)
            hoja_patrono.write(1, 16, 'Documento Identificación Responsable',estilo_morado)
            hoja_patrono.write(1, 17, 'Email de la empresa del  Responsable',estilo_morado)
            hoja_patrono.write(1, 18, 'Telefono del Resposable',estilo_morado)
            hoja_patrono.write(1, 19, 'Pais Origen responsable',estilo_morado)

            xlwt.add_palette_colour("custom_colour_gree", 0x23)
            libro.set_colour_RGB(0x23, 25, 51, 0)
            estilo_verde = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour_gree;border: bottom thin, left thin,right thin, top thin;align: wrap on, vert centre, horiz center')

            hoja_patrono.write(1, 20, 'Existe sindicato',estilo_verde)
            hoja_patrono.write(1, 21, 'Cantidad Total Empleados Inicio de Año',estilo_verde)
            hoja_patrono.write(1, 22, 'Cantidad Total Empleados Final de Año',estilo_verde)
            hoja_patrono.write(1, 23, 'Tiene planificado contratar nuevo personal',estilo_verde)
            hoja_patrono.write(1, 24, 'Medir Rango de Ingresos Anual',estilo_verde)
            hoja_patrono.write(1, 25, 'Contabilidad Completa de la empresa',estilo_verde)
            hoja_patrono.write(1, 26, 'Nombre Representante legal',estilo_verde)
            hoja_patrono.write(1, 27, 'Documento Identificación ',estilo_verde)
            hoja_patrono.write(1, 28, 'Nacionalidad del Representante Legal',estilo_verde)
            hoja_patrono.write(1, 29, 'Nombre Jefe de Recursos Humanos',estilo_verde)
            hoja_patrono.write(1, 30, 'Año Informe',estilo_verde)

            hoja_patrono.write(2, 0, datos_compania.company_registry, estilo_borde)
            hoja_patrono.write(2, 1, datos_compania.origen_compania, estilo_borde)
            hoja_patrono.write(2, 2, datos_compania.numero_patronal, estilo_borde)
            hoja_patrono.write(2, 3, datos_compania.vat, estilo_borde)
            hoja_patrono.write(2, 4, datos_compania.name, estilo_borde)
            hoja_patrono.write(2, 5, datos_compania.actividad_economica, estilo_borde)
            hoja_patrono.write(2, 6, datos_compania.phone, estilo_borde)
            hoja_patrono.write(2, 7, datos_compania.email, estilo_borde)
            hoja_patrono.write(2, 8, datos_compania.website, estilo_borde)
            hoja_patrono.write(2, 9, datos_compania.zip, estilo_borde)

            hoja_patrono.write(2, 10, datos_compania.zona_centro_trabajo, estilo_borde)
            hoja_patrono.write(2, 11, datos_compania.barrio_colonia, estilo_borde)
            hoja_patrono.write(2, 12, datos_compania.street, estilo_borde)
            hoja_patrono.write(2, 13, datos_compania.street2, estilo_borde)
            hoja_patrono.write(2, 14, datos_compania.nomenclatura, estilo_borde)

            hoja_patrono.write(2, 15, responsable_id.name, estilo_borde)
            hoja_patrono.write(2, 16, responsable_id.identification_id, estilo_borde)
            hoja_patrono.write(2, 17, responsable_id.work_email, estilo_borde)
            hoja_patrono.write(2, 18, responsable_id.work_phone, estilo_borde)
            hoja_patrono.write(2, 19, responsable_id.country_id.name, estilo_borde)

            hoja_patrono.write(2, 20, datos_compania.sindicato, estilo_borde)
            hoja_patrono.write(2, 21, empleados_inicio_anio, estilo_borde)
            hoja_patrono.write(2, 22, empleados_fin_anio, estilo_borde)
            hoja_patrono.write(2, 23, datos_compania.contratar_personal, estilo_borde)
            hoja_patrono.write(2, 24, datos_compania.rango_ingresos, estilo_borde)
            hoja_patrono.write(2, 25, datos_compania.contabilidad_completa, estilo_borde)
            hoja_patrono.write(2, 26, datos_compania.representante_legal_id.name, estilo_borde)
            hoja_patrono.write(2, 27, datos_compania.representante_legal_id.identification_id, estilo_borde)
            hoja_patrono.write(2, 28, datos_compania.representante_legal_id.country_id.name, estilo_borde)
            hoja_patrono.write(2, 29, datos_compania.jefe_recursos_humanos_id.name, estilo_borde)
            hoja_patrono.write(2, 30, dict['anio'])


            hoja_empleado = libro.add_sheet('Empleado')
            datos = libro.add_sheet('Hoja2')
            xlwt.add_palette_colour("custom_colour_pink", 0x24)
            libro.set_colour_RGB(0x24, 228, 55, 247)
            estilo_rosado = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour_purp;border: bottom thin, left thin,right thin, top thin;align: wrap on, vert centre, horiz center')

            lista = [0]
            try:
                for i in lista:
                    hoja_empleado.col(i).width = col_width
                    hoja_empleado.row(i).height = row_height
            except ValueError:
                pass

            hoja_empleado.write(0, 0, 'Numero de trabajadores',estilo_rosado)
            hoja_empleado.write(0, 1, 'Primer Nombre',estilo_rosado)
            hoja_empleado.write(0, 2, 'Segundo Nombre',estilo_rosado)
            hoja_empleado.write(0, 3, 'Primer Apellido',estilo_rosado)
            hoja_empleado.write(0, 4, 'Segundo Apellido',estilo_rosado)
            hoja_empleado.write(0, 5, 'Nacionalidad',estilo_rosado)
            hoja_empleado.write(0, 6, 'Estado Civil',estilo_rosado)
            hoja_empleado.write(0, 7, 'Documento Identificación',estilo_rosado)
            hoja_empleado.write(0, 8, 'Número de Documento',estilo_rosado)
            hoja_empleado.write(0, 9, 'Pais Origen',estilo_rosado)
            hoja_empleado.write(0, 10, 'Lugar Nacimiento',estilo_rosado)
            hoja_empleado.write(0, 11, 'NIT',estilo_rosado)
            hoja_empleado.write(0, 12, 'Número de Afiliación IGSS',estilo_rosado)
            hoja_empleado.write(0, 13, 'Sexo (M) O (F)',estilo_rosado)
            hoja_empleado.write(0, 14, 'Fecha Nacimiento',estilo_rosado)
            hoja_empleado.write(0, 15, 'Cantidad de Hijos',estilo_rosado)
            hoja_empleado.write(0, 16, 'A trabajado en el extranjero ',estilo_rosado)
            hoja_empleado.write(0, 17, 'En que forma',estilo_rosado)
            hoja_empleado.write(0, 18, 'Pais',estilo_rosado)
            hoja_empleado.write(0, 19, 'Motivo de finalización de la relación laboral en el extranjero',estilo_rosado)
            hoja_empleado.write(0, 20, 'Nivel Academico',estilo_rosado)
            hoja_empleado.write(0, 21, 'Profesión',estilo_rosado)
            hoja_empleado.write(0, 22, 'Etnia',estilo_rosado)
            hoja_empleado.write(0, 23, 'Idioma',estilo_rosado)

            xlwt.add_palette_colour("custom_colour_azul", 0x25)
            libro.set_colour_RGB(0x25, 55, 81, 247)
            estilo_azul = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour_azul;border: bottom thin, left thin,right thin, top thin')
            hoja_empleado.write(0, 24, 'Tipo Contrato',estilo_azul)
            hoja_empleado.write(0, 25, 'Fecha Inicio Labores',estilo_azul)
            hoja_empleado.write(0, 26, 'Fecha Reinicio-laboreso',estilo_azul)
            hoja_empleado.write(0, 27, 'Fecha Retiro Labores',estilo_azul)
            hoja_empleado.write(0, 28, 'Puesto',estilo_azul)
            hoja_empleado.write(0, 29, 'Jornada de Trabajo',estilo_azul)
            hoja_empleado.write(0, 30, 'Dias Laborados en el Año',estilo_azul)



            xlwt.add_palette_colour("custom_colour_amarillo", 0x26)
            libro.set_colour_RGB(0x26, 239, 255, 0)
            estilo_amarillo = xlwt.easyxf('pattern: pattern solid, fore_colour custom_colour_amarillo;border: bottom thin, left thin,right thin, top thin;align: wrap on, vert centre, horiz center')
            hoja_empleado.write(0, 31, 'Permiso de  Trabajo',estilo_amarillo)
            hoja_empleado.write(0, 32, 'Salario Anual Nominal',estilo_amarillo)
            hoja_empleado.write(0, 33, 'Bonificación Decreto 78-89  (Q.250.00)',estilo_amarillo)
            hoja_empleado.write(0, 34, 'Total Horas Extras Anuales',estilo_amarillo)
            hoja_empleado.write(0, 35, 'Valor de Hora Extra',estilo_amarillo)
            hoja_empleado.write(0, 36, 'Monto Aguinaldo Decreto 76-78',estilo_amarillo)
            hoja_empleado.write(0, 37, 'Monto Bono 14  Decreto 42-92,estilo_amarillo',estilo_amarillo)
            hoja_empleado.write(0, 38, 'Retribución por Comisiones',estilo_amarillo)
            hoja_empleado.write(0, 39, 'Viaticos',estilo_amarillo)
            hoja_empleado.write(0, 40, 'Bonificaciones Adicionales',estilo_amarillo)
            hoja_empleado.write(0, 41, 'Retribución por vacaciones',estilo_amarillo)
            hoja_empleado.write(0, 42, 'Retribución por Indemnización (Articulo 82)',estilo_amarillo)
            hoja_empleado.write(0, 43, 'Nombre, Denominación  o Razón Social del Patrono',estilo_amarillo)

            fila = 1
            empleado_numero = 1
            numero = 1
            for empleado in empleados:
                nombre_empleado = empleado.name.split( )
                if len(nombre_empleado) >=4:
                    nominas_lista = []
                    contrato = self.env['hr.contract'].search([['employee_id', '=', empleado.id]])
                    nomina_id = self.env['hr.payslip'].search([['employee_id', '=', empleado.id]])
                    dias_trabajados = 0
                    salario_anual_nominal = 0
                    bonificacion = 0
                    estado_civil = 0
                    horas_extras = 0
                    aguinaldo = 0
                    bono = 0
                    bonificaciones_adicionales = 0
                    valor_horas_extras = 0
                    retribucion_comisiones = 0
                    viaticos = 0
                    retribucion_vacaciones = 0
                    indemnizacion = 0
                    for nomina in nomina_id:
                        nomina_anio = datetime.strptime(nomina.date_from, "%Y-%m-%d").year
                        if w['anio'] == nomina_anio:
                            for linea in nomina.worked_days_line_ids:
                                dias_trabajados += linea.number_of_days
                            for linea in nomina.line_ids:
                                if linea.salary_rule_id in nomina.company_id.salario_ids:
                                    salario_anual_nominal += linea.total
                                if linea.salary_rule_id in nomina.company_id.bonificacion_ids:
                                    bonificacion = linea.total
                                if linea.salary_rule_id in nomina.company_id.aguinaldo_ids:
                                    aguinaldo = linea.total
                                if linea.salary_rule_id in nomina.company_id.bono_ids:
                                    bono = linea.total
                                if linea.salary_rule_id in nomina.company_id.horas_extras_ids:
                                    horas_extras = linea.quantity
                                    valor_horas_extras = linea.total
                                if linea.salary_rule_id in nomina.company_id.retribucion_comisiones_ids:
                                    retribucion_comisiones = linea.total
                                if linea.salary_rule_id in nomina.company_id.viaticos_ids:
                                    viaticos = linea.total
                                if linea.salary_rule_id in nomina.company_id.retribucion_vacaciones_ids:
                                    retribucion_vacaciones = linea.total
                                if linea.salary_rule_id in nomina.company_id.indemnizacion_ids:
                                    indemnizacion = linea.total
                                if linea.salary_rule_id in nomina.company_id.bonificaciones_adicionales_ids:
                                    bonificaciones_adicionales = linea.total
                    if empleado.gender == 'male':
                        genero = 'H'
                    if empleado.gender == 'female':
                        genero = 'M'
                    if empleado.marital == 'single':
                        estado_civil = 1
                    if empleado.marital == 'married':
                        estado_civil = 2
                    if empleado.marital == 'widower':
                        estado_civil = 3
                    if empleado.marital == 'divorced':
                        estado_civil = 4
                    if empleado.marital == 'separado':
                        estado_civil = 5
                    if empleado.marital == 'unido':
                        estado_civil = 6
                    hoja_empleado.write(fila, 0, empleado_numero,estilo_borde)
                    hoja_empleado.write(fila, 1, nombre_empleado[0],estilo_borde)
                    hoja_empleado.write(fila, 2, nombre_empleado[1],estilo_borde)
                    hoja_empleado.write(fila, 3, nombre_empleado[2],estilo_borde)
                    hoja_empleado.write(fila, 4, nombre_empleado[3],estilo_borde)
                    hoja_empleado.write(fila, 5, empleado.country_id.informe_empleador_id,estilo_borde)
                    hoja_empleado.write(fila, 6, estado_civil,estilo_borde)
                    hoja_empleado.write(fila, 7, empleado.documento_identificacion,estilo_borde)
                    hoja_empleado.write(fila, 8, empleado.identification_id,estilo_borde)
                    hoja_empleado.write(fila, 9, empleado.pais_origen.name,estilo_borde)
                    hoja_empleado.write(fila, 10, empleado.place_of_birth,estilo_borde)
                    hoja_empleado.write(fila, 11, empleado.nit,estilo_borde)
                    hoja_empleado.write(fila, 12, empleado.igss,estilo_borde)
                    hoja_empleado.write(fila, 13, genero,estilo_borde)
                    hoja_empleado.write(fila, 14, empleado.birthday,estilo_borde)
                    hoja_empleado.write(fila, 15, empleado.children,estilo_borde)
                    hoja_empleado.write(fila, 16, empleado.trabajado_extranjero,estilo_borde)
                    hoja_empleado.write(fila, 17, empleado.forma_trabajo_extranjero,estilo_borde)
                    hoja_empleado.write(fila, 18, empleado.pais_trabajo_extranjero_id.name,estilo_borde)
                    hoja_empleado.write(fila, 19, empleado.finalizacion_laboral_extranjero,estilo_borde)
                    hoja_empleado.write(fila, 20, empleado.nivel_academico,estilo_borde)
                    hoja_empleado.write(fila, 21, empleado.profesion,estilo_borde)
                    hoja_empleado.write(fila, 22, empleado.etnia,estilo_borde)
                    hoja_empleado.write(fila, 23, empleado.idioma,estilo_borde)
                    hoja_empleado.write(fila, 24, contrato.type_id.name,estilo_borde)
                    hoja_empleado.write(fila, 25, contrato.date_start,estilo_borde)
                    hoja_empleado.write(fila, 26, contrato.fecha_reinicio_labores,estilo_borde)
                    hoja_empleado.write(fila, 27, contrato.date_end,estilo_borde)
                    hoja_empleado.write(fila, 28, contrato.job_id.name,estilo_borde)
                    hoja_empleado.write(fila, 29, contrato.resource_calendar_id.name,estilo_borde)
                    hoja_empleado.write(fila, 30, dias_trabajados,estilo_borde)
                    hoja_empleado.write(fila, 31, empleado.permiso_trabajo,estilo_borde)
                    hoja_empleado.write(fila, 32, salario_anual_nominal,estilo_borde)
                    hoja_empleado.write(fila, 33, bono,estilo_borde)
                    hoja_empleado.write(fila, 34, horas_extras,estilo_borde)
                    hoja_empleado.write(fila, 35, valor_horas_extras,estilo_borde)
                    hoja_empleado.write(fila, 36, aguinaldo,estilo_borde)
                    hoja_empleado.write(fila, 37, bono,estilo_borde)
                    hoja_empleado.write(fila, 38, retribucion_comisiones,estilo_borde)
                    hoja_empleado.write(fila, 39, viaticos,estilo_borde)
                    hoja_empleado.write(fila, 40, bonificaciones_adicionales,estilo_borde)
                    hoja_empleado.write(fila, 41, retribucion_vacaciones,estilo_borde)
                    hoja_empleado.write(fila, 42, indemnizacion,estilo_borde)
                    hoja_empleado.write(fila, 43, datos_compania.company_registry,estilo_borde)
                    empleado_numero +=1

                    fila += 1
                    numero += 1

            f = io.BytesIO()
            libro.save(f)
            datos = base64.b64encode(f.getvalue())
            self.write({'archivo':datos, 'name':'informe_del_empleador.xls'})

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'rrhh.informe_empleador',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
