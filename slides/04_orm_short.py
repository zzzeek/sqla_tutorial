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
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)

    def __repr__(self):
        return "<User(%r, %r)>" % (
                self.name, self.fullname
            )

### slide::
# the User class now has a Table object associated with it.

User.__table__

### slide::
# The Mapper object mediates the relationship between User
# and the "user" Table object.

User.__mapper__

### slide::
# User has a default constructor, accepting field names
# as arguments.

ed_user = User(name='ed', fullname='Edward Jones')

### slide::
# The "id" field is the primary key, which starts as None
# if we didn't set it explicitly.

print(ed_user.name, ed_user.fullname)
print(ed_user.id)

### slide:: p
# The MetaData object is here too, available from the Base.

from sqlalchemy import create_engine
engine = create_engine('sqlite://')
Base.metadata.create_all(engine)

### slide::
# To persist and load User objects from the database, we
# use a Session object.

from sqlalchemy.orm import Session
session = Session(bind=engine)

### slide::
# new objects are placed into the Session using add().
session.add(ed_user)

### slide:: pi
# the Session will *flush* *pending* objects
# to the database before each Query.

our_user = session.query(User).filter_by(name='ed').first()
our_user

### slide::
# the User object we've inserted now has a value for ".id"
print(ed_user.id)

### slide::
# the Session maintains a *unique* object per identity.
# so "ed_user" and "our_user" are the *same* object

ed_user is our_user

### slide::
# Add more objects to be pending for flush.

session.add_all([
    User(name='wendy', fullname='Wendy Weathersmith'),
    User(name='mary', fullname='Mary Contrary'),
    User(name='fred', fullname='Fred Flinstone')
])

### slide::
# modify "ed_user" - the object is now marked as *dirty*.

ed_user.fullname = 'Ed Jones'

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

ed_user.fullname

### slide::
# Make another "dirty" change, and another "pending" change,
# that we might change our minds about.

ed_user.name = 'Edwardo'
fake_user = User(name='fakeuser', fullname='Invalid')
session.add(fake_user)

### slide:: p
# run a query, our changes are flushed; results come back.

session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()

### slide::
# But we're inside of a transaction.  Roll it back.
session.rollback()

### slide:: p
# ed_user's name is back to normal
ed_user.name

### slide::
# "fake_user" has been evicted from the session.
fake_user in session

### slide:: p
# and the data is gone from the database too.

session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all()

### slide::
### title:: Exercises - Basic Mapping
#
# 1. Create a class/mapping for this table, call the class Network
#
# CREATE TABLE network (
#      network_id INTEGER PRIMARY KEY,
#      name VARCHAR(100) NOT NULL,
# )
#
# 2. emit Base.metadata.create_all(engine) to create the table
#
# 3. commit a few Network objects to the database:
#
# Network(name='net1'), Network(name='net2')
#
#

### slide::
### title:: ORM Querying
# The attributes on our mapped class act like Column objects, and
# produce SQL expressions.

print(User.name == "ed")

### slide:: p
# These SQL expressions are compatible with the select() object
# we introduced earlier.

from sqlalchemy import select

sel = select([User.name, User.fullname]).\
        where(User.name == 'ed').\
        order_by(User.id)

session.connection().execute(sel).fetchall()


### slide:: p
# but when using the ORM, the Query() object provides a lot more functionality,
# here selecting the User *entity*.

query = session.query(User).filter(User.name == 'ed').order_by(User.id)

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

for name, in session.query(User.name).\
                filter_by(fullname='Ed Jones'):
    print(name)

### slide:: p
# or filter(), which is more flexible

for name, in session.query(User.name).\
                filter(User.fullname == 'Ed Jones'):
    print(name)

### slide:: p
# conjunctions can be passed to filter() as well

from sqlalchemy import or_

for name, in session.query(User.name).\
                filter(or_(User.fullname == 'Ed Jones', User.id < 5)):
    print(name)

### slide::
# multiple filter() calls join by AND just like select().where()

for user in session.query(User).\
                        filter(User.name == 'ed').\
                        filter(User.fullname == 'Ed Jones'):
    print(user)

### slide::
# Query has some variety for returning results

query = session.query(User).filter_by(fullname='Ed Jones')

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

query = session.query(User).filter_by(fullname='nonexistent')
query.one()

### slide:: p
# if there's more than one(), you get an error

query = session.query(User)
query.one()

### slide::
### title:: Exercises - ORM Querying
# 1. Produce a Query object representing the list of "fullname" values for
#    all User objects in alphabetical order.
#
# 2. call .all() on the query to make sure it works!
#
# 3. build a second Query object from the first that also selects
#    only User rows with the name "mary" or "ed".
#
# 4. return only the second row of the Query from #3.


### slide::
### title:: Joins and relationships
# A new class called Address, with a *many-to-one* relationship to User.

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    user = relationship("User", backref="addresses")

    def __repr__(self):
        return "<Address(%r)>" % self.email_address

### slide:: p
# create the new table.

Base.metadata.create_all(engine)

### slide::
# a new User object also gains an empty "addresses" collection now.

jack = User(name='jack', fullname='Jack Bean')
jack.addresses

### slide::
# populate this collection with new Address objects.

jack.addresses = [
                Address(email_address='jack@gmail.com'),
                Address(email_address='j25@yahoo.com'),
                Address(email_address='jack@hotmail.com'),
                ]

### slide::
# the "backref" sets up Address.user for each User.address.

jack.addresses[1]
jack.addresses[1].user

### slide::
# adding User->jack will *cascade* each Address into the Session as well.

session.add(jack)
session.new

### slide:: p
# commit.
session.commit()

### slide:: p
# After expiration, jack.addresses emits a *lazy load* when first
# accessed.
jack.addresses

### slide:: i
# the collection stays in memory until the transaction ends.
jack.addresses

### slide:: p
# collections and references are updated by manipulating objects,
# not primary / foreign key values.

fred = session.query(User).filter_by(name='fred').one()
jack.addresses[1].user = fred

fred.addresses

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

session.query(User.name).join(User.addresses).\
    filter(Address.email_address == 'jack@gmail.com').first()

### slide:: p
# we can specify an explicit FROM using select_from().

session.query(User, Address).select_from(Address).join(Address.user).all()

### slide:: p
# A query that refers to the same entity more than once in the FROM
# clause requires *aliasing*.

from sqlalchemy.orm import aliased

a1, a2 = aliased(Address), aliased(Address)
session.query(User).\
        join(a1).\
        join(a2).\
        filter(a1.email_address == 'jack@gmail.com').\
        filter(a2.email_address == 'jack@hotmail.com').\
        all()

### slide:: p
# We can also join with subqueries.  subquery() returns
# an "alias" construct for us to use.

from sqlalchemy import func

subq = session.query(
                func.count(Address.id).label('count'),
                User.id.label('user_id')
                ).\
                join(Address.user).\
                group_by(User.id).\
                subquery()

session.query(User.name, func.coalesce(subq.c.count, 0)).\
            outerjoin(subq, User.id == subq.c.user_id).all()

### slide::
### title:: Exercises
# 1. Run this SQL JOIN:
#
#    SELECT user.name, address.email_address FROM user
#    JOIN address ON user.id=address.user_id WHERE
#    address.email_address='j25@yahoo.com'
#
# 2. Tricky Bonus!  Select all pairs of distinct user names.
#    Hint: "... ON user_alias1.name < user_alias2.name"
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

for address in session.query(Address).\
                join(Address.user).\
                filter(User.name == 'jack').\
                options(joinedload(Address.user)):
    print(address, address.user)

### slide:: p
# to join() *and* joinedload() at the same time without using two
# JOIN clauses, use contains_eager()

from sqlalchemy.orm import contains_eager

for address in session.query(Address).\
                join(Address.user).\
                filter(User.name == 'jack').\
                options(contains_eager(Address.user)):
    print(address, address.user)

### slide:: p
### title:: Delete Cascades
# removing an Address sets its foreign key to NULL.
# We'd prefer it gets deleted.

jack = session.query(User).filter_by(name='jack').one()

del jack.addresses[0]
session.commit()

### slide::
# This can be configured on relationship() using
# "delete-orphan" cascade on the User->Address
# relationship.

User.addresses.property.cascade = "all, delete, delete-orphan"

### slide:: p
# Removing an Address from a User will now delete it.

fred = session.query(User).filter_by(name='fred').one()

del fred.addresses[0]
session.commit()

### slide:: p
# Deleting the User will also delete all Address objects.

session.delete(jack)
session.commit()

### slide::
### title:: Exercises - Final Exam !
# 1. Create a class called 'Account', with table "account":
#
#      id = Column(Integer, primary_key=True)
#      owner = Column(String(50), nullable=False)
#      balance = Column(Numeric, default=0)
#
# 2. Create a class "Transaction", with table "transaction":
#      * Integer primary key
#      * numeric "amount" column
#      * Integer "account_id" column with ForeignKey('account.id')
#
# 3. Add a relationship() on Transaction named "account", which refers
#    to "Account", and has a backref called "transactions".
#
# 4. Create a database, create tables, then insert these objects:
#
#      a1 = Account(owner='Jack Jones', balance=5000)
#      a2 = Account(owner='Ed Rendell', balance=10000)
#      Transaction(amount=500, account=a1)
#      Transaction(amount=4500, account=a1)
#      Transaction(amount=6000, account=a2)
#      Transaction(amount=4000, account=a2)
#
# 5. Produce a report that shows:
#     * account owner
#     * account balance
#     * summation of transaction amounts per account (should match balance)
#       A column can be summed using func.sum(Transaction.amount)
#
from sqlalchemy import Integer, String, Numeric

### slide::


