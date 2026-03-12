from db import db

class Author(db.Model):

    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150),unique=True)
    age = db.Column(db.Integer)
    phone = db.Column(db.String(10),unique=True)
    country = db.Column(db.String(100),nullable=False)
    role=db.Column(db.String(10),nullable=False)
    