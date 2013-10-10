from demo.models.meta import DBSession
from demo.models.core import Page

def get_url(info):
    url = info['match']['url']
    if url and url.endswith('/'):
        url = url[:-1]
    url = '/' + url
    return url

def page_exists(info, request):
    url  = get_url(info)
    if url == '/':
        page = DBSession.query(Page).filter_by(sort = 1, parent = None).first()
    else:
        page = DBSession.query(Page).filter_by(slug = url).first()
    
    if page is None:
        return False

    info['match']['page'] = page
    return True

def factory(request):
    page = request.matchdict.get('page')
    if page:
        return page