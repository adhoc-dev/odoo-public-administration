# -*- coding: utf-8 -*-
{'active': False,
    'author':  'Ingenieria ADHOC',
    'website': 'www.ingadhoc.com',
    'category': 'Accounting & Finance',
    'data': [
        'wizard/transaction_definitive_make_invoice_view.xml',
        'views/res_partner_view.xml',
        'views/custom_views.xml',
        'views/account_asset_view.xml',
        'views/account_voucher_view.xml',
        'views/account_check_view.xml',
        'workflow/account_voucher_workflow.xml',
        'workflow/account_check_workflow.xml',
        'data/data.xml',
        'data/public_budget.expedient_founder.csv',
        'data/public_budget.expedient_category.csv',
        'data/public_budget.transaction_type.csv',
        'data/public_budget.budget_position_category.csv',
        'data/public_budget.budget_pos_exc_rest.csv',
        'security/security.xml',
        'reports/receipt_report.xml',
    ],
    'demo': [
        'demo/company_demo.xml',
        'demo/res.partner.csv',
        'demo/public_budget.location.csv',
        'demo/user_demo.xml',
        'demo/account.account.csv',
        'demo/account.journal.csv',
        'demo/account.checkbook.csv',
        'demo/account_properties.xml',
        'demo/account_period.xml',
        'demo/taxes.xml',
        'demo/tax_settlement.xml',
        'demo/account.tax.withholding.csv',
        'demo/public_budget.transaction_type.csv',
        'demo/public_budget.expedient.csv',
        'demo/public_budget.budget_position.csv',
        'demo/public_budget.budget.csv',
        'demo/public_budget_demo.xml',
        'demo/public_budget.budget_detail.csv',
        'demo/public_budget.transaction.csv',
        'demo/public_budget.preventive_line.csv',
        'demo/public_budget.definitive_line.csv',
        'demo/public_budget.remit.csv',
        'demo/public_budget.budget_modification.csv',
        'demo/public_budget.budget_modification_detail.csv',
    ],
    'depends': [
        'l10n_ar_invoice',
        'l10n_ar_aeroo_voucher',
        'public_budget',
        'account_asset',
        'share',
        'web_m2x_options',
        'account_voucher_double_validation',
        'account_tax_settlement_withholding',
    ],
    'description': '''
Public Budget Sipreco Customizations
====================================
Customizaciones especificas al modulo public_budget para SIPRECO
* Agregar punto de venta y numero de factura en wizar de generacion de factura
''',
    'installable': True,
    'name': 'Public Budget Sipreco Customizations',
    'test': [],
    'version': '1.243'}