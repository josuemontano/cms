import datetime

from sqlalchemy.orm import (scoped_session, sessionmaker)
from sqlalchemy.ext.declarative import declarative_base
from zope.sqlalchemy import ZopeTransactionExtension

Base      = declarative_base()
DBSession = scoped_session(sessionmaker())