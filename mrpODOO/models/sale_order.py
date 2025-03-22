from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def get_bom_lines(self):
        """Manually trigger the BOM component update."""
        self.ensure_one()

        grouped_lines = {}

        for line in self.order_line:
            bom = self.env['mrp.bom'].sudo().search([
                ('product_id', '=', line.product_id.id)
            ], limit=1)

            if not bom:
                bom = self.env['mrp.bom'].sudo().search([
                    ('product_tmpl_id', '=', line.product_id.product_tmpl_id.id),
                    ('product_id', '=', False)
                ], limit=1)

            if bom:
                for bom_line in bom.bom_line_ids:
                    variant_names = ', '.join(bom_line.product_id.product_template_variant_value_ids.mapped('name'))
                    product_name = bom_line.product_id.name
                    uom = bom_line.product_uom_id.name

                    product_key = f"{product_name} ({variant_names})" if variant_names else product_name

                    if product_key in grouped_lines:
                        grouped_lines[product_key]['qty'] += bom_line.product_qty * line.product_uom_qty
                    else:
                        grouped_lines[product_key] = {
                            'qty': bom_line.product_qty * line.product_uom_qty,
                            'uom': uom
                        }

        new_lines = [(0, 0, {
            'x_studio_rn_kodu': key,
            'x_name': f"[{data['uom']}]",
            'x_studio_ihtiyac': data['qty']
        }) for key, data in grouped_lines.items()]

        if new_lines:
            self.sudo().write({'x_studio_one2many_field_4qs_1imdadie9': new_lines})

        self.env.cr.flush()
        self.env.cr.commit()
        self.env.invalidate_all()
