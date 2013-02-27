=============
django-vcards
=============

Features
--------
* URL based vcards generator for django.
* Application generate dynamically from database vcards for each entry, 
the generated vcard is compatible with all devices, even Iphone and Ipad
by using a calendar entry wrapper

Installation
------------
To install it, run the following command inside this directory:

    python setup.py install

Or if you'd prefer you can simply place the included "whatismyip"
directory somewhere on your Python path, or symlink to it from
somewhere on your Python path.

Once you have django-whatismyip in your path, you should add it to

your ``INSTALLED_APPS`` in ``settings.py``::

    INSTALLED_APPS = (
        ...
        'vcards',
        ...
    )

And in the urls.py, you should add this line:
	 urlpatterns = patterns('',
	 	...
	 	url(r'^vcards/', include('vcards.urls')),
		...
	 )


Use
---
Under admin interface generate a new vcard named vcard_name and point your 
browser to /vcards/vcard_name.vcf directory of your project.

Note
----
This application has been develop using Python 2.7 and Django 1.4,
maybe can run in older version but is not tested. 
You can obtain Python from http://www.python.org/ and
Django from http://www.djangoproject.com/.
