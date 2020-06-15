### slide::
### title:: Joins / Foreign Keys / Subqueries / CTEs
# create the same table as we used earlier..

from sqlalchemy import MetaData, Table, Column
from sqlalchemy import String, Integer

metadata = MetaData()
user_table = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50)),
    Column("fullname", String(50)),
)

### slide::
# Then a second table to illustrate multi-table operations
from sqlalchemy import ForeignKey

address_table = Table(
    "address",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user.id"), nullable=False),
    Column("email_address", String(100), nullable=False),
)


### slide:: p
# new SQLite database and generate both.

from sqlalchemy import create_engine

engine = create_engine("sqlite://")
with engine.begin() as conn:
    metadata.create_all(conn)


### slide:: p
# insert data

with engine.begin() as connection:
    connection.execute(
        user_table.insert(),
        [
            {
                "user_id": 1,
                "username": "spongebob",
                "fullname": "Spongebob Squarepants",
            },
            {"user_id": 2, "username": "sandy", "fullname": "Sandy Cheeks"},
            {"user_id": 3, "username": "patrick", "fullname": "Patrick Star"},
        ],
    )

    connection.execute(
        address_table.insert(),
        [
            {"user_id": 1, "email_address": "spongebob@spongebob.com"},
            {"user_id": 1, "email_address": "spongebob@gmail.com"},
            {"user_id": 2, "email_address": "sandy@yahoo.com"},
            {"user_id": 3, "email_address": "patrick@gmail.com"},
        ],
    )

### slide::
# we will show off more capabilities of select(), but also
# some new capabilities for 1.4 / 2.0

from sqlalchemy import select
from sqlalchemy.future import select as future_select

connection = engine.connect()

### slide::
# two Table objects can be joined using join()
#
# <left>.join(<right>, [<onclause>]).

join_obj = user_table.join(
    address_table, user_table.c.id == address_table.c.user_id
)
print(join_obj)

### slide:: i
# ForeignKey allows the join() to figure out the ON clause automatically

join_obj = user_table.join(address_table)
print(join_obj)

### slide:: p
# to SELECT from a JOIN, use select_from()

select_stmt = select(
    [user_table.c.username, address_table.c.email_address]
).select_from(join_obj)
connection.execute(select_stmt).fetchall()

### slide:: p
# the new version of select makes this simpler, we can use
# the .join() method of select.  note also we pass the
# column arguments positionally


select_stmt = future_select(
    user_table.c.username, address_table.c.email_address
).join(address_table)
connection.execute(select_stmt).fetchall()

### slide:: p
# in order to refer to the same table mutiple times in the FROM clause,
# the .alias() construct will create an alias of a table.
address_alias_1 = address_table.alias()
address_alias_2 = address_table.alias()

select_stmt = (
    select(
        [
            user_table.c.username,
            address_alias_1.c.email_address,
            address_alias_2.c.email_address,
        ]
    )
    .select_from(user_table.join(address_alias_1).join(address_alias_2))
    .where(address_alias_1.c.email_address == "spongebob@spongebob.com")
    .where(address_alias_2.c.email_address == "spongebob@gmail.com")
)

connection.execute(select_stmt).fetchall()

### slide::
# A subquery is used much like a table alias, except we start with a select
# statement.   We call the .alias(), or .subquery() method
# of select()  (1.3 only has .alias())

select_subq = (
    select([user_table.c.username, address_table.c.email_address])
    .select_from(user_table.join(address_table))
    .alias()
)

### slide:: pi
# the subquery object itself has a .c attribute, and is used just like
# a table.

stmt = select([select_subq.c.username]).where(
    select_subq.c.username == "spongebob"
)
print(stmt)

### slide::
# With subquery and join we can compose more elaborate statements.  This
# subquery introduces the "func" and "group by" concepts

from sqlalchemy import func

address_select = select(
    [address_table.c.user_id, func.count(address_table.c.id).label("count")]
).group_by(address_table.c.user_id)

address_subq = address_select.alias()

### slide:: pi
# we use join() to link the alias() with another select()

username_plus_count = (
    select([user_table.c.username, address_subq.c.count])
    .select_from(user_table.join(address_subq))
    .order_by(user_table.c.username)
)

connection.execute(username_plus_count).fetchall()


### slide::
# joining to a subquery can also be achieved using a common table
# expression, or CTE. By calling
# cte() instead of alias(), we get a CTE:

address_cte = address_select.cte()

### slide:: i
# we select/join to the CTE in exactly the same way as we did the subquery.

username_plus_count = (
    select([user_table.c.username, address_cte.c.count])
    .select_from(user_table.join(address_cte))
    .order_by(user_table.c.username)
)

### slide:: i

connection.execute(username_plus_count).fetchall()

### slide::
### title:: Correlated subqueries
# a *scalar subquery* returns exactly one row and one column.
# we indicate this intent using the as_scalar() or scalar_subquery() method
# after construction (1.3 only has as_scalar() :)  )

address_corr = (
    select([func.count(address_table.c.id)])
    .where(user_table.c.id == address_table.c.user_id)
    .as_scalar()
)

### slide:: i
# the subquery here refers to two tables.  printing it alone,
# we see both tables in the FROM clause.
print(address_corr)

### slide:: i
# However, a scalar subquery will by default **auto-correlate** in a larger
# SQL expression, omitting a FROM that is found in the immediate
# enclosing SELECT.

select_stmt = select([user_table.c.username, address_corr])
print(select_stmt)


### slide::
### title:: Questions?


### slide::
