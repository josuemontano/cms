SpartanCMS
===

One of the best CMS I've found is [SilverStripe](http://www.silverstripe.org). But something more flexible was needed, so I wrote this content managment system in python.

Much work is still ahead, documentation and some functionality is incomplete, but it works! Feel free to contribute.

Dependencies
===

SpartanCMS is a web application built with:

* [Pyramid](http://www.pylonsproject.org/projects/pyramid/about) and Python 3
* SQLAlchemy
* PostgreSQL (it's the default DBMS)
* WTForms
* Jinja2
* cryptography
* psycopg2 (change it to your DMBS library in case you won't use PostgreSQL)

It is included an .htaccess file and a FGCI script as an example of how SpartanCMS can be deployed on the web over an Apache web server. To use these on a production enviroment you must **install Flup for python 3**. I use [flup-py3.3](https://github.com/Pyha/flup-py3.3).

Installation
===

This software can be installed and run as any other Pyramid app. Once you have Python 3 and PostgreSQL installed follow these steps (I assume you have a virtual enviroment installed on your $HOME, called, let us say, *env*):

* Run PostgreSQL and create a new PostgreSQL database called *demo*
* ``` cd $HOME/env/cms/spartan ```
* ``` ../../bin/python setup.py develop ```
* ``` ../../bin/initialize_spartan_db development.ini ```
* ``` ../../bin/pserve development.ini --reload ```

To run the public demo site do:
* ``` cd $HOME/env/cms/public ```
* ``` ../../bin/python setup.py develop ```
* ``` ../../bin/pserve development.ini --reload ```

**Important:** The public package imports some models from spartan, so make sure spartan is properly installed.

I'm a big fun of [OpenShift](http://www.openshift.com), it's simply the best PaaS out there, I believe. It is hosting some web pages I made with SpartanCMS. To install this app, and any other Pyramid app, on OpenShift view my project [OpenshiftStarter](http://github.com/josuemontano/OpenshiftStarter).
