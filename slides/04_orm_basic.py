### slide::
### title:: Object Relational Mapping
# SQLAlchemy mappings in 1.4 / 2.0 start with a central object
# known as the *registry*

from sqlalchemy.orm import registry


mapper_registry = registry()

### slide::
# Using the registry, we can map classes in various ways, below illustrated
# using its "mapped" decorator.
# In this form, we arrange class attributes in terms of Column objects
# to be mapped to a Table, which is named based on an attribute
# "__tablename__"

from sqlalchemy import Column, Integer, String


@mapper_registry.mapped
class User:
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


### slide:: p
# Using our registry, we can create a database schema for this class using
# a MetaData object that is part of the registry.

from sqlalchemy import create_engine

engine = create_engine("sqlite://")
with engine.begin() as connection:
    mapper_registry.metadata.create_all(connection)

### slide::
# To persist and load User objects from the database, we
# use a Session object, illustrated here from a factory called
# sessionmaker.  The Session object makes use of a connection
# factory (i.e. an Engine) and will handle the job of connecting,
# committing, and releasing connections to this engine.

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine, future=True)

session = Session()

### slide::
# new objects are placed into the Session using add().
session.add(spongebob)

### slide:: i
# This did not yet modify the database, however the object is now known as
# **pending**.  We can see the "pending" objects by looking at the session.new
# attribute.
session.new


### slide:: p
# We can now query for this **pending** row, by emitting a SELECT statement
# that will refer to "User" entities.   This will first **autoflush**
# the pending changes, then SELECT the row we requested.

from sqlalchemy import select

select_statement = select(User).filter_by(username="spongebob")
result = session.execute(select_statement)

### slide:: i
# We can get the data back from the result, in this case using the
# .scalar() method which will return the first column of the first row.
also_spongebob = result.scalar()
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
# start a *new* transaction and re-load from the database.  This is
# our first example of the ORM *lazy loading* pattern.

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

result = session.execute(
    select(User).where(User.username.in_(["Spongy", "fakeuser"]))
)
result.all()

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

result = session.execute(
    select(User).where(User.username.in_(["spongebob", "fakeuser"]))
)
result.all()


### slide::
### title:: ORM Querying
# The attributes on our mapped class act like Column objects, and
# produce SQL expressions.

print(User.username == "spongebob")


### slide::
# When ORM-specific expressions are used with select(), the Select construct
# itself takes on ORM-enabled features, the most basic of which is that
# it can discern between selecting from *columns* vs *entities*.  Below,
# the SELECT is to return rows that contain a single element, which would
# be an instance of User.   This is translated from the actual SELECT
# sent to the database that SELECTs for the individual columns of the
# User entity.

query = (
    select(User).where(User.username == "spongebob").order_by(User.id)
)

### slide:: ip
# the rows we get back from Session.execute() then contain User objects
# as the first element in each row.
result = session.execute(query)

for row in result:
    print(row)


### slide:: p
# As it is typically convenient for rows that only have a single element
# to be delivered as the element alone, we can use the .scalars() method
# of Result as we did earlier to return just the first column of each row

result = session.execute(query)
for user_obj in result.scalars():
    print(user_obj)

### slide:: pi
# we can also qualify the rows we want to get back with methods like
# .one()

result = session.execute(query)

user_obj = result.scalars().one()
print(user_obj)


### slide:: p
# An ORM query can make use of any combination of columns and entities.
# To request the fields of User separately, we name them separately in the
# columns clause

query = select(User.username, User.fullname)
result = session.execute(query)
for row in result:
    print(f"{row.username} {row.fullname}")

### slide:: p
# as well as combinations of "entities" and columns
query = select(User, User.username)
result = session.execute(query)
for row in result:
    print(f"{row.User.id} {row.User.fullname} {row.username}")

### slide:: p
# the WHERE clause is either by filter_by(), which is convenient

for (username, ) in session.execute(
    select(User.username).filter_by(
        fullname="Spongebob Jones"
    )
):
    print(username)

### slide:: pi
# or where() for more explicitness

from sqlalchemy import or_

for (user, ) in (
    session.execute(
        select(User)
        .where(User.username == "spongebob")
        .where(or_(User.fullname == "Spongebob Jones", User.id < 5))
    )
):
    print(user)

### slide::
### title:: Questions?


### slide::
