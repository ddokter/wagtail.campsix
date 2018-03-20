import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()

REQUIREMENTS = [
    'setuptools',
    'django',
    'djangorestframework',
    'wagtail',
    'django-filter'
],


__version__ = "0.0.1"


setup(
    # package name in pypi
    name='wagtail-campsix',
    # extract version from module.
    version=__version__,
    description="REST API on Wagtail following HATEOAS",
    long_description=README,
    classifiers=[],
    keywords='Wagtail CMS REST API HATEOAS',
    author='D.A.Dokter',
    author_email='d@etcanemtuum.org',
    url='',
    license='',
    # include all packages in the egg, except the test package.
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    # for avoiding conflict have one namespace for all apc related eggs.
    namespace_packages=[],
    # include non python files
    include_package_data=True,
    zip_safe=False,
    # specify dependencies
    install_requires=REQUIREMENTS,
)
