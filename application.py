import os, flask, csv
from requests import *
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = flask.Flask(__name__)
grkey = 'zLFuXqj995fTRUsM5pxA'
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET"])
def index():
    return flask.render_template('index.html')

@app.route("/", methods=["POST"])
def main():

    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    if db.execute("SELECT id FROM users WHERE username = :username AND password = :password;", {"username":username, "password":password}).rowcount != 0 :
        reviews = db.execute("SELECT username, author, title, score, review FROM reviews r INNER JOIN books b ON book_id=b.id INNER JOIN users u ON user_id=u.id ORDER BY r.id DESC LIMIT 10;")
        return flask.render_template('main.html', username = username, latest_reviews = reviews)
    else:
        return flask.render_template('signin.html', error="Wrong username or password.")


@app.route("/about")
def about():
    return flask.render_template('about.html')

@app.route("/signin")
def signin():
    return flask.render_template('signin.html')

@app.route("/register")
def register():
    return flask.render_template('register.html')

@app.route("/registration", methods=['POST'])
def registration():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    if db.execute("SELECT * FROM users WHERE username = :username", {"username":username}).rowcount == 0:
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {"username":username, "password":password})
        db.commit()
        return flask.redirect(flask.url_for('main'), code="307")
    else:
        return flask.render_template('register.html', error="Username already exists.")

@app.route("/users/", methods=['POST'])
def profile():
    pass

@app.route("/libraries/", methods=['POST'])
def library():
    pass

@app.route("/reviews/", methods=['POST'])
def reviews():
    if mode=='mine':
        reviews = db.execute("SELECT username, author, title, score, review FROM reviews r \
        INNER JOIN books b ON book_id=b.id INNER JOIN users u ON user_id=u.id ORDER BY r.id DESC")
        return flask.render_template('main.html', username = username, reviews = reviews)
    else:
        reviews = db.execute("SELECT username, author, title, score, review FROM reviews r \
        INNER JOIN books b ON book_id=b.id INNER JOIN users u ON user_id=u.id ORDER BY r.id DESC WHERE username = :username", {"username":username})
        return flask.render_template('main.html', username = username, reviews = reviews)
