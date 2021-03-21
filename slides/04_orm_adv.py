### slide::
### title:: Relationships, Joins, What's New ?
# start with the same mapping as before.  Except we will also
# give it a one-to-many **relationship** to a second entity.

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

mapper_registry = registry()


@mapper_registry.mapped
class User:
    __tablename__ = "user_account"

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


@mapper_registry.mapped
class Address:
    __tablename__ = "email_address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(%r)>" % self.email_address


### slide:: p
# Create tables

from sqlalchemy import create_engine

engine = create_engine("sqlite://")
with engine.begin() as connection:
    mapper_registry.metadata.create_all(connection)

### slide:: p
# Insert data into the User table. Here we illustrate the sessionmaker
# factory as a transactional context manager.

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine, future=True)

with Session.begin() as session:
    session.add_all(
        [
            User(username="spongebob", fullname="Spongebob Squarepants"),
            User(username="sandy", fullname="Sandy Cheeks"),
            User(username="patrick", fullname="Patrick Star"),
        ]
    )

### slide::
# a new User object also gains an empty "addresses" collection now.

squidward = User(username="squidward", fullname="Squidward Tentacles")
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

session = Session()

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

from sqlalchemy import select

spongebob = session.execute(
    select(User).filter_by(username="spongebob")
).scalar_one()
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
# a SELECT statement can select from multiple entities simultaneously.

stmt = select(User, Address).where(User.id == Address.user_id)

for row in session.execute(stmt):
    print(row)

### slide:: p
# As is the same case in Core, we use the select().join() method
# to create joins.   An entity can be given as the target which will
# join along foreign keys.

stmt = select(User, Address).join(Address)
session.execute(stmt).all()


### slide:: pi
# or you can give it an explicit SQL expression for the ON clause

stmt = select(User, Address).join(Address, User.id == Address.user_id)

session.execute(stmt).all()

### slide:: p
# however the most accurate and succinct way is to use the relationship-bound
# attribute.

stmt = (
    select(User, Address).
    join(User.addresses).
    where(Address.email_address == "squidward@gmail.com")
)

session.execute(stmt).first()

### slide:: p
# the ORM version of table.alias() is to use the aliased() function
# on a mapped entity.

from sqlalchemy.orm import aliased

a1, a2 = aliased(Address), aliased(Address)

stmt = (
    select(User).
    join_from(User, a1).
    join_from(User, a2).
    where(a1.email_address == "squidward@gmail.com").
    where(a2.email_address == "squidward@hotmail.com")
)

session.execute(stmt).all()

### slide:: p
# to join() to an aliased() object with more specificity, a form such
# as "Class.relationship.of_type(aliased)" may be used

stmt = (
    select(User).
    join(User.addresses.of_type(a1)).
    join(User.addresses.of_type(a2)).
    where(a1.email_address == "squidward@gmail.com").
    where(a2.email_address == "squidward@hotmail.com")
)

session.execute(stmt).all()

### slide:: p
# As was the case with Core, we can use subqueries and joins
# with ORM mapped classes as well.

from sqlalchemy import func

subq = (
    select(func.count(Address.id).label("count"), Address.user_id)
    .group_by(Address.user_id)
    .subquery()
)

stmt = (
    select(User.username, func.coalesce(subq.c.count, 0)).
    outerjoin(subq, User.id == subq.c.user_id)
)
session.execute(stmt).all()

### slide::
# Questions before the next section?

### slide:: p
### title:: Eager Loading
# the "N plus one" problem is an ORM issue which refers to the many SELECT
# statements emitted when loading collections against a parent result.
# As SQLAlchemy is a full featured ORM, we of course include this! :)

with Session() as session:
    for user in session.execute(
        select(User)
    ).scalars():
        print(user, user.addresses)

### slide:: p
# However, SQLAlchemy was designed from the start to tame the "N plus one"
# problem by implementing **eager loading**.  Eager loading is now very mature,
# and the most effective strategy for collections is currently the
# **selectinload** option.

from sqlalchemy.orm import selectinload

with Session() as session:
    for user in session.execute(
        select(User).
        options(
            selectinload(User.addresses)
        )
    ).scalars():
        print(user, user.addresses)

### slide:: p
# The oldest eager loading strategy is joinedload().  This uses a LEFT OUTER
# JOIN or INNER JOIN to load parent + child in one query.  joinedload() can
# work for collections as well, however it is best tailored towards many-to-one
# relationships, particularly those where the foreign key is "not null".

from sqlalchemy.orm import joinedload

with Session() as session:
    for address_obj in session.execute(
        select(Address).
        options(
            joinedload(Address.user, innerjoin=True)
        )
    ).scalars():
        print(address_obj.email_address, address_obj.user.username)

### slide:: p
### title:: Instant Zen of Eager Loading
# eager loading *does not* change the *result* of the Query.
# only how related collections are loaded.   An explicit join()
# can be mixed with the joinedload() and they are kept separate

with Session() as session:
    for address in session.execute(
        select(Address)
        .join(Address.user)
        .where(User.username == "squidward")
        .options(joinedload(Address.user))
    ).scalars():
        print(address, address.user)

### slide:: p
# To optimize the common case of "join to many-to-one and also load it on
# the object", the contains_eager() option is used

from sqlalchemy.orm import contains_eager

with Session() as session:
    for address in session.execute(
        select(Address)
        .join(Address.user)
        .where(User.username == "squidward")
        .options(contains_eager(Address.user))
    ).scalars():
        print(address, address.user)



### slide::
### title:: Questions?


### slide::
