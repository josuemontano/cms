from pyramid.view import (view_config, forbidden_view_config, notfound_view_config)

from spartan.factories.core import *
from spartan.factories.extra import *
from spartan.factories.security import *
from spartan.factories.custom import *


@forbidden_view_config(renderer = '403.html')
def forbidden(request):
    if authenticated_userid(request):
        return { 'user' : authenticated_userid(request) }
    else:
        next = request.route_url('login' , _query = (('next', request.path), ))
        return HTTPFound(location = next)

@notfound_view_config(renderer='404.html')
def not_found(request):
    request.response.status = 404
    return { }


class HomeView(object):
    def __init__(self, request):
        self.request = request
        self.factory = HomeFactory(request)

    @view_config(route_name = 'home', renderer = 'home/index.html', permission = 'view')
    def index (self):
        return self.factory.index()



class UserViews(object):    
    def __init__(self, request):
        self.request = request
        self.factory = UserFactory(request)

    @view_config(route_name = 'login', renderer = 'login.html')
    def login(self):
        request = self.request
        if authenticated_userid(request) is None:
            login_url = request.route_url('login')
            referrer  = request.url
            if referrer == login_url:
                referrer = '/'
            next = request.params.get('next', referrer) or request.route_url('home')
            return self.factory.login(next)
        else:
            next = request.params.get('next') or request.route_url('home')
            return HTTPFound(location = next)

    @view_config(route_name = 'logout', renderer = 'string')
    def logout(self):
        return self.factory.logout()



class PagesViews(object):    
    def __init__(self, request):
        self.request = request
        self.factory = PageFactory(request)

    @view_config(route_name = 'pages_index', renderer = 'pages/index.html', permission = 'view')
    def index (self):
        return self.factory.index()

    @view_config(route_name = 'pages_sort', renderer = 'string', permission = 'admin')
    def sort (self):
        return self.factory.sort()

    @view_config(route_name = 'pages_create', renderer = 'pages/create.html', permission = 'admin')
    def create (self):
        return self.factory.create()

    @view_config(route_name = 'pages_update', renderer = 'pages/update.html', permission = 'edit')
    def update (self):
        return self.factory.update()

    @view_config(route_name = 'pages_delete', renderer = 'pages/delete.html', permission = 'admin')
    def delete (self):
        return { }



class SiteViews(object):
    def __init__(self, request):
        self.request = request
        self.factory = SiteFactory(request)

    @view_config(route_name = 'site_index', renderer = 'site/index.html', permission = 'admin')
    def index (self):
        return self.factory.index()

    @view_config(route_name = 'site_update', renderer = 'site/update.html', permission = 'admin')
    def update (self):
        return self.factory.update()



class FilesViews(object):
    def __init__(self, request):
        self.request = request
        self.factory = FileFactory(request)

    @view_config(route_name = 'files_index', renderer = 'files/index.html')
    def index (self):
        return self.factory.index()

    @view_config(route_name = 'files_get_images', renderer = 'json')
    def get_images (self):
        return self.factory.get_images()

    @view_config(route_name = 'files_upload_file', renderer = 'json')
    def upload_file (self):
        return self.factory.upload_file()

    @view_config(route_name = 'files_upload_image', renderer = 'json')
    def upload_image (self):
        return self.factory.upload_image()



class AccountsViews(object):
    def __init__(self, request):
        self.request = request
        self.factory = AccountFactory(request)

    @view_config(route_name = 'accounts_index', renderer = 'accounts/index.html', permission = 'admin')
    def index (self):
        return self.factory.index()

    @view_config(route_name = 'accounts_create', renderer = 'accounts/create.html', permission = 'admin')
    def create (self):
        return self.factory.create()

    @view_config(route_name = 'accounts_update', renderer = 'accounts/update.html', permission = 'admin')
    def update (self):
        return self.factory.update()

    @view_config(route_name = 'accounts_delete', renderer = 'string', permission = 'admin')
    def delete (self):
        return self.factory.delete()