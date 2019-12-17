# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class InvoiceSellerReport(models.TransientModel):
    _name = 'invoice.seller.report'
    _description = 'Invoice Seller Report'

    start_date = fields.Date(required=True, default=fields.Datetime.now)
    end_date = fields.Date(required=True, default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', 'Vendedor', required=True)
    supplier_id = fields.Many2one('res.partner', 'Proveedor', required=True)
<<<<<<< HEAD
    customer_id = fields.Many2one('res.partner', 'Cliente', required=True)
=======
>>>>>>> 701f21aff508c9b25301695323e7eed1a462f58c

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.end_date < self.start_date:
            self.start_date = self.end_date

    @api.multi
    def generate_report(self):
        data = {}
<<<<<<< HEAD
        data['form'] = self.read(['start_date', 'end_date', 'user_id', 'supplier_id', 'customer_id'])[0]
=======
        data['form'] = self.read(['start_date', 'end_date', 'user_id', 'supplier_id'])[0]
>>>>>>> 701f21aff508c9b25301695323e7eed1a462f58c
        return self.env.ref('account_invoice_seller_report.action_report_invoiceseller').report_action([], data=data)
