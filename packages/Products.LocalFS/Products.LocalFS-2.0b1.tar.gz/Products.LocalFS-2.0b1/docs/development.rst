Development
===========

.. highlight:: console

Getting the source code
-----------------------
The source code is maintained on GitHub. To check out the main branch::

  $ git clone https://github.com/MineralWare/Products.LocalFS.git

You can also browse the code online at
https://github.com/MineralWare/Products.LocalFS

Bug tracker
-----------
For bug reports, suggestions or questions please use the
GitHub issue tracker at
https://github.com/zopefoundation/Products.LocalFS/issues.

Setting up a development sandbox and testing
--------------------------------------------
Once you've obtained a source checkout, you can follow these
instructions to perform various development tasks.
All development requires that you create a virtual envoronment and run the
buildout from the package root directory::

  $ cd Products.LocalFS
  $ python3 -m venv .
  $ bin/pip install -U pip wheel
  $ bin/pip install "zc.buildout>=3.0.0rc3" tox twine
  $ bin/buildout

Once you have a buildout, the tests can be run as follows::

  $ bin/test

To run tests for all supported Python versions, code coverage and a
PEP-8 coding style checker, you can use ``tox`` after completing the
buildout step above::

  $ bin/tox

Building the documentation
--------------------------
The Sphinx documentation is built in the ``docs`` subfolder after you have run
the buildout, which installs the required tools::

  $ cd docs
  $ make html

The finished HTML files are under `docs/_build/html`.
