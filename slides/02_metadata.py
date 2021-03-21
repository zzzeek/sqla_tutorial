### slide::
### title:: Schema and MetaData
# The structure of a relational schema is represented in Python
# using MetaData, Table, and other objects.

from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String
from sqlalchemy import select

metadata = MetaData()
user_table = Table(
    "user_account",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), nullable=False),
    Column("fullname", String(255)),
)

### slide::
# Table provides a single point of information regarding
# the structure of a table in a schema.

user_table.name

### slide:: i
# The .c. attribute of Table is an associative array
# of Column objects, keyed on name.

user_table.c.username

### slide:: i
# It's a bit like a Python dictionary but not totally.

print(user_table.c)

### slide::
# Column itself has information about each Column, such as
# name and type
user_table.c.username.name
user_table.c.username.type

### slide:: i
# Table has other information available, such as the collection
# of columns which comprise the table's primary key.
user_table.primary_key

### slide::
# The Table object is at the core of the SQL expression
# system - this is a quick preview of that.
print(select(user_table))

### slide:: p
# Table and MetaData objects can be used to generate a schema
# in a database; MetaData features the create_all() method.
from sqlalchemy import create_engine

engine = create_engine("sqlite://")

with engine.begin() as conn:
    metadata.create_all(conn)

### slide:: p
# Types are represented using objects such as String, Integer,
# DateTime.  These objects can be specified as "class keywords",
# or can be instantiated with arguments.

from sqlalchemy import String, Numeric, DateTime, Enum

fancy_table = Table(
    "fancy",
    metadata,
    Column("key", String(50), primary_key=True),
    Column("timestamp", DateTime),
    Column("amount", Numeric(10, 2)),
    Column("type", Enum("a", "b", "c")),
)

with engine.begin() as conn:
    fancy_table.create(conn)

### slide:: p
# at this point, the two Table objects we've created are part of a collection
# in the MetaData object called .tables
metadata.tables.keys()
metadata.tables['user_account']


### slide:: p
# table metadata also allows for constraints and indexes.
# ForeignKey is used to link one column to a remote primary
# key.  Note we can omit the datatype for a ForeignKey column.

from sqlalchemy import ForeignKey

addresses_table = Table(
    "email_address",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email_address", String(100), nullable=False),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
)

with engine.begin() as conn:
    addresses_table.create(conn)

### slide::
# ForeignKey is a shortcut for ForeignKeyConstraint,
# which should be used for composite references.

from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import Text

story_table = Table(
    "story",
    metadata,
    Column("story_id", Integer, primary_key=True),
    Column("version_id", Integer, primary_key=True),
    Column("headline", String(100), nullable=False),
    Column("body", Text),
)

published_table = Table(
    "published",
    metadata,
    Column("pub_id", Integer, primary_key=True),
    Column("pub_timestamp", DateTime, nullable=False),
    Column("story_id", Integer),
    Column("version_id", Integer),
    ForeignKeyConstraint(
        ["story_id", "version_id"], ["story.story_id", "story.version_id"]
    ),
)

### slide:: p
# create_all() by default checks for tables existing already

with engine.begin() as conn:
    metadata.create_all(conn)


### slide:: p
### title:: Reflection
# 'reflection' refers to loading Table objects based on
# reading from an existing database.
metadata2 = MetaData()

with engine.connect() as conn:
    user_reflected = Table("user_account", metadata2, autoload_with=conn)


### slide:: p
# the user_reflected object is now filled in with all the columns
# and constraints and is ready to use

print(user_reflected.c)
print(user_reflected.primary_key)
print(select(user_reflected))

### slide::
# Information about a database at a more specific level is available
# using the Inspector object.

from sqlalchemy import inspect

# inspector will work with an engine or a conneciton.
# no plans to change that :)
inspector = inspect(engine)

### slide:: p
# the inspector provides things like table names:
inspector.get_table_names()

### slide:: p
# column information
inspector.get_columns("email_address")

### slide:: p
# constraints
inspector.get_foreign_keys("email_address")


### slide:: p
### title:: Reflecting an entire schema
# The MetaData object also includes a feature that will reflect all the
# tables in a particular schema at once.

metadata3 = MetaData()
with engine.connect() as conn:
    metadata3.reflect(conn)

### slide::
# the Table objects are then in the metadata.tables collection

story, published = metadata3.tables['story'], metadata3.tables['published']

story
published

### slide:: i
# ready to use

print(select(story).join(published))

### slide::
### title:: Questions?

### slide::
