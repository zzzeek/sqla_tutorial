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
# "future" means we want the full 2.0 behavior.

from sqlalchemy import create_engine

engine = create_engine("sqlite:///some.db", future=True)


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
# the result object we get back is similar to a cursor, with more methods,
# such as first() which will return the first row and close the result set
row = result.first()

### slide:: i
# the row looks and acts mostly like a named tuple
row
row[1]
row.emp_name

### slide::
# it also has a dictionary interface, which is available via an accessor
# call .mapping
row._mapping["emp_name"]

### slide:: i
# folks usually use the named tuple interface in any case
row.emp_name


### slide:: p
# result objects can also be iterated

result = connection.execute(text("select * from employee"))
for row in result:
    print(row)

### slide:: p
# and there are methods like all()
result = connection.execute(text("select * from employee"))
result.all()

### slide:: p
# there are also column-selection methods like scalars()
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
    rpws = connection.execute(text("select * from employee")).all()

    # releases connection back to the pool


### slide:: p
### title:: transactions, committing

# Unlike previous SQLAlchemy versoins, SQLAlchemy 2.0 has no concept
# of "library level" autocommit; which means, if the DBAPI driver is in
# a transaction, SQLAlchemy will never commit it automatically.   The usual
# way to commit is called "commit as you go"

with engine.connect() as connection:
    connection.execute(
        text("insert into employee_of_month (emp_name) values (:emp_name)"),
        {"emp_name": "sandy"},
    )
    connection.commit()


### slide:: p
# the other way is called "begin once", when you just have a single transaction
# to commit

with engine.begin() as connection:
    connection.execute(
        text("insert into employee_of_month (emp_name) values (:emp_name)"),
        {"emp_name": "squidward"},
    )
    # commits transaction, releases connection back to the connection pool.
    # rolls back if there is an exception before re-throwing


### slide:: p
# You can also use begin() blocks local to the connection
#
with engine.connect() as connection:
    with connection.begin():
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
    with connection.begin():
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

### slide:: p
# most DBAPIs support autocommit now, which is why SQLAlchemy no longer
# does.  To use driver level autocommit, use execution options:

with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
    connection.execute(
        text("insert into employee(emp_name) values (:name)"),
        {"name": "plankton"},
    )

### slide:: pi
# the data was autocommitted
with engine.connect() as connection:
    planktons_id = connection.execute(
        text("select emp_id from employee where emp_name=:name"),
        {"name": "plankton"}
    ).scalar()
    print(planktons_id)

### slide::
### title:: Questions?

### slide::
