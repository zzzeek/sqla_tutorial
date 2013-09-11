### slide::
### title:: SQL Expression Language
# We begin with a Table object
from sqlalchemy import MetaData, Table, Column, String, Integer

metadata = MetaData()
user_table = Table('user', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('username', String(50)),
                    Column('fullname', String(50))
                   )

### slide:: p
# new SQLite database and generate the table.

from sqlalchemy import create_engine
engine = create_engine("sqlite://")
metadata.create_all(engine)

### slide::
# as we saw earlier, Table has a collection of Column objects,
# which we can access via table.c.<columnname>

user_table.c.username

### slide::
# Column is part of a class known as "ColumnElement",
# which exhibit custom Python expression behavior.

user_table.c.username == 'ed'

### slide:: i
# They become SQL when evaluated as a string.
str(user_table.c.username == 'ed')

### slide::
# ColumnElements can be further combined to produce more ColumnElements

print(
    (user_table.c.username == 'ed') | (user_table.c.username == 'jack')
    )

### slide::
# OR and AND are available with |, &, or or_() and and_()

from sqlalchemy import and_, or_

print(
    and_(
        user_table.c.fullname == 'ed jones',
            or_(
                user_table.c.username == 'ed',
                user_table.c.username == 'jack'
            )
        )
    )

### slide::
# comparison operators

print(user_table.c.id > 5)

### slide::
# Compare to None produces IS NULL

print(user_table.c.fullname == None)

### slide::
# "+" might mean "addition"....

print(user_table.c.id + 5)

### slide:: i
# ...or might mean "string concatenation"

print(user_table.c.fullname + "some name")

### slide::
# an IN

print(user_table.c.username.in_(["wendy", "mary", "ed"]))

### slide::
# The "bound" placeholders take the place of literal values,
# which are stored away for use when the statement is executed.

expression = user_table.c.username == 'ed'
print(expression)

### slide:: l
# Expressions produce different strings according to *dialect*
# objects.

expression = user_table.c.fullname + "some name"

### slide:: i
# PostgreSQL...
from sqlalchemy.dialects import postgresql
print(expression.compile(dialect=postgresql.dialect()))

### slide:: i
# MySQL....
from sqlalchemy.dialects import mysql
print(expression.compile(dialect=mysql.dialect()))

### slide::
# the Compiled object also converts literal values to "bound"
# parameters.

compiled = expression.compile()
compiled.params

### slide::
# The "bound" parameters are extracted when we execute()

engine.execute(
        user_table.select().where(user_table.c.username == 'ed')
    )

### slide:: l
### title:: Exercises
# Produce these expressions using "user_table.c.fullname",
# "user_table.c.id", and "user_table.c.username":
#
# 1. user.fullname = 'ed'
#
# 2. user.fullname = 'ed' AND user.id > 5
#
# 3. user.username = 'edward' OR (user.fullname = 'ed' AND user.id > 5)
#


### slide:: p
# we can insert data using the insert() construct

insert_stmt = user_table.insert().values(username='ed', fullname='Ed Jones')

conn = engine.connect()
result = conn.execute(insert_stmt)

### slide:: p
# insert() and other DML can run multiple parameters at once.

conn.execute(user_table.insert(), [
    {'username': 'jack', 'fullname': 'Jack Burger'},
    {'username': 'wendy', 'fullname': 'Wendy Weathersmith'}
])

### slide:: p
# select() is used to produce any SELECT statement.

from sqlalchemy import select
select_stmt = select([user_table.c.username, user_table.c.fullname]).\
            where(user_table.c.username == 'ed')
result = conn.execute(select_stmt)
for row in result:
    print(row)

### slide:: lp
# select all columns from a table

select_stmt = select([user_table])
conn.execute(select_stmt).fetchall()

### slide:: lp
# specify a WHERE clause

select_stmt = select([user_table]).\
                    where(
                        or_(
                            user_table.c.username == 'ed',
                            user_table.c.username == 'wendy'
                        )
                    )
conn.execute(select_stmt).fetchall()

### slide:: lp
# specify multiple WHERE, will be joined by AND

select_stmt = select([user_table]).\
                    where(user_table.c.username == 'ed').\
                    where(user_table.c.fullname == 'ed jones')
conn.execute(select_stmt).fetchall()


### slide:: l
### title:: Exercises
# 1. use user_table.insert() and "r = conn.execute()" to emit this
# statement:
#
# INSERT INTO user (username, fullname) VALUES ('dilbert', 'Dilbert Jones')
#
# 2. Using "select([user_table])", execute this SELECT:
#
# SELECT id, username, fullname FROM user WHERE username = 'wendy' OR
#   username = 'dilbert'
#
#

### slide:: p
# to round out INSERT and SELECT, this is an UPDATE

update_stmt = user_table.update().\
                    values(fullname="Jack Brown").\
                    where(user_table.c.username == "jack")

result = conn.execute(update_stmt)

### slide:: p
# an UPDATE can also use expressions based on other columns

update_stmt = user_table.update().\
                    values(fullname=user_table.c.username +
                            " " + user_table.c.fullname)

result = conn.execute(update_stmt)

### slide:: i
conn.execute(select([user_table])).fetchall()

### slide:: p
# and this is a DELETE

delete_stmt = user_table.delete().\
                where(user_table.c.username == 'jack')

result = conn.execute(delete_stmt)

### slide:: l
### title:: Exercises
# 1. Execute this UPDATE - keep the "result" that's returned by
#    conn.execute() (e.g. result = conn.execute(stmt))
#
#    UPDATE user SET fullname='Ed Jones' WHERE username='ed'
#
# 2. Examine result.rowcount, which will show how many rows were matched
#
# 3. delete the row with this statement:
#
#    DELETE FROM user WHERE username='ed'
#

### slide::
