from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    payment_methods = fields.Char(
        # related='payment_ids.payment_method',
        compute="_compute_payment_methods",
    )


    def _compute_payment_methods(self):
        for rec in self:
            rec.payment_methods = ', '.join(rec.payment_ids.mapped('payment_method'))
