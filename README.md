tehorng is a search engine and community for music.

There are some things that are broken or require attention but for the most
part the base functionality is there. 

Because of this you should be prepared to encounter bugs. 

How to install:


1. virtualenv tehorng_env --python=python2.7 --no-site-packages

2. cd tehorng_env/ && source bin/activate

3. git clone git@github.com:tsoporan/tehorng.git

4. pip install -r requirements.txt

5. touch .private-settings

6. ./manage.py syncdb

7. At the time of writing this produces the error:

   """
   haystack.exceptions.MissingDependency: The 'xapian' backend requires the
   installation of 'xapian'. Please refer to the documentation.
   """

   This is because we need the installation of xapian for xapian-haystack to
   work. Since this is in virtualenv we'll have to mimick this by copying over
   xapian from /usr/lib/python (this means you should have xapian and
   xapian-bindings installed system-wide)

   Once you have xapian and the bindings installed:

   """
   cp /usr/lib/python2.7/site-packages/xapian/ -r
   ../lib/python2.7/site-packages
   """

8. At this point syncdb should work and you're up and running in a sane
   environment. Follow the steps in "how to use tehorng" for what to do next.



How to use tehorng:

This needs to be written.

