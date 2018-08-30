## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import xlrd
import shutil

#class xmartsstockpicking(models.Model):
#	_inherit ='stock.picking'
#  	xmpack= fields.Boolean(string="Empaquetado",default=False)


class InheritZona(models.Model):

	_inherit = 'res.partner'

	zone = fields.Char(string='Zona de Residencia', help='Coloca la zona de residencia para especificar la zona de localizacion')

