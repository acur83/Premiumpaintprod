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
        supplier_id = data.get('supplier_id', False) and data.get('supplier_id', False)[0]
<<<<<<< HEAD
        customer_id = data.get('customer_id', False) and data.get('customer_id', False)[0]
=======
>>>>>>> 701f21aff508c9b25301695323e7eed1a462f58c
        domain = [('name','=',supplier_id)]
        supplierinfo = self.env['product.supplierinfo'].search(domain)
        product_tmpl_ids = [si.product_tmpl_id.id for si in supplierinfo]
        domain = [('product_tmpl_id','in',product_tmpl_ids)]
        products = self.env['product.product'].search(domain)
        product_ids = [p.id for p in products]
        if not product_ids:
            return self.env['account.invoice.line']

        cr = self.env.cr
<<<<<<< HEAD
        if customer_id:
            query = """ SELECT ail.id FROM account_invoice_line ail
                    JOIN account_invoice ai ON ail.invoice_id=ai.id
                    WHERE ai.date_invoice >= %s
                        AND ai.date_invoice <= %s
                        AND ai.partner_id <= %s
=======
        query = """ SELECT ail.id FROM account_invoice_line ail
                    JOIN account_invoice ai ON ail.invoice_id=ai.id
                    WHERE ai.date_invoice >= %s
                        AND ai.date_invoice <= %s
>>>>>>> 701f21aff508c9b25301695323e7eed1a462f58c
                        AND ai.type IN ('out_invoice','out_refund')
                        AND ai.payment_type = %s
                        AND ai.user_id = %s
                        AND ai.state IN ('open','paid')
                        AND ail.product_id IN %s
                """
<<<<<<< HEAD
            args = (start_date, end_date, customer_id, payment_type, user_id, tuple(product_ids))
        else:
            query = """ SELECT ail.id FROM account_invoice_line ail
                    JOIN account_invoice ai ON ail.invoice_id=ai.id
                    WHERE ai.date_invoice >= %s
                        AND ai.date_invoice <= %s
                        AND ai.type IN ('out_invoice','out_refund')
                        AND ai.payment_type = %s
                        AND ai.user_id = %s
                        AND ai.state IN ('open','paid')
                        AND ail.product_id IN %s
                """
            args = (start_date, end_date,payment_type, user_id, tuple(product_ids))
=======
        args = (start_date, end_date,payment_type, user_id, tuple(product_ids))
>>>>>>> 701f21aff508c9b25301695323e7eed1a462f58c
        cr.execute(query, args)
        result = [row[0] for row in self._cr.fetchall()]
        return self.env['account.invoice.line'].browse(result).sorted(key=lambda r: r.invoice_id.date_invoice)

    @api.multi
    def get_report_values(self, docids, data=None):
        data = dict(data or {})
        return {
            'data': data.get('form', {}),
            'get_report_user': self.get_report_user
        }
