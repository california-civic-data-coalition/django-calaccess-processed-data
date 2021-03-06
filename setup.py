#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from distutils.core import Command


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3'
                }
            },
            INSTALLED_APPS=('calaccess_processed',),
            MIDDLEWARE_CLASSES=()
        )
        from django.core.management import call_command
        import django
        django.setup()
        call_command('test', 'calaccess_processed')


setup(
    name='django-calaccess-processed-data',
    version='0.3.0',
    license='MIT',
    description='A Django app to transform and refine campaign finance data from the California Secretary of State’s \
CAL-ACCESS database',
    url='http://django-calaccess.californiacivicdata.org',
    author='California Civic Data Coalition',
    author_email='b@palewi.re',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,  # because we're including static files
    install_requires=(
        'django-calaccess-raw-data==3.0.1',
        'django-calaccess-scraped-data==3.0.1',
        'django>=3.2.*',
        'csvkit>=1.0',
        'opencivicdata @ git+ssh://git@github.com/california-civic-data-coalition/python-opencivicdata@7ab286179255a9d6067b2f3ff2c64ad8f82e2d9a#egg=opencivicdata',
    ),
    cmdclass={'test': TestCommand,},
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'License :: OSI Approved :: MIT License',
    ),
)
