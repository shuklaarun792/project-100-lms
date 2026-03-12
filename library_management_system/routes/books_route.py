from flask import *
book_bp=Blueprint("book",__name__)

@book_bp.route("/book-register")
def book_register():
    return render_template("book/book-register.html")


@book_bp.route("/all-books")
def all_books():

    books = Book.query.all()

    return render_template("books/all_books.html", books=books)