from wtforms import *
from wtforms.validators import *


BLANK_NAME_REQUIRED  = 'El nombre no puede ser nulo'
BLANK_EMAIL_REQUIRED = 'Es necesario que ingrese un valor del tipo example@example.com'
BLANK_REQUIRED       = 'Este campo no puede estar vacío'

class ContactForm (Form):
    name    = TextField('Nombre', [InputRequired(message = BLANK_NAME_REQUIRED), length(max = 300)])
    email   = TextField('email', [InputRequired(message = BLANK_EMAIL_REQUIRED), length(max = 300)])
    phone   = TextField('Tel&eacute;fono')
    comment = TextField('Consulta', widget = widgets.TextArea(), validators = [InputRequired(message = BLANK_REQUIRED)])