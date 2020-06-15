### slide::
### title:: Object Relational Mapping
# The *declarative* system is normally used to configure
# object relational mappings.

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

### slide::
# a basic mapping.  __repr__() is optional.

from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return "<User(%r, %r)>" % (self.name, self.fullname)


### slide::
# the User class now has a Table object associated with it.

User.__table__

### slide::
# The Mapper object mediates the relationship between User
# and the "user" Table object.  This mapper object is generally behind
# the scenes.

User.__mapper__

### slide::
# User has a default constructor, accepting field names
# as arguments.

spongebob = User(name="spongebob", fullname="Spongebob Squarepants")

### slide::
# The "id" field is the primary key, which starts as None
# if we didn't set it explicitly.

print(spongebob.name, spongebob.fullname)
print(spongebob.id)

### slide:: p
# The MetaData object is here too, available from the Base.

from sqlalchemy import create_engine

engine = create_engine("sqlite://")
with engine.begin() as connection:
    Base.metadata.create_all(connection)

### slide::
# To persist and load User objects from the database, we
# use a Session object.

from sqlalchemy.orm import Session

session = Session(bind=engine)

### slide::
# new objects are placed into the Session using add().
session.add(spongebob)

### slide:: pi
# the Session will *flush* *pending* objects
# to the database before each Query.

also_spongebob = session.query(User).filter_by(name="spongebob").first()
also_spongebob

### slide::
# the User object we've inserted now has a value for ".id"
print(spongebob.id)

### slide::
# the Session maintains a *unique* object per identity.
# so "spongebob" and "our_user" are the *same* object

spongebob is also_spongebob

### slide::
# Add more objects to be pending for flush.

session.add_all(
    [
        User(name="patrick", fullname="Patrick Star"),
        User(name="sandy", fullname="Sandy Cheeks"),
    ]
)

### slide::
# modify "spongebob" - the object is now marked as *dirty*.

spongebob.fullname = "Spongebob Jones"

### slide::
# the Session can tell us which objects are dirty...

session.dirty

### slide::
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
# Make another "dirty" change, and another "pending" change,
# that we might change our minds about.

spongebob.name = "Spongy"
fake_user = User(name="fakeuser", fullname="Invalid")
session.add(fake_user)

### slide:: p
# run a query, our changes are flushed; results come back.

session.query(User).filter(User.name.in_(["Spongy", "fakeuser"])).all()

### slide::
# But we're inside of a transaction.  Roll it back.
session.rollback()

### slide:: p
# spongebob's name is back to normal
spongebob.name

### slide::
# "fake_user" has been evicted from the session.
fake_user in session

### slide:: p
# and the data is gone from the database too.

session.query(User).filter(User.name.in_(["spongebob", "fakeuser"])).all()


### slide::
### title:: ORM Querying
# The attributes on our mapped class act like Column objects, and
# produce SQL expressions.

print(User.name == "spongebob")


### slide::
# This works similarly as the core select().  ORM Query adds lots of additional
# functionalities in terms of how it interprets what is passed.   Here,
# an *entity*, rather than a plain Table or Column object, is passed.

query = session.query(User).filter(User.name == "spongebob").order_by(User.id)

### slide:: ip
# The ORM Query then returns actual User objects.  in this case,
# it returns them directly and not as a "row".  When Query was first
# implemented years ago, this is all it could do.
query.all()


### slide:: p
# Later, Query was enhanced to also be able to return rows of individual
# columns...
for name, fullname in session.query(User.name, User.fullname):
    print(name, fullname)

### slide:: p
# as well as combinations of "entities" and columns
for row in session.query(User, User.name):
    print(row.User, row.name)

### slide:: p
# the WHERE clause is either by filter_by(), which is convenient

for (name,) in session.query(User.name).filter_by(fullname="Spongebob Jones"):
    print(name)

### slide:: p
# or filter(), which works just like select().where().

from sqlalchemy import or_

for user in (
    session.query(User)
    .filter(User.name == "spongebob")
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
