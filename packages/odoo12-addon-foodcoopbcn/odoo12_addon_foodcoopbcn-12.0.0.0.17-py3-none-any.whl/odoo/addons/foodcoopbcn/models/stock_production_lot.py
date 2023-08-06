from odoo import models, fields
import datetime


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    def _get_dates(self, product_id=None):
        res = super()._get_dates(product_id)
        product = self.env['product.product'].browse(product_id) or self.product_id
        if (
            product and not res['removal_date'] and 
            product.categ_id.removal_time
        ):
            duration = product.categ_id.removal_time
            date = datetime.datetime.now() + datetime.timedelta(days=duration)
            res['removal_date'] = date
        return res


