# -*- coding: utf-8 -*-
{
    'name':
    "Open Library",
    'summary':
    """
        """,
    'description':
    """
    """,
    'author':
    "My Company",
    'website':
    "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':
    'Services',
    'version':
    '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license':
    'LGPL-3',
    'pre_init_hook':
    'pre_init_hook',
    'post_init_hook':
    'post_init_hook',
    'uninstall_hook':
    'uninstall_hook',
}
