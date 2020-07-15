### slide::
### title:: Relationships, Joins, What's New ?
# start with the same mapping as before.  Except we will also
# give it a one-to-many **relationship** to a second entity.

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    fullname = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return "<User(%r, %r)>" % (self.username, self.fullname)


### slide::
# for the other end of one-to-many, create another mapped class with
# a ForeignKey referring back to User

from sqlalchemy import ForeignKey


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(%r)>" % self.email_address


### slide:: p
# Create tables

from sqlalchemy import create_engine

engine = create_engine("sqlite://")
with engine.connect() as connection:
    Base.metadata.create_all(connection)

### slide:: p
# Insert data into the User table...

from sqlalchemy.orm import Session

session = Session(bind=engine)

session.add_all(
    [
        User(username="spongebob", fullname="Spongebob Squarepants"),
        User(username="sandy", fullname="Sandy Cheeks"),
        User(username="patrick", fullname="Patrick Star"),
    ]
)
session.commit()

### slide::
# a new User object also gains an empty "addresses" collection now.

squidward = User(username="squidward", fullname="Squidward Tentacles")
squidward.addresses


### slide:: i
# New in 1.4, in the same way that column attributes are not part of the
# object's state by accessing it, neither are collections, until they are
# mutated.
squidward.__dict__

### slide::
# populate this collection with new Address objects.

squidward.addresses = [
    Address(email_address="squidward@gmail.com"),
    Address(email_address="s25@yahoo.com"),
    Address(email_address="squidward@hotmail.com"),
]

### slide::
# "back populates" sets up Address.user for each User.address.

squidward.addresses[1]
squidward.addresses[1].user

### slide::
# adding User->squidward will *cascade* each Address into the Session as well.

session.add(squidward)
session.new

### slide:: p
# commit.
session.commit()

### slide:: p
# After expiration, squidward.addresses emits a *lazy load* when first
# accessed.
squidward.addresses

### slide:: i
# the collection stays in memory until the transaction ends.
squidward.addresses

### slide:: p
# collections and references are updated by manipulating objects themselves;
# setting up of foreign key column values is handled automatically.

spongebob = session.query(User).filter_by(username="spongebob").one()
spongebob.addresses
squidward.addresses[1].user = spongebob

### slide:: i
# by assigning .user on one of squidward's email addresses, the object moved
# from one "addresses" collection to the other.  this is the back populates
# feature at work.
spongebob.addresses
squidward.addresses

### slide:: ip
# commit the data.
session.commit()

### slide::
# Questions before the next section?

### slide:: p
### title:: Querying with multiple tables
# Query can select from multiple tables at once. Below selects from
# two different entities.  Results are returned as rows with two
# "columns", a User and an Address.

for row in session.query(User, Address).filter(User.id == Address.user_id):
    print(row)

### slide:: p
# ORM query creates joins usually using the .join() method.  Like the Core
# join() methods, it can figure out the ON clause for simple cases

session.query(User, Address).join(Address).all()


### slide:: pi
# or you can give it an explicit SQL expression for the ON clause
session.query(User, Address).join(Address, User.id == Address.user_id).all()

### slide:: p
# however the most accurate and succinct way is to use the relationship-bound
# attribute.

session.query(User.username).join(User.addresses).filter(
    Address.email_address == "squidward@gmail.com"
).first()

### slide:: p
# the ORM version of table.alias() is to use the aliased() function
# on a mapped entity.

from sqlalchemy.orm import aliased

a1, a2 = aliased(Address), aliased(Address)
session.query(User).join(a1).join(a2).filter(
    a1.email_address == "squidward@gmail.com"
).filter(a2.email_address == "squidward@hotmail.com").all()

### slide:: p
# to join() to an aliased() object with more specificity, a form such
# as "Class.relationship.of_type(aliased)" may be used

session.query(User).join(User.addresses.of_type(a1)).join(
    User.addresses.of_type(a2)
).filter(a1.email_address == "squidward@gmail.com").filter(
    a2.email_address == "squidward@hotmail.com"
).all()

### slide:: p
# We can also join with subqueries.  subquery() returns
# a Subquery construct for us to use.  This converts the ORM Query
# object into a Core select().subquery() construct.

from sqlalchemy import func

subq = (
    session.query(func.count(Address.id).label("count"), Address.user_id)
    .group_by(Address.user_id)
    .subquery()
)

session.query(User.username, func.coalesce(subq.c.count, 0)).outerjoin(
    subq, User.id == subq.c.user_id
).all()

### slide::
# Questions before the next section?

### slide:: p
### title:: Eager Loading
# the "N plus one" problem is an ORM issue which refers to the many SELECT
# statements emitted when loading collections against a parent result.
# As SQLAlchemy is a full featured ORM, we of course include this! :)

for user in session.query(User):
    print(user, user.addresses)

### slide:: p
# However, SQLAlchemy was designed from the start to tame the "N plus one"
# problem by implementing **eager loading**.  Eager loading is now very mature,
# and the most effective strategy for collections is currently the
# **selectinload** option.

session.rollback()  # so we can see the load happen again.

from sqlalchemy.orm import selectinload

for user in session.query(User).options(selectinload(User.addresses)):
    print(user, user.addresses)

### slide:: p
# The oldest eager loading strategy is joinedload().  This uses a LEFT OUTER
# JOIN or INNER JOIN to load parent + child in one query.  joinedload() can
# work for collections as well, however it is best tailored towards many-to-one
# relationships, particularly those where the foreign key is "not null".

session.rollback()

from sqlalchemy.orm import joinedload

for address_obj in session.query(Address).options(
    joinedload(Address.user, innerjoin=True)
):
    print(address_obj.email_address, address_obj.user.username)

### slide:: p
### title:: Instant Zen of Eager Loading
# eager loading *does not* change the *result* of the Query.
# only how related collections are loaded.   An explicit join()
# can be mixed with the joinedload() and they are kept separate

for address in (
    session.query(Address)
    .join(Address.user)
    .filter(User.username == "squidward")
    .options(joinedload(Address.user))
):
    print(address, address.user)

### slide:: p
# To optimize the common case of "join to many-to-one and also load it on
# the object", the contains_eager() option is used

from sqlalchemy.orm import contains_eager

for address in (
    session.query(Address)
    .join(Address.user)
    .filter(User.username == "squidward")
    .options(contains_eager(Address.user))
):
    print(address, address.user)

### slide::
# Questions before the next section?

### slide:: p
### title:: What's new in 1.4 / 2.0 ?
# As Query has evolved for years to look more and more like a select(),
# the next step is that select() and Query() basically merge

from sqlalchemy import select

future_session = Session(bind=engine, future=True)

stmt = (
    select(User, Address.email_address)
    .join(User.addresses)
    .order_by(User.username, Address.email_address)
)

result = future_session.execute(stmt)

### slide:: p
# part of the reason is that people wanted more flexibility in how
# Query returns results.   so now the full Result object is returned, which
# allows for a method chained approach to customize how results are
# returned.

result.scalars().unique().all()

### slide:: p
# additionally, the strange duplication of query.filter() / select.where()
# is solved by making it all just select.where().

stmt = select(User).where(User.username == "spongebob")
result = future_session.execute(stmt)

user = result.scalar()

### slide:: p
# select() also gains features taken from the ORM, that now work in Core,
# like join() and filter_by().

stmt = select(User).filter_by(username="squidward").join(Address)

with engine.connect() as connection:
    result = connection.execute(stmt)
    result.all()


### slide:: pi
# the unification also rearranges things on the inside and is actually
# part of how ORM Query, select() and everything else are now cachable,
# including that time spent on the outside of the cache building the
# object is at a minimum.

future_session.execute(stmt).scalars().all()


### slide::
### title:: Questions?


### slide::
