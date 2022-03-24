# -*- coding: utf-8 -*-
{
    'name': "Formation",

    'summary': 'Formation Management software',

    'sequence': -100,

    'description': """Formation Management software""",

    'author': "Nader Hajji (The Team)",
    'website': "http://www.theteam.com.tn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project Management',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/session_views.xml',
        'views/formateur_views.xml',
        'views/theme_views.xml',
        'views/participant_views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
