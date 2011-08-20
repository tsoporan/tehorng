What is it?
-----------

**tehorng** is a search engine/network for music. It is a place where the
community can get together to share and discuss music. It is entirely self
sustained and relies on the userbase to populate it with content and keep it
active.


Helping out
-----------

Currently the project is developed by a couple developers in their spare time
(sporatically).
A few extra hands on deck would be awesome; particularly in the fields of:
graphic design, front-end development (CSS, HTML, javascript), and back-end (Python, Django)

If you feel you can lend a hand in any way shape or form don't hesitat to get
in contact with us (via github) 

There are some things that are broken and require attention but for the most
part the base functionality is there. 

Because of this you should be prepared to encounter bugs or non-working code. 

How to install
--------------

tehorng is built on Django a Python web framework. The assumption is that you
have experience with Django and thus there is some terminology that is Django
specific.

1. `virtualenv tehorng_env --python=python2.7 --no-site-packages`

2. `cd tehorng_env/ && source bin/activate`

3. `git clone git@github.com:tsoporan/tehorng.git`

4. `pip install -r requirements.txt`

5. `touch .private-settings`

6. `./manage.py syncdb`

7. At the time of writing this produces the error:

    `haystack.exceptions.MissingDependency: The 'xapian' backend requires the installation of 'xapian'. Please refer to the documentation.`

    This is because we need the installation of xapian for xapian-haystack to
    work. Since this is in virtualenv we'll have to mimick this by copying over
    xapian from /usr/lib/python (this means you should have xapian and
    xapian-bindings installed system-wide)

8. Once you have xapian and the bindings installed:

    `cp /usr/lib/python2.7/site-packages/xapian/ -r ../lib/python2.7/site-packages`

    At this point syncdb should work and you're up and running in a sane
    environment.

9. Remove the comment before the static serving line in urls.py and fire up
   runserver. (We assume this is for development, the static serving is NOT
   adequate for a production environment)

10. Squeeze and enjoy.

