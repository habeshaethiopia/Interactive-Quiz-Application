#!/usr/bin/env python3
from App.forms import RegistrationForm, LoginForm  # Import forms
from App.utils import hash_password
from App import app, login_manager
from App.model import db, Quiz, Question, Option, User
from flask_login import current_user,LoginManager, UserMixin,login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from flask import redirect, url_for, request, session, make_response
from flask import Flask, render_template, jsonify, flash

@app.route("/",strict_slashes=False)
def index():
    # Retrieve quizzes from the database
    if current_user.is_authenticated:
        quizzes = Quiz.query.all()
        return render_template("index.html", quizzes=quizzes)
    return redirect(url_for('login'))

@app.route("/quiz",strict_slashes=False)
@login_required
def quiz():
    quizzes = Quiz.query.all()
    return render_template("quiz.html", quizzes=quizzes)
@app.route("/quiz/<int:quiz_id>",strict_slashes=False)
@login_required
def display_quiz(quiz_id):
    # Retrieve quiz data from the database based on the quiz_id
    quiz = Quiz.query.get_or_404(quiz_id)
    # Pass quiz data to the template
    quiz_dict = {
        'title': quiz.title,
        'description': quiz.description,
        'questions': [
            {
                'content': question.content,
                'options': [option.content for option in question.options],
                'answer': [answer.content for answer in question.options if answer.is_correct]
            }
            for question in quiz.questions
        ]
    }
    print(jsonify(quiz_dict))
    return render_template("takeQuiz.html", quiz=quiz_dict)




@app.route("/quiz/<int:quiz_id>/delete", methods=["POST"],strict_slashes=False)
@login_required
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


@app.route("/register", methods=["GET", "POST"],strict_slashes=False)
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data

        # Check if the username already exists in the database
        if User.query.filter_by(username=username).first():
            return render_template(
                "register.html", form=form, error="Username already exists"
            )

        # Create a new User object and add it to the database
        new_user = User(username=username, password=hash_password(password))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
       
    return render_template("register.html", form=form)


# Login: User login endpoint
@app.route("/login", methods=["GET", "POST"],strict_slashes=False)
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
            login_user(user)
            # Set a cookie for the user
            return redirect(url_for("index"))
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))

    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))


@app.route('/users',strict_slashes=False)
def user():
    users = User.query.all()
    # Convert the users into a list of dictionaries so it can be JSON serialized
    users_list =[{ "id": user.id, "username": user.username, "created_at": user.created_at, "updated_at": user.updated_at} for user in users]

    # Return the users as a JSON response
    return jsonify(users_list)
# Logout route
@app.route('/logout',strict_slashes=False)
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
