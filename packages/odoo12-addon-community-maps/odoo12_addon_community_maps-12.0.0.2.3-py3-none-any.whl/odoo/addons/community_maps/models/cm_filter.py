from odoo import models, api, fields
from odoo.tools.translate import _

class CmFilter(models.Model):
  _name = 'cm.filter'

  _inherit = ["cm.slug.id.mixin"]

  name = fields.Char(string=_("Name"),translate=True)
  icon = fields.Char(string=_("Icon"))
  color = fields.Char(string=_("Color"))
  description = fields.Char(string=_("Description"),translate=True)
  filter_group_id = fields.Many2one('cm.filter.group',string="Filter Group")
  places_mids = fields.Many2many(
    'crm.team', 
    'cm_places_filters','filter_id','place_id',string=_("Related places"))

  def get_datamodel_dict(self):
    datamodel = {
      'slug': self.slug_id,
      'name': self.name,
      'iconKey': None,
      'iconColor': None,
      'description': None
    }
    if self.icon:
      datamodel['iconKey'] = self.icon
    if self.color:
      datamodel['iconColor'] = self.color
    if self.description:
      datamodel['description'] = self.description
    return datamodel