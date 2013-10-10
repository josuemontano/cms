from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from spartan.models.meta import (DBSession, Base)
from .security import (EntryFactory, groupfinder)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    
    authentication_policy = AuthTktAuthenticationPolicy(settings['auth.secret'], callback = groupfinder)
    authorization_policy  = ACLAuthorizationPolicy()

    config = Configurator(settings              = settings,
                          authentication_policy = authentication_policy,
                          authorization_policy  = authorization_policy,
                          root_factory          = EntryFactory)

    config.include('pyramid_jinja2')
    config.add_renderer('.html', 'pyramid_jinja2.renderer_factory')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.include(addroutes)
    config.scan()
    return config.make_wsgi_app()


def addroutes(config):
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('pages_index', '/pages')
    config.add_route('pages_sort', '/pages/sort')
    config.add_route('pages_create', '/pages/create')
    config.add_route('pages_update', '/pages/update/{id}')
    config.add_route('pages_delete', '/pages/delete/{id}')

    config.add_route('site_index', '/site')
    config.add_route('site_update', '/site/update')

    config.add_route('files_index', '/files')
    config.add_route('files_upload_file', '/files/upload/file')
    config.add_route('files_upload_image', '/files/upload/image')

    config.add_route('accounts_index', '/accounts')
    config.add_route('accounts_create', '/accounts/create')
    config.add_route('accounts_update', '/accounts/update/{id}')
    config.add_route('accounts_delete', '/accounts/delete/{id}')
