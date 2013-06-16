.. _glossary:

========
Glossary
========

The glossary is broken into two distinct areas of terminology, for those who
want to read the whole thing.

:ref:`glossary_relational`

:ref:`glossary_sqlalchemy`

.. _glossary_relational:

Relational Terms
================

.. glossary::
    :sorted:

    constraint
    constraints
        Rules established within a relational database that ensure
        the validity and consistency of data.   Common forms
        of constraint include :term:`primary key constraint`,
        :term:`foreign key constraint`, and :term:`check constraint`.

        .. seealso::

            :ref:`consistency`

    primary key
    primary key constraint

        A :term:`constraint` that uniquely defines the characteristics
        of each :term:`row`. The primary key has to consist of
        characteristics that cannot be duplicated by any other row.
        The primary key may consist of a single attribute or
        multiple attributes in combination.
        (via Wikipedia)

        The primary key of a table is typically, though not always,
        defined within the ``CREATE TABLE`` :term:`DDL`:

        .. sourcecode:: sql

            CREATE TABLE employee (
                 emp_id INTEGER,
                 emp_name VARCHAR(30),
                 dep_id INTEGER,
                 PRIMARY KEY (emp_id)
            )

        .. seealso::

            :ref:`primary_key`

            http://en.wikipedia.org/wiki/Primary_Key

    foreign key constraint
        A referential constraint between two tables.  A foreign key is a field or set of fields in a
        relational table that matches a :term:`candidate key` of another table.
        The foreign key can be used to cross-reference tables.
        (via Wikipedia)

        A foreign key constraint can be added to a table in standard
        SQL using :term:`DDL` like the following:

        .. sourcecode:: sql

            ALTER TABLE employee ADD CONSTRAINT dep_id_fk
            FOREIGN KEY (employee) REFERENCES department (dep_id)

        .. seealso::

            :ref:`foreign_key`

            http://en.wikipedia.org/wiki/Foreign_key_constraint

    candidate key

        A :term:`relational algebra` term referring to an attribute or set
        of attributes that form a uniquely identifying key for a
        row.  A row may have more than one candidate key, each of which
        is suitable for use as the primary key of that row.
        The primary key of a table is always a candidate key.

        .. seealso::

            :ref:`primary_key`

            http://en.wikipedia.org/wiki/Candidate_key

    check constraint

        A check constraint is a
        condition that defines valid data when adding or updating an
        entry in a table of a relational database. A check constraint
        is applied to each row in the table.

        (via Wikipedia)

        A check constraint can be added to a table in standard
        SQL using :term:`DDL` like the following:

        .. sourcecode:: sql

            ALTER TABLE distributors ADD CONSTRAINT zipchk CHECK (char_length(zipcode) = 5);

        .. seealso::

            http://en.wikipedia.org/wiki/Check_constraint

    unique constraint
    unique key index
        A unique key index can uniquely identify each row of data
        values in a database table. A unique key index comprises a
        single column or a set of columns in a single database table.
        No two distinct rows or data records in a database table can
        have the same data value (or combination of data values) in
        those unique key index columns if NULL values are not used.
        Depending on its design, a database table may have many unique
        key indexes but at most one primary key index.

        (via Wikipedia)

        .. seealso::

            http://en.wikipedia.org/wiki/Unique_key#Defining_unique_keys

    ACID
    ACID model
        An acronym for "Atomicity, Consistency, Isolation,
        Durability"; a set of properties that guarantee that
        database transactions are processed reliably.
        (via Wikipedia)

        .. seealso::

            :ref:`acid_model`

            http://en.wikipedia.org/wiki/ACID_Model

    atomicity
        Atomicity is one of the components of the :term:`ACID` model,
        and requires that each transaction is "all or nothing":
        if one part of the transaction fails, the entire transaction
        fails, and the database state is left unchanged. An atomic
        system must guarantee atomicity in each and every situation,
        including power failures, errors, and crashes.
        (via Wikipedia)

        .. seealso::

            :ref:`atomicity`

            http://en.wikipedia.org/wiki/Atomicity_(database_systems)

    consistency
        Consistency is one of the compoments of the :term:`ACID` model,
        and ensures that any transaction will
        bring the database from one valid state to another. Any data
        written to the database must be valid according to all defined
        rules, including but not limited to :term:`constraints`, cascades,
        triggers, and any combination thereof.
        (via Wikipedia)

        .. seealso::

            :ref:`consistency`

            http://en.wikipedia.org/wiki/Consistency_(database_systems)

    isolation
    isolated
        The isolation property of the :term:`ACID` model
        ensures that the concurrent execution
        of transactions results in a system state that would be
        obtained if transactions were executed serially, i.e. one
        after the other. Each transaction must execute in total
        isolation i.e. if T1 and T2 execute concurrently then each
        should remain independent of the other.[citation needed]
        (via Wikipedia)

        .. seealso::

            :ref:`isolation`

            http://en.wikipedia.org/wiki/Isolation_(database_systems)

    durability
        Durability is a property of the :term:`ACID` model
        which means that once a transaction has been committed,
        it will remain so, even in the event of power loss, crashes,
        or errors. In a relational database, for instance, once a
        group of SQL statements execute, the results need to be stored
        permanently (even if the database crashes immediately
        thereafter).
        (via Wikipedia)

        .. seealso::

            :ref:`durability`

            http://en.wikipedia.org/wiki/Durability_(database_systems)

    commit
        Denotes the successful completion of a :term:`transaction`.
        In SQL, we normally denote the commit using the ``COMMIT`` statement:

        .. sourcecode:: sql

            BEGIN TRANSACTION

            INSERT INTO employee (emp_id, emp_name, dep_id)
                        VALUES (1, 'dilbert', 1);

            INSERT INTO employee (emp_id, emp_name, dep_id)
                        VALUES (2, 'wally', 1);

            COMMIT

        Above, the ``employee`` rows for ``dilbert`` and ``wally``
        will be permanently available following the ``COMMIT`` statement.

    rollback
        Denotes the end to a :term:`transaction` which reverses
        all the effects of the transaction that have proceeded thus far; the
        state established within the transaction is discarded.   In SQL,
        this is normally denoted using the ``ROLLBACK`` statement:

        .. sourcecode:: sql

            BEGIN TRANSACTION

            INSERT INTO employee (emp_id, emp_name, dep_id)
                        VALUES (1, 'dilbert', 1);

            INSERT INTO employee (emp_id, emp_name, dep_id)
                        VALUES (2, 'wally', 1);

            ROLLBACK

        Above, no new rows will be present in the database following
        the ``ROLLBACK`` statement; both rows inserted for ``dilbert``
        and ``wally`` will be discarded.

    multi version concurrency control
    MVCC
        A system by which modern databases provide concurrent
        access to database data.   By assigning *versions* to
        snapshots of data in time, multiple transactions may simultaneously
        view different versions of the data, relative to the time
        that they were begun.

        .. seealso::

            :ref:`isolation`

            http://en.wikipedia.org/wiki/Multiversion_concurrency_control

    transaction
    transactional
        A transaction comprises a unit of work (not to be confused
        with SQLAlchemy's :term:`unit of work` pattern, which is
        similar) performed within a database management system
        against a database, and treated in a coherent and reliable way
        independent of other transactions. Transactions in a database
        environment have two main purposes:

            * To provide reliable units of work that allow correct
              recovery from failures and keep a database consistent even
              in cases of system failure, when execution stops
              (completely or partially) and many operations upon a
              database remain uncompleted, with unclear status.

            * To provide isolation between programs accessing a database
              concurrently. If this isolation is not provided, the
              programs' outcomes are possibly erroneous.

        (via Wikipedia)

        .. seealso::

            http://en.wikipedia.org/wiki/Database_transaction

            :ref:`acid_model`

            :term:`commit`

            :term:`rollback`


    surrogate primary key

        A :term:`primary key` that is not derived from application
        data.

        (via Wikipedia)

        Surrogate primary keys in practice are often
        integer values generated by database sequences
        or other incrementing counters,
        or less commonly global unique identifiers (GUIDs).

        .. seealso::

            :term:`natural primary key`

            http://en.wikipedia.org/wiki/Surrogate_key

    natural primary key

        A :term:`primary key` that is formed of attributes that
        already exist in the real world. For example, a USA citizen's
        social security number could be used as a natural key. In
        other words, a natural key is a :term:`candidate key` that has a
        logical relationship to the attributes within that :term:`row`.

        (via Wikipedia)

        .. seealso::

            :term:`surrogate primary key`

            http://en.wikipedia.org/wiki/Natural_key

    FROM clause
        A component of the ``SELECT`` statement which specifies the source
        tables or subqueries from which rows are to be selected.  The ``FROM``
        clause follows the :term:`columns clause` and may contain a comma-separated
        list of tables and subqueries, as well as :term:`join` expressions:

        .. sourcecode:: sql

            -- FROM clause illustrating an explicit join

            SELECT id, name, email_address
             FROM user_account
             JOIN email_address ON user_account.id=email_address.user_account_id

            -- FROM clause illustrating an implicit join

            SELECT id, name, email_address
             FROM user_account, email_address
             WHERE user_account.id=email_address.user_account_id

    WHERE clause
        A component of the ``SELECT`` statement which specifies logical criteria
        to be applied to each row retrieved from the :term:`FROM clause`.
        The ``SELECT`` statement discards all rows which do not evaluate to
        "true" for a given WHERE clause.

        Below, we select rows from the ``email_address`` table, but use the
        WHERE clause to limit the results to only those rows which refer to email
        addresses that contain ``@gmail.com``:

        .. sourcecode:: sql

            SELECT id, email_address FROM email_address
            WHERE email_address LIKE '%@gmail.com'


    columns clause
        The portion of a ``SELECT`` statement that enumerates a series of SQL
        expressions to be evaulated as the returned result set.  Typically,
        these expressions refer directly to table columns.  The columns
        clause follows the ``SELECT`` keyword and precedes the ``FROM``
        keyword.

        In the following ``SELECT`` statement, the "id" and "name" columns
        will be returned for each row, and this enumeration of columns
        forms the "columns clause":

        .. sourcecode:: sql

            SELECT id, name FROM user_account


    column
    columns
        A vertical unit of storage in a :term:`table`.   The table
        defines one or more columns as fixed types of data to
        be stored within rows.

    table
        A fundamental storage component used by relational databases.
        The table corresponds to what's known as a :term:`relation`
        in :term:`relational algebra`, and defines a series of
        :term:`columns`, each of which represents a particular
        type of data value to be stored in the table.  The columns
        are then organized at the data storage level into a collection
        of :term:`rows`, each of which corresponds to a unit of
        data.

    row
    rows
        A horizontal unit of storage in a :term:`table`.  Each new data
        record inserted into a table comprises a row; the row in turn
        is broken into individual :term:`column` values.

    tuple
    tuples
    row value
        An ordered collection of typed values, such as
        ``(1, 'ed', 'ed@msn.com')``.

    table value
    rowset
        An ordered collection of row values, each of the same length and types.

    scalar
    scalar value
        A single value, such as ``'a'``, ``123`` or ``'2008-02-01'``.

    normalization
        Database normalization is the process of organizing the fields
        and tables of a relational database to minimize redundancy and
        dependency. Normalization usually involves dividing large
        tables into smaller (and less redundant) tables and defining
        relationships between them. The objective is to isolate data
        so that additions, deletions, and modifications of a field can
        be made in just one table and then propagated through the rest
        of the database via the defined relationships.
        (via Wikipedia)

        .. seealso::

            :ref:`normalization`

            http://en.wikipedia.org/wiki/Database_normalization

    relational model
    relational algebra
        The relational model for database management is a database model
        based on first-order predicate logic, first formulated and
        proposed in 1969 by :term:`Edgar F. Codd`. In the relational model
        of a database, all data is represented in terms of :term:`tuples`, grouped
        into :term:`relations`. A database organized in terms of the relational
        model is a relational database.
        (via Wikipedia)

        .. seealso::

            http://en.wikipedia.org/wiki/Relational_model

    Edgar Codd
    Edgar F. Codd
        Creator of the :term:`relational model`.

        .. seealso::

            http://en.wikipedia.org/wiki/Edgar_F._Codd


    Structured Query Language
    SQL
        A special-purpose programming language designed
        for managing data in relational database management systems
        (RDBMS).

        Originally based upon relational algebra and tuple relational
        calculus, its scope includes data insert, query, update and
        delete, schema creation and modification, and data access
        control.

        (via Wikipedia)

        .. seealso::

            http://en.wikipedia.org/wiki/Sql

    cartesian product
        A mathematical operation which returns a set (or product set) from multiple sets.
        The Cartesian product is the result of crossing members of each set with one another.
        (via Wikipedia)

        .. seealso::

            http://en.wikipedia.org/wiki/Cartesian_product

    relation
    relations
        In :term:`relational algebra`, a single grid of data represented by
        zero or more :term:`tuples`. In a SQL database, the most common
        relation is the :term:`table`, which defines one or more columns of zero
        or more :term:`rows`. The output of a ``SELECT`` statement is also a relation.


    data manipulation language
    DML
        The SQL commands that manipulate data.
        For example, ``SELECT``, ``INSERT``, ``UPDATE`` and ``DELETE``.

        .. seealso::

            :ref:`dml`

            http://en.wikipedia.org/wiki/Data_Manipulation_Language


    data definition language
    DDL
        The SQL commands that define a schema.
        For example, ``CREATE TABLE``, ``DROP TABLE``, ``ALTER TABLE``.

        .. seealso::

            :ref:`ddl`

            http://en.wikipedia.org/wiki/Data_Definition_Language

    query
    queries
        The means of interrogating a relational database for
        data.   The primary feature in SQL used for querying
        is the ``SELECT`` statement.

        .. seealso::

            :ref:`queries`

            http://en.wikipedia.org/wiki/Sql#Queries


    join
    inner join
        Combines the rows of two tables.  Considers each pair of rows
        in turn, and returns one combined row for each pair that
        matches an ON criteria.

        .. sourcecode:: sql

            SELECT ua.id, ua.name, ea.email, ea.user_account_id
             FROM user_account AS ua
              JOIN email_address AS ea
              ON ua.id = ea.user_account_id

             id | name  |      email     | user_account_id
            ----+-------+----------------+----------------
              1 | jack  |  jack@jack.com |       1
              2 | ed    |  ed@yahoo.com  |       2
              2 | ed    |  ed@msn.com    |       2
              3 | wendy |  wendy@nyt.com |       3

        The result of the join can be defined in a logical
        sense by first
        determining the :term:`cartesian product` of the left and
        right side tables; then, for each row within this product,
        evaluating ``ON`` clause for each row, selecting only those
        rows for which the clause evaluates to "true".
        In practice, relational database systems
        use more efficient approaches internally in order to evaluate
        the result of a join.

        Usage of the ``JOIN`` or ``INNER JOIN`` keyword is logically
        equivalent to a so-called *implicit join*, where the ``JOIN``
        keyword is not present, and instead the left and right side
        expressions are delivered to the :term:`FROM clause` as a comma
        separated list, with the ON criteria stated instead in
        the ``WHERE`` clause:

        .. sourcecode:: sql

            SELECT ua.id, ua.name, ea.email, ea.user_account_id
             FROM user_account AS ua, email_address.ea
             WHERE ua.id = ea.user_account_id


        .. seealso::

            :term:`left outer join`

            http://en.wikipedia.org/wiki/Sql_join


    left outer join
        A variant of the :term:`join` whereby the criteria for
        including rows from the "left" side is relaxed, such that
        not only left-side rows which correspond to the right side
        are returned, but also left-side rows for which no right
        side row corresponds.   In the case where no right
        side row corresponds, all columns from the right side
        are returned as NULL.

        Below, we illustrate selecting all user names from the
        ``user_account`` table, in addition to all the ``email_address``
        rows for each ``user_account`` row, but also including
        rows from ``user_account`` for which no row in ``email_address``
        is present:

        .. sourcecode:: sql


            SELECT ua.id, ua.name, ea.email, ea.user_account_id
             FROM user_account AS ua
              JOIN email_address AS ea
              ON ua.id = ea.user_account_id

             id | name  |      email     | user_account_id
            ----+-------+----------------+----------------
              1 | jack  |  jack@jack.com |       1
              2 | ed    |  ed@yahoo.com  |       2
              2 | ed    |  ed@msn.com    |       2
              3 | wendy |  wendy@nyt.com |       3
              4 | mary  |     (null)     |     (null)

        The left outer join is a key technique used in object relational
        systems in order to resolve a :term:`one to many` collection,
        that is a series of objects that contain zero or more related objects.

        .. seealso::

            :term:`join`

    right outer join
        Like a :term:`left outer join`, except the left and right side
        are swapped.  At least
        one row will be returned for every row in the right table, and
        columns from the left row will be filled with NULL if the ON
        criteria does not match.  Right outer joins are not frequently
        used.

    subquery
        A ``SELECT`` statement embedded in another ``SELECT`` statement.  Data
        returned from the inner ``SELECT`` is available for use by the
        outer.

        The subquery is a fundamental capability in SQL that allows
        so-called *derived tables* to be created; meaning, the rows
        from a particular ``SELECT`` statement can be named as a unit of
        rows within an enclosing ``SELECT`` that causes it to behave more or
        less like a plain :term:`table`.

        Example:

        .. sourcecode:: sql

            SELECT user_account.name, subq.ad_count FROM
                user_account JOIN
                (SELECT user_account_id, count(id) AS ad_count
                FROM email_address GROUP BY user_account_id) AS subq
                ON user_account.id=subq.user_account_id

        Subqueries can be placed in a variety of ways inside of an enclosing
        ``SELECT`` statement.    Three common locations include the :term:`columns clause`,
        the :term:`WHERE clause`, and the :term:`FROM clause`.   The placement
        of the subquery has an impact on the kind of data the query must return.
        In standard SQL, subqueries placed within the columns or WHERE clause must
        be :term:`scalar subqueries`, i.e. queries that return a single value, unless
        they are evaluated by a boolean aggregation operator such as :term:`IN`,
        :term:`EXISTS`, ``ANY`` or ``ALL``.   A subquery used in the :term:`FROM clause`,
        on the other hand, can return any number of rows and columns.

        Subqueries within the WHERE clause or columns clause are often :term:`correlated subqueries`
        as well, as they are invoked for each row received in the enclosing query.
        For a FROM clause subquery, correlation is not an option as the FROM clause
        is evaluated before the correlatable rows are chosen.

    scalar subquery
    scalar subqueries
        A scalar subquery is a :term:`subquery` that returns a single column from a
        single row.  Scalar subqueries can be used like columns or anywhere
        an expression is required, which typically includes the :term:`columns clause`
        or :term:`WHERE clause` of a ``SELECT`` statement.

        Below, a scalar subquery is used in the columns clause to select the ``name``
        column from the ``user_account`` table for each row selected from the
        ``email_address`` table:

        .. sourcecode:: sql


            SELECT
                email_address.email,
                (SELECT user_account.name FROM user_account WHERE id=1) AS name
            FROM email_address WHERE email_address.user_account_id=1

                 email     | name
            ---------------+----------
             jack@jack.com | jack

        Selecting an email address by user name, using a scalar subquery
        in the ``WHERE`` clause:

        .. sourcecode:: sql

            SELECT email_address.email FROM email_address
            WHERE email_address.user_account_id=
                (SELECT id FROM user_account WHERE name='jack')

                email
            ---------------
             jack@jack.com

    uncorrelated subquery
        A :term:`subquery` is uncorrelated if the database can execute it in
        isolation, without referring to the enclosing ``SELECT``
        statement.

        .. sourcecode:: sql

            SELECT user_account.name FROM user_account
            WHERE user_account.id IN (SELECT user_account_id FROM email_address)

             name
            -------
             jack
             ed
             wendy

    correlated subquery
    correlated subqueries
        A :term:`subquery` is correlated if it depends on data in the
        enclosing ``SELECT``.

        Below, a subquery selects the aggregate value ``MIN(a.id)``
        from the ``email_address`` table, such that
        it will be invoked for each value of ``user_account.id``, correlating
        the value of this column against the ``email_address.user_account_id``
        column:

        .. sourcecode:: sql

            SELECT user_account.name, email_address.email
             FROM user_account
             JOIN email_address ON user_account.id=email_address.user_account_id
             WHERE email_address.id = (
                SELECT MIN(a.id) FROM email_address AS a
                WHERE a.user_account_id=user_account.id
             )

        The above subquery refers to the ``user_account`` table, which is not itself
        in the ``FROM`` clause of this nested query.   Instead, the ``user_account``
        table is recieved from the enclosing query, where each row selected from
        ``user_account`` results in a distinct execution of the subquery.

        A correlated subquery is nearly always present in the :term:`WHERE clause`
        or :term:`columns clause` of the enclosing ``SELECT`` statement, and never
        in the :term:`FROM clause`; this is because
        the correlation can only proceed once the original source rows from the enclosing
        statement's FROM clause are available.


    IN
    IN operator
        A comparison operator.  Compares an expression against a list of
        values, and is true if it matches at least one of them.

        .. sourcecode:: sql

            SELECT email FROM email_address
            WHERE user_account_id IN (1, 2)


        A :term:`subquery` can be used in place of a literal list of values:

        .. sourcecode:: sql

            SELECT email FROM email_address
            WHERE user_account_id IN
            (SELECT id FROM user_account WHERE name='jack' OR name='ed')


    EXISTS
    EXISTS operator
        The EXISTS operator tests a subquery and returns true if the
        subquery returns any rows:

        .. sourcecode:: sql

            SELECT name FROM user_account
             WHERE EXISTS
             (SELECT * FROM email_address
                WHERE email_address.user_account_id=user_account.id)

             name
            -------
             jack
             ed
             wendy

        The columns selected by the subquery are ignored.  Only the
        number of rows are considered: no rows or at least one.
        ``EXISTS <subquery>`` is a :term:`scalar`, boolean expresion
        and can be used like any other boolean value in a WHERE clause:

        .. sourcecode:: sql

            SELECT name FROM user_account
              WHERE EXISTS (SELECT * FROM email_address WHERE email_address.user_account_id=user_account.id)
              AND name='ed'

             name
            ------
              ed

        The subquery used within an ``EXISTS`` expression is nearly always
        a :term:`correlated subquery`.


.. _glossary_sqlalchemy:

SQLAlchemy Core / Object Relational Terms
==========================================


.. glossary::
    :sorted:

    threadlocal
        A shared data structure whose data members are visible only to
        the thread which set them. The concept of "thread local" in
        Python is normally provided by the ``threading.local``
        construct.

        .. seealso::

            http://docs.python.org/2/library/threading.html#threading.local

    reflection
        The process of constructing SQLAlchemy :class:`~sqlalchemy.schema.Table`
        objects in an automated or semi-automated fashion, where information about
        tables, columns and constraints are loaded from an existing
        database's internal catalogs in order to compose in-memory
        structures representing a schema.

        .. seealso::

            :ref:`metadata_reflection`

    engine
        An object that provides a source of database connectivity.  The
        :class:`~sqlalchemy.engine.Engine` object maintains a :term:`connection pool`,
        which keeps track of a series of :term:`DBAPI` connection objects,
        as well as a :term:`dialect`, which keeps track of all the information known
        about the particular kind of database and Python driver being used
        by this particular engine.  An :class:`~sqlalchemy.engine.Engine`
        is created using the :func:`~sqlalchemy.create_engine`
        factory function, and a database connection can be requested
        from the :class:`~sqlalchemy.engine.Engine` using the
        :meth:`~sqlalchemy.engine.Engine.connect` method::

            >>> from sqlalchemy import create_engine
            >>> engine = create_engine("postgresql://scott:tiger@localhost/test")
            >>> connection = engine.connect()
            >>> connection.scalar("SELECT now()")
            datetime.datetime(2013, 2, 18, 18, 26, 37)
            >>> connection.close()

        While the above pattern illustrates a literal, rudimentary use of
        :class:`~sqlalchemy.engine.Engine`, it's normally used in a more
        abstracted way than the above.  When dealing with the SQLAlchemy
        ORM, the :class:`~sqlalchemy.engine.Engine` is usually :term:`bound`
        to an ORM :term:`session` object when the program starts,
        where it then remains hidden as a source of connectivity for that
        session.


        The primary facade for a database. An :class:`.Engine` manages a pool of
        database connections and provides methods to execute SQL
        statements and fetch result sets.

        .. seealso::

            :ref:`sqla:engines_toplevel` - in the SQLAlchemy documentation

            :ref:`sqla:connections_toplevel` - in the SQLAlchemy documentation

    flush
        The operation by which a :term:`session` emits INSERT, UPDATE
        and DELETE statements to the database in response to the accumulation
        of a series of in-memory changes to objects.  The flush
        operation is a key component of the :term:`unit of work` pattern,
        and is normally invoked before the :class:`~sqlalchemy.orm.session.Session`
        emits a new SELECT statement, as well as right before the
        :class:`~sqlalchemy.orm.session.Session` commits a transaction.

        .. seealso::

            :ref:`sqla:session_flushing` - in the SQLAlchemy documentation


    identity map
        A mapping between Python objects and their database identities.
        The identity map is a collection that's associated with an
        ORM :term:`session` object, and maintains a single instance
        of every database object keyed to its identity.   The advantage
        to this pattern is that all operations which occur for a particular
        database identity are transparently coordinated onto a single
        object instance.  When using an identity map in conjunction with
        an :term:`isolated` transaction, having a reference
        to an object that's known to have a particular primary key can
        be considered from a practical standpoint to be a
        proxy to the actual database row.

        .. seealso::

            Martin Fowler - Identity Map - http://martinfowler.com/eaaCatalog/identityMap.html


    instance
        Refers to an instantiated object, that is, the result of calling
        the constructor of a Python class.

        We use this term to specify that we are dealing with a stateful
        Python object, rather than the class.  Suppose we have a class
        called ``User``::

            class User(object):
                def __init__(self, name):
                    self.name = name

        The above Python code represents only the :term:`class` ``User``,
        and not an actual instance.  The instance refers to when we construct
        a ``User``, and in this case assign to it a ``.name`` :term:`attribute`::

            my_user = User('some user')

        The SQLAlchemy ORM deals heavily with user-defined classes and instances
        of those classes; therefore throughout its documentation as well
        as its source code, it's important that we keep straight
        whether we're dealing with a class or an instance of one.


    instrumentation
    instrumented
        Instrumentation refers to the process of augmenting the functionality
        and attribute set of a particular class.   Ideally, the
        behavior of an instrumented class should remain close to a regular
        class, except that additional behviors and features are
        made available.  The SQLAlchemy :term:`mapping` process,
        among other things, adds database-enabled :term:`descriptors`
        to a mapped
        class which each represent a particular database column
        or relationship to a related class.

    declarative
        An API included with the SQLAlchemy ORM that in modern usage
        serves as the primary system used to configure the ORM.
        The central idea of the declarative system is that one
        defines a class to be :term:`mapped`, and then applies to
        this class a series of directives which denote the :term:`table metadata`
        to be associated with this class, which establishes the table(s)
        and columns that this class will be associated with when the
        ORM performs queries.

        The declarative system provides a relatively concise
        and very extensible series of patterns allowing not
        just for basic class mapping, but also allowing
        the construction of repeatable
        and composable mapping patterns using custom base classes,
        abstract classes, and mixins.

        .. seealso::

            :ref:`ormtutorial_toplevel`

            :ref:`declarative_toplevel`

    mapped
    mapper
    mapping
        We say a class is "mapped" when it has been passed through the
        :func:`sqlalchemy.orm.mapper` function.   This process associates the
        class with a database table or other :term:`selectable`
        construct, so that instances of it can be persisted
        and loaded using a :term:`session` object.

        Modern usage of the SQLAlchemy ORM typically "maps" classes using
        the :term:`declarative` system, which provides a relatively concise
        and very extensible series of patterns allowing classes to be
        mapped.  The declarative system actually rides on top of the so-called
        :ref:`sqla:classical_mapping` system, which is more
        fundamental and less automated.   Early versions of SQLAlchemy
        only featured the classical mapping system.

    metadata
    table metadata
        A collection of related :class:`.Table` objects.  These objects
        collected together may define :class:`.ForeignKey` objects which refer
        to other tables as dependencies.   The full collection of tables can
        be created and dropped in a target database schema en masse.

        .. seealso::

            :ref:`sqla:metadata_toplevel` - in the SQLAlchemy documentation

    attribute
        In Python, a field of an instance or class.   Essentially, any time
        the "." operator is used to access a field from a parent record, you're
        dealing with attribute access.

        Below, the ``Car`` class has attributes ``color`` and ``model``::

            class Car(object):
                color = "green"
                model = "Dodge"

        and attributes are accessed using the "." operator::

            print("Color: %s" % Car.color)

        In SQLAlchemy, an ORM :term:`mapped` class is :term:`instrumented` using
        Python :term:`descriptors` to provide attributes that have
        additional behaviors used by the mapper, including that changes
        in value are detected and also that SQL load operations can
        transparently occur when they are first accessed (known as
        :term:`lazy loading`).


    descriptor
    descriptors
        In Python, a descriptor is an object attribute with “binding behavior” whose
        attribute access has been overridden by methods in the `descriptor protocol <http://docs.python.org/howto/descriptor.html>`_.
        Those methods are __get__(), __set__(), and __delete__(). If any of those methods are defined
        for an object, it is said to be a descriptor.

        In SQLAlchemy, descriptors are used heavily in order to provide attribute behavior
        on mapped classes.   When a class is mapped as such::

            class MyClass(Base):
                __tablename__ = 'foo'

                id = Column(Integer, primary_key=True)
                data = Column(String)

        The ``MyClass`` class will be :term:`mapped` when its definition
        is complete, at which point the ``id`` and ``data`` attributes,
        starting out as :class:`sqlalchemy.schema.Column` objects, will be replaced
        by the :term:`instrumentation` system with customized
        descriptor objects, providing special behavior for the
        ``__get__()``, ``__set__()`` and ``__delete__()`` methods.   The
        descriptors (for the curious, they are instances of
        :class:`sqlalchemy.orm.attributes.InstrumentedAttribute`, though this detail
        is generally transparent) will generate a SQL expression when used at the class level::

            >>> print MyClass.data == 5
            data = :data_1

        When used at the instance level, these descriptors help to keep
        track of changes to values, and also :term:`lazy load` unloaded values
        and collections from the database when the attribute is accessed.

    lazy load
    lazy loads
    lazy loading
        In object relational mapping, a "lazy load" refers to an
        attribute that does not contain its database-side value
        for some period of time, typically when the object is
        first loaded.  Instead, the attribute receives a
        *memoization* that causes it to go out to the database
        and load its data when it's first used.   Using this pattern,
        the complexity and time spent within object fetches can
        sometimes be reduced, in that
        attributes for related tables don't need to be addressed
        immediately.

        .. seealso::

            Martin Fowler - Lazy Load - http://martinfowler.com/eaaCatalog/lazyLoad.html

            :term:`N plus one problem`


    N plus one problem
        The N plus one problem is a common side effect of the
        :term:`lazy load` pattern, whereby an application wishes
        to iterate through a related attribute or collection on
        each member of a result set of objects, where that
        attribute or collection is set to be loaded via the lazy
        load pattern.   The net result is that a SELECT statement
        is emitted to load the initial result set of parent objects;
        then, as the application iterates through each member,
        an additional SELECT statement is emitted for each member
        in order to load the related attribute or collection for
        that member.  The end result is that for a result set of
        N parent objects, there will be N + 1 SELECT statements emitted.

        The N plus one problem is alleviated using :term:`eager loading`.

    DBAPI
        DBAPI is shorthand for the phrase "Python Database API
        Specification".  This is a widely used specification
        within Python to define common usage patterns for all
        database connection packages.   The DBAPI is a "low level"
        API which is typically the lowest level system used
        in a Python application to talk to a database.  SQLAlchemy's
        :term:`dialect` system is constructed around the
        operation of the DBAPI, providing individual dialect
        classes which service a specific DBAPI on top of a
        specific database engine; for example, the :func:`.create_engine`
        URL ``postgresql+psycopg2://@localhost/test``
        refers to the :mod:`psycopg2 <sqlalchemy.dialects.postgresql.psycopg2>`
        DBAPI/dialect combination, whereas the URL ``mysql+mysqldb://@localhost/test``
        refers to the :mod:`MySQL for Python <sqlalchemy.dialects.mysql.mysqldb>`
        DBAPI/dialect combination.

        .. seealso::

            PEP 249 - Python Database API Specification v2.0: http://www.python.org/dev/peps/pep-0249/


    unit of work
        This pattern is where the system transparently keeps
        track of changes to objects and periodically flushes all those
        pending changes out to the database. SQLAlchemy's Session
        implements this pattern fully in a manner similar to that of
        Hibernate.

        .. seealso::

            Martin Fowler - Unit of Work - http://martinfowler.com/eaaCatalog/unitOfWork.html

            :ref:`sqla:session_toplevel` - in the SQLAlchemy documentation

    autocommit
        This refers to a behavior whereby individual statements are
        automatically committed to the database after execution, essentially
        removing the need to explicitly demarcate the beginining and
        end of a transactional block.   Autocommit is something that
        can take place at many levels and in different ways; some databases
        will start an interactive SQL session with autocommit implicitly
        enabled, and others will not, requiring that the user invoke an
        explicit ``COMMIT`` statement in order to commit any changes.

        When using the Python :term:`DBAPI`, the ``connection`` object
        provided by DBAPI is always non-autocommitting by default;
        that is, the user must call ``connection.commit()`` in order
        for the effect of any statements to be committed.   Some DBAPIs
        offer "autocommit" options, but these are not standard.

        SQLAlchemy's take on autocommit is that operations which involve
        executing statements using the Core :class:`~sqla:sqlalchemy.engine.Engine`
        or :class:`~sqla:sqlalchemy.engine.Connection`
        objects are by default autocommitting if the statement represents
        one that modifies data.  If one wants to control the scope of these
        transactions explicitly, this control is readily
        available via the :meth:`~sqla:sqlalchemy.engine.Connection.begin`
        method.  The rationale here is that the Core can be expediently
        used in a "one-off" style for scripting without the need to
        deal with transaction demarcation if not needed.

        However, when using the ORM
        :class:`~sqla:sqlalchemy.orm.session.Session` object, the default
        in modern versions is that the :meth:`~sqla:sqlalchemy.orm.session.Session.commit`
        method must be called in order to commit the ongoing transaction.
        The rationale for this is so that the :term:`unit of work` pattern
        can be used most effectively, where it can safely autoflush data
        to the database automatically knowing that it's not implicitly
        permanent, as well as that the explicit commit step provides
        a clear boundary as to when the ORM-mapped objects should be
        expired so that they can re-load their state from the database.
        Ironically, the explicit commit pattern of the
        :class:`~sqla:sqlalchemy.orm.session.Session` ultimately allows
        for code that is *more* succinct than if autocommit were turned on,
        as without it, it's often the case that flushing and expiration
        must be handled manually.

    bind
    bound
        This term refers to the association of a connection-producing
        object, usually an :term:`engine`, with a query-producing object, which in
        modern usage is usually a :term:`session` object, and in
        less common usage a :term:`metadata` object.

        Most of SQLAlchemy's usage patterns involve dealing with
        objects that produce SQL queries to be emitted to a database.
        But it makes a distinction between these objects and objects
        that represent actual database connections, or a source
        of database connections.

        For example, we can create an ORM
        :class:`~sqlalchemy.orm.session.Session` object::

            >>> from sqlalchemy.orm import Session
            >>> session = Session()

        But if we try to execute a query with it, we'd get an
        error::

            >>> session.scalar("select current_timestamp")
            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
              File "/Users/classic/dev/sqlalchemy/lib/sqlalchemy/orm/session.py", line 921, in scalar
                clause, params=params, mapper=mapper, bind=bind, **kw).scalar()
              File "/Users/classic/dev/sqlalchemy/lib/sqlalchemy/orm/session.py", line 912, in execute
                bind = self.get_bind(mapper, clause=clause, **kw)
              File "/Users/classic/dev/sqlalchemy/lib/sqlalchemy/orm/session.py", line 1083, in get_bind
                ', '.join(context)))
            sqlalchemy.exc.UnboundExecutionError: Could not
                locate a bind configured on SQL expression or this Session

        This is because we haven't given this :class:`~sqlalchemy.orm.session.Session`
        a source of connectivity.   We can make one using
        :func:`~sqlalchemy.create_engine` and attaching it using ``.bind``::

            >>> from sqlalchemy import create_engine
            >>> engine = create_engine("sqlite://")
            >>> session.bind = engine
            >>> session.scalar("select current_timestamp")
            u'2013-02-18 21:13:31'

        Binding gets more elaborate than this, as a
        :class:`~sqlalchemy.orm.session.Session` can be bound to multiple
        databases at once; some use cases also involve binding
        the session directly to an individual connection object, rather than to
        an engine.   The practice of using binds with a Core :term:`metadata`
        object is also something seen commonly, though we've tried to discourage
        the use of this pattern as it tends to be overused and
        misunderstood.

    cascade
        The propagation of particular lifecycle events from one mapped
        instance to another, following along the paths formed
        by :term:`relationships` between mappings.

        An example of the most common cascade is the ``save-update``
        cascade, which states that if an object is associated with a
        parent, then that object should also be associated with the same
        :term:`session` as that parent::

            >>> from sqlalchemy.orm import Session
            >>> session = Session()
            >>> user_obj = User()
            >>> session.add(user_obj)
            >>> user_obj in session
            True
            >>> address_obj = Address()
            >>> user_obj.addresses.append(address_obj)
            >>> address_obj in session
            True

        Above, we associated an ``Address`` object with a
        parent ``User`` object by appending it to the mapped
        ``User.addresses`` collection.  As a result, that
        ``Address`` object became associated with the same
        :class:`~sqlalchemy.orm.session.Session` object
        as that of the ``User``.

        The behavior of cascades is customizable, but in most
        cases the default cascade of ``save-update`` remains
        in place.

        There are two optional cascades known as ``delete``
        and ``delete-orphan`` which are also very
        prominent.   These cascades add on the behavior that the
        child object should also be *deleted* when the parent
        object is deleted, and additionally that the child object
        should be deleted when detached from any parent.

        The concept of configurable cascade behavior was part
        of the SQLAlchemy ORM very early on and was inspired
        by the same configurability in the Hibernate
        ORM.

        .. seealso::

            :ref:`sqla:unitofwork_cascades` - in the SQLAlchemy documentation

            :ref:`sqla:tutorial_delete_cascade` - in the SQLAlchemy documentation


    collection
        In the SQLAlchemy ORM, this refers to a series of objects associated with
        a parent object, using a :term:`relationship` to manage
        these associations.   A collection corresponds to either a
        :term:`one to many` or :term:`many to many` relationship,
        and can be managed in Python by a variety of data types, the
        most common being the Python ``list()``, but also including the
        Python ``set()``, the Python ``dict()``, as well as any
        user-defined type which corresponds to certain interfaces.

        When starting out with the SQLAlchemy ORM, we generally stick
        to plain lists and sets for collections.  Dictionaries
        and custom-build collections are generally for more advanced
        usage patterns.

        .. seealso::

            :ref:`sqla:collections_toplevel` - advanced collection
            options,  in the SQLAlchemy documentation

    connection
        Refers to an active database handle.  The term "connection"
        can refer to different specific constructs; the most fundamental
        is the "connection" object provided by the Python :term:`DBAPI`.
        In SQLAlchemy, the DBAPI connection is normally maintained
        transparently behind a
        :term:`facade` known as the :class:`~sqlalchemy.engine.Connection`
        object.  This object is obtained from a :term:`engine` object,
        and has a one-to-one correspondence with a DBAPI connection.

        .. seealso::

            :ref:`sqla:engines_toplevel` - in the SQLAlchemy documentation

            :ref:`sqla:connections_toplevel` - in the SQLAlchemy documentation

    connection pool
        An object that maintains a series of :term:`connection` objects persistently
        in memory, allowing individual connections to be *checked out* by a particular
        application function, used for some period of time, and then *checked in*
        to the pool when usage of the connection is complete.

        The usage of connection pools in SQLAlchemy has two primary purposes:

        1. To reduce the latency involved in acquiring a database connection.
           By maintaining a series of connections in memory, the overhead of
           the TCP/IP connection as well as the initial negotiation of the
           client :term:`DBAPI` library with the backend database is incurred
           only a limited number of times, rather than for all distinct usages
           of a connection.

        2. To place a limit on the number of database connections a single
           Python process can use at once.  SQLAlchemy's default connection pool
           allows the specification of a *pool size* as well as *max overflow*
           parameters; the size indicates the largest number of connections
           that should be held in memory persistently, and the max overflow indicates
           an optional additional number of connections that may be temporarily
           procured on top of the base size.

        The SQLAlchemy :term:`engine` object maintains a reference to a connection
        pool where it retrieves and stores DBAPI connections - in most cases this
        pool is an instance of :class:`sqlalchemy.pool.QueuePool`.   Connection
        pooling can be disabled for a particular engine by replacing the pool
        implementation with the so-called :class:`sqlalchemy.pool.NullPool`,
        which has the same interface as a pool but doesn't actually maintain
        connections persistently.

        Note that SQLAlchemy's built-in pooling is only one style of pooling,
        known as *application level pooling*.  An architecture can also use
        *pool middleware*, i.e., a server that runs separately and mediates
        connectivity between one or more applications and a database backend.
        The `PgBouncer <http://wiki.postgresql.org/wiki/PgBouncer>`_ product
        is one such middleware service designed for usage with Postgresql.

        .. seealso::

            :ref:`pooling_toplevel`

    transient
        This describes one of the four major object states which
        an object can have within a :term:`session`; a transient object
        is a new object that doesn't have any database identity
        and has not been associated with a session yet.  When the
        object is added to the session, it moves to the
        :term:`pending` state.

        .. seealso::

            :ref:`sqla:session_object_states` - in the SQLAlchemy documentation

    pending
        This describes one of the four major object states which
        an object can have within a :term:`session`; a pending object
        is a new object that doesn't have any database identity,
        but has been recently associated with a session.   When
        the session emits a flush and the row is inserted, the
        object moves to the :term:`persistent` state.

        .. seealso::

            :ref:`sqla:session_object_states` - in the SQLAlchemy documentation

    persistent
        This describes one of the four major object states which
        an object can have within a :term:`session`; a persistent object
        is an object that has a database identity (i.e. a primary key)
        and is currently associated with a session.   Any object
        that was previously :term:`pending` and has now been inserted
        is in the persistent state, as is any object that's
        been loaded by the session from the database.   When a
        persistent object is removed from a session, it is known
        as :term:`detached`.

        .. seealso::

            :ref:`sqla:session_object_states` - in the SQLAlchemy documentation

    detached
        This describes one of the four major object states which
        an object can have within a :term:`session`; a detached object
        is an object that has a database identity (i.e. a primary key)
        but is not associated with any session.  An object that
        was previously :term:`persistent` and was removed from its
        session either because it was expunged, or the owning
        session was closed, moves into the detached state.
        The detached state is generally used when objects are being
        moved between sessions or when being moved to/from an external
        object cache.

        .. seealso::

            :ref:`sqla:session_object_states` - in the SQLAlchemy documentation

    one to many
        A style of :func:`~sqlalchemy.orm.relationship` which links
        the primary key of the parent mapper's table to the foreign
        key of a related table.   Each unique parent object can
        then refer to zero or more unique related objects.

        The related objects in turn will have an implicit or
        explicit :term:`many to one` relationship to their parent
        object.

        An example one to many schema (which, note, is identical
        to the :term:`many to one` schema):

        .. sourcecode:: sql

            CREATE TABLE department (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30)
            )

            CREATE TABLE employee (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30),
                dep_id INTEGER REFERENCES department(id)
            )

        The relationship from ``department`` to ``employee`` is
        one to many, since many employee records can be associated with a
        single department.  A SQLAlchemy mapping might look like::

            class Department(Base):
                __tablename__ = 'department'
                id = Column(Integer, primary_key=True)
                name = Column(String(30))
                employees = relationship("Employee")

            class Employee(Base):
                __tablename__ = 'employee'
                id = Column(Integer, primary_key=True)
                name = Column(String(30))
                dep_id = Column(Integer, ForeignKey('department.id'))

        .. seealso::

            :term:`relationship`

            :term:`many to one`

            :term:`backref`

    many to one
        A style of :func:`~sqlalchemy.orm.relationship` which links
        a foreign key in the parent mapper's table to the primary
        key of a related table.   Each parent object can
        then refer to exactly zero or one related object.

        The related objects in turn will have an implicit or
        explicit :term:`one to many` relationship to any number
        of parent objects that refer to them.

        An example many to one schema (which, note, is identical
        to the :term:`one to many` schema):

        .. sourcecode:: sql

            CREATE TABLE department (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30)
            )

            CREATE TABLE employee (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30),
                dep_id INTEGER REFERENCES department(id)
            )


        The relationship from ``employee`` to ``department`` is
        many to one, since many employee records can be associated with a
        single department.  A SQLAlchemy mapping might look like::

            class Department(Base):
                __tablename__ = 'department'
                id = Column(Integer, primary_key=True)
                name = Column(String(30))

            class Employee(Base):
                __tablename__ = 'employee'
                id = Column(Integer, primary_key=True)
                name = Column(String(30))
                dep_id = Column(Integer, ForeignKey('department.id'))
                department = relationship("Department")

        .. seealso::

            :term:`relationship`

            :term:`one to many`

            :term:`backref`

    backref
        An extension to the :term:`relationship` system whereby two
        distinct :func:`~sqlalchemy.orm.relationship` objects can be
        mutually associated with each other, such that they coordinate
        in memory as changes occur to either side.   The most common
        way these two relationships are constructed is by using
        the :func:`~sqlalchemy.orm.relationship` function explicitly
        for one side and specifying the ``backref`` keyword to it so that
        the other :func:`~sqlalchemy.orm.relationship` is created
        automatically.  We can illustrate this against the example we've
        used in :term:`one to many` as follows::

            class Department(Base):
                __tablename__ = 'department'
                id = Column(Integer, primary_key=True)
                name = Column(String(30))
                employees = relationship("Employee", backref="department")

            class Employee(Base):
                __tablename__ = 'employee'
                id = Column(Integer, primary_key=True)
                name = Column(String(30))
                dep_id = Column(Integer, ForeignKey('department.id'))

        A backref can be applied to any relationship, including one to many,
        many to one, and :term:`many to many`.

        .. seealso::

            :term:`relationship`

            :term:`one to many`

            :term:`many to one`

            :term:`many to many`

    many to many
        A style of :func:`sqlalchemy.orm.relationship` which links two tables together
        via an intermediary table in the middle.   Using this configuration,
        any number of rows on the left side may refer to any number of
        rows on the right, and vice versa.

        A schema where employees can be associated with projects:

        .. sourcecode:: sql

            CREATE TABLE employee (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30)
            )

            CREATE TABLE project (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30)
            )

            CREATE TABLE employee_project (
                employee_id INTEGER PRIMARY KEY,
                project_id INTEGER PRIMARY KEY,
                FOREIGN KEY employee_id REFERENCES employee(id),
                FOREIGN KEY project_id REFERENCES project(id)
            )

        Above, the ``employee_project`` table is the many-to-many table,
        which naturally forms a composite primary key consisting
        of the primary key from each related table.

        In SQLAlchemy, the :func:`sqlalchemy.orm.relationship` function
        can represent this style of relationship in a mostly
        transparent fashion, where the many-to-many table is
        specified using plain table metadata::

            class Employee(Base):
                __tablename__ = 'employee'

                id = Column(Integer, primary_key)
                name = Column(String(30))

                projects = relationship(
                    "Project",
                    secondary=Table('employee_project', Base.metadata,
                                Column("employee_id", Integer, ForeignKey('employee.id'),
                                            primary_key=True),
                                Column("project_id", Integer, ForeignKey('project.id'),
                                            primary_key=True)
                            ),
                    backref="employees"
                    )

            class Project(Base):
                __tablename__ = 'project'

                id = Column(Integer, primary_key)
                name = Column(String(30))

        Above, the ``Employee.projects`` and back-referencing ``Project.employees``
        collections are defined::

            proj = Project(name="Client A")

            emp1 = Employee(name="emp1")
            emp2 = Employee(name="emp2")

            proj.employees.extend([emp1, emp2])

        .. seealso::

            :term:`association relationship`

            :term:`relationship`

            :term:`one to many`

            :term:`many to one`

    association relationship
        A two-tiered :term:`relationship` which links two tables
        together using an association table in the middle.  The
        association relationship differs from a :term:`many to many`
        relationship in that the many-to-many table is mapped
        by a full class, rather than invisibly handled by the
        :func:`sqlalchemy.orm.relationship` construct as in the case
        with many-to-many, so that additional attributes are
        explicitly available.

        For example, if we wanted to associate employees with
        projects, also storing the specific role for that employee
        with the project, the relational schema might look like:

        .. sourcecode:: sql

            CREATE TABLE employee (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30)
            )

            CREATE TABLE project (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30)
            )

            CREATE TABLE employee_project (
                employee_id INTEGER PRIMARY KEY,
                project_id INTEGER PRIMARY KEY,
                role_name VARCHAR(30),
                FOREIGN KEY employee_id REFERENCES employee(id),
                FOREIGN KEY project_id REFERENCES project(id)
            )

        A SQLAlchemy declarative mapping for the above might look like::

            class Employee(Base):
                __tablename__ = 'employee'

                id = Column(Integer, primary_key)
                name = Column(String(30))


            class Project(Base):
                __tablename__ = 'project'

                id = Column(Integer, primary_key)
                name = Column(String(30))


            class EmployeeProject(Base):
                __tablename__ = 'employee_project'

                employee_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
                project_id = Column(Integer, ForeignKey('project.id'), primary_key=True)
                role_name = Column(String(30))

                project = relationship("Project", backref="project_employees")
                employee = relationship("Employee", backref="employee_projects")


        Employees can be added to a project given a role name::

            proj = Project(name="Client A")

            emp1 = Employee(name="emp1")
            emp2 = Employee(name="emp2")

            proj.project_employees.extend([
                EmployeeProject(employee=emp1, role="tech lead"),
                EmployeeProject(employee=emp2, role="account executive")
            ])

        .. seealso::

            :term:`many to many`


    relationship
    relationships
        A connecting unit between two mapped classes, corresponding
        to some relationship between the two tables in the database.

        The relationship is defined using the SQLAlchemy function
        :func:`~sqlalchemy.orm.relationship`.   Once created, SQLAlchemy
        inspects the arguments and underlying mappings involved
        in order to classify the relationship as one of three types:
        :term:`one to many`, :term:`many to one`, or :term:`many to many`.
        With this classification, the relationship construct
        handles the task of persisting the appropriate linkages
        in the database in response to in-memory object associations,
        as well as the job of loading object references and collections
        into memory based on the current linkages in the
        database.

        .. seealso::

            :ref:`sqla:relationship_config_toplevel` - in the SQLAlchemy documentation

    scoped session
        A helper object intended to provide a *registry* of
        :term:`session` objects, allowing an application to refer
        to the registry as a global variable which provides
        access to a contextually appropriate session object.

        The scoped session object is an optional construct
        often used with web applications.

        .. seealso::

            :term:`Session`

            :ref:`sqla:unitofwork_contextual` - an in-depth
            introduction to the :class:`sqlalchemy.orm.scoped_session` object,
            in the SQLAlchemy documentation


    selectable
        Refers to the SQLAlchemy analogue for a "relation" in relational
        algebra, which is any object that represents a series of
        rows in a database.   "Selectable"
        actually refers in the API to objects that extend from the
        :class:`sqlalchemy.sql.expression.Selectable` class, and
        refers to such row-representing constructs as the
        :class:`~sqlalchemy.schema.Table`, the :class:`~sqlalchemy.sql.expression.Join`,
        and the :class:`~sqlalchemy.sql.expression.Select`
        construct.

    Session
        The container or scope for ORM database operations. Sessions
        load instances from the database, track changes to mapped
        instances and persist changes in a single unit of work when
        flushed.

        .. seealso::

            :ref:`session_toplevel`

    sessionmaker
        A *factory* for :term:`session` objects.   The :class:`~sqlalchemy.orm.session.sessionmaker`
        construct basically allows a series of parameters to be associated
        with a :class:`~sqlalchemy.orm.session.Session` constructor.

        In reality, the sessionmaker is just slightly more elaborate
        than a simple function.  An expression like this::

            from sqlalchemy.orm import sessionmaker
            my_session = sessionmaker(bind=engine, autoflush=False)

        is conceptually very similar to the following::

            from sqlalchemy.orm import Session
            my_session = lambda: Session(bind=engine, autoflush=False)

        .. seealso::

            :term:`Session`

            :term:`scoped session`
