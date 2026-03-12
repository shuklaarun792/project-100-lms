from flask import Flask, render_template, request, redirect, flash, session, url_for
from sqlalchemy import text

from models import *
from models.student_model import Student
from models.author_model import Author

from routes.students_routes import student_bp
from routes.books_route import book_bp
from routes.author_route import author_bp

from db import db
from config import Config

from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.secret_key = "library_secret_key"

# Config
app.config.from_object(Config)

# DB
db.init_app(app)

# Migration
migrate = Migrate(app, db)

# Bcrypt
bcrypt = Bcrypt(app)


# ---------------------
# DB Health
# ---------------------

@app.route("/db-health")
def db_health():
    try:
        db.session.execute(text("SELECT 1"))
        return {"status":"ok","database":"Connected"}
    except Exception as e:
        return {"status":str(e)}


# ---------------------
# HOME
# ---------------------

@app.route("/")
def home():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("home.html")


# ---------------------
# LOGIN
# ---------------------

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        # student login
        student = Student.query.filter_by(stu_email=email).first()

        if student and bcrypt.check_password_hash(student.stu_pass, password):

            session["user"] = student.stu_name
            session["role"] = "student"

            return redirect(url_for("home"))


        # author login
        author = Author.query.filter_by(email=email).first()

        if author and bcrypt.check_password_hash(author.password, password):

            session["user"] = author.author_name
            session["role"] = "author"

            return redirect(url_for("home"))


        flash("Invalid Email or Password")


    return render_template("login.html")


# ---------------------
# LOGOUT
# ---------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ---------------------
# Register Blueprints
# ---------------------

app.register_blueprint(student_bp, url_prefix="/student")
app.register_blueprint(book_bp, url_prefix="/book")
app.register_blueprint(author_bp, url_prefix="/author")


# ---------------------
# Run Server
# ---------------------

if __name__ == "__main__":
    app.run(debug=True)