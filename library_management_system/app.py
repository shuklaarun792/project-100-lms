from flask import Flask, render_template
from sqlalchemy import text
from models import*

from routes.students_routes import student_bp
from routes.books_route import book_bp
from routes.author_route import author_bp

from db import db
from config import Config

from flask_migrate import Migrate


app = Flask(__name__)

# Config load
app.config.from_object(Config)

# Database initialize
db.init_app(app)

# Migration initialize
migrate = Migrate(app, db)


@app.route("/db-health")
def db_health():
    try:
        db.session.execute(text("SELECT 1"))
        return{"status":"ok","database":"Connected"}
    except Exception as e:
        return {"status":str(e)}

@app.route("/")
def home():
    return render_template("home.html")


# Register Blueprints
app.register_blueprint(student_bp, url_prefix="/student")
app.register_blueprint(book_bp, url_prefix="/book")
app.register_blueprint(author_bp, url_prefix="/author")


if __name__ == "__main__":
    app.run(debug=True)