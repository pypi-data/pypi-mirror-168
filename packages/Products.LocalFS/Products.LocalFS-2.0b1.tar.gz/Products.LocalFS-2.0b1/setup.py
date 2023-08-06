__version__ = '2.0b1'

import os

from setuptools import find_packages
from setuptools import setup


NAME = 'Products.LocalFS'
here = os.path.abspath(os.path.dirname(__file__))
_boundary = '\n' + ('-' * 60) + '\n\n'


def _read(name):
    f = open(os.path.join(here, name))
    return f.read()


setup(name=NAME,
      version=__version__,
      license='BSD License',
      description='The Local File System product',
      long_description=_read('README.rst'),
      classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Web Environment',
        'Framework :: Zope',
        'Framework :: Zope :: 4',
        'Framework :: Zope :: 5',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        ],
      keywords='web application server zope zope2',
      author='Jonothan Farr and contributors',
      author_email='jfarr@speakeasy.org',
      maintainer='Jens Vagelpohl',
      maintainer_email='jens@plyp.com',
      url='https://github.com/dataflake/%s' % NAME,
      project_urls={
          'Issue Tracker': 'https://github.com/dataflake/%s/issues' % NAME,
          'Sources': 'https://github.com/dataflake/%s' % NAME,
      },
      packages=find_packages('src'),
      include_package_data=True,
      namespace_packages=['Products'],
      package_dir={'': 'src'},
      zip_safe=False,
      python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
      install_requires=[
        'setuptools',
        'Zope',
        'Products.PythonScripts',
        ],
      extras_require={
          'docs': ['Sphinx < 2;python_version < "3"',
                   'Sphinx;python_version >= "3"']
        },
      )
