# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import openerp.addons.decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class definitive_line(models.Model):
    """Definitive Line"""

    _name = 'public_budget.definitive_line'
    _description = 'Definitive Line'
    _rec_name = 'preventive_line_id'

    issue_date = fields.Date(
        string='Issue Date',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]},
        default=fields.Date.context_today
        )
    supplier_id = fields.Many2one(
        'res.partner',
        string='Supplier',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]},
        context={'default_supplier': True},
        domain=[('supplier', '=', True)]
        )
    amount = fields.Float(
        string='Amount',
        readonly=True,
        required=True,
        states={'draft': [('readonly', False)]},
        digits=dp.get_precision('Account'),
        )
    residual_amount = fields.Float(
        string=_('Residual Amount'),
        compute='_get_amounts',
        digits=dp.get_precision('Account'),
        store=True,
        )
    to_pay_amount = fields.Float(
        string=_('To Pay Amount'),
        compute='_get_amounts',
        digits=dp.get_precision('Account'),
        store=True,
        )
    paid_amount = fields.Float(
        string=_('Paid Amount'),
        compute='_get_amounts',
        digits=dp.get_precision('Account'),
        store=True,
        )
    invoiced_amount = fields.Float(
        string=_('Invoiced Amount'),
        compute='_get_amounts',
        digits=dp.get_precision('Account'),
        store=True,
        )
    preventive_line_id = fields.Many2one(
        'public_budget.preventive_line',
        ondelete='cascade',
        string='Preventive Line',
        required=True,
        auto_join=True,
        )
    transaction_id = fields.Many2one(
        readonly=True,
        store=True,
        related='preventive_line_id.transaction_id',
        auto_join=True,
        )
    budget_id = fields.Many2one(
        readonly=True,
        store=True,
        related='preventive_line_id.budget_id',
        auto_join=True,
        )
    state = fields.Selection(
        selection=[('draft', _('Draft')), ('invoiced', _('Invoiced'))],
        string=_('State'),
        states={'draft': [('readonly', False)]},
        default='draft',
        compute='_get_state'
        )
    invoice_line_ids = fields.One2many(
        'account.invoice.line',
        'definitive_line_id',
        string='Invoice Lines',
        readonly=True,
        auto_join=True,
        )

    @api.constrains('issue_date')
    def check_dates(self):
        if self.issue_date < self.transaction_id.issue_date:
            raise Warning(_(
                'La fecha de la línea definitiva debe ser mayor a la fecha de '
                'la transacción'))

    @api.one
    def _get_state(self):
        _logger.info('Getting state for definitive line %s' % self.id)
        if self.invoice_line_ids:
            self.state = 'invoiced'
        else:
            self.state = 'draft'

    @api.multi
    def write(self, vals):
        # TODO ver si se puede sacar esto.
        # No le pude encontrar la vuelta de porque algunas veces al guardar las
        # definitives se va a setear esto en cero y termina borrando los
        # vinculos desde las invoice lines a las definitives
        if 'invoice_line_ids' in vals:
            vals.pop('invoice_line_ids')
        return super(definitive_line, self).write(vals)

    @api.one
    def unlink(self):
        if self.invoice_line_ids:
            raise Warning(_(
                "You can not delete a definitive line that has been invoiced"))
        return super(definitive_line, self).unlink()

    @api.one
    @api.depends(
        'amount',
        # 'invoice_line_ids.invoice_id.state',
        # 'invoice_line_ids.invoice_id.type',
        # no haria falta depende de price_subtotal porque to pay amount y paid
        # amount ya lo tienen como dependencia (corre dos veces el calculo)
        # 'invoice_line_ids.price_subtotal',
        'invoice_line_ids.to_pay_amount',
        'invoice_line_ids.paid_amount',
    )
    def _get_amounts(self):
        """Update the following fields with the related values to the budget
        and the budget position:
        -invoiced_amount: amount sum of lines with a related invoice line
        -residual_amount: pending amount to be invoiced
        -to_pay_amount: amount sum of lines that has a related voucher in draft
        state
        -paid_amount: amount sum of lines that has a related voucher in open
        state
        """
        _logger.info('Getting amounts for definitive line %s' % self.id)

        if not self.invoice_line_ids:
            self.residual_amount = self.amount
            return False

        filter_domain = [
            ('id', 'in', self.invoice_line_ids.ids),
            ('invoice_id.state', 'not in', ('cancel', 'draft'))
            ]

        # Add this to allow analysis between dates
        # from_date = self._context.get('analysis_from_date', False)
        to_date = self._context.get('analysis_to_date', False)

        # if from_date:
        #     filter_domain += [('invoice_id.date_invoice', '>=', from_date)]
        if to_date:
            filter_domain += [('invoice_id.date_invoice', '<=', to_date)]

        debit_filter_domain = filter_domain + [
            ('invoice_id.type', 'in', ('out_invoice', 'in_invoice'))]
        credit_filter_domain = filter_domain + [
            ('invoice_id.type', 'in', ('out_refund', 'in_refund'))]
        debit_invoice_lines = self.invoice_line_ids.search(
            debit_filter_domain)
        credit_invoice_lines = self.invoice_line_ids.search(
            credit_filter_domain)

        invoiced_amount = (
            sum(debit_invoice_lines.mapped('price_subtotal')) -
            sum(credit_invoice_lines.mapped('price_subtotal'))
            )
        to_pay_amount = (
            sum(debit_invoice_lines.mapped('to_pay_amount')) -
            sum(credit_invoice_lines.mapped('to_pay_amount'))
            )
        paid_amount = (
            sum(debit_invoice_lines.mapped('paid_amount')) -
            sum(credit_invoice_lines.mapped('paid_amount'))
            )

        self.invoiced_amount = invoiced_amount
        self.residual_amount = self.amount - invoiced_amount
        self.to_pay_amount = to_pay_amount
        self.paid_amount = paid_amount
        _logger.info('Finish getting amounts for definitive line %s' % self.id)

    @api.multi
    def get_invoice_line_vals(self, to_invoice_amount=False, journal=False):
        self.ensure_one()
        if not to_invoice_amount:
            to_invoice_amount = self.residual_amount
        print 'wizard.journal_id.type', journal.type
        if journal.type in ('sale_refund', 'purchase_refund'):
            to_invoice_amount = -1.0 * to_invoice_amount
        print 'refund2', to_invoice_amount
        preventive_line = self.preventive_line_id
        line_vals = {
            'name': preventive_line.budget_position_id.name,
            'price_unit': to_invoice_amount,
            'quantity': 1,
            'definitive_line_id': self.id,
            'account_id': preventive_line.account_id.id,
            # 'discount': ,
            # 'product_id': line.product_id.id or False,
            # 'uos_id': line.uos_id.id or False,
            # 'sequence': line.sequence,
        }
        return line_vals

    @api.one
    @api.constrains(
        'amount')
    def check_budget_state_open(self):
        if self.budget_id and self.budget_id.state not in 'open':
            raise Warning(
                'Solo puede cambiar afectaciones definitivas si '
                'el presupuesto está abierto')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
