from odoo.addons.component.core import Component


class ProductTemplateListener(Component):
    _name = 'product.template.listener'
    _inherit = 'base.event.listener'
    _apply_on = ['product.template']

    def on_record_write(self, record, fields=None):
        if 'standard_price' in fields:
            record.label_to_be_printed = True
