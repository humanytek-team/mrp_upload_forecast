# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Rubén Bravo <rubenred18@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import base64
#import datetime
_logger = logging.getLogger(__name__)


class UploadForecast(models.TransientModel):
    _name = "upload.forecast"

    name = fields.Char('File Name')
    data_file = fields.Binary('File')
    state = fields.Selection([('choose', 'choose'), ('get', 'get')],
                            default='choose')

    @api.multi
    def confirm(self):
        ProductProduct = self.env['product.product']
        SaleForecast = self.env['sale.forecast']
        data_file = self.data_file
        data_file_decoded = base64.b64decode(data_file)
        aux = data_file_decoded.split('\n')
        num_line = 0
        list_projects = []
        for line in aux[:-1]:
            if num_line == 0:
                line_aux = line.split(';')
                num_line += 1
                continue
            num_line += 1
            column = line.split(';')
            #quitar el num de columnas
            #if len(column) == 3:
            #busco el producto por referencia
            products = ProductProduct.search([('default_code', '=', column[0])])
            if products:
                if products.id not in list_projects:
                    SaleForecast.search(
                        [('product_id.id', '=', products.id)]).unlink()
                    products.write(
                        {'mps_active': True, 'apply_active': True})
                    list_projects.append(products.id)
                try:
                    #recorrer todas las columnas
                    cont = 1
                    for col in column[1:]:

                        _logger.info('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
                        _logger.info(products.id)
                        _logger.info(line_aux[cont].strip())
                        _logger.info(col.strip())
                        SaleForecast.create({
                                    'product_id': products.id,
                                    'date': line_aux[cont].strip(),
                                    'forecast_qty': col.strip()})
                        cont += 1
                except:
                    error = 'check the line: ' + str(num_line)
                    raise UserError(_(error))
                continue
            else:
                error = 'the product does not exist! line: ' + str(num_line)
                raise UserError(_(error))
            #else:
                #error = 'file must have 3 columns! line: ' + str(num_line)
                #raise UserError(_(error))

