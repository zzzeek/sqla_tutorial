===============================================
2.0 - The One-Point-Four-Ening 2021 - Download
===============================================

This package is the full source code for the SQLAlchemy 2021 Tutorial.

The main thing participants will be interested in is to walk through the
interactive code demonstrations, which are present here in the
./slides/ folder.

**note:  You don't have to install the software in order to participate in the
tutorial!  Mike will be running through the same code in the screenshare.**

The .py files in this folder are plain Python files and can be read directly
as the code is presented.  Alternatively, they can be run within the same
"slide runner" environment as follows (prerequisites: git, Python virtualenv
are installed):

1. Download this repo using ``git clone``::

    git clone https://github.com/zzzeek/sqla_tutorial

2. cd into the ./slides directory and create a virtual environment::

    cd sqla_tutorial/slides
    virtualenv .venv

3. install requirements::

    .venv/bin/pip install -r requirements.txt

4. Run slides::

    .venv/bin/sliderepl 01_engine_usage.py

    .venv/bin/sliderepl 02_metadata.py

    # ... etc


The source .rst for the presentation itself is in ./presentation/, and there
is also a Sphinx documentation build for an "Introduction to SQL" handout
in the ./handout/ directory, which may be interesting to some viewers.
