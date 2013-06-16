### slide::
### title:: Schema and MetaData
# The structure of a relational schema is represented in Python
# using MetaData, Table, and other objects.

from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String

metadata = MetaData()
user_table = Table('user', metadata,
               Column('id', Integer, primary_key=True),
               Column('name', String),
               Column('fullname', String)
             )

### slide::
# Table provides a single point of information regarding
# the structure of a table in a schema.

user_table.name

### slide:: i
# The .c. attribute of Table is an associative array
# of Column objects, keyed on name.

user_table.c.name

### slide:: i
# It's a bit like a Python dictionary but not totally.

print(user_table.c)

### slide::
# Column itself has information about each Column, such as
# name and type
user_table.c.name.name
user_table.c.name.type

### slide:: i
# Table has other information available, such as the collection
# of columns which comprise the table's primary key.
user_table.primary_key

### slide::
# The Table object is at the core of the SQL expression
# system - this is a quick preview of that.
print(user_table.select())

### slide:: p
# Table and MetaData objects can be used to generate a schema
# in a database.
from sqlalchemy import create_engine
engine = create_engine("sqlite://")
metadata.create_all(engine)

### slide:: p
# Types are represented using objects such as String, Integer,
# DateTime.  These objects can be specified as "class keywords",
# or can be instantiated with arguments.

from sqlalchemy import String, Numeric, DateTime, Enum

fancy_table = Table('fancy', metadata,
                    Column('key', String(50), primary_key=True),
                    Column('timestamp', DateTime),
                    Column('amount', Numeric(10, 2)),
                    Column('type', Enum('a', 'b', 'c'))
                )

fancy_table.create(engine)

### slide:: p
# table metadata also allows for constraints and indexes.
# ForeignKey is used to link one column to a remote primary
# key.

from sqlalchemy import ForeignKey
addresses_table = Table('address', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('email_address', String(100), nullable=False),
                    Column('user_id', Integer, ForeignKey('user.id'))
                  )

addresses_table.create(engine)

### slide::
# ForeignKey is a shortcut for ForeignKeyConstraint,
# which should be used for composite references.

from sqlalchemy import Unicode, UnicodeText, DateTime
from sqlalchemy import ForeignKeyConstraint

story_table = Table('story', metadata,
               Column('story_id', Integer, primary_key=True),
               Column('version_id', Integer, primary_key=True),
               Column('headline', Unicode(100), nullable=False),
               Column('body', UnicodeText)
          )

published_table = Table('published', metadata,
            Column('pub_id', Integer, primary_key=True),
            Column('pub_timestamp', DateTime, nullable=False),
            Column('story_id', Integer),
            Column('version_id', Integer),
            ForeignKeyConstraint(
                            ['story_id', 'version_id'],
                            ['story.story_id', 'story.version_id'])
                )

### slide:: p
# create_all() by default checks for tables existing already
metadata.create_all(engine)


### slide::
### title:: Exercises
# 1. Write a Table construct corresponding to this CREATE TABLE
#    statement.
#
# CREATE TABLE network (
#      network_id INTEGER PRIMARY KEY,
#      name VARCHAR(100) NOT NULL,
#      created_at DATETIME NOT NULL,
#      owner_id INTEGER,
#      FOREIGN KEY owner_id REFERENCES user(id)
# )
#
# 2. Then emit metadata.create_all(), which will
# emit CREATE TABLE for this table (it will skip
# those that already exist).
#
# The necessary types are imported here:

from sqlalchemy import Integer, String, DateTime

### slide:: p
### title:: Reflection
# 'reflection' refers to loading Table objects based on
# reading from an existing database.
metadata2 = MetaData()

user_reflected = Table('user', metadata2, autoload=True, autoload_with=engine)

### slide:: i
print(user_reflected.c)

### slide::
# Information about a database at a more specific level is available
# using the Inspector object.

from sqlalchemy import inspect

inspector = inspect(engine)

### slide:: p
# the inspector provides things like table names:
inspector.get_table_names()

### slide:: p
# column information
inspector.get_columns('address')

### slide:: p
# constraints
inspector.get_foreign_keys('address')

### slide::
### title:: Exercises
#
# 1. Using 'metadata2', reflect the "network" table in the same way
#    we just did 'user', then display the columns (or bonus, display
#    just the column names)
#
# 2. Using "inspector", print a list of all table names that
#    include a column called "story_id"
#

### slide::