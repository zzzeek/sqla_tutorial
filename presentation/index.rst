.. rst-class:: titleslide

=================================
 Introduction to SQLAlchemy 2020
=================================

.. image:: sqlalchemy.png
    :height: 4em
    :align: center
    :class: titleimage


.. rst-class:: bottom
..

  Mike Bayer

  Companion package::

      git clone http://github.com/zzzeek/sqla_tutorial



Prerequisite Knowledge
=================================

* This tutorial assumes some basic knowledge about SQL (in order of
  importance):

    * structure: tables, columns, CREATE TABLE, etc.
    * querying: selecting rows with SELECT
    * modifying data with INSERT, UPDATE, DELETE
    * general idea of database transactions (e.g. BEGIN/COMMIT/ROLLBACK)
    * joins, grouping


SQLAlchemy - Overview
=================================

* the Database Toolkit for Python
* introduced 2005
* end-to-end system for working with the Python DBAPI, relational databases,
  and the SQL language
* Current release 1.3.17
* 1.4 is the next major version, which itself is a transitional version for
  **SQLAlchemy 2.0**


SQLAlchemy Goals
=================================

* Provide helpers, tools and components to assist with and automate database
  application development at every level
* Provide a consistent and fully featured facade over the Python DBAPI
* Provide an industrial strength, but optional, object relational mapper (ORM)
* Act as the foundation for any number of third party or in-house tools


SQLAlchemy Philosophies
=================================

* Bring the usage of different databases and adapters to an interface as
  consistent as possible...
* ...but still expose distinct behaviors and features of each backend.
* Never "hide" the database or its concepts - developers must know / continue
  to think in SQL...
* Instead....provide automation and DRY
* Favor declarative and compositional patterns over flags and switches
  whenever possible
* Stay true to SQL - don't invent a new query language or relational paradigm


SQLAlchemy Overview
=================================

.. rst-class:: center-text

SQLAlchemy consists of the Core and the ORM

.. image:: sqla_arch.png
    :align: center

SQLAlchemy - Core
=================================

* Engine - a factory for database connections which are maintained by
  a connection pool
* Dialect - interprets generic SQL and database commands in terms of a specific
  DBAPI and database backend.
* Connection Pool - holds a collection of database connections in memory for
  fast re-use.
* SQL Expression Language - Allows SQL statements to be written using Python
  expressions
* Schema / Types - Uses Python objects to represent tables, columns, and
  datatypes.


SQLAlchemy - ORM
=================================

* Allows construction of Python objects which can be mapped to relational
  database tables.
* Transparently persists objects into their corresponding database tables using
  the unit of work pattern.
* Provides a query system which loads objects and attributes using SQL
  generated from mappings.
* Builds on top of the Core - uses the Core to generate SQL and talk to the
  database.
* Presents a slightly more object centric perspective, as opposed to a schema
  centric perspective.

SQLAlchemy - Other Subsystems
=============================

.. rst-class:: subheader

Some of which didn't exist when this tutorial was first written !

* ``sqlalchemy.events`` - a sophisticated event registration system which
  provides user-definable hooks throughout all SQLAlchemy components.
* ``sqlalchemy.inspect`` - a generalized system that provides a "deeper look"
  at SQLAlchemy constructs, including a schema inspection system for engines
  and an object inspector for ORM-persisted objects
* ``sqlalchemy.ext`` - a series of extensions most (but not all) tailored towards
  extending ORM functionality.
* ``sqlalchemy.testing`` - an exported test suite that is used for third party
  dialect authors to test their dialects for full feature compliance
* ``sqlalchemy.examples`` - includes an in-depth performance testing suite
  as well as the home for Space Invaders and over a dozen other recipes and
  ideas.    Many more are on the Github wiki.



The Big News:  1.4, 2.0
========================

* With the standardization of Python 3, SQLAlchemy is on the path to
  an **all new 2.0 release**.
* 2.0 includes major new features, a significant streamling of APIs, and
  removes lots of long-standing patterns that have legacy roots
* Release 1.4 is a **transitional** release.   All of 2.0's features and
  usage patterns will be present in 1.4
* For full 2.0 patterns, a "future mode" is provided that changes Core APIs
  to work in the new way fully.
* It will include a deprecation mode that warns for all the patterns that
  2.0 will remove.

1.4 / 2.0 Major Changes
===============================

.. rst-class:: subheader

(for people who already know some SQLAlchemy)

* 2.0 is Python 3 only.  1.4 still supports Python 2
* Engine changes - autocommit is removed, "connectionless" execution is
  removed.
* Result set changes - rows are completely tuple-like, many new features
  for iterating and slicing up rows
* The vast majority of SQL compilation is now cached
* ORM Query is unified with select(); can use select() to get ORM results
* The Result set is unified between Core and ORM, results in both systems
  come back in the same way


SQLAlchemy is like an Onion
=================================

.. image:: onion.png
    :align: center

.. rst-class:: center-text

Can be learned from the inside out, or the outside in.


Level 1, Engine, Connection, Transactions
==========================================

.. image:: onion.png
    :align: center


The Python DBAPI
=================================

* DBAPI - PEP-0249, Python Database API
* The de-facto system for providing Python database interfaces
* There are many DBAPI implementations available, most databases have more than
  one
* Features/performance/stability/API quirks/maintenance vary wildly

DBAPI - Nutshell
=================================

::

    import psycopg2
    connection = psycopg2.connect("scott", "tiger", "test")

    cursor = connection.cursor()
    cursor.execute(
        "select emp_id, emp_name from employee where emp_id=%(emp_id)s",
        {'emp_id':5}
    )

    emp_name = cursor.fetchone()[1]

    cursor.execute(
        "insert into employee_of_month (emp_name) values (%(emp_name)s)",
        {"emp_name":emp_name}
    )

    cursor.close()
    connection.commit()


Important DBAPI Facts
=================================

* DBAPI assumes by default that a transaction is always in progress. There is
  no ``.begin()`` method, only ``.commit()`` and ``.rollback()``.
* Most DBAPIs achieve this by employing an "autobegin" system that is typically
  invoked when the first statement is run.
* Most DBAPIs now have an ".autocommit" feature, disabled by default. When
  enabled, the "autobegin" is turned off and there is never a transaction in
  progress; ``.commit()`` and ``.rollback()`` are no-ops.
* DBAPI encourages the use of bound parameters when statements are executed,
  but it has **six** different formats.
* All DBAPIs have significant inconsistencies in how they behave.  It is not
  possible to write non-trivial DBAPI-agnostic code without the use of
  libraries on top of it.

Sample DBAPI Inconsistencies
=============================

* DBAPIs publish their own exception classes that must be caught explicitly;
  messages are completely different.
* SQLite does not fully accommodate datetime objects, they must be stored and
  retreived as strings.
* pyodbc with SQL Server will sometimes fail to use a VARCHAR table index
  because Python strings are Unicode and it passes them as NVARCHAR.
* psycopg2's ``cursor.executemany()`` call is extremely slow; special
  extensions must be employed for it to perform acceptably
* cx_Oracle requires extensive use of ``cursor.setinputsizes()`` to support
  passing simple datatypes such dates and binary objects.
* MySQL drivers require a special flag so that ``cursor.rowcount`` works the
  same as all other DBAPIs

SQLAlchemy and the DBAPI
=================================

* SQLAlchemy's first goal is to "tame" the DBAPI.
* Provides a consistent URL-based connectivity pattern
* Provides a fully-encompassing, extensible type system
* Abstracts away autoincrement / sequences / identity columns and post-fetching
  for INSERT statements
* Provides a single bound parameter format
* Provides a fixed exception hierarchy (doesn't normalize messaging though)


The SQLAlchemy Engine
=================================

.. rst-class:: subheader

The ``sqlalchemy.Engine`` object is the most fundamental gateway to
database connectivity.

::

  .venv/bin/sliderepl 01_engine.py



Level 2, Table Metadata, Reflection, DDL
=========================================

.. image:: onion.png
    :align: center

What is "Metadata"?
=================================

* Popularized by Martin Fowler, Patterns of Enterprise Architecture
* Describes the structure of the database, i.e. tables, columns, constraints,
  in terms of data structures in Python
* Serves as the basis for SQL generation and object relational mapping
* Can generate to a schema, i.e. turned into DDL that is emitted to the
  database
* Can be generated from a schema, i.e. database introspection is performed
  to generate Python structures that represent those tables
* Forms the basis for database migration tools like SQLAlchemy Alembic.


MetaData and Table
=================================

::

    .venv/bin/sliderepl 02_metadata.py

Some Basic Types
=================================

* ``Integer()`` - basic integer type, generates INT
* ``String()`` - strings, generates VARCHAR
* ``Unicode()`` - Unicode strings - generates VARCHAR, NVARCHAR depending on
  database
* ``Boolean()`` - generates BOOLEAN, INT, TINYINT, BIT
* ``DateTime()`` - generates DATETIME or TIMESTAMP, returns Python datetime()
  objects
* ``Float()`` - floating point values
* ``Numeric()`` - precision numerics using Python ``Decimal()``
* ``JSON()`` - now supported by PostgreSQL, MySQL and SQLite
* ``ARRAY()``- supported by PostgreSQL


CREATE and DROP
=================================

* ``metadata.create_all(connection, checkfirst=<True|False>)`` emits CREATE
  statements for all tables.
* ``table.create(connection, checkfirst=<True|False>)`` emits CREATE for a single
  table.
* ``metadata.drop_all(connection, checkfirst=<True|False>)`` emits DROP statements
  for all tables.
* ``table.drop(connection, checkfirst=<True| False>)`` emits DROP for a single
  table.
* It's a bit up in the air if these methods will continue to accept an
  ``Engine`` object directly or if a ``Connection`` is required.


Level 3, Core SQL Expression Language
=====================================

.. image:: onion.png
    :align: center


Core SQL Expression Language
=================================

* The SQL Expression system builds upon Table Metadata in order to compose SQL
  statements in Python.
* We will build Python objects that represent individual SQL strings
  (statements) we'd send to the database.
* These objects are composed of other objects that each represent some unit of
  SQL, like a comparison, a SELECT statement, a conjunction such as AND or OR.
* We work with these objects in Python, which are then converted to strings
  when we "execute" them (as well as if we print them).
* SQL expressions in both Core and ORM variants rely heavily on the "method
  chaining" programming pattern


SQL Expressions
=================================

::

    .venv/bin/sliderepl 03_sql_basic.py

    .venv/bin/sliderepl 03_sql_adv.py


Level 4, Object Relational Mapping
==================================

.. image:: onion.png
    :align: center


Object Relational Mapping
=================================

* Object Relational Mapping, or ORM, is the process of associating object
  oriented classes with database tables.

* We refer to the set of object oriented classes as a domain model.



What does an ORM Do?
=================================

.. rst-class:: subheader

The most basic task is to translate between a domain object and a table row.

.. image:: tablemap.png
    :align: center


What does an ORM Do?
=================================

.. rst-class:: subheader

Some ORMs can also represent arbitrary rows as domain objects within the
application, that is, rows derived from SELECT statements or views.

.. image:: selectorm.png
    :align: center


What does an ORM Do?
=================================

.. rst-class:: subheader

Most ORMs also represent basic compositions, primarily one-to-many and
many-to-one, using foreign key associations.

.. image:: relationshiporm.png
    :align: center


What does an ORM Do?
=================================

* Other things ORMs do:
    * provide a means of querying the database in terms of the domain model
      structure
    * Some can represent class inheritance hierarchies using a variety of
      schemes
    * Some can handle "sharding" of data, i.e. storing a domain model across
      multiple schemas or databases
    * Provide various patterns for concurrency, including row versioning
    * Provide patterns for data validation and coercion

Flavors of ORM
=================================

The two general styles of ORM are Active Record and Data Mapper. Active Record
has domain objects handle their own persistence::

    user_record = User(name="ed", fullname="Ed Jones")
    user_record.save()
    user_record = User.query(name='ed').fetch()
    user_record.fullname = "Edward Jones"
    user_record.save()


Flavors of ORM
=================================

The Data Mapper approach tries to keep the details of persistence separate from
the object being persisted::

    dbsession = Session()
    user_record = User(name="ed", fullname="Ed Jones")
    dbsession.add(user_record)
    user_record = dbsession.query(User).filter(name='ed').first()
    user_record.fullname = "Edward Jones"
    dbsession.commit()


Flavors of ORM
=================================

ORMs may also provide different configurational patterns. Most use an "all-at-
once", or declarative style where class and table information is together.

::

    class User(Base):
        __tablename__ = 'user'
        id = Column(Integer, primary_key=True)
        name = Column(String(length=50))
        fullname = Column(String(length=100))

    class Address(Base):
        __tablename__ = 'address'
        id = Column(Integer, primary_key=True)
        user_id = Column(ForeignKey("user.id"))
        email_address = Column(String(length=100))
        user = relationship("User")

Flavors of ORM
=================================

A less common style keeps the declaration of domain model and table metadata
separate.

::

    # class is declared without any awareness of database
    class User(object):
        def __init__(self, name, username):
            self.name = name
            self.username = username

    # elsewhere, it's associated with a database table
    mapper(
        User,
        Table(
          "user",
          metadata,
          Column("id", Integer, primary_key=True),
          Column("name", String(50)),
          Column("fullname", String(100))
        )
    )


SQLAlchemy ORM
=================================


* The SQLAlchemy ORM is essentially a data mapper style ORM.
* Modern versions use declarative configuration; the "domain and schema
  separate" configuration model is present underneath this layer.
* The ORM builds upon SQLAlchemy Core.  All of the SQL Expression language
  concepts are present when working with the ORM as well.
* In contrast to the SQL Expression language, which presents a schema-centric
  view of data, it presents a domain-model centric view of data.


Key ORM Patterns
=================================

* Unit of Work - objects are maintained by a system that tracks changes over
  the course of a transaction, and flushes pending changes periodically, in a
  transparent or semi-transparent manner
* Identity Map - objects are tracked by their primary key within the unit of
  work, and are kept unique on that primary key identity.
* Lazy Loading - Some attributes of an object may emit additional SQL queries
  when they are accessed.
* Eager Loading - attributes are loaded immediately.  Related tables may be
  loaded using JOINs to the primary SELECT statement or additional queries
  can be emitted.

ORM Walkthrough
=================================

::

    .venv/bin/sliderepl 04_orm.py


Thanks !
=================================



.. rst-class:: bottom

http://www.sqlalchemy.org
@zzzeek