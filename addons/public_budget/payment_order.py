# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class payment_order(models.Model):
    """"""

    _name = 'payment.order'
    _inherits = {}
    _inherit = ['payment.order']

    type_with_advance_payment = fields.Boolean(
        string='With advance payment?',
        readonly=True,
        related='transaction_id.type_id.with_advance_payment'
        )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        states={'done': [('readonly', True)]}
        )
    note = fields.Html(
        string='Note'
        )
    paid = fields.Boolean(
        string='Paid',
        compute='_get_paid'
        )
    transaction_id = fields.Many2one(
        'public_budget.transaction',
        string='Transaction'
        )

    _constraints = [
    ]

    @api.one
    def _get_paid(self):
        """"""
        self.paid = False

    @api.one
    def create_voucher(self):
        res = super(payment_order, self).create_voucher()
        for voucher_ids in res:
            vouchers = self.env['account.voucher'].browse(voucher_ids)
            vouchers.signal_workflow(
                'proforma_confirmed')
        return res

    @api.multi
    def action_search_entries(self):
        if not self.transaction_id:
            raise Warning(
                _('This action is only available for Payment Orders with Transaction'))
        move_lines = self.env['account.move.line']
        models = self.env['ir.model.data']
        domain = [
            ('reconcile_id', '=', False),
            ('account_id.type', '=', 'payable'),
            ('credit', '>', 0),
            ('invoice.transaction_id', '=', self.transaction_id.id),
            ('account_id.reconcile', '=', True)]
        move_lines = move_lines.search(domain)
        context = dict(
            self._context, line_ids=move_lines.ids,
            default_entries=move_lines.ids)
        models = models.search(
            [('model', '=', 'ir.ui.view'),
             ('name', '=', 'view_create_payment_order_lines')])
        resource_id = models.read(fields=[
            'res_id'])[0]['res_id']
        return {'name': _('Entry Lines'),
                'context': context,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'payment.order.create',
                'views': [(resource_id, 'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
                }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
