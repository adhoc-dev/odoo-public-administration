# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)


class PublicBudgetSubsidyRendition(models.Model):

    _name = 'public_budget.subsidy.rendition'

    subsidy_id = fields.Many2one(
        'public_budget.subsidy',
        'Subsidy',
        required=True,
        ondelete='cascade',
    )
    date = fields.Date(
        required=True,
        default=fields.Date.context_today
    )
    # approval_arrangement_ids = fields.One2many(
    #     'public_budget.subsidy.approval_arrangement',
    #     'rendition_id',
    #     # 'public_budget_rendition_approval_arrangement_rel',
    #     # 'rendition_id', 'approval_arrangement_id',
    #     'Disposiciones de aprobación',
    # )
    approval_arrangement_id = fields.Many2one(
        'public_budget.subsidy.approval_arrangement',
        # 'rendition_id',
        # 'public_budget_rendition_approval_arrangement_rel',
        # 'rendition_id', 'approval_arrangement_id',
        'Disposición de aprobación',
    )
    rendition_amount = fields.Monetary(
        'Importe Rendido',
    )
    approved_amount = fields.Monetary(
        'Importe Aprobado',
        related='approval_arrangement_id.approved_amount',
        readonly=True,
        store=True,
        # digits=dp.get_precision('Account'),
    )
    pending_amount = fields.Monetary(
        'Importe Pendiente',
        compute='get_pending_amount',
    )
    expedient_id = fields.Many2one(
        'public_budget.expedient',
        'Expediente',
        help='Expediente Administrativo de Rendición de Subsidio',
    )

    @api.one
    @api.constrains('rendition_amount', 'approved_amount')
    def check_amounts(self):
        if self.approved_amount > self.rendition_amount:
            raise ValidationError(
                'Importe Aprobado no puede ser mayor al importe rendido')

    @api.one
    @api.depends('rendition_amount', 'approved_amount')
    def get_pending_amount(self):
        self.pending_amount = self.rendition_amount - self.approved_amount
