### slide::
### title:: Core Joins / Foreign Keys / Subqueries
# We start with two tables this time.
from sqlalchemy import MetaData, Table, Column, String, Integer, select

metadata = MetaData()
user_table = Table('user', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('username', String(50)),
                    Column('fullname', String(50))
                   )

### slide::
# Then a second table to illustrate multi-table operations
from sqlalchemy import ForeignKey

address_table = Table("address", metadata,
                        Column('id', Integer, primary_key=True),
                        Column('user_id', Integer, ForeignKey('user.id'),
                                                            nullable=False),
                        Column('email_address', String(100), nullable=False)
                      )


### slide:: p
# new SQLite database and generate both.

from sqlalchemy import create_engine
engine = create_engine("sqlite://")
metadata.create_all(engine)


### slide:: p
# insert data

conn = engine.connect()

conn.execute(user_table.insert(), [
    {'username': 'ed', 'fullname': 'Ed Jones'},
    {'username': 'jack', 'fullname': 'Jack Burger'},
    {'username': 'wendy', 'fullname': 'Wendy Weathersmith'}
])

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

### slide:: l
### title:: Exercises
# Produce this SELECT:
#
# SELECT fullname, email_address FROM user JOIN address
#   ON user.id = address.user_id WHERE username='ed'
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


### slide:: l
### title:: Exercises
# Using user_table.update() in conjunction with select().as_scalar(),
# construct and execute this UPDATE:
#
#    UPDATE user SET fullname=fullname ||
#        (select email_address FROM address WHERE user_id=user.id)
#       WHERE username IN ('jack', 'wendy')
#
# Hints:
#
# 1. First construct the "select" statement, assign it to a variable,
#    then use that variable in a second statement representing the UPDATE.
#
# 2. The "values" method of update() takes keyword column names,
#    e.g. upd.values(fullname = <expression>)
#
# 3. to concatenate string values, use +, e.g. user_table.c.fullname + my_scalar_select
#
# 4. use user_table.c.username.in_() to produce the IN expression
#
### slide::
