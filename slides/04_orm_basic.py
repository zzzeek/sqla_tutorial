### slide::
### title:: Object Relational Mapping
# The *declarative* system is the primary system used to configure
# object relational mappings.

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

### slide::
# a basic mapping.  __repr__() is optional.

from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return "<User(%r, %r)>" % (self.username, self.fullname)


### slide::
# the User class now has a Table object associated with it.

User.__table__

### slide:: i
# The Mapper object mediates the relationship between User
# and the "user" Table object.  This mapper object is generally behind
# the scenes.

User.__mapper__

### slide::
# User has a default constructor, accepting field names
# as arguments.

spongebob = User(username="spongebob", fullname="Spongebob Squarepants")
spongebob

### slide::
# Attributes which we didn't set, such as the "id", are displayed as
# None when we access them

repr(spongebob.id)

### slide:: i
# Since SQLAlchemy 1.0, these "implicit" attribute values are not
# actually part of the object's state even when we access them.

spongebob.__dict__


### slide:: p
# Using our Base, we can create a database schema for this class using
# a MetaData object that is part of the Base.

from sqlalchemy import create_engine

engine = create_engine("sqlite://")
with engine.begin() as connection:
    Base.metadata.create_all(connection)

### slide::
# To persist and load User objects from the database, we
# use a Session object.  The Session object makes use of a connection
# factory (i.e. an Engine) and will handle the job of connecting,
# committing, and releasing connections to this engine.

from sqlalchemy.orm import Session

session = Session(bind=engine)

### slide::
# new objects are placed into the Session using add().
session.add(spongebob)

### slide:: i
# This did not yet modify the database, however the object is now known as
# **pending**.  We can see the "pending" objects by looking at the session.new
# attribute.
session.new


### slide:: p
# We can now query for this **pending** row, using an ORM query. the way
# this will work is the ORM will first **flush** pending changes to the
# database, then emit a SELECT.  The ORM Query object is much like the
# select(), but also can deliver results directly.

also_spongebob = session.query(User).filter_by(username="spongebob").first()
also_spongebob

### slide::
# the User object we've inserted now has a value for ".id"
spongebob.id

### slide:: i
# the Session maintains a *unique* object per identity.
# so "spongebob" and "also_spongebob" are the *same* object

spongebob is also_spongebob

### slide:: i
# this is known as the **identity map**, and we can look at it on
# the Session.

session.identity_map.items()

### slide::
### title:: Making Changes
# Add more objects to be pending for flush.

session.add_all(
    [
        User(username="patrick", fullname="Patrick Star"),
        User(username="sandy", fullname="Sandy Cheeks"),
    ]
)

### slide:: i
# modify "spongebob" - the object is now marked as *dirty*.

spongebob.fullname = "Spongebob Jones"

### slide::
# the Session can tell us which objects are dirty...

session.dirty

### slide:: i
# and can also tell us which objects are pending...

session.new

### slide:: p i
# The whole transaction is committed.  Commit always triggers
# a final flush of remaining changes.

session.commit()

### slide:: p
# After a commit, theres no transaction.  The Session
# *invalidates* all data, so that accessing them will automatically
# start a *new* transaction and re-load from the database.

spongebob.fullname

### slide::
### title:: rolling back changes
# Make another "dirty" change, and another "pending" change,
# that we might change our minds about.

spongebob.username = "Spongy"
fake_user = User(username="fakeuser", fullname="Invalid")
session.add(fake_user)

### slide:: p
# run a query, our changes are flushed; results come back.

session.query(User).filter(User.username.in_(["Spongy", "fakeuser"])).all()

### slide::
# But we're inside of a transaction.  Roll it back.
session.rollback()

### slide:: p
# Again, the transaction is over, objects are expired.
# Accessing an attribute refreshes the object and the "Spongy" username is gone
spongebob.username

### slide::
# "fake_user" has been evicted from the session.
fake_user in session

### slide:: pi
# and the data is gone from the database too.

session.query(User).filter(User.username.in_(["spongebob", "fakeuser"])).all()


### slide::
### title:: ORM Querying
# The attributes on our mapped class act like Column objects, and
# produce SQL expressions.

print(User.username == "spongebob")


### slide::
# Within the ORM, we historically use these expressions with the
# Query object, which is very similar to select(), but adds ORM-specific
# functionalities in terms of how it interprets what is passed.   Here,
# an *entity*, rather than a plain Table or Column object, is passed.

query = (
    session.query(User).filter(User.username == "spongebob").order_by(User.id)
)

### slide:: ip
# The ORM Query then returns actual User objects.  in this case,
# it returns them directly and not as a "row".  When Query was first
# implemented years ago, this is all it could do.
query.all()


### slide:: p
# Later, Query was enhanced to also be able to return rows of individual
# columns...
for username, fullname in session.query(User.username, User.fullname):
    print(username, fullname)

### slide:: p
# as well as combinations of "entities" and columns
for row in session.query(User, User.username):
    print(row.User, row.username)

### slide:: p
# the WHERE clause is either by filter_by(), which is convenient

for (username,) in session.query(User.username).filter_by(
    fullname="Spongebob Jones"
):
    print(username)

### slide:: p
# or filter(), which works just like select().where().

from sqlalchemy import or_

for user in (
    session.query(User)
    .filter(User.username == "spongebob")
    .filter(or_(User.fullname == "Spongebob Jones", User.id < 5))
):
    print(user)

### slide::
# Query has some variety for returning results

query = session.query(User).filter_by(fullname="Spongebob Jones")

### slide:: pi
# all() returns a list

query.all()

### slide:: pi
# first() returns the first row, or None

query.first()

### slide:: pi
# one() returns the first row and verifies that there's one and only one

query.one()

### slide:: p
# if there's not one(), you get an error

query = session.query(User).filter_by(fullname="nonexistent")
query.one()

### slide:: p
# if there's more than one(), you get an error

query = session.query(User)
query.one()

### slide::
### title:: Questions?


### slide::
