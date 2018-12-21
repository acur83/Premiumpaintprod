# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from base64 import b64decode, b64encode
from odoo import api, fields, models


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    fiscal_payment = fields.Selection([
            ('01', 'Efectivo'),
            ('02', 'Efectivo'),
            ('03', 'Efectivo'),
            ('04', 'Efectivo'),
            ('05', 'Cheque'),
            ('06', 'Cheque'),
            ('07', 'Cheque'),
            ('08', 'Cheque'),
            ('09', 'Tarjeta 1'),
            ('10', 'Tarjeta 1'),
            ('11', 'Tarjeta 1'),
            ('12', 'Tarjeta 1'),
            ('13', 'Tarjeta 2'),
            ('14', 'Tarjeta 2'),
            ('15', 'Tarjeta 2'),
            ('16', 'Credito')
        ], string='Medio de Pago', required=True, default=lambda *a:'01')

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    fiscal_printer_status = fields.Selection([
            ('unsent','Sin enviar'),
            ('sent','Enviada'),
            ('printed','Impresa'),
        ], 'Impresora Fiscal', readonly=True, default=lambda *a: 'unsent')

    @api.multi
    def send_invoice_proxy(self):
        self.ensure_one()
        cmd = "jR%s"%(self.partner_id.vat,)
        cmd += "\njS%s"%(self.partner_id.name,)
        cmd += "\nj%s"%(self.partner_id.street,) if self.partner_id.street else ''
        for line in self.invoice_line_ids:
            if line.invoice_line_tax_ids:
                tmp = '\n!{:011.2f}{:09.3f}{}'.format(line.price_unit, line.quantity, line.name.replace('\n','')[:117])
                cmd += tmp.replace('.','')
            else:
                tmp = '\n {:011.2f}{:09.3f}{}'.format(line.price_unit, line.quantity, line.name.replace('\n','')[:117])
                cmd += tmp.replace('.','')
        cmd += "\n3\n1%s"%(self.payment_term_id and self.payment_term_id.fiscal_payment or '01')
        if self.payment_term_id and self.payment_term_id.fiscal_payment == '16':
            cmd += "\nRU00000000000000"
        cmd = b64encode(cmd.encode('utf-8'))
        self.fiscal_printer_status = 'sent'
        proxy_url = self.env['ir.config_parameter'].sudo().get_param(
            'fiscal.printer.proxy.url', 'http://127.0.0.1:8080')
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '%s/sendcmd/%s'%(proxy_url, cmd.decode("utf-8"),),
        }

    @api.multi
    def send_credit_proxy(self):
        self.ensure_one()
        cmd = "iR%s"%(self.partner_id.vat,)
        cmd += "\niS%s"%(self.partner_id.name,)
        cmd += "\niFTBSR110004190-00005321"
        cmd += "\ni%s"%(self.partner_id.street,) if self.partner_id.street else ''
        for line in self.invoice_line_ids:
            if line.invoice_line_tax_ids:
                tmp = '\nd1{:011.2f}{:09.3f}{}'.format(line.price_unit, line.quantity, line.name.replace('\n','')[:117])
                cmd += tmp.replace('.','')
            else:
                tmp = '\nd0{:011.2f}{:09.3f}{}'.format(line.price_unit, line.quantity, line.name.replace('\n','')[:117])
                cmd += tmp.replace('.','')
        cmd += "\nf01"
        cmd = b64encode(cmd.encode('utf-8'))
        self.fiscal_printer_status = 'sent'
        proxy_url = self.env['ir.config_parameter'].sudo().get_param(
            'fiscal.printer.proxy.url', 'http://127.0.0.1:8080')
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '%s/sendcmd/%s'%(proxy_url, cmd.decode("utf-8"),),
        }
    