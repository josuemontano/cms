from pyramid.security import (ALL_PERMISSIONS, Allow)

from spartan.models.security import User

class EntryFactory(object):
    __name__ = ''
    __acl__  = [(Allow, 'g:editors', ('view', 'edit')),
                (Allow, 'g:administrators', ALL_PERMISSIONS)]

    def __init__(self, request):
        self.request = request


def groupfinder(userid, request):
    user = User.by_name(userid)
    if user is not None:
        ans = ['g:%s' % user.group.name]
        return ans