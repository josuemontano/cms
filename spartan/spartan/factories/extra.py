import os
import uuid

from .meta import *

class HomeFactory(object):
    def __init__(self, request):
        self.request = request

    def index(self):
        from .security import User

        pages = DBSession.query(Page).order_by(Page.sort).all()
        site  = DBSession.query(Site).first()
        users = DBSession.query(User).all()
        return { 'site'  : site,
                 'pages' : pages,
                 'users' : users,
                 'user'  : authenticated_userid(self.request) }


class FileFactory(object):
    def __init__(self, request):
        self.request = request
        self.here    = os.path.dirname(__file__)

    def index (self):
        return { }

    def get_images (self):
        images      = os.listdir(os.path.join(self.here, '..', 'static', 'uploads/images'))
        images_list = []

        for img in images:
            i = self.request.static_url('spartan:static/uploads/images/' + img)
            images_list.append(dict(thumb=i, image=i))
        return images_list

    def upload_image (self):
        filename   = self.request.POST['file'].filename
        input_file = self.request.POST['file'].file
        ext        = filename.rsplit('.', 1)[-1]

        if ext in ['jpg', 'jpeg', 'png', 'gif']:
            name           = '%s.%s' % (uuid.uuid4(), ext)
            file_path      = os.path.join(self.here, '..', 'static', 'uploads/images', name)
            temp_file_path = file_path + '~'
            output_file    = open(temp_file_path, 'wb')

            input_file.seek(0)
            while True:
                data = input_file.read(2<<16)
                if not data:
                    break
                output_file.write(data)
            output_file.close()
            os.rename(temp_file_path, file_path)

            link = self.request.static_url('spartan:static/uploads/images/' + name)
            return { 'filelink': link, 'filename': name }

    def upload_file (self):
        return { }