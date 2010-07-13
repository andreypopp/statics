Getting started with statics
============================

This is about how to get statics powered site running. Ofcourse, you need
statics installed.

Installing statics
------------------

Install statics with the following command::

    $ easy_install statics

Or if you're using virtualenv::

    $ virtualenv --no-site-packages mysiteenv
    $ source mysiteenv/bin/activate
    (mysiteenv) $ easy_install statics

I'm, personally, prefer using virtualenv each time I'm using Python, but you
can go another way here, there is no problem. Just remember, if something goes
wrong -- please first try to reproduce problem inside isolated (created with
``--no-site-packages``) virtualenv instance and just after that -- report a bug.
You have been warned.

Creating site with statics
--------------------------

Create new site with command::

    $ statics-init mysite

After that there will be directory named ``mysite`` with the following contents:

::

    mysite
    |-- build
    |-- site.conf
    |-- src
    |   |-- index.txt
    |   `-- static
    |-- static.py
    `-- templates
        `-- page.html

There are site configuration ``site.conf`` stored in ini-like format, script
``statics.py`` used for building your site.

Now you have just run::

    $ ./statics.py build

And point your webserver to ``./build`` directory.
