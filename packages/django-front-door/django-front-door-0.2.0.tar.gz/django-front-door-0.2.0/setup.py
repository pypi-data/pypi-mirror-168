#!/usr/bin/env python
import ast
import codecs
import os
import re
from setuptools import find_packages, setup

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
init = os.path.join(ROOT, 'src', 'front_door', '__init__.py')

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open(init, 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

requirements = ["django_regex"]
constance_require = ["django-picklefield", "django-constance"]
redis_require = ["redis", ]
tests_require = ["django-webtest",
                 "isort",
                 "flake8",
                 "pytest",
                 "pytest-django",
                 "pytest-echo",
                 "tox",
                 "django-picklefield",
                 "django-constance",
                 "redis",
                 "pytest-coverage"]
ua_require = ["user_agents",]
dev_require = ["pdbpp",
               "django"]
docs_require = []

setup(
    name='django-front-door',
    version=version,
    url='https://github.com/saxix/django-front-door',
    download_url='https://github.com/saxix/django-front-door',
    author='sax',
    author_email='s.apostolico@gmail.com',
    description="",
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    install_requires=requirements,
    tests_require=tests_require,
    extras_require={
        'test': requirements + tests_require + constance_require + redis_require + ua_require,
        'dev': dev_require + tests_require,
        'docs': dev_require + docs_require,
        'constance': constance_require,
        'redis': redis_require,
        'ua': ua_require
    },
    zip_safe=False,
    platforms=['any'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Intended Audience :: Developers'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
