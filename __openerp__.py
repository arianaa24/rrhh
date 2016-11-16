# -*- encoding: utf-8 -*-

#
# Status 1.0 - tested on Open ERP 8
#

{
    'name': 'rrhh',
    'version': '1.0',
    'category': 'Custom',
    'description': """
Módulo para generación de planilla
""",
    'author': 'Rodrigo Fernandez',
    'website': 'http://solucionesprisma.com/',
    'depends': ['hr_payroll'],
    'data': [
        'planilla.xml',
        'reports.xml',
        'wizard/planilla.xml',
        'views/recibo.xml',
    ],
    'demo': [],
    'installable': True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
