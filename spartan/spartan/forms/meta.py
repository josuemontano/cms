from wtforms import *
from wtforms.validators import *

BLANK_REQUIRED    = 'Este campo no puede ser nulo'
BLANK_USERNAME    = 'Debe ingresar un nombre de usuario'
BLANK_PASSWORD    = 'La contraseña no puede ser nula'
SHORT_USERNAME    = 'El nombre de usuario debe constar de al menos 4 caracteres'
SHORT_PASSWORD    = 'La contraseña debe constar de al menos 8 caracteres'
PASSWORD_MISMATCH = 'Las contraseñas beben coincidir'


class RequiredIf(Required):
    # a validator which makes a field required if
    # another field is set and has a truthy value

    def __init__(self, other_field_name, *args, **kwargs):
        self.other_field_name = other_field_name
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if bool(other_field.data):
            super(RequiredIf, self).__call__(form, field)