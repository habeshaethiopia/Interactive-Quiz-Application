#!/usr/bin/env python3

from flask import Flask, render_template
from model import db, Quiz, Question, Option, User
from flask import redirect, url_for, request, session, make_response
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm  # Import forms
from utils import hash_password

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz.db"
app.config["SECRET_KEY"] = "IjA3ZGI2Zjc3YjI1Y2E0NGZkZTY1ZmRmYjBlZWExNjQ0MGFiNzgw"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
from flask_wtf.csrf import CSRFProtect

# Initialize CSRF protection
db.init_app(app)
csrf = CSRFProtect(app)

# Create database tables
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    # Retrieve quizzes from the database
    quizzes = Quiz.query.all()
    return render_template("index.html", quizzes=quizzes)


@app.route("/quiz/<int:quiz_id>")
def display_quiz(quiz_id):
    # Retrieve quiz data from the database based on the quiz_id
    quiz = Quiz.query.get_or_404(quiz_id)
    # Pass quiz data to the template
    return render_template("quiz.html", quiz=quiz)


from flask import redirect, url_for


@app.route("/quiz/<int:quiz_id>/delete", methods=["POST"])
def delete_quiz(quiz_id):
    # Retrieve the quiz from the database
    quiz = Quiz.query.get_or_404(quiz_id)

    # Delete associated questions
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    for question in questions:
        db.session.delete(question)

    # Delete the quiz
    db.session.delete(quiz)
    db.session.commit()

    # Redirect to the main quiz list page
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data

        # Check if the username already exists in the database
        if User.query.filter_by(username=username).first():
            print(" ")
            return render_template(
                "register.html", form=form, error="Username already exists"
            )

        # Create a new User object and add it to the database
        new_user = User(username=username, password=hash_password(password))
        db.session.add(new_user)
        db.session.commit()

        # Store the user ID in the session
        session["user_id"] = new_user.id
        # Set a cookie for the user
        response = make_response(redirect(url_for("index")))
        response.set_cookie("user_id", str(new_user.id))
        return response

    return render_template("register.html", form=form)


# Login: User login endpoint
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data

        # Retrieve the user from the database
        user = User.query.filter_by(username=username).first()

        # Verify the password
        if user and user.check_password(password):
            # Store the user ID in the session
            session["user_id"] = user.id
            # Set a cookie for the user
            response = make_response(redirect(url_for("index")))
            response.set_cookie("user_id", str(user.id))

            return response  # Redirect to the main page after login

    return render_template(
        "login.html", form=form, error="Invalid username or password"
    )


# Logout route
@app.route("/logout")
def logout():
    session.clear()  # Clear the session
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
