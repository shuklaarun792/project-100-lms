from flask import Blueprint, render_template, request, redirect, flash
from models.author_model import Author
from db import db

author_bp = Blueprint("author", __name__)


# Register Author

@author_bp.route("/author-register", methods=["GET","POST"])
def author_register():

    if request.method == "POST":

        name = request.form.get("author_name")
        email = request.form.get("email")
        age = request.form.get("age")
        phone = request.form.get("phone")
        country = request.form.get("country")

        new_author = Author(
            author_name=name,
            email=email,
            age=age,
            phone=phone,
            country=country,
            role="Author"
        )

        db.session.add(new_author)
        db.session.commit()

        flash("Author added successfully!", "success")

    return render_template("author/author-register.html")


# All Authors

@author_bp.route("/all-authors")
def all_authors():

    authors = Author.query.all()

    return render_template("author/all_authors.html", authors=authors)


# Author Details

@author_bp.route("/author-details/<int:id>")
def author_details(id):

    author = Author.query.get(id)

    return render_template("author/author-details.html", author=author)


# Edit Author

@author_bp.route("/edit-author/<int:id>", methods=["GET","POST"])
def edit_author(id):

    author = Author.query.get(id)

    if request.method == "POST":

        author.author_name = request.form.get("author_name")
        author.age = request.form.get("age")
        author.email = request.form.get("email")
        author.phone = request.form.get("phone")
        author.country = request.form.get("country")

        db.session.commit()
        flash("Author updated successfully!", "success")
        return redirect("/author/all-authors")

    return render_template("author/edit-author.html", author=author)


# Delete Author

@author_bp.route("/delete-author/<int:id>")
def delete_author(id):

    author = Author.query.get(id)

    db.session.delete(author)
    db.session.commit()

    return redirect("/author/all-authors")