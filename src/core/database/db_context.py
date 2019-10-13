import psycopg2
import datetime
from src.core.database.book import Book
from src.core.database.user import User
from src.core.database.rented_book_info import RentedBookInfo
from src.core.database.vacation import Vacation


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
                    "created_at timestamp not null,"
                    "salary_date timestamp,"
                    "salary float,"
                    "position varchar(100))")
        crs.execute("create table if not exists lib ("
                    "id serial primary key not null,"
                    "name varchar(200) not null,"
                    "author varchar(100) not null,"
                    "amount int not null)")
        crs.execute("create table if not exists on_hands ("
                    "book_id int not null,"
                    "user_id int not null,"
                    "start_date timestamp  not null,"
                    "end_date timestamp,"
                    "constraint fk_user_id foreign key (user_id) references users(id) on delete cascade, "
                    "constraint fk_book_id foreign key (book_id) references lib(id) on delete cascade)")
        crs.execute("create table if not exists vacations ("
                    "user_id int not null,"
                    "start_date timestamp not null,"
                    "end_date timestamp not null,"
                    "constraint pk_vacations primary key (user_id, start_date),"
                    "constraint fk_user_id foreign key (user_id) references users(id) on delete cascade)")

        self.conn.commit()

    # book_id will be ignored
    def add_books(self, books):
        data = list(map(lambda x: [x.name.lower(), x.author.lower(), x.amount], books))
        self.crs.executemany("insert into lib (name,author,amount) values (%s,%s,%s)", data)
        self.conn.commit()

    # book_id will be ignored
    def add_book(self, book):
        self.crs.execute("insert into lib (name,author,amount) values (%s,%s,%s)", [book.name.lower(), book.author.lower(), book.amount])
        self.conn.commit()

    def get_books_from_lib(self, amount):
        self.crs.execute("select * from lib limit %s", [amount])
        return list(map(lambda x: Book(x[0], x[1], x[2], x[3]), self.crs.fetchall()))

    def get_books_by_name(self, name):
        self.crs.execute("select * from lib where name like %s", ['%' + name + '%'])
        return list(map(lambda x: Book(x[0], x[1], x[2], x[3]), self.crs.fetchall()))

    def get_books_by_author(self, author):
        self.crs.execute("select * from lib where author like %s", ['%' + author + '%'])
        return list(map(lambda x: Book(x[0], x[1], x[2], x[3]), self.crs.fetchall()))

    def get_rented_book_info(self, book_id):
        self.crs.execute("select * from on_hands where book_id=%s", [book_id])
        return list(map(lambda x: RentedBookInfo(x[0], x[1], x[2], x[3]), self.crs.fetchall()))

    def rent_book(self, book_id, user_id):
        self.crs.execute("insert into on_hands (book_id,user_id,start_date) values (%s,%s,%s)", [book_id, user_id, datetime.datetime.now()])
        self.conn.commit()

    def return_book(self, book_id, user_id):
        self.crs.execute("delete from on_hands where book_id=%s and user_id=%s", [book_id, user_id])
        self.conn.commit()

    def remove_book(self, book_id):
        self.crs.execute("delete from books where id=%s", [book_id])
        self.conn.commit()

    def add_user(self, user):
        self.crs.execute(
            "insert into users (id, first_name, second_name, username, created_at, salary_date, salary, position) values (%s,%s,%s,%s,%s,%s,%s,%s)",
            [user.bot_id, user.first_name.lower(), user.second_name.lower(), user.username, user.created_at, user.salary_date, user.salary,user.position])
        self.conn.commit()

    def add_users(self, users):
        data = list(map(lambda x: [x.bot_id, x.first_name.lower(), x.second_name.lower(), x.username, x.created_at, x.salary_date, x.salary, x.position], users))
        self.crs.executemany(
            "insert into users (id, first_name, second_name, username, created_at, salary_date, salary, position) values (%s,%s,%s,%s,%s,%s,%s,%s)", data)
        self.conn.commit()

    def get_users(self):
        self.crs.execute("select * from users")
        return list(map(lambda x: User(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7]), self.crs.fetchall()))

    def get_user(self, bot_id):
        self.crs.execute("select * from users where id=%s", [bot_id])
        x = self.crs.fetchone()
        if x is not None:
            return User(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])

    def remove_user(self, user_id):
        self.crs.execute("delete from users where id=%s", [user_id])
        self.conn.commit()

    def get_user_by_name(self, first_name, second_name):
        self.crs.execute("select * from users where first_name like %s and second_name like %s", ['%' + first_name + '%', '%' + second_name + '%'])
        x = self.crs.fetchone()
        if x is not None:
            return User(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7])

    def add_vacation(self, user_id, start, end):
        self.crs.execute("insert into vacations (user_id,start_date,end_date) values (%s,%s,%s)", [user_id, start, end])
        self.conn.commit()

    def remove_vacation(self, user_id):
        self.crs.execute("delete from vacations where user_id=%s", [user_id])
        self.conn.commit()

    def get_vacations(self, user_id):
        self.crs.execute("select * from vacations where user_id=%s", [user_id])
        return list(map(lambda x: Vacation(x[0], x[1], x[2]), self.crs.fetchall()))


db = PostgresDbContext(False)
# db.add_books([Book(0, "book5", "author5", 25), Book(1, "book4", "author4", 15)])
# db.add_user([4, "fill", "notfill", "username", datetime.datetime.now()])

# db.add_users([
#     User(1, "first1", "first1", "first1", datetime.datetime.now(), datetime.datetime.now(), 200, "п"),
#     User(2, "second2", "second2", "second2", datetime.datetime.now(), datetime.datetime.now(), 300, "c"),
#     User(3, "third3", "third3", "third3", datetime.datetime.now(), datetime.datetime.now(), 400, "aha")
# ])

# db.remove_user(1)

# db.add_books([
#     Book(0, "Властелин колец", "Толкин", 35),
#     Book(1, "Преступление и наказание", "Достоевский", 40),
#     Book(2, "Тихий дон", "Шолохов", 45),
# ])

# db.rent_book(3, 2)
# db.rent_book(3, 1)
# db.return_book(3, 1)

# db.remove_user(2)

# for bookRenterInfo in db.get_rented_book_info(3):
#     usr = db.get_user(bookRenterInfo.user_id)
#     print("Book %s rented by user %s %s from %s"
#           % (bookRenterInfo.book_id, usr.second_name, usr.first_name, bookRenterInfo.start_date))

# db.add_vacation(1, datetime.datetime.now(), datetime.datetime.now())
# db.add_vacation(2, datetime.datetime.now(), datetime.datetime.now())

# db.remove_vacation(1)

# for vacation in db.get_vacations(1):
#     print("Vacation of user %s, lasting from %s to %s date" % (vacation.user_id, vacation.start_date, vacation.end_date))

# for usr in db.get_users():
#     print("User %s with first_name %s, second_name %s, username %s, created at %s, salary date at %s and salary %s, position %s"
#           % (usr.bot_id, usr.first_name, usr.second_name, usr.username, usr.created_at, usr.salary_date, usr.salary, usr.position))

# usr = db.get_user_by_name("Сергей", "Собянин")
# print("User %s with first_name %s, second_name %s, username %s, created at %s, salary date at %s and salary %s"
#       % (usr.bot_id, usr.first_name, usr.second_name, usr.username, usr.created_at, usr.salary_date, usr.salary))

# for book in db.get_books_from_lib(100):
#     print("Book %s, named '%s' by author %s, amount = %s" % (book.book_id, book.name, book.author, book.amount))

# for book in db.get_books_by_author("тол"):
#     print("Book %s, named '%s' by author %s, amount = %s" % (book.book_id, book.name, book.author, book.amount))

# print(len(db.get_rented_book_info(1)))
# db.rent_book(1, 16)
# print(len(db.get_books_by_name("book")))

