#! /usr/bin/env python3
"""A module to import quizes
    from a json file"""

import json
from app import app

from model import db, Quiz, Question, Option
def import_quiz_data():
    with app.app_context():
        with open("quiz_data.json", "r") as file:
            quizzes = json.load(file)
            for quiz_data in quizzes:
                quiz = Quiz(title=quiz_data["title"], description=quiz_data["description"])
                db.session.add(quiz)
                db.session.commit()

                for question_data in quiz_data["questions"]:
                    question = Question(content=question_data["content"], quiz_id=quiz.id)
                    db.session.add(question)
                    db.session.commit()

                    for option_data in question_data["options"]:
                        option = Option(
                            content=option_data["content"],
                            is_correct=option_data["is_correct"],
                            question_id=question.id,
                        )
                        db.session.add(option)
                        db.session.commit()


if __name__ == "__main__":
    import_quiz_data()
