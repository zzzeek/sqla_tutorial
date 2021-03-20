### slide::
### title:: SQL Expression Language
# We begin with a Table object
from sqlalchemy import MetaData, Table, Column, String, Integer
from sqlalchemy import select

metadata = MetaData()
user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50)),
    Column("fullname", String(50)),
)

### slide:: p
# new SQLite database and generate the table.

from sqlalchemy import create_engine

engine = create_engine("sqlite://")
with engine.begin() as conn:
    metadata.create_all(conn)

### slide::
# as we saw earlier, Table has a collection of Column objects,
# which we can access via table.c.<columnname>

user_table.c.username

### slide::
# Column is part of a class known as "ColumnElement",
# which exhibit custom Python expression behavior.

user_table.c.username == "spongebob"

### slide::
# They are objects that can be **compiled** into a SQL string.   This
# process occurs when they are part of a statement to be executed.  It
# also can be viewed for debugging purposes by calling str() on the object.
str(user_table.c.username == "spongebob")

### slide:: i
# as we view these column expressions, keep in mind that literal values
# like "spongebob" above are converted into **bound parameters*.  They
# are not as visible but are not lost

(user_table.c.username == "spongebob").compile().params


### slide::
# ColumnElements can be further combined to produce more ColumnElements

print(
    (user_table.c.username == "spongebob")
    | (user_table.c.username == "patrick")
)

### slide::
# OR and AND are available with |, &, or or_() and and_()

from sqlalchemy import and_, or_

print(
    and_(
        user_table.c.fullname == "spongebob squarepants",
        or_(
            user_table.c.username == "spongebob",
            user_table.c.username == "patrick",
        ),
    )
)

### slide::
### title:: More Operators

# comparison operators

print(user_table.c.id > 5)

### slide:: i
# Compare to None produces IS NULL / IS NOT NULL

print(user_table.c.fullname == None)
print(user_table.c.fullname != None)

### slide::
# Operators may also be type sensitive.
# "+" with numbers means "addition"....

print(user_table.c.id + 5)

### slide:: i
# ...with strings it means "string concatenation"

print(user_table.c.fullname + " Jr.")

### slide::
# the IN operator will dynamically calculate bound parameter holders
# at compile time.

with engine.connect() as connection:
    connection.execute(
        select(
            user_table.c.username.in_(["sandy", "squidward", "spongebob"])
        )
    ).all()

### slide:: p
# "empty sets" for IN are available as well, which makes use of special
# subqueries to provide a server-side "empty set"

with engine.connect() as connection:
    connection.execute(
        select(
            user_table.c.username.in_([])
        )
    ).all()


### slide:: p
# we can insert data using the insert() construct

insert_stmt = user_table.insert().values(
    username="spongebob", fullname="Spongebob Squarepants"
)

with engine.begin() as connection:
    connection.execute(insert_stmt)

### slide:: p
# insert() and update() against plain Python values normally generate their
# VALUES/SET clauses from the list of parameters that are passed to execute().

with engine.begin() as connection:
    connection.execute(
        user_table.insert(), {"username": "sandy", "fullname": "Sandy Cheeks"}
    )

    # this format also accepts an "executemany" style that the DBAPI can optimize
    connection.execute(
        user_table.insert(),
        [
            {"username": "patrick", "fullname": "Patrick Star"},
            {"username": "squidward", "fullname": "Squidward Tentacles"},
        ],
    )

### slide:: p
# select() is used to produce any SELECT statement.

from sqlalchemy import select

select_stmt = select(user_table.c.username, user_table.c.fullname).where(
    user_table.c.username == "spongebob"
)
connection = engine.connect()

result = connection.execute(select_stmt)
for row in result:
    print(row)

### slide:: lp
# select all columns from a table

select_stmt = select(user_table)
connection.execute(select_stmt).all()

### slide:: lp
# specify WHERE and ORDER BY

select_stmt = select(user_table).where(
    or_(
        user_table.c.username == "spongebob",
        user_table.c.username == "sandy",
    )
).order_by(user_table.c.username)
connection.execute(select_stmt).all()

### slide:: lp
# specify multiple WHERE, will be joined by AND

select_stmt = (
    select(user_table)
    .where(user_table.c.username == "spongebob")
    .where(user_table.c.fullname == "Spongebob Squarepants")
    .order_by(user_table.c.username)
)
connection.execute(select_stmt).all()


### slide:: p
# More Result methods.   In the engine chapter, we were introduced to
# .all() and .first().   Result also has most of what
# previously was only in the ORM, such as the .one() and .one_or_none()
# methods.

# the one() method returns exactly one row
result = connection.execute(
    select(user_table.c.fullname).where(user_table.c.username == 'spongebob')
)
result.one()

### slide:: pi
# if there are no rows, or many rows, it raises an error.
result = connection.execute(
    select(user_table.c.fullname).order_by(user_table.c.username)
)
result.one()

### slide:: p
# one_or_none() will only raise if there are more than one row, but
# returns None for no result
result = connection.execute(
    select(user_table).where(user_table.c.username == 'nonexistent')
)
result.one_or_none()

### slide:: p
# result objects now support slicing at the result level.   We can SELECT
# some rows, and change the ordering and/or presence of columns after the
# fact using the .columns() method:

result = connection.execute(
    select(user_table).order_by(user_table.c.username)
)
for fullname, username in result.columns("fullname", "username"):
    print(f"{fullname} {username}")

### slide:: p
# a single column from the results can be delivered without using
# rows by applying the .scalars() modifier.   This accepts an optional
# column name, or otherwise assumes the first column:

result = connection.execute(
    select(user_table).order_by(user_table.c.username)
)
for fullname in result.scalars("fullname"):
    print(fullname)


### slide:: p
# an UPDATE, invoked with implicit "SET" clause

update_stmt = (
    user_table.update()
    .where(user_table.c.username == "patrick")
)

result = connection.execute(update_stmt, {"fullname": "Patrick Star"})

### slide:: p
# update() uses the .values() method to explicitly indicate the SET clause.
# It supports SQL expressions as well

update_stmt = user_table.update().values(
    fullname=user_table.c.username + " " + user_table.c.fullname
)

result = connection.execute(update_stmt)

### slide:: p
# and this is a DELETE

delete_stmt = user_table.delete().where(user_table.c.username == "patrick")

result = connection.execute(delete_stmt)


### slide::
### title:: Questions?

### slide::
