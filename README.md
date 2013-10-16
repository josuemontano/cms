SpartanCMS
===

One of the best CMS I've found is [SilverStripe](http://www.silverstripe.org). But something more flexible was needed, so I wrote this content managment system in python 3.

Much work is still ahead, documentation and some functionality is incomplete, but it works! Feel free to contribute.

Dependencies
===

SpartanCMS is a web application written in Pyramid and uses:

* Pyramid 1.5a2 (obviously)
* Python 3
* SQLAlchemy
* PostgreSQL
* WTForms
* Jinja2

It is included an .htaccess file and a FGCI script as an example of how SpartanCMS can be deployed on the web over apache. To use these on a production enviroment you must **install Flup for python 3**. I use [flup-py3.3](https://github.com/Pyha/flup-py3.3).

Installation
===

This software can be installed and run as any other Pyramid app. Once you have Python 3 and PostgreSQL installed follow these steps (I assume you have a virtual enviroment installed on your $HOME, called, let us say, *env*):

* Run PostgreSQL and create a new PostgreSQL database called *demo*
* ``` cd $HOME/env/cms/spartan ```
* ``` ../../bin/python setup.py develop ```
* ``` ../../bin/initialize_spartan_db development.ini ```
* ``` ../../bin/pserve development.ini --reload ```

To run the demo site do:
* ``` cd $HOME/env/cms/demo ```
* ``` ../../bin/python setup.py develop ```
* ``` ../../bin/pserve development.ini --reload ```

**Important:** The demo package imports some models from spartan, so make sure spartan is properly installed.
