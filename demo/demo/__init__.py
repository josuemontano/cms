from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models.meta import (DBSession, Base)
from .route import (page_exists, factory)
from .views import (not_found, index)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind = engine)
    Base.metadata.bind = engine
    config = Configurator(settings = settings)

    config.include('pyramid_jinja2')
    config.add_renderer('.html', 'pyramid_jinja2.renderer_factory')

    config.add_static_view('static', 'static', cache_max_age = 3600)
    config.add_route('dispatcher', '/{url:.*}', custom_predicates = (page_exists,), factory = factory)
    config.add_notfound_view(not_found, append_slash = True, renderer = '404.html')
    config.scan()

    return config.make_wsgi_app()