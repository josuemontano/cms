from .meta import *

class PageTemplate (Base):
    __tablename__ = 'page_templates'
    
    id       = Column(Integer, primary_key = True, autoincrement = True)
    name     = Column(String(100), unique = True, nullable = False)
    filename = Column(String, nullable = False)

    def __init__(self, name, filename = None):
        self.name     = name
        if filename is None:
            self.filename = name.lower() + '.html'
        else:
            self.filename = filename

    def __str__(self):
        return self.name


class Page (LoggedTable, Base):
    __tablename__ = 'pages'
    
    id          	 = Column(Integer, primary_key = True, autoincrement = True)
    name        	 = Column(String(300), nullable = False)
    slug             = Column(String, nullable = False, unique = True)
    template_id      = Column(Integer, ForeignKey('page_templates.id'), nullable = False)
    sort             = Column(Integer, nullable = False, default = 1)
    parent_id        = Column(Integer, ForeignKey('pages.id'))

    description 	 = Column(String)
    content     	 = Column(String)
    show        	 = Column(Boolean, default = True, nullable = False)
    searchable       = Column(Boolean, default = True, nullable = False)
    
    floating_content = Column(String)
    show_floating    = Column(Boolean, default = False, nullable = False)
    
    template         = relationship('PageTemplate')
    children         = relationship('Page', backref=backref('parent', remote_side=[id]), order_by='Page.sort')

    def __init__(self, name = None, template_id = 2, description = None, content = None, show = True, searchable = True, show_floating = False, parent = None):
        self.name          = name
        self.template_id   = template_id
        self.description   = description
        self.content       = content
        self.show          = show
        self.searchable    = searchable
        self.show_floating = show_floating
        self.parent        = parent
        self.set_slug()
        
    def __str__(self):
        return self.name

    def has_children(self):
        return len(self.children) > 0

    def set_slug(self):
        if self.name is not None:
            root = '/'
            if self.parent is not None:
                root = self.parent.slug + '/'
            self.slug = root + ''.join(e for e in self.name.lower() if e.isalnum())

class Site (LoggedTable, Base):
    __tablename__ = 'site'
    
    id               = Column(Integer, primary_key = True, autoincrement = True)
    title            = Column(String(300), unique = True, nullable = False)
    contact_mails    = Column(String)
    logo             = Column(String)

    facebook         = Column(String)
    twitter          = Column(String)
    youtube          = Column(String)
    ga_code          = Column(String)

    meta_description = Column(String)
    meta_keywords    = Column(String)
    meta_copyright   = Column(String)

    def __init__(self, title, contact_mails, logo = None, facebook = None, twitter = None, youtube = None, ga_code = None):
        self.title         = title
        self.contact_mails = contact_mails
        self.logo          = logo
        self.facebook      = facebook
        self.twitter       = twitter
        self.youtube       = youtube
        self.ga_code       = ga_code

    def __str__(self):
        return self.name
        