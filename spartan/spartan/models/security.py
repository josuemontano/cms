from .util import *
from .meta import *


class Group (MixinTable, Base):
    __tablename__ = 'groups'
    
    id   = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(100), unique = True, nullable = False)

    def __init__(self, name):
        self.name  = name

    def __str__(self):
        return self.name


class User (MixinTable, Base):
    __tablename__ = 'users'
    
    id          = Column(Integer, primary_key = True, autoincrement = True)
    name        = Column(String(255), unique = True, nullable = False)
    group_id    = Column(Integer, ForeignKey('groups.id'), nullable = False)
    last_logged = Column(DateTime)
    misses      = Column(Integer, default = 0)
    _password   = Column('password', Unicode(256), nullable = False)
    salt        = Column(Unicode(64), nullable = False)

    group       = relationship(Group, backref = 'users')

    # ============================
    # Password getters ans setters
    # ============================
    def _get_password(self):
        return self._password
 
    def _set_password(self, password):
        self.salt, self._password = DigestUtil.hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor = password)


    def __init__(self, name = None, password = None, group = None):
        self.name     = name
        self.password = password
        self.group    = group
        self.misses   = 0
        
    def __str__(self):
        return self.name

    @classmethod
    def by_name(_class, name):
        """Returns the first user found having the provided name."""
        return DBSession.query(User).filter(_class.name == name).first()

    @classmethod
    def check_password(_class, username, password):
        """
        Returns whether the provided password matches that of the username or not and
        if the given account is disabled or not.
        """
        user = User.by_name(username)
        if not user:
            return False, False
        else:
            if user.misses >= 3:
                return False, True

            ans         = DigestUtil.check(password, user.salt, user.password)
            update_dict = {}
            if ans is False:
                user.misses += 1
            else:
                user.misses = 0
                update_dict['last_logged'] = datetime.datetime.now()
            
            update_dict['misses'] = user.misses
            DBSession.query(User).update(update_dict)
            return ans, user.misses >= 3;
