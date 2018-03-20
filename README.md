# Wagtail Camp Six

This package provides a REST API on top of the Wagtail CMS. Currently,
the intention is to show what an API implemented according to the
guidelines of REST could look like, where special attention is paid to
the _HATEOAS_ guideline, or in other words: Hypertext as the Engine of
Application State.

The current implemetation is a demo for RFC 019 that has been
submitted to the Wagtail core team.


## HATEOAS

Hypertext as the Engine of Application State means that an REST API
should provide hyperlinks for any given consumer, that show the
consumer exactely what can be done with the requested resource. For a
Page resource, for example, the resource should provide a hyperlink
for publishing that page if, and only if, the current consumer can
actually publish the page.


## Install

Install the campsix in your virtual env (if you have that) using

    python setup.py develop

in this directory. Or even

    python setup.py install

if you don't feel like making changes or developing at all.

Then, in your favorite Wagtail project, add the following to our URL conf:

    from campsix import urls as campsix_urls

    ...

    urlpatterns = [
        ...
        url(r'^campsix/', include(campsix_urls)),
        url(r'', include(wagtail_urls)),
        ...
    ]

or any prefix of your liking. Make sure you add it _before_ the
wagtail URL's.

Add _django\_filters_ to your INSTALLED_APPS. That's it.


## See

When installation was succesful, rev up your server and navigate to

    http://<host, probably localhost>:<port, probably 8000>/campsix/

You should see the root resource, that allows you to navigate deeper
into the API.
