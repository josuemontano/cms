from .meta import *

from spartan.models.security import *
from spartan.forms.security import *

class UserFactory (object):
    def __init__(self, request):
        self.request = request

    def login(self, next):
        request = self.request
        message = None
        form    = LoginForm(request.POST)

        if request.method == 'POST' and form.validate():
            username = request.POST.get('username')
            password = request.POST.get('password')
            if User.check_password(username, password):
                headers = remember(request, username)
                return HTTPFound(location = next, headers = headers)
            else:
                message = 'Su nombre de usuario y/o contrase&ntilde;a son incorrectos. Por favor verif&iacute;quelos e intente nuevamente'
                
        return { 'form'     : form,
                 'next'     : next,
                 'message'  : message,
                 'save_url' : request.resource_url(request.root, 'login') }
        
    def logout(self):
        request = self.request
        headers = forget(request)
        return HTTPFound(location = request.route_url('home'), headers = headers)


class AccountFactory(BaseFactory):
    def __init__(self, request):
        self.request    = request
        self.baseUrl    = 'accounts'
        self.formClass  = AccountForm
        self.modelClass = User

    def index(self):
        request  = self.request
        accounts = DBSession.query(User).order_by(User.name).all()
        
        return { 'accounts'   : accounts,
                 'create_url' : request.resource_url(request.root, 'accounts', 'create'),
                 'update_url' : request.resource_url(request.root, 'accounts', 'update'),
                 'sort_url'   : request.resource_url(request.root, 'accounts', 'sort'),
                 'user'       : authenticated_userid(request) }
    
    def delete(self):
        pass

    def bake_form(self, form):
        form.group_id.choices = [(group.id, group.name) for group in DBSession.query(Group).order_by(Group.name).all()]
        return form

    def populate_model(self, form, _object):
        _object.name  = form.name.data
        group = DBSession.query(Group).get(form.group_id.data)
        if group is not None:
            _object.group = group
        if form.password.data is not '':
            _object._set_password(form.password.data)