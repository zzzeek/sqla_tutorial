### slide::
### title:: Advanced Object Relational Mapping
# start with the same mapping as before...

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return "<User(%r, %r)>" % (self.name, self.fullname)


### slide::
# But then, we'll also add a second table.

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", backref="addresses")

    def __repr__(self):
        return "<Address(%r)>" % self.email_address


### slide:: p
# Create tables

from sqlalchemy import create_engine

engine = create_engine("sqlite://")
Base.metadata.create_all(engine)

### slide:: p
# Insert data into the User table...

from sqlalchemy.orm import Session

session = Session(bind=engine)

session.add_all(
    [
        User(name="spongebob", fullname="Spongebob Squarepants"),
        User(name="sandy", fullname="Sandy Cheeks"),
        User(name="patrick", fullname="Patrick Star"),

    ]
)
session.commit()

### slide::
# a new User object also gains an empty "addresses" collection now.

squidward = User(name="squidward", fullname="Squidward Tentacles")
squidward.addresses

### slide::
# populate this collection with new Address objects.

squidward.addresses = [
    Address(email_address="squidward@gmail.com"),
    Address(email_address="s25@yahoo.com"),
    Address(email_address="squidward@hotmail.com"),
]

### slide::
# the "backref" sets up Address.user for each User.address.

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
# collections and references are updated by manipulating objects,
# not primary / foreign key values.

spongebob = session.query(User).filter_by(name="spongebob").one()
squidward.addresses[1].user = spongebob

spongebob.addresses

session.commit()

### slide:: p
# Query can select from multiple tables at once.
# Below is an *implicit join*.

session.query(User, Address).filter(User.id == Address.user_id).all()

### slide:: p
# join() is used to create an explicit JOIN.

session.query(User, Address).join(Address, User.id == Address.user_id).all()

### slide:: p
# The most succinct and accurate way to join() is to use the
# the relationship()-bound attribute to specify ON.

session.query(User, Address).join(User.addresses).all()

### slide:: p
# join() will also figure out very simple joins just using entities.

session.query(User, Address).join(Address).all()


### slide:: p
# Either User or Address may be referred to anywhere in the query.

session.query(User.name).join(User.addresses).filter(
    Address.email_address == "squidward@gmail.com"
).first()

### slide:: p
# we can specify an explicit FROM using select_from().

session.query(User, Address).select_from(Address).join(Address.user).all()

### slide:: p
# A query that refers to the same entity more than once in the FROM
# clause requires *aliasing*.

from sqlalchemy.orm import aliased

a1, a2 = aliased(Address), aliased(Address)
session.query(User).join(a1).join(a2).filter(
    a1.email_address == "squidward@gmail.com"
).filter(a2.email_address == "squidward@hotmail.com").all()

### slide:: p
# We can also join with subqueries.  subquery() returns
# an "alias" construct for us to use.

from sqlalchemy import func

subq = (
    session.query(
        func.count(Address.id).label("count"), User.id.label("user_id")
    )
    .join(Address.user)
    .group_by(User.id)
    .subquery()
)

session.query(User.name, func.coalesce(subq.c.count, 0)).outerjoin(
    subq, User.id == subq.c.user_id
).all()

### slide::
### title:: Exercises
# 1. Run this SQL JOIN:
#
#    SELECT user.name, address.email_address FROM user
#    JOIN address ON user.id=address.user_id WHERE
#    address.email_address='j25@yahoo.com'
#

### slide:: p
### title:: Eager Loading
# the "N plus one" problem refers to the many SELECT statements
# emitted when loading collections against a parent result

for user in session.query(User):
    print(user, user.addresses)

### slide:: p
# *eager loading* solves this problem by loading *all* collections
# at once.

session.rollback()  # so we can see the load happen again.

from sqlalchemy.orm import subqueryload

for user in session.query(User).options(subqueryload(User.addresses)):
    print(user, user.addresses)

### slide:: p
# joinedload() uses a LEFT OUTER JOIN to load parent + child in one query.

session.rollback()

from sqlalchemy.orm import joinedload

for user in session.query(User).options(joinedload(User.addresses)):
    print(user, user.addresses)

### slide:: p
# eager loading *does not* change the *result* of the Query.
# only how related collections are loaded.

for address in (
    session.query(Address)
    .join(Address.user)
    .filter(User.name == "squidward")
    .options(joinedload(Address.user))
):
    print(address, address.user)

### slide:: p
# to join() *and* joinedload() at the same time without using two
# JOIN clauses, use contains_eager()

from sqlalchemy.orm import contains_eager

for address in (
    session.query(Address)
    .join(Address.user)
    .filter(User.name == "squidward")
    .options(contains_eager(Address.user))
):
    print(address, address.user)


### slide::
### title:: Questions?

### slide::
