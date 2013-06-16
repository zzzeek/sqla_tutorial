### slide:: s
from sqlalchemy import create_engine
import os

if os.path.exists("some.db"):
    os.remove("some.db")
e = create_engine("sqlite:///some.db")
e.execute("""
    create table employee (
        emp_id integer primary key,
        emp_name varchar
    )
""")

e.execute("""
    create table employee_of_month (
        emp_id integer primary key,
        emp_name varchar
    )
""")

e.execute("""insert into employee(emp_name) values ('ed')""")
e.execute("""insert into employee(emp_name) values ('jack')""")
e.execute("""insert into employee(emp_name) values ('fred')""")

### slide::
### title:: Engine Basics
# create_engine() builds a *factory* for database connections.

from sqlalchemy import create_engine

engine = create_engine("sqlite:///some.db")

### slide:: p
# Engine features an *execute()* method that will run a query on
# a connection for us.

result = engine.execute(
                 "select emp_id, emp_name from "
                 "employee where emp_id=:emp_id",
                 emp_id=3)

### slide::
# the result object we get back features methods like fetchone(),
# fetchall()
row = result.fetchone()

### slide:: i
# the row looks like a tuple
row

### slide:: i
# but also acts like a dictionary
row['emp_name']

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

engine.execute("insert into employee_of_month (emp_name) values (:emp_name)",
                    emp_name='fred')

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
conn.execute("insert into employee (emp_name) values (:emp_name)", emp_name="wendy")
conn.execute("update employee_of_month set emp_name = :emp_name", emp_name="wendy")
trans.commit()
conn.close()

### slide:: p
# a context manager is supplied to streamline this process.

with engine.begin() as conn:
    conn.execute("insert into employee (emp_name) values (:emp_name)", emp_name="mary")
    conn.execute("update employee_of_month set emp_name = :emp_name", emp_name="mary")


### slide::
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
