import datetime
import transaction

from pyramid.httpexceptions import (HTTPFound, HTTPNotFound)
from pyramid.security import (authenticated_userid, remember, forget)

from sqlalchemy.sql import null
from sqlalchemy.exc import (DBAPIError, IntegrityError, SQLAlchemyError)

from spartan.models.core import *
from spartan.forms.core import *


UPDATED_MESSAGE    = 'Sus cambios se guardaron exitosamente'
FORMERRORS_MESSAGE = 'Por favor corrija los errores indicados'
SQLERROR_MESSAGE   = 'Verifique sus datos e intente nuevamente'

class BaseFactory(object):
    baseUrl     = None
    formClass   = None
    modelClass  = None

    def __init__(self, request):
        self.request = request

    def create(self):
        request = self.request
        form    = self.bake_form(self.formClass(request.POST))
        _object = self.modelClass()
        message = None

        if request.method == 'POST':
            if form.validate():
                self.populate_model(form, _object)
                with transaction.manager:
                    try:
                        DBSession.add(_object)
                    except SQLAlchemyError:
                        message = SQLERROR_MESSAGE
                    else:
                        message = UPDATED_MESSAGE
            else:
                message = FORMERRORS_MESSAGE

        _dict = { 'form'      : form,
                  'save_url'  : request.resource_url(request.root, self.baseUrl , 'create'),
                  'message'   : message,
                  'user'      : authenticated_userid(request) }
                  
        return self.bake_dict(_dict)


    def update(self):
        request = self.request
        _id     = request.matchdict['id']
        _object = DBSession.query(self.modelClass).get(_id)
        message = None

        if _object is not None:
            form = self.bake_form(self.formClass(request.POST, _object))
            if request.method == 'POST':
                if form.validate():
                    try:
                        self.populate_model(form, _object)
                    except SQLAlchemyError:
                        message = SQLERROR_MESSAGE
                    else:
                        message = UPDATED_MESSAGE
                else:
                    message = FORMERRORS_MESSAGE

            _dict =  { 'form'     : form,
                       'save_url' : request.resource_url(request.root, self.baseUrl , 'update', _id),
                       'message'  : message,
                       'user'     : authenticated_userid(request) }

            return self.bake_dict(_dict)

        raise HTTPNotFound()


    def bake_form(self, form):
        return form

    def populate_model(self, form, _object):
        form.populate_obj(_object)

    def bake_dict(self, _dict):
        return _dict