from datetime import timedelta

from odoo import api, models




class ResourceCalendarLeaves(models.Model):
    _inherit = 'resource.calendar.leaves'

    @api.model
    def is_public_holiday(self, date):
        work_entry_type_ids = list(
            filter(
                None,
                [
                    self.env.ref("public_budget.feriado", raise_if_not_found=False),
                    self.env.ref("public_budget.no_laboral", raise_if_not_found=False),
                ],
            )
        )
        work_entry_type_ids = [record.id for record in work_entry_type_ids] or False

        leave = self.search([("date_from", "<=", date),
                ("date_to", ">=", date),
                ("work_entry_type_id", "in", work_entry_type_ids),
                ])

        return True if leave else False
