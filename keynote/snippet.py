# class is declared without any awareness of database
class User(object):
    def __init__(self, name, username):
        self.name = name
        self.username = username


# elsewhere, it's associated with a database table
mapper(
     User,
     Table("user", metadata,
           Column("name", String(50)),
           Column("fullname", String(100))
     )
)