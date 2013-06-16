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
# Expressions produce different strings according to *dialect*
# objects.

expression = user_table.c.username == 'ed'

### slide:: i
# MySQL....
from sqlalchemy.dialects import mysql
print(expression.compile(dialect=mysql.dialect()))

### slide:: i
# PostgreSQL...
from sqlalchemy.dialects import postgresql
print(expression.compile(dialect=postgresql.dialect()))

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

### slide::
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

### slide:: i
# executing an insert() gives us the "last inserted id"
result.inserted_primary_key

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

### slide:: p
# select all columns from a table

select_stmt = select([user_table])
conn.execute(select_stmt).fetchall()

### slide:: p
# specify a WHERE clause

select_stmt = select([user_table]).\
                    where(
                        or_(
                            user_table.c.username == 'ed',
                            user_table.c.username == 'wendy'
                        )
                    )
conn.execute(select_stmt).fetchall()

### slide:: p
# specify multiple WHERE, will be joined by AND

select_stmt = select([user_table]).\
                    where(user_table.c.username == 'ed').\
                    where(user_table.c.fullname == 'ed jones')
conn.execute(select_stmt).fetchall()

### slide:: p
# ordering is applied using order_by()

select_stmt = select([user_table]).\
                    order_by(user_table.c.username)
print(conn.execute(select_stmt).fetchall())

### slide::
### title:: Exercises
# 1. use user_table.insert() and "r = conn.execute()" to emit this
# statement:
#
# INSERT INTO user (username, fullname) VALUES ('dilbert', 'Dilbert Jones')
#
# 2. What is the value of 'user.id' for the above INSERT statement?
#
# 3. Using "select([user_table])", execute this SELECT:
#
# SELECT id, username, fullname FROM user WHERE username = 'wendy' OR
#   username = 'dilbert' ORDER BY fullname
#
#

### slide:: p
### title:: Joins / Foreign Keys
# We create a new table to illustrate multi-table operations
from sqlalchemy import ForeignKey

address_table = Table("address", metadata,
                        Column('id', Integer, primary_key=True),
                        Column('user_id', Integer, ForeignKey('user.id'),
                                                            nullable=False),
                        Column('email_address', String(100), nullable=False)
                      )
metadata.create_all(engine)

### slide:: p
# data
conn.execute(address_table.insert(), [
    {"user_id": 1, "email_address": "ed@ed.com"},
    {"user_id": 1, "email_address": "ed@gmail.com"},
    {"user_id": 2, "email_address": "jack@yahoo.com"},
    {"user_id": 3, "email_address": "wendy@gmail.com"},
])

### slide::
# two Table objects can be joined using join()
#
# <left>.join(<right>, [<onclause>]).

join_obj = user_table.join(address_table,
                            user_table.c.id == address_table.c.user_id)
print(join_obj)

### slide::
# ForeignKey allows the join() to figure out the ON clause automatically

join_obj = user_table.join(address_table)
print(join_obj)

### slide:: pi
# to SELECT from a JOIN, use select_from()

select_stmt = select([user_table, address_table]).select_from(join_obj)
conn.execute(select_stmt).fetchall()

### slide::
# the select() object is a "selectable" just like Table.
# it has a .c. attribute also.

select_stmt = select([user_table]).where(user_table.c.username == 'ed')

print(
    select([select_stmt.c.username]).
        where(select_stmt.c.username == 'ed')
   )

### slide::
# In SQL, a "subquery" is usually an alias() of a select()

select_alias = select_stmt.alias()
print(
    select([select_alias.c.username]).
        where(select_alias.c.username == 'ed')
   )

### slide::
# A subquery against "address" counts addresses per user:

from sqlalchemy import func
address_subq = select([
                    address_table.c.user_id,
                    func.count(address_table.c.id).label('count')
                ]).\
                group_by(address_table.c.user_id).\
                alias()
print(address_subq)


### slide:: i
# we use join() to link the alias() with another select()

username_plus_count = select([
                            user_table.c.username,
                            address_subq.c.count
                        ]).select_from(
                            user_table.join(address_subq)
                         ).order_by(user_table.c.username)

### slide:: i

conn.execute(username_plus_count).fetchall()

### slide::
### title:: Exercises
# Produce this SELECT:
#
# SELECT fullname, email_address FROM user JOIN address
#   ON user.id = address.user_id WHERE username='ed'
#   ORDER BY email_address
#

### slide::
### title:: Scalar selects, updates, deletes
# a *scalar select* returns exactly one row and one column

address_sel = select([
                func.count(address_table.c.id)
                ]).\
                where(user_table.c.id == address_table.c.user_id)
print(address_sel)

### slide:: ip
# scalar selects can be used in column expressions,
# specify it using as_scalar()

select_stmt = select([user_table.c.username, address_sel.as_scalar()])
conn.execute(select_stmt).fetchall()

### slide:: p
# to round out INSERT and SELECT, this is an UPDATE

update_stmt = address_table.update().\
                    values(email_address="jack@msn.com").\
                    where(address_table.c.email_address == "jack@yahoo.com")

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

delete_stmt = address_table.delete().\
                where(address_table.c.email_address == "ed@ed.com")

result = conn.execute(delete_stmt)

### slide:: i
# UPDATE and DELETE have a "rowcount", number of rows matched
# by the WHERE clause.
result.rowcount


### slide::
### title:: Exercises
# 1. Execute this UPDATE - keep the "result" that's returned
#
#    UPDATE user SET fullname='Ed Jones' where username='ed'
#
# 2. how many rows did the above statement update?
#
# 3. Tricky bonus!  Combine update() along with select().as_scalar()
#    to execute this UPDATE:
#
#    UPDATE user SET fullname=fullname ||
#        (select email_address FROM address WHERE user_id=user.id)
#       WHERE username IN ('jack', 'wendy')
#

### slide::
