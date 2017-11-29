## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import xlrd
import shutil
import logging
_logger = logging.getLogger(__name__)

class AccountInvoiceLIne(models.Model):
    _inherit ='account.invoice.line'
    costo= fields.Float(string='Costo')
    utilidad = fields.Float(string='Utilidad')

    @api.onchange('product_id')
    def costoproduct_onchange(self):
        self.costo=self.product_id.standard_price
    @api.model
    def create(self,vals):
        #producto = self.env['product.product'].search([('id','=',vals['product_id'])])
        if 'costo' in vals:
            costo= vals['costo']
            total=  vals['price_unit'] - costo
            vals['utilidad']=total * vals['quantity']
        else:
            producto = self.env['product.product'].search([('id', '=', vals['product_id'])])
            costo = producto.standard_price
            total = vals['price_unit'] - costo
            vals['utilidad'] = total * vals['quantity']
        return super(AccountInvoiceLIne,self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get("costo") is not None:
            costo = vals.get("costo")
            precio =self.price_unit
            qty=self.quantity
            total = precio- costo
            vals['utilidad'] = total * qty
        return super(AccountInvoiceLIne, self).write(vals)
class AccountInvoice(models.Model):
    _inherit='account.invoice'
    ganancy= fields.Float(string="ganancia", store=True, compute="_compute_ganancy")

    @api.one
    def _compute_bank(self):
        bank_obj = self.env['res.partner.bank']
        partner=self.company_emitter_id.partner_id
        bank_ids = bank_obj.search([('partner_id', '=', partner.id)])
        bank =''
        apa = True
        for bk in bank_ids:
            bank = bank+ ' '+str(bk.acc_number)
        self.bank = bank

    @api.one
    def _compute_banks(self):
        bank_obj = self.env['res.partner.bank']
        partner = self.company_emitter_id.partner_id
        bank_ids = bank_obj.search([('partner_id', '=', partner.id)])
        bank = ''
        apa = True
        for bk in bank_ids:
            bank = bank + ' ' + str(bk.bank_id.name)
        self.banco = bank

    @api.one
    def _compute_clabe(self):
        bank_obj = self.env['res.partner.bank']
        partner = self.company_emitter_id.partner_id
        bank_ids = bank_obj.search([('partner_id', '=', partner.id)])
        bank = ''
        apa = True
        for bk in bank_ids:
            bank = bank + ' ' + str(bk.clabe)
        self.clabe= bank

    bank = fields.Char(string="Banco clave interbancaria",compute="_compute_bank")
    banco =fields.Char(string="Banco",compute="_compute_banks")
    clabe = fields.Char(string="Clabe", compute="_compute_clabe")
    @api.depends('invoice_line_ids')
    @api.one
    def _compute_ganancy(self):
        total=0
        for i in self.invoice_line_ids:
            total += i.utilidad
        self.ganancy = total

    invoice_line_ids = fields.One2many('account.invoice.line', 'invoice_id', string='Invoice Lines',
                                       oldname='invoice_line',
                                       readonly=True, states={'draft': [('readonly', False)],'open': [('readonly', False)]}, copy=True)

class AccountPayment(models.Model):
    _inherit ='account.payment'
    @api.multi
    def get_teamwise_commission(self):
        sum_line_manager = []
        sum_line_person = []
        amount_person, amount_manager = 0.0, 0.0
        for payment in self:
            if not payment.sales_team_id:
                raise Warning(_('Plaese select Sales Team.'))
            if not payment.sales_user_id:
                raise Warning(_('Plaese select Sales User.'))
            if payment.invoice_ids:
                for invoice in payment.invoice_ids:
                    ##modificacion naye
                    sum_line_manager.append((invoice.ganancy * invoice.team_id.sales_manager_commission)/100)
                    sum_line_person.append((invoice.ganancy * invoice.team_id.sales_person_commission)/100)
                amount_manager = sum(sum_line_manager)
                amount_person = sum(sum_line_person)
            else:
                amount_manager = (invoice.ganancy * payment.sales_team_id.sales_manager_commission)/100
                amount_person =  (invoice.ganancy * payment.sales_team_id.sales_person_commission)/100
        return amount_person, amount_manager