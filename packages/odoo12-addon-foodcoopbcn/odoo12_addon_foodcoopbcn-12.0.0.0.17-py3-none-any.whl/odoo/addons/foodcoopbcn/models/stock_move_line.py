from odoo import models, fields


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    removal_date = fields.Datetime()

    def _action_done(self):
        for ml in self:
            super(StockMoveLine, ml)._action_done()
            if ml.lot_id and ml.removal_date:
                ml.lot_id.removal_date = ml.removal_date

