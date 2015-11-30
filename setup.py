#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os.path import join, dirname


from tsip import NAME, VERSION, LICENSE, AUTHOR, EMAIL, DESCRIPTION, URL

readme = open(join(dirname(__file__), 'README.rst')).read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    # 'package1', 'package2'
    
]

test_requirements = [
    # 'package1', 'package2'
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme + '\n\n' + history,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=[
        NAME,
    ],
    package_dir={'tsip':
                 'tsip'},
    include_package_data=True,
    install_requires=requirements,
    license=LICENSE,
    zip_safe=False,
    keywords='TSIP, Trimble, GPS',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    test_suite='tests',
    tests_require=test_requirements
)


# References
#
# - https://pythonhosted.org/setuptools/index.html
# - http://foobar.lu/wp/2012/05/13/a-comprehensive-step-through-python-packaging-a-k-a-setup-scripts/
# - https://pypi.python.org/pypi?%3Aaction=list_classifiers
