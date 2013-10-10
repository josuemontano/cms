from .meta import *

class PageForm (Form):
    name             = TextField('Nombre', [InputRequired(message = BLANK_REQUIRED), length(max = 300)])
    description      = TextField('Descripci&oacute;n')
    content          = TextAreaField('Contenido')
    show             = BooleanField('Mostrar')
    searchable       = BooleanField('Incluir en b&uacute;squeda')
    template_id      = SelectField('Tipo', [InputRequired(message = BLANK_REQUIRED)], coerce = int)

    show_floating    = BooleanField('Mostrar flotante', default = False)
    floating_content = TextAreaField('Contenido flotante')


class SiteForm (Form):
    title            = TextField('Nombre', [InputRequired(message = BLANK_REQUIRED), length(max = 300)])
    logo             = TextAreaField('Logo')
    contact_mails    = TextField('Correos de contacto', [InputRequired(message = BLANK_REQUIRED)])

    facebook         = TextField('Facebook')
    twitter          = TextField('Twitter')
    youtube          = TextField('Youtube')
    ga_code          = TextField('Google Analytics')

    meta_description = TextField('Descripci&oacute;n')
    meta_keywords    = TextField('Palabras clave')
    meta_copyright   = TextField('Copyright')
