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
    name = Column(String)
    fullname = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return "<User(%r, %r)>" % (self.name, self.fullname)


### slide::
# for the other end of one-to-many, create another mapped class with
# a ForeignKey referring back to User

from sqlalchemy import ForeignKey


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

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

spongebob = session.query(User).filter_by(name="spongebob").one()
squidward.addresses[1].user = spongebob

spongebob.addresses

session.commit()


### slide:: p
### title: Querying with multiple tables
# Query can select from multiple tables at once. Below selects from
# two different entities.  Results are returned as rows with two
# "columns", a User and an Address.

session.query(User, Address).filter(User.id == Address.user_id).all()

### slide:: p
# ORM query creates joins usually using the .join() method.

session.query(User, Address).join(Address, User.id == Address.user_id).all()

### slide:: p
# the most succinct way to join is to use the relationship-bound attribute.

session.query(User.name).join(User.addresses).filter(
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

### slide:: p
### title:: Eager Loading
# the "N plus one" problem refers to the many SELECT statements
# emitted when loading collections against a parent result

for user in session.query(User):
    print(user, user.addresses)

### slide:: p
# *eager loading* solves this problem by loading *all* collections
# at once.  selectinload is currently the most effective eager loader
# for collections.

session.rollback()  # so we can see the load happen again.

from sqlalchemy.orm import selectinload

for user in session.query(User).options(selectinload(User.addresses)):
    print(user, user.addresses)

### slide:: p
# joinedload() uses a LEFT OUTER JOIN or JOIN to load parent + child in one query.
# it is best tailored towards many-to-one relationships

session.rollback()

from sqlalchemy.orm import joinedload

for address_obj in session.query(Address).options(
    joinedload(Address.user, innerjoin=True)
):
    print(address_obj.email_address, address_obj.user.username)

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

### slide:: p
### Title: The basic idea of ORM query in 1.4 /2.0
# As Query has evolved for years to look more and more like a select(),
# the next step is that select() and Query() basically merge

from sqlalchemy.future import select as future_select

stmt = (
    future_select(User, Address.email_address)
    .join(User.addresses)
    .order_by(User.name, Address.email_address)
)

result = session.execute(stmt)

### slide:: p
# part of the reason is that people wanted more flexibility in how
# Query returns results.   so now the full Result object is returned, which
# allows for a method chained approach to customize how results are
# returned.

result.scalars().unique().all()

### slide:: p
# additionally, the strange duplication of query.filter() / select.where()
# is solved by making it all just select.where().

stmt = future_select(User).where(User.username == "spongebob")
result = session.execute(stmt)

user = result.scalar()

### slide:: p
# select() also gains features taken from the ORM, that now work in Core,
# like join() and filter_by().

stmt = future_select(User.__table__).join(Address).filter_by(username="sandy")

with engine.connect() as connection:
    result = connection.execute(stmt)

    result.all()


### slide::
### title:: Questions?


### slide::
