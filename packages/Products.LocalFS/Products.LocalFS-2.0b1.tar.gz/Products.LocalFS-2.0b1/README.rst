.. image:: https://github.com/dataflake/Products.LocalFS/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/dataflake/Products.LocalFS/actions/workflows/tests.yml

.. image:: https://coveralls.io/repos/github/dataflake/Products.LocalFS/badge.svg
   :target: https://coveralls.io/github/dataflake/Products.LocalFS

.. image:: https://img.shields.io/pypi/v/Products.LocalFS.svg
   :target: https://pypi.python.org/pypi/Products.LocalFS
   :alt: Current version on PyPI

.. image:: https://img.shields.io/pypi/pyversions/Products.LocalFS.svg
   :target: https://pypi.org/project/Products.LocalFS
   :alt: Supported Python versions

Local File System product
==========================

This product allows you to serve files and browse directories from the 
local file system (or network shares on Windows platforms). It also
allows you to upload files to the file system through a browser or WebDAV.

**WARNING**: Allowing any type of write access to a folder on disk straight
from a web application represents a security risk. Please secure your
application before using this package.
 
The documentation for this product is maintained by Sphinx
using sources underneath the ``docs`` folder.

To get started without the compiled HTML documentation see the 
file ``docs/development.rst``
