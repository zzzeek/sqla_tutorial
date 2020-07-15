### slide:: s
import os
from sqlalchemy import create_engine
from sqlalchemy import text

if os.path.exists("some.db"):
    os.remove("some.db")
e = create_engine("sqlite:///some.db")
with e.begin() as conn:
    conn.execute(
        text(
            """
        create table employee (
            emp_id integer primary key,
            emp_name varchar
        )
    """
        )
    )

    conn.execute(
        text(
            """
        create table employee_of_month (
            emp_id integer primary key,
            emp_name varchar
        )
    """
        )
    )

    conn.execute(
        text("insert into employee(emp_name) values (:name)"),
        [{"name": "spongebob"}, {"name": "sandy"}, {"name": "squidward"}],
    )


### slide::
### title:: Engine Basics
# create_engine() builds a *factory* for database connections.
# Below we create an engine that will connect to a SQLite database.

from sqlalchemy import create_engine

engine = create_engine("sqlite:///some.db")


### slide::
# So that we can show off some 2.0 features, we will make a second
# engine against the same database

future_engine = create_engine("sqlite:///some.db", future=True)


### slide::
# The Engine doesn't actually connect until we tell it to for the first
# time.  When using it directly, we get a connection using the .connect()
# method.

connection = engine.connect()
connection

### slide::
# The Connection is a so-called **proxy** for a DBAPI connection.  We can
# see it by peeking at the .connection attribute, then .connection again

connection.connection.connection

### slide:: p

# The Connection then features an .execute() method that will run queries.
# To invoke a textual query we use the text() construct

from sqlalchemy import text

stmt = text("select emp_id, emp_name from employee where emp_id=:emp_id")
result = connection.execute(stmt, {"emp_id": 2})

### slide::
# the result object we get back is similar to a cursor, and features methods
# like fetchone(), fetchall()
row = result.fetchone()

### slide:: i
# the row looks and acts mostly like a named tuple
row
row[1]
row.emp_name

### slide::
# it also has a dictionary interface, however this is moving...
row["emp_name"]

### slide:: i
# in SQLAlchemy 1.4, the "dictionary" view is available via ._mapping
row._mapping["emp_name"]

### slide:: i
# folks usually use the named tuple interface in any case
row.emp_name

### slide::
### title:: our first 1.3 -> 1.4 "future" migration note
# the dictionary thing is special because it implies the behavior of
# "contains", e.g. "elem in collection".    In 1.3, "row" acts like a dictionary

row
row.keys()
"emp_name" in row
"sandy" in row

### slide:: i
# in 1.4 future / 2.0 it acts like a tuple
with future_engine.connect() as future_conn:
    row = future_conn.execute(stmt, {"emp_id": 2}).first()

"emp_name" in row
"sandy" in row


### slide::
# results close automatically when all rows are exhausted, but we can
# also close explicitly.
result.close()

### slide:: p
# result objects can also be iterated

result = connection.execute(text("select * from employee"))
for row in result:
    print(row)

### slide:: p
# and there are methods like fetchall()
result = connection.execute(text("select * from employee"))
result.fetchall()

### slide:: p
# in 1.4 there are fancier methods too
result = connection.execute(text("select * from employee"))
result.scalars("emp_name").all()

### slide::
# Connection has a .close() method.  This **releases** the
# DBAPI connection back to the connection pool.  This may or
# may not actually close the DBAPI connection.
connection.close()

### slide::
# however it is preferred to use context managers to manage the connect/
# release process

with engine.connect() as connection:
    connection.execute(text("select * from employee")).all()

    # releases connection back to the pool


### slide:: p
### title:: transactions, committing and autocommit
# In 1.x SQLAlchemy versions, statements like INSERT statements, even
# when they are passed as plain strings, are subject to autocommit
# behavior.

connection = engine.connect()
connection.execute(
    text("insert into employee_of_month (emp_name) values (:emp_name)"),
    {"emp_name": "spongebob"},
)


### slide:: p
# In 2.0, this autocommit is removed.   There is instead a local
# .commit() method for commit-as-you-go style use.

with future_engine.connect() as future_connection:
    future_connection.execute(
        text("insert into employee_of_month (emp_name) values (:emp_name)"),
        {"emp_name": "sandy"},
    )
    future_connection.commit()


### slide:: p
# To explicitly demarcate begin/commit, the most idiomatic way is to use the
# .begin() method of Engine which returns a context manager that yields
# the connection

with engine.begin() as connection:
    connection.execute(
        text("insert into employee_of_month (emp_name) values (:emp_name)"),
        {"emp_name": "squidward"},
    )
    # commits transaction, releases connection back to the connection pool.
    # rolls back if there is an exception before re-throwing


### slide:: p
# You can also explicitly begin() from the Connection, returning a
# Transaction object which supports rollback and commit

with engine.connect() as connection:
    trans = connection.begin()
    connection.execute(
        text("insert into employee (emp_name) values (:emp_name)"),
        {"emp_name": "patrick"},
    )
    trans.commit()
    trans = connection.begin()
    connection.execute(
        text("update employee_of_month set emp_name = :emp_name"),
        {"emp_name": "patrick"},
    )
    trans.rollback()  # sorry patrick

### slide:: p
# The Transaction also supports context manager use which is
# much easier to use.  rollback is called automatically if an exception
# is raised

with engine.connect() as connection:
    with connection.begin() as trans:
        connection.execute(
            text("update employee_of_month set emp_name = :emp_name"),
            {"emp_name": "squidward"},
        )
        # commits transaction, or rollback if exception
    # closes connection


### slide:: p
# transactions support "nesting", which is implemented using the
# SAVEPOINT construct.

with engine.connect() as connection:
    with connection.begin() as trans:
        savepoint = connection.begin_nested()
        connection.execute(
            text("update employee_of_month set emp_name = :emp_name"),
            {"emp_name": "patrick"},
        )
        savepoint.rollback()  # sorry patrick

        with connection.begin_nested() as savepoint:
            connection.execute(
                text("update employee_of_month set emp_name = :emp_name"),
                {"emp_name": "spongebob"},
            )
            # releases savepoint

        # commits transaction, or rollback if exception
    # closes connection

### slide::
### title:: Questions?

### slide::
