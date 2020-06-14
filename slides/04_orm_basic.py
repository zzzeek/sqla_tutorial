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


### slide:: p
# This works similarly as the core select(), but Query()
# object provides a lot more functionality,
# here selecting the User *entity*.

query = session.query(User).filter(User.name == "spongebob").order_by(User.id)

query.all()


### slide:: p
# Query can also return individual columns

for name, fullname in session.query(User.name, User.fullname):
    print(name, fullname)

### slide:: p
# and can mix entities / columns together.

for row in session.query(User, User.name):
    print(row.User, row.name)

### slide:: p
# Array indexes will OFFSET to that index and LIMIT by one...

u = session.query(User).order_by(User.id)[2]
print(u)

### slide:: pi
# and array slices work too.

for u in session.query(User).order_by(User.id)[1:3]:
    print(u)

### slide:: p
# the WHERE clause is either by filter_by(), which is convenient

for (name,) in session.query(User.name).filter_by(fullname="spongebob Jones"):
    print(name)

### slide:: p
# or filter(), which is more flexible

for (name,) in session.query(User.name).filter(User.fullname == "spongebob Jones"):
    print(name)

### slide:: p
# conjunctions can be passed to filter() as well

from sqlalchemy import or_

for (name,) in session.query(User.name).filter(
    or_(User.fullname == "spongebob Jones", User.id < 5)
):
    print(name)

### slide::
# multiple filter() calls join by AND just like select().where()

for user in (
    session.query(User)
    .filter(User.name == "spongebob")
    .filter(User.fullname == "spongebob Jones")
):
    print(user)

### slide::
# Query has some variety for returning results

query = session.query(User).filter_by(fullname="spongebob Jones")

### slide:: p
# all() returns a list

query.all()

### slide:: p
# first() returns the first row, or None

query.first()

### slide:: p
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
