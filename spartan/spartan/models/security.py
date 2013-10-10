import cryptacular.bcrypt

from .meta import *

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

class Group (LoggedTable, Base):
    __tablename__ = 'groups'
    
    id   = Column(Integer, primary_key = True, autoincrement = True)
    name = Column(String(100), unique = True, nullable = False)

    def __init__(self, name):
        self.name  = name

    def __str__(self):
        return self.name


class User (LoggedTable, Base):
    __tablename__ = 'users'
    
    id          = Column(Integer, primary_key = True, autoincrement = True)
    name        = Column(String(255), unique = True, nullable = False)
    group_id    = Column(Integer, ForeignKey('groups.id'), nullable = False)
    last_logged = Column(DateTime, default = datetime.datetime.utcnow)
    _password   = Column('password', Unicode(60), nullable = False)

    group       = relationship(Group, backref = 'users')

    def __init__(self, name = None, password = None, group = None):
        self.name      = name
        self._password = password
        self.group     = group
        
    def __str__(self):
        return self.name

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = crypt.encode(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor = password)


    @classmethod
    def by_name(_class, name):
        return DBSession.query(_class).filter(_class.name == name).first()

    @classmethod
    def check_password(_class, username, password):
        user = _class.by_name(username)
        if not user:
            return False
        return crypt.check(user.password, password)
