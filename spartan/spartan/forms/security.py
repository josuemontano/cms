from .meta import *

class LoginForm (Form):
    username = TextField('Usuario', [InputRequired(message = BLANK_USERNAME), Length(max = 255)])
    password = PasswordField('Contrase&ntilde;a', [InputRequired(message = BLANK_PASSWORD), Length(max = 60)])

class AccountForm(Form):
    name             = TextField('Nombre de usuario', [InputRequired(message = BLANK_REQUIRED), Length(min = 4, max = 255, message = SHORT_USERNAME)])
    password         = PasswordField('Contrase&ntilde;a', [Optional(), equal_to('password_confirm', message = PASSWORD_MISMATCH), length(min = 8, max = 60, message = SHORT_PASSWORD)])
    password_confirm = PasswordField('Repetir contrase&ntilde;a', [RequiredIf('password', message = BLANK_REQUIRED), Length(max = 60)])
    group_id         = SelectField('Grupo', [InputRequired(message = BLANK_REQUIRED)], coerce = int)

        