from flask import Blueprint, render_template, request
from models.student_model import Student
from db import db

student_bp = Blueprint("student", __name__)


# -------------------------
# Student Registration
# -------------------------

@student_bp.route("/student-register", methods=["GET", "POST"])
def register_student():

    if request.method == "POST":

        name = request.form.get("student_name")
        age = request.form.get("age")
        email = request.form.get("email")
        phone = request.form.get("phone")
        address = request.form.get("address")

        new_student = Student(
            stu_name=name,
            stu_age=age,
            stu_email=email,
            stu_phone=phone,
            stu_address=address
        )

        db.session.add(new_student)
        db.session.commit()

        print("Student saved successfully")

    return render_template("students/student-register.html")


# -------------------------
# All Students Page
# -------------------------

@student_bp.route("/all-students")
def all_students():

    students = Student.query.all()   # select * from student

    return render_template("students/all_students.html", students=students)


@student_bp.route("/student-details/<int:id>")
def student_details(id):

    student = Student.query.get(id)

    return render_template("students/student-details.html", student=student)



@student_bp.route("/delete-student/<int:id>")
def delete_student(id):

    student = Student.query.get(id)

    db.session.delete(student)
    db.session.commit()

    return redirect("/student/all-students")




# -------------------------
# Edit Student
# -------------------------

@student_bp.route("/edit-student/<int:id>", methods=["GET","POST"])
def edit_student(id):

    student = Student.query.get(id)

    if request.method == "POST":

        student.stu_name = request.form.get("student_name")
        student.stu_age = request.form.get("age")
        student.stu_email = request.form.get("email")
        student.stu_phone = request.form.get("phone")
        student.stu_address = request.form.get("address")

        db.session.commit()

        return redirect("/student/all-students")

    return render_template("students/edit-student.html", student=student)