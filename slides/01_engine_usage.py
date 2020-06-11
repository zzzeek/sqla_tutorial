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
        [{"name": "squidward"}, {"name": "spongebob"}, {"name": "sandy"}],
    )


### slide::
### title:: Engine Basics
# create_engine() builds a *factory* for database connections.
# Below we create an engine that will connect to a SQLite database.

from sqlalchemy import create_engine

engine = create_engine("sqlite:///some.db")

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

result = connection.execute(
    text("select emp_id, emp_name from employee where emp_id=:emp_id"),
    {"emp_id": 3}
)

### slide::
# the result object we get back is similar to a cursor, and features methods
# like fetchone(), fetchall()
row = result.fetchone()

### slide:: i
# the row looks and acts mostly like a tuple
row
row[1]

### slide:: i
# but also acts like a dictionary (deprecated version)
row["emp_name"]

### slide:: i
# in SQLAlchemy 1.4, the "dictionary" view is available via ._mapping
row._mapping["emp_name"]


### slide::
# results close automatically when all rows are exhausted, but we can
# also close explicitly.
result.close()

### slide:: p
# result objects can also be iterated

result = engine.execute("select * from employee")
for row in result:
    print(row)

### slide:: p
# the fetchall() method is a shortcut to producing a list
# of all rows.
result = engine.execute("select * from employee")
print(result.fetchall())

### slide:: p
# The execute() method of Engine will *autocommit*
# statements like INSERT by default.

engine.execute(
    "insert into employee_of_month (emp_name) values (:emp_name)",
    emp_name="fred",
)

### slide:: p
# We can control the scope of connection using connect().

conn = engine.connect()
result = conn.execute("select * from employee")
result.fetchall()
conn.close()

### slide:: p
# to run several statements inside a transaction, Connection
# features a begin() method that returns a Transaction.

conn = engine.connect()
trans = conn.begin()
conn.execute(
    "insert into employee (emp_name) values (:emp_name)", emp_name="wendy"
)
conn.execute(
    "update employee_of_month set emp_name = :emp_name", emp_name="wendy"
)
trans.commit()
conn.close()

### slide:: p
# a context manager is supplied to streamline this process.

with engine.begin() as conn:
    conn.execute(
        "insert into employee (emp_name) values (:emp_name)", emp_name="mary"
    )
    conn.execute(
        "update employee_of_month set emp_name = :emp_name", emp_name="mary"
    )


### slide:: l
### title:: Exercises
# Assuming this table:
#
#     CREATE TABLE employee (
#         emp_id INTEGER PRIMARY KEY,
#         emp_name VARCHAR(30)
#     }
#
# And using the "engine.execute()" method to invoke a statement:
#
# 1. Execute an INSERT statement that will insert the row with emp_name='dilbert'.
#    The primary key column can be omitted so that it is generated automatically.
#
# 2. SELECT all rows from the employee table.
#

### slide::
