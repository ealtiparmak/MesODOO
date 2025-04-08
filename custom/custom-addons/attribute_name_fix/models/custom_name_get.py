from odoo import models

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    def name_get(self):
        result = []
        for record in self:
            if record.attribute_id.name == "Renk":
                name = record.name
            else:
                name = "%s: %s" % (record.attribute_id.name, record.name)
            result.append((record.id, name))
        return result
