# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

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