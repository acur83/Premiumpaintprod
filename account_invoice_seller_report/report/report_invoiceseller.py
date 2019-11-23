# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ReportInvoiceSeller(models.AbstractModel):

    _name = 'report.account_invoice_seller_report.report_invoiceseller'

    @api.multi
    def get_report_user(self, data={}, payment_type='Contado', type='out_invoice'):
        start_date = data.get('start_date', False) or fields.Date.context_today(self)
        end_date = data.get('end_date', False) or fields.Date.context_today(self)
        user_id = data.get('user_id', False) and data.get('user_id', False)[0]
        
        cr = self.env.cr
        query = """ SELECT ail.id FROM account_invoice_line ail
                    JOIN account_invoice ai ON ail.invoice_id=ai.id
                    WHERE ai.date_invoice >= '{0}'
                        AND ai.date_invoice <= '{1}'
                        AND ai.type = '{2}'
                        AND ai.payment_type = '{3}'
                        AND ai.user_id = {4}
                        AND ai.state IN ('open','paid')
                """
        query = query.format(start_date, end_date, type, payment_type, user_id)
        cr.execute(query)
        result = [row[0] for row in self._cr.fetchall()]
        return self.env['account.invoice.line'].browse(result)

    @api.multi
    def get_report_values(self, docids, data=None):
        data = dict(data or {})
        return {
            'data': data.get('form', {}),
            'get_report_user': self.get_report_user
        }
