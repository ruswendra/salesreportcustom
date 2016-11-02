# -*- coding: utf-8 -*-
from openerp import http

# class DutaAlisan(http.Controller):
#     @http.route('/duta_alisan/duta_alisan/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/duta_alisan/duta_alisan/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('duta_alisan.listing', {
#             'root': '/duta_alisan/duta_alisan',
#             'objects': http.request.env['duta_alisan.duta_alisan'].search([]),
#         })

#     @http.route('/duta_alisan/duta_alisan/objects/<model("duta_alisan.duta_alisan"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('duta_alisan.object', {
#             'object': obj
#         })