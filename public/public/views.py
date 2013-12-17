from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from spartan.models.core import *
from .models import DBSession
from .forms import *


def not_found(request):
    request.response.status = 404
    site = DBSession.query(Site).first()
    return { 'site' : site, }


@view_config(route_name = 'dispatcher', renderer = 'index.html')
def index(page, request):
    site = DBSession.query(Site).first()
    tree = DBSession.query(Page).filter_by(parent = None, show = True).order_by(Page.sort).all()
    ans  = { 'page' : page,
             'site' : site,
             'tree' : tree }

    if page.template.filename == 'contact.html':
        bake_form(page, site, ans, request)

    return ans

def bake_form(page, site, ans, request):
    form    = ContactForm(request.POST)
    message = 'Por favor ingrese todos los campos obligatorios'

    if request.method == 'POST':
        if form.validate():
            import smtplib
            from smtplib import SMTPException
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            sender    = form.email.data
            receivers = site.contact_mails.split(';')

            msg            = MIMEMultipart('alternative')
            msg['Subject'] = 'Correo de contacto desde el sitio web'
            msg['From']    = sender
            msg['To']      = site.contact_mails
            html           = "<html><head></head><body><div style='text-align:center'><h2>Mensaje de %s</h2><h3>TEL&Eacute;FONO: %s</h3></div><p>%s</p></body></html>" % (form.name.data, form.phone.data, form.comment.data)
            msg.attach(MIMEText(html, 'html'))
            try:
                SMTPServer = smtplib.SMTP('localhost')
                SMTPServer.sendmail(sender, receivers, msg.as_string())
                SMTPServer.quit()
                message = 'Su mensaje se envi&oacute; exitosamente. Gracias por escribirnos, ATC se pondr&aacute; en contacto con usted a la brevedad posible.'
            except:
                message = 'Lo sentimos, no pudimos enviar su mensaje. Por favor escr&iacute;banos a ' + site.contact_mails
        else:
            message = 'Por favor corrija los errores indicados'

    ans.update({ 'form'     : form,
                 'send_url' : page.slug,
                 'message'  : message })

    return ans