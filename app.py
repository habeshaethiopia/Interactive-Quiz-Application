#!/usr/bin/env python3

from flask import Flask, render_template
from model import db, Quiz, Question, Option
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SECRET_KEY'] = 'IjA3ZGI2Zjc3YjI1Y2E0NGZkZTY1ZmRmYjBlZWExNjQ0MGFiNzgw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from flask_wtf.csrf import CSRFProtect

# Initialize CSRF protection
db.init_app(app)
# csrf = CSRFProtect(app)

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Retrieve quizzes from the database
    quizzes = Quiz.query.all()
    return render_template('index.html', quizzes=quizzes)
@app.route('/quiz/<int:quiz_id>')
def display_quiz(quiz_id):
    # Retrieve quiz data from the database based on the quiz_id
    quiz = Quiz.query.get_or_404(quiz_id)
    # Pass quiz data to the template
    return render_template('quiz.html', quiz=quiz)
from flask import redirect, url_for

@app.route('/quiz/<int:quiz_id>/delete', methods=['POST'])
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
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)