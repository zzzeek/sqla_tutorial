=============
Package Setup
=============

Contents
========

This package contains:

* student handout built as a PDF file ``handout.pdf``.

* Interactive Python "slide runner" application, which
  is essentially a customized `REPL <http://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop>`_
  that can step through segments of a Python script.

* Demonstration Python scripts which illustrate various features
  of SQLAlchemy; these scripts are formatted to work best with the
  "slide runner" application, though can be run directly as
  well.

* Packages required to run the interactive slide runner and the
  example SQLAlchemy programs in ``sw/``, including SQLAlchemy
  itself, as well as virtualenv_.

Obtaining the Package
======================

A zipfile of the package is currently available on the techspot blog::

  http://techspot.zzzeek.org/sqlalchemy_tutorial.zip

Environment Install Prerequisites
=================================

This section will discuss the prerequisites to installing the sample
SQLAlchemy environment and slide runner application.

A minimum version of Python 2.6 is recommended; Python 2.7
as well as newer Python 3 versions (3.3, 3.4, etc.) are also fine.

For database access, the tutorials use the SQLite_ database by default,
which is included as part of the Python standard library.

If your Python was custom built and does not include SQLite_, it
can be added in by rebuilding with the SQLite_ libraries available or
by installing pysqlite.

Installing the Slide Environment
================================

The slide environment features a working SQLAlchemy environment as
well as several tutorial-style Python scripts which illustrate usage
patterns.   The slides are best run using a specialized "slide runner"
application, which we will be running as part of the class.

To make the installation as easy as possible, as well as to minimize
the need for network access, source installation packages for the non-
standard prerequisite libraries are included here in the ``sw/``
directory.

Steps to install:

1. If virtualenv is not installed locally, or if you're not sure, the
   ``install_venv.py`` script will install using a local virtualenv script.
   Assuming a Python intepreter is in the path::

      $ python install_venv.py

   This script will create a virtual Python environment in the local directory
   ``.venv`` into which it will then run the ``install.py`` script to install
   the rest of the libraries.

2. If the local workstation does have virtualenv installed, it can be run
   manually::

      $ virtualenv .venv

   This will create a virtual Python environment in the directory ``.venv``.
   The ``install.py`` script should then be run, which will then setup
   libraries in this environment. On Linux/OSX::

	     $ .venv/bin/python install.py

   On Windows::

	     $ .venv\Scripts\python.exe install.py

3. Once ``.venv`` is present and the libraries are installed, a
   particular tutorial script can be run using the ``sliderepl`` program.

   On Linux/OSX::

	     $ .venv/bin/sliderepl 01_engine_usage.py

   On Windows::

	     $ .venv\Scripts\sliderepl.exe 01_engine_usage.py

.. _SQLite: http://sqlite.org/

.. _virtualenv: http://pypi.python.org/pypi/virtualenv