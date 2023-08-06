from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_category = fields.Char(
        compute='_compute_product_category',
        string="Product Category",
        store=True
    )

    @api.depends('product_id')
    def _compute_product_category(self):
        for move in self:
            move.product_category = move.product_id.product_tmpl_id.categ_id.name
