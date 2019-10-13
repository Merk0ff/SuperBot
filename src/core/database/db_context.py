import psycopg2
import datetime
from src.core.database.book import Book
from src.core.database.user import User
from src.core.database.rented_book_info import RentedBookInfo


class PostgresDbContext:
    def __init__(self, to_clear):
        self.conn = psycopg2.connect(dbname='selectel', user='postgres', password='mydb', host='185.91.53.8')
        self.crs = self.conn.cursor()

        crs = self.crs
        if to_clear:
            crs.execute("drop table if exists on_hands")
            crs.execute("drop table if exists vacations")
            crs.execute("drop table if exists lib")
            crs.execute("drop table if exists users")

        crs.execute("create table if not exists users ("
                    "id int primary key not null, "
                    "first_name varchar(100) not null, "
                    "second_name varchar(100) not null,"
                    "username varchar(100),"
                    "created_at timestamp not null)")
        crs.execute("create table if not exists lib ("
                    "id serial primary key not null,"
                    "name varchar(200) not null,"
                    "author varchar(100) not null,"
                    "amount int not null)")
        crs.execute("create table if not exists on_hands ("
                    "book_id int not null references lib(id),"
                    "user_id int not null references users(id),"
                    "start_date timestamp  not null,"
                    "end_date timestamp)")
        crs.execute("create table if not exists vacations ("
                    "user_id int not null references users(id),"
                    "start_date timestamp not null,"
                    "end_date timestamp not null,"
                    "constraint pk_vacations primary key (user_id, start_date))")

        self.conn.commit()

    def add_books(self, books):
        self.crs.executemany("insert into lib (name,author,amount) values (%s,%s,%s)", books)
        self.conn.commit()

    def add_book(self, book):
        self.crs.execute("insert into lib (name,author,amount) values (%s,%s,%s)", book)
        self.conn.commit()

    def get_books_from_lib(self, amount):
        self.crs.execute("select * from lib limit %s", [amount])
        return list(map(lambda x: Book(x[0], x[1], x[2], x[3]), self.crs.fetchall()))

    def get_books_by_name(self, name):
        self.crs.execute("select * from lib where name like %s", ['%' + name + '%'])
        return list(map(lambda x: Book(x[0], x[1], x[2], x[3]), self.crs.fetchall()))

    def get_rented_book_info(self, book_id):
        self.crs.execute("select * from on_hands where book_id=%s", [book_id])
        return list(map(lambda x: RentedBookInfo(x[0], x[1], x[2], x[3]), self.crs.fetchall()))

    def add_user(self, user):
        self.crs.execute(
            "insert into users (id, first_name, second_name, username, created_at) values (%s,%s,%s,%s,%s)", user)
        self.conn.commit()

    def add_users(self, users):
        self.crs.executemany(
            "insert into users (id, first_name, second_name, username, created_at) values (%s,%s,%s,%s,%s)", users)
        self.conn.commit()

    def rent_book(self, book_id, user_id):
        self.crs.execute("insert into on_hands (book_id,user_id,start_date) values (%s,%s,%s)", [book_id, user_id, datetime.datetime.now()])
        self.conn.commit()

    def return_book(self, book_id, user_id):
        self.crs.execute("delete from on_hands where book_id=%s and user_id=%s", [book_id,user_id])
        self.conn.commit()

    def get_users(self):
        self.crs.execute("select * from users")
        return list(map(lambda x: User(x[0], x[1], x[2], x[3], x[4]), self.crs.fetchall()))

    def get_user(self, bot_id):
        self.crs.execute("select * from users where id=%s", [bot_id])
        return list(map(lambda x: User(x[0], x[1], x[2], x[3], x[4]), self.crs.fetchall()))[0]

    def get_user(self, last_name, given_name):
        if given_name is not 0:
            self.crs.execute("select * from users where second_name=%s && first_name=%s", [last_name], [given_name])
        return list(map(lambda x: User(x[0], x[1], x[2], x[3], x[4]), self.crs.fetchall()))[0]

    def add_vacation(self, user_id, start, end):
        self.crs.execute("insert into vacations (user_id,start_date,end_date) values (%s,%s,%s)", [user_id, start, end])
        self.conn.commit()

    def remove_vacation(self, user_id, start):
        self.crs.execute("delete from vacations where user_id=%s and start_date=%s", [user_id, start])
        self.conn.commit()


db = PostgresDbContext(False)

# db.add_user([4, "fill", "notfill", "username", datetime.datetime.now()])

for usr in db.get_users():
    print(usr)

# print(len(db.get_rented_book_info(1)))
# db.rent_book(1, 16)
# print(len(db.get_books_by_name("book")))

