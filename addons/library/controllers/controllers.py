# -*- coding: utf-8 -*-
from odoo import http


class Mytest(http.Controller):

    @http.route('/mytest/mytest', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/mytest/mytest/objects', auth='public')
    def list(self, **kw):
        return http.request.render(
            'mytest.listing', {
                'root': '/mytest/mytest',
                'objects': http.request.env['mytest.mytest'].search([]),
            })

    @http.route('/mytest/mytest/objects/<model("mytest.mytest"):obj>',
                auth='public')
    def object(self, obj, **kw):
        return http.request.render('mytest.object', {'object': obj})
