import datetime

from sqlalchemy import (Table, Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Enum, Unicode)
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship, backref, synonym)
from sqlalchemy.ext.declarative import (declared_attr, declarative_base)
from zope.sqlalchemy import ZopeTransactionExtension

Base      = declarative_base()
DBSession = scoped_session(sessionmaker(autoflush = True, autocommit = False, extension = ZopeTransactionExtension()))


class LoggedTable (object):
    @declared_attr
    def created(_class):
        return Column(DateTime, nullable = False, default = datetime.datetime.now)
    
    @declared_attr
    def modified(_class):
        return Column(DateTime, onupdate = datetime.datetime.now)
