from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'
    removal_time = fields.Integer(string='Product Removal Time',
       help='Number of days before the goods should be removed from the stock. It will be computed on the lot/serial number.')
 
