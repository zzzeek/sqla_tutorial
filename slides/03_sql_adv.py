### slide::
### title:: Joins / Aliases / Subqueries / CTEs
# create the same table as we used earlier..

from sqlalchemy import MetaData, Table, Column
from sqlalchemy import String, Integer

metadata = MetaData()
user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50)),
    Column("fullname", String(50)),
)

### slide::
# Then a second table to illustrate multi-table operations
from sqlalchemy import ForeignKey

address_table = Table(
    "email_address",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
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

connection = engine.connect()

### slide::
### title:: SELECT from more than one table, joins
# the select() construct will include in the FROM clause all
# those tables that we mention in the columns clause or WHERE clause.
# by default, they are separated by a comma.
#
stmt = select(user_table.c.username, address_table.c.email_address)

print(stmt)


### slide:: pi
# however, selecting from multiple tables without relating them
# to each other produces an effect known as the **cartesian product**.
# SQLAlchemy will usually warn when this is detected during statement
# execution.

result = connection.execute(stmt)

### slide:: i
# the cartesian result contains every combination of rows which is redundant
# and slow to generate for larger datasets
result.all()

### slide:: p
# So, when we have more than one table mentioned, we want to relate them
# together, which is most easily achieved using join_from():

stmt = select(
    user_table.c.username, address_table.c.email_address
).join_from(user_table, address_table)

connection.execute(stmt).all()

### slide:: p
# there is also .join(), which will infer the left hand side automatically

stmt = select(
    user_table.c.username, address_table.c.email_address
).join(address_table)

connection.execute(stmt).all()

### slide:: p
# the ON clause of the JOIN is also inferred automatically from the
# foreign key relationships of the involved tables.   We may choose
# to express this join condition explicitly, as would be needed if the
# join condition were otherwise ambiguous

stmt = select(
    user_table.c.username, address_table.c.email_address
).join(address_table, user_table.c.id == address_table.c.user_id)

connection.execute(stmt).all()

### slide:: p
### title:: working with table aliases and subqueries
# When a SELECT wants to refer to the same table more than once, a SQL
# alias is used.  This is available using the  .alias() method, which
# returns a unique Alias object representing that table with a particular
# SQL alias.
address_alias_1 = address_table.alias()
address_alias_2 = address_table.alias()

select_stmt = (
    select(
            user_table.c.username,
            address_alias_1.c.email_address,
            address_alias_2.c.email_address,
    )
    .join_from(user_table, address_alias_1)
    .join_from(user_table, address_alias_2)
    .where(address_alias_1.c.email_address == "spongebob@spongebob.com")
    .where(address_alias_2.c.email_address == "spongebob@gmail.com")
)

connection.execute(select_stmt).all()

### slide::
# A subquery is used much like a table alias, except we start with a select
# statement.   We call the .subquery() method of select()

select_subq = (
    select(user_table.c.username, address_table.c.email_address)
    .join(address_table).subquery()
)

### slide:: pi
# the subquery object itself has a .c attribute, and is used just like
# a table.

stmt = select(select_subq.c.username).where(
    select_subq.c.username == "spongebob"
)
print(stmt)

### slide::
# With subqueries and joins we can compose more elaborate statements.  This
# subquery introduces the "func" and "group by" concepts

from sqlalchemy import func

address_select = select(
    address_table.c.user_id, func.count(address_table.c.id).label("count")
).group_by(address_table.c.user_id)

address_subq = address_select.subquery()

### slide:: pi
# we use join() to link the subquery() with another select()

username_plus_count = (
    select(user_table.c.username, address_subq.c.count)
    .join(address_subq)
    .order_by(user_table.c.username)
)

connection.execute(username_plus_count).all()


### slide::
### title:: Common Table Expressions
# joining to a subquery can also be achieved using a common table
# expression, or CTE. By calling
# cte() instead of subquery(), we get a CTE:

address_cte = address_select.cte()

### slide:: i
# we select/join to the CTE in exactly the same way as we did the subquery.

username_plus_count = (
    select(user_table.c.username, address_cte.c.count)
    .join(address_cte)
    .order_by(user_table.c.username)
)

### slide:: i

connection.execute(username_plus_count).all()

### slide::
### title:: Correlated subqueries
# a *scalar subquery* returns exactly one row and one column.
# we indicate this intent using the scalar_subquery() method
# after construction

address_corr = (
    select(func.count(address_table.c.id))
    .where(user_table.c.id == address_table.c.user_id)
    .scalar_subquery()
)

### slide:: i
# the subquery here refers to two tables.  printing it alone,
# we see both tables in the FROM clause.
print(address_corr)

### slide:: p
# However, a scalar subquery will by default **auto-correlate** in a larger
# SQL expression, omitting a FROM that is found in the immediate
# enclosing SELECT.

select_stmt = select(user_table.c.username, address_corr)
print(select_stmt)


### slide::
### title:: Questions?


### slide::
