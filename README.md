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

If you feel you can lend a hand in any way shape or form don't hesitate to get
in contact with us (via github that is @tsoporan @lrvick) 

There are some things that are broken and require attention but for the most
part the base functionality is there. 

Because of this you should be prepared to encounter bugs or non-working code. 

How to install
--------------

tehorng is built on Django a Python web framework. The assumption is that you
have experience with Django and thus there is some terminology that is Django
specific.

1. `mkvirtualenv tehorng --python=python2.7`

2. `cd /where/ever/you/want/to/start/work`

3. `git clone git@github.com:tsoporan/tehorng.git`

4. `pip install -r requirements.txt`

5. `python manage.py syncdb`

6. Remove the comment before the static serving line in urls.py and fire up
   runserver. (We assume this is for development, the static serving is NOT
   adequate for a production environment)

7. Squeeze and enjoy.

