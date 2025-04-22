

def post_init_set_lang(env):

    lang_code = 'es_AR'
    import pdb; pdb.set_trace()  # noqa

    if not env['res.lang'].search([('code', '=', lang_code)]):
        en_AR_language = env['res.lang'].with_context(active_test=False).sudo().search([('code', '=', lang_code)], limit=1)
        env['base.language.install'].create({'lang_ids': [(6, 0, en_AR_language.ids)]}).lang_install()

    # Asignar el idioma a todos los usuarios
    users = env['res.users'].search([])
    users.write({'lang': lang_code})
