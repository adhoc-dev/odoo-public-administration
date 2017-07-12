# -*- coding: utf-8 -*-
from openerp import fields, models, api
import logging
_logger = logging.getLogger(__name__)


class AccountPaymentGroup(models.Model):

    _inherit = 'account.payment.group'

    cargo_date = fields.Date(
        compute='get_cargo_data',
        string='Fecha del Cargo',
        # necesitamos store para poder ordenarlo
        store=True,
    )
    cargo_amount = fields.Monetary(
        'Cargo',
        help='Cargos Efectuados',
        compute='get_cargo_data',
        store=True,
    )

    @api.one
    @api.depends(
        'payment_date',
        'payments_amount',
        'state',
        'payment_ids.check_ids.amount',
        'payment_ids.check_ids.state',
    )
    def get_cargo_data(self):
        cargo_amount = 0.0
        cargo_date = False
        if self.state == 'posted':
            check_ids = self.payment_ids.mapped('check_ids')
            if check_ids:
                # si hay cheques, controlamos que esten entregados, si no
                # tomamos el monto del payment
                haneded_checks = check_ids.search([
                    ('id', 'in', check_ids.ids),
                    ('state', 'in', ['handed', 'debited'])],
                    # order='handed_date desc'
                )
                cargo_amount += sum(haneded_checks.mapped('amount'))
                # cargo_date = haneded_checks and haneded_checks[0].handed_date
            else:
                cargo_amount += self.payments_amount
                cargo_date = self.payment_date
        self.cargo_date = cargo_date
        self.cargo_amount = cargo_amount