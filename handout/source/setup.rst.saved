=============
Package Setup
=============

Contents
========

This package contains:

* student handout built as a PDF file ``handout.pdf``, as well as
  an HTML layout starting at ``handout/index.html``.

* Sphinx_ source files for the handout in ``handout/source``.  Those
  familiar with Sphinx can build the handout document in other formats
  using the makefile ``handout/Makefile``.

* Interactive Python "slide runner" application, which
  is essentially a customized `REPL <http://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop>`_
  that can step through segments of a Python script.

* Demonstration Python scripts which illustrate various features
  of SQLAlchemy; these scripts are formatted to work best with the
  "slide runner" application, though can be run directly as
  well.

* Packages required to run the interactive slide runner and the
  example SQLAlchemy programs in ``sw/``, including SQLAlchemy
  itself.


Prerequisites
=============

A minimum version of Python 2.6 is recommended;
Python 2.7, 3.1, 3.2 or 3.3 are also fine.

For database access, the tutorials use the SQLite_ database by default,
which is included as part of the Python standard library.

If your Python was custom built and does not include SQLite_, it
can be added in by rebuilding with the SQLite_ libraries available or
by installing pysqlite.

To build the documentation, the Sphinx_ documentation system and
its prerequistites must be installed.

To install the slide runner and dependencies, virtualenv_ is strongly
recommended, available at http://pypi.python.org/pypi/virtualenv.   Students are encouraged to gain rudimental familiarity with virtualenv_ prior to the class.  By using virtualenv, there will
be no dependency between the libraries used to run the local applications here
versus those libraries that may be installed with the system-wide Python.
For example, if students have old and broken versions of SQLAlchemy installed, they will
be left untouched by this process, but will not interfere with the usage
of the local application, which will be using the latest and greatest.

Obtaining the Package
======================

The most recent version of this package is available using git::

	git clone https://bitbucket.org/zzzeek/pycon2013_student_package.git

While git is preferred so that the package can easily be updated,
those who don't have git installed can also download the file
directly as a .zip file via
https://bitbucket.org/zzzeek/pycon2013_student_package/get/master.zip.

Building the Documentation Handout
==================================

The documentation can be built using standard Sphinx_ techniques.

To build HTML on Linux / OSX::

	cd handout
	make html

To build HTML on Windows::

	cd handout
	make html

The documentation can also be built as PDF or any other format supported by Sphinx_.   See the Sphinx_ documentation at http://sphinx-doc.org/ for further usage and configuration information.

Installing the Slide Environment
================================

The slide environment features a working SQLAlchemy environment as well as several tutorial-style Python scripts which illustrate usage patterns.   The slides are best run using a specialized "slide runner" application, which we
will be running as part of the class.

To make the installation as easy as possible, as well as to minimize the need for network access, source installation
packages for the non-standard prerequisite libraries are included here in the ``sw/`` directory.    However, the system is best run using a Python virtualenv_ environment, so that system-wide installation is not required.

Steps to install:

1. Ensure that virtualenv_ is installed, preferably systemwide.

2. Create a local virtualenv_::

	     $ virtualenv --no-site-packages .venv

   This will create a directory ``.venv/bin`` which is where scripts are run.  On Windows, the directory is called ``.venv/Scripts``.

3. Run the ``install.py`` script, which will install packages from the ``sw/``
   directory into the local virtualenv_.  On Linux/OSX::

	     $ .venv/bin/python install.py

   On Windows::

	     $ .venv\Scripts\python.exe install.py

4. A particular tutorial script can be run using the ``sliderepl`` program.
   On Linux OSX::

	     $ .venv/bin/sliderepl 01_engine_usage.py

   On Windows::

	     $ .venv\Scripts\sliderepl.exe 01_engine_usage.py

.. _Sphinx: http://sphinx-doc.org/

.. _SQLite: http://sqlite.org/

.. _virtualenv: http://pypi.python.org/pypi/virtualenv