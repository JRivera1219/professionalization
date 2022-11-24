# -*- coding: utf-8 -*-
# from odoo import http


# class Professionalization(http.Controller):
#     @http.route('/professionalization/professionalization/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/professionalization/professionalization/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('professionalization.listing', {
#             'root': '/professionalization/professionalization',
#             'objects': http.request.env['professionalization.professionalization'].search([]),
#         })

#     @http.route('/professionalization/professionalization/objects/<model("professionalization.professionalization"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('professionalization.object', {
#             'object': obj
#         })
