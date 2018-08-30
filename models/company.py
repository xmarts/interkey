## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import xlrd
import shutil
import logging
_logger = logging.getLogger(__name__)

class ResCompany(models.Model):
    _inherit ='res.company'

    @api.one
    def _compute_rfc(self):
        self.vat_split = str(self.vat)[2:]
    vat_split= fields.Char(string="RFC sin prefijo", compute="_compute_rfc")