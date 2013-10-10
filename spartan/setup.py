import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'pyramid_jinja2',
    'WTForms',
    'psycopg2',
    'cryptacular'
    ]

setup(name='spartan',
      version='1.0',
      description='spartan',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Josue Montano',
      author_email='josuemontanoa@gmail.com',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='spartan',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = spartan:main
      [console_scripts]
      initialize_spartan_db = spartan.scripts.initializedb:main
      """,
      )
