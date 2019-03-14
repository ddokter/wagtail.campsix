# Wagtail Camp Six

This package provides a REST API on top of the Wagtail CMS. Currently,
the intention is to show what an API implemented according to the
guidelines of REST could look like, where special attention is paid to
the _HATEOAS_ guideline, or in other words: Hypertext as the Engine of
Application State.

The current implementation is a demo for RFC 019 that has been
submitted to the Wagtail core team.

The current Wagtail API is limited in terms of resource coverage and
per-resource explicitness. Use cases for an extensive API range from a
full blown headless CMS to browsable objects for front-end selection
of, for example, pages, images and documents. Even though full
coverage may not be in the scope of development for now, the API needs
to be set up in a way that enables consumers to extract information in
a uniform way and that allows for future extension.


## Implementation details

There is several ways in which you can implement a RESTful interface
upon any given back-end. This package has been set up according to the
guidelines set out in this section.  CampSix is implemented based on
the de facto REST framework for Django, _Django\_rest\_framwork_ or,
_DRF_.  The core idea is that __all__ resources should be derivable
from one base resource, and should be self-explanatory for a given
consumer, be it humanoid or no.


### HATEOAS


HATEOAS is one of the concepts for implementing a truly RESTful
interface as defined by Roy Fielding in his original work. The fourth
guiding constraint states, among other things:

    ... hypermedia as the engine of application state.

or in other words: the state of the resource should be reflected in
it's representation. This phrase is usually shortened to
HATEOAS. Indeed, not all acronyms are making the world a better place.

A typical example in the context of a CMS would be the representation
of a page. Let us assume that a page can either be public, or private,
and that a consumer with the proper authorisation can change this
state.  A representation of the page would then not only need to show
the state, but also the way to change it. HATEOAS does not dictate
*how* to achieve this. However, usually implementations use some kind
of meta information on a resource. So, this would be a resource representation
lacking in hypermedia:

    {
      'id': 666,
      'title': 'Designing great beers',
      'author': 'Bob Dobalina',
      'state': private'
    }

and this would be the HATEOAS version:

    {
      'id': 666,
      'title': 'Designing great beers',
      'author': 'Bob Dobalina',
      'state': private',
      '_links': {
        'self': 'http://be.er/api/pages/666/',
        'publish': 'http://be.er/api/pages/666/publish/'
      }
    }

and this would be the same page, for a consumer without proper
authorisation for publishing (but enough to see private pages...):

    {
      'id': 666,
      'title': 'Designing great beers',
      'author': 'Bob Dobalina',
      'state': private',
      '_links': {
        'self': 'http://be.er/api/pages/666/',
      }
    }

After publication, the page to the authorised consumer, would look like this:

    {
      'id': 666,
      'title': 'Designing great beers',
      'author': 'Bob Dobalina',
      'state': public',
      '_links': {
        'self': 'http://be.er/api/pages/666/',
        'unpublish': 'http://be.er/api/pages/666/unpublish/'
      }
    }

So: if the consumer can perform any kind of action other than the
standard CRUD methods for REST, it should be reflected in the
resource. This allows any consumer, be it human or robot, to navigate
through the API and to detect what actions may be performed on a given
resource. A page edit screen using the REST resource for example,
would show the 'publish' button only if the link is available.


### Nesting

In many cases nesting of resources is needed. In the case of a CMS,
typically pages may contain sub-pages and images. To prevent unlimited
recursion, we need a way to represent nesting. This package uses the
concept of two serializers for representation: a _base_ serializer and
a _summary_ serializer. The base serializer is used for detail, edit
and create views, and for primary level listings. Summary serializers
are used for nesting, and should in general not contain any further
listings.  Truly recursive REST views should be implemented
explicitly, to prevent huge amounts of data going over the line. This
for instance applies to the _all pages_ view of the CMS.


### Search, ordering

The _DRF_ provides standard ways of searching and sorting. CampSix
uses these. This means that searching can be performed adding a
_search_ parameter with the search query as argument:

    http://<host>:<port>/<api>/<resource>/?search=dobalina

Ordering is done based on the _ordering_ parameter. Ordering may be
performed on any field defined in the serializer for that resource,
either the natural ordering:

    http://<host>:<port>/<api>/<resource>/?ordering=title

or the reverse:

    http://<host>:<port>/<api>/<resource>/?ordering=-title


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

When installation was successful, rev up your server and navigate to

    http://<host, probably localhost>:<port, probably 8000>/campsix/

You should see the root resource, that allows you to navigate deeper
into the API.
