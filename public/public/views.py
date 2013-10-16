from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from spartan.models.core import *
from .models import DBSession

def not_found(request):
    request.response.status = 404
    return { }


@view_config(route_name = 'dispatcher', renderer = 'index.html')
def index(context, request):
    site = DBSession.query(Site).first()
    tree = DBSession.query(Page).filter_by(parent = None, show = True).order_by(Page.sort).all()
    return { 'page' : context,
             'site' : site,
             'tree' : tree }