import json

from .meta import *

class SiteFactory(object):
    def __init__(self, request):
        self.request = request

    def index(self):
        site = DBSession.query(Site).get(1)
        return { 'object' : site,
                 'user'   : authenticated_userid(self.request) }

    def update(self):
        request = self.request
        site    = DBSession.query(Site).get(1)
        form    = SiteForm(request.POST, site)
        message = None
        
        if request.method == 'POST':
            if form.validate():
                try:
                    form.populate_obj(site)
                    message = UPDATED_MESSAGE
                except SQLAlchemyError:
                    message = SQLERROR_MESSAGE
            else:
                message = FORMERRORS_MESSAGE

        return { 'form'     : form,
                 'save_url' : request.resource_url(request.root, 'site', 'update'),
                 'message'  : message,
                 'user'     : authenticated_userid(request) }


class PageFactory(BaseFactory):
    def __init__(self, request):
        self.request    = request        
        self.baseUrl    = 'pages'
        self.formClass  = PageForm
        self.modelClass = Page

    def index(self):
        request = self.request
        pages   = DBSession.query(Page).filter_by(parent_id = None).order_by(Page.sort).all()
        
        return { 'pages'      : pages,
                 'create_url' : request.resource_url(request.root, 'pages', 'create'),
                 'update_url' : request.resource_url(request.root, 'pages', 'update'),
                 'sort_url'   : request.resource_url(request.root, 'pages', 'sort'),
                 'user'       : authenticated_userid(request) }

    def sort(self):
        request = self.request
        message = 'Su solicitud no es v&aacute;lida'
        if request.method == 'POST':
            data = json.loads(request.POST.get('sort_string'))
            self.set_sort(data, None)
            message = 'Sus cambios se guardaron exitosamente'

        return message

    # TODO: Improve update slug
    def set_sort(self, pages_dict, parent_id):
        pages_id = list(map(lambda dict: dict['id'], pages_dict))
        for idx in range(0, len(pages_id)):
            page_id = pages_id[idx]
            DBSession.query(Page).filter(Page.id == page_id).update({ 'sort' : idx + 1, 'parent_id' : parent_id })
            page = DBSession.query(Page).get(page_id)
            page.set_slug()

            if 'children' in pages_dict[idx]:
                self.set_sort(pages_dict[idx]['children'], page_id)

    def bake_form(self, form):
        form.template_id.choices = [(template.id, template.name) for template in DBSession.query(PageTemplate).order_by('name').all()]
        return form

    def populate_model(self, form, page):
        form.populate_obj(page)
        page.set_slug()


class HomeFactory(object):
    def __init__(self, request):
        self.request = request

    def index(self):
        from .security import User

        pages = DBSession.query(Page).order_by(Page.sort).all()
        site  = DBSession.query(Site).first()
        users = DBSession.query(User).all()
        return { 'site'  : site,
                 'pages' : pages,
                 'users' : users,
                 'user'  : authenticated_userid(self.request) }
    