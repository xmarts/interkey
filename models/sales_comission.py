## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import xlrd
import shutil
import logging
_logger = logging.getLogger(__name__)

class SalesCommision(models.Model):
    _inherit ='sales.commission'
    @api.one
    def action_paid(self):
        self.state = 'paid'
        for x in self.sales_commission_line:
            x.state = 'paid'
