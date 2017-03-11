{
    'name': 'Public Budget',
    'license': 'AGPL-3',
    'version': '9.0.1.0.0',
    'author': 'ADHOC SA',
    'website': 'www.adhoc.com.ar',
    'category': 'base.module_category_knowledge_management',
    'depends': [
        'account',
    ],
    'data': [
        'security/public_budget_group.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/transaction_definitive_make_invoice_view.xml',
        'wizard/transaction_definitive_mass_invoice_create_view.xml',
        'wizard/budget_analysis_wizard_view.xml',
        'wizard/avance_request_report_wizard_view.xml',
        'reports/advance_request_analysis_view.xml',
        # 'reports/public_budget_budget_report_view_3.xml',
        'view/inventory_rule_view.xml',
        # 'view/voucher_view.xml',
        # 'view/invoice_view.xml',
        'view/advance_request_type_view.xml',
        'view/advance_request_view.xml',
        'view/transaction_type_view.xml',
        'view/transaction_type_amo_rest_view.xml',
        'view/advance_return_view.xml',
        'view/expedient_category_view.xml',
        'view/location_view.xml',
        'view/budget_modification_detail_view.xml',
        'view/funding_move_view.xml',
        'view/invoice_line_view.xml',
        'view/rest_type_view.xml',
        'view/users_view.xml',
        'view/preventive_line_view.xml',
        'view/budget_position_view.xml',
        'view/company_view.xml',
        'view/budget_detail_view.xml',
        'view/budget_prec_detail_view.xml',
        'view/definitive_line_view.xml',
        'view/transaction_view.xml',
        'view/budget_position_category_view.xml',
        'view/budget_view.xml',
        'view/remit_view.xml',
        'view/budget_pos_exc_rest_view.xml',
        'view/budget_modification_view.xml',
        'view/expedient_view.xml',
        'view/expedient_founder_view.xml',
        'view/res_partner_view.xml',
        'data/sequence.xml',
        'view/public_budget_menuitem.xml',
        'view/public_budget_actions.xml',
    ],
    'test': [],
    'installable': True,
}
