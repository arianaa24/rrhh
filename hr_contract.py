from openerp.osv import fields, osv
from openerp.tools.translate import _


class hr_contract_type(osv.osv):
    _inherit = "hr.contract.type"

    _columns = {
        'calcula_indemnizacion': fields.boolean('Calcula indemnizacion'),
    }

class hr_contract(osv.osv):
    _inherit = "hr.contract"

    _columns = {
        'motivo_terminacion': fields.selection([
            ('reuncia', 'Renuncia'),
            ('despido', 'Despido'),
            ('despido_justificado', 'Despido Justificado'),
            ], 'Motivo de terminacion'),
    }
