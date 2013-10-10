import os
import sys
import transaction

from sqlalchemy import engine_from_config
from pyramid.paster import (get_appsettings,setup_logging)

from spartan.models.core import *
from spartan.models.security import *

LOREM_IPSUM = '<p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Nam cursus. Morbi ut mi. Nullam enim leo, egestas id, condimentum at, laoreet mattis, massa. Sed eleifend nonummy diam. Praesent mauris ante, elementum et, bibendum at, posuere sit amet, nibh. Duis tincidunt lectus quis dui viverra vestibulum. Suspendisse vulputate aliquam dui. Nulla elementum dui ut augue. Aliquam vehicula mi at mauris. Maecenas placerat, nisl at consequat rhoncus, sem nunc gravida justo, quis eleifend arcu velit quis lacus. Morbi magna magna, tincidunt a, mattis non, imperdiet vitae, tellus. Sed odio est, auctor ac, sollicitudin in, consequat vitae, orci. Fusce id felis. Vivamus sollicitudin metus eget eros.</p><p>Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. In posuere felis nec tortor. Pellentesque faucibus. Ut accumsan ultricies elit. Maecenas at justo id velit placerat molestie. Donec dictum lectus non odio. Cras a ante vitae enim iaculis aliquam. Mauris nunc quam, venenatis nec, euismod sit amet, egestas placerat, est. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Cras id elit. Integer quis urna. Ut ante enim, dapibus malesuada, fringilla eu, condimentum quis, tellus. Aenean porttitor eros vel dolor. Donec convallis pede venenatis nibh. Duis quam. Nam eget lacus. Aliquam erat volutpat. Quisque dignissim congue leo.</p><p>Mauris vel lacus vitae felis vestibulum volutpat. Etiam est nunc, venenatis in, tristique eu, imperdiet ac, nisl. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. In iaculis facilisis massa. Etiam eu urna. Sed porta. Suspendisse quam leo, molestie sed, luctus quis, feugiat in, pede. Fusce tellus. Sed metus augue, convallis et, vehicula ut, pulvinar eu, ante. Integer orci tellus, tristique vitae, consequat nec, porta vel, lectus. Nulla sit amet diam. Duis non nunc. Nulla rhoncus dictum metus. Curabitur tristique mi condimentum orci. Phasellus pellentesque aliquam enim. Proin dui lectus, cursus eu, mattis laoreet, viverra sit amet, quam. Curabitur vel dolor ultrices ipsum dictum tristique. Praesent vitae lacus. Ut velit enim, vestibulum non, fermentum nec, hendrerit quis, leo. Pellentesque rutrum malesuada neque.</p><p>Maecenas aliquet velit vel turpis. Mauris neque metus, malesuada nec, ultricies sit amet, porttitor mattis, enim. In massa libero, interdum nec, interdum vel, blandit sed, nulla. In ullamcorper, est eget tempor cursus, neque mi consectetuer mi, a ultricies massa est sed nisl. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos hymenaeos. Proin nulla arcu, nonummy luctus, dictum eget, fermentum et, lorem. Nunc porta convallis pede.</p>'

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        site = Site('Example', 'josuemontanoa@gmail.com; josue@talentoscreativos.com', ga_code = 'UA-XXXXXX-XX')
        DBSession.add(site)

        group_a = Group('administrators')
        group_b = Group('editors')
        DBSession.add(group_a)
        DBSession.add(group_b)

        admin = User('josuemontanoa@gmail.com', '$2a$10$5ZMcPETX/dioXjFWzh29K.SIHmxWVYuYiMl1rblB5zZdol4fCE8E.', group_a)
        DBSession.add(admin)

        template_a = PageTemplate('Home', 'home.html')
        template_b = PageTemplate('Content', 'content.html')
        template_c = PageTemplate('Image/video gallery', 'gallery.html')
        template_d = PageTemplate('Contact', 'contact.html')
        DBSession.add(template_a)
        DBSession.add(template_b)
        DBSession.add(template_c)
        DBSession.add(template_d)

        home_page = Page(name = 'Inicio', description = 'This is my home page', content = LOREM_IPSUM)
        DBSession.add(home_page)

        page_a = Page(name = 'Contactos', description = 'This is my contact page')
        DBSession.add(page_a)

        page_b = Page(name = 'Quienes somos', description = 'This is my about us page', content = LOREM_IPSUM)
        DBSession.add(page_b)

        page_b1 = Page(name = 'Nuestras actividades', description = 'This is my about us page', content = LOREM_IPSUM, parent = page_b)
        DBSession.add(page_b1)

        page_c = Page(name = 'Noticias', description = 'This is my news page', content = LOREM_IPSUM)
        DBSession.add(page_c)
