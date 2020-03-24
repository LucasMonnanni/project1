from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv

engine = create_engine('postgres://aknoifscbjkggf:5bba853b0d6903168703fdab85cf9d10817478f1eea77080ab6deda2cb479365@ec2-52-200-119-0.compute-1.amazonaws.com:5432/dfol2tolo2l87h')
db = scoped_session(sessionmaker(bind=engine))

# f = open('books.csv')
# dialect = csv.Sniffer().sniff(f.read())
# f.seek(0)
# reader = csv.reader(f, dialect='unix')
# for line in reader:
#     if len(line)==4:
#         db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {'isbn': line[0], 'title': line[1], 'author': line[2], 'year': int(line[3])})
#
# db.commit()

db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, password VARCHAR NOT NULL)")
