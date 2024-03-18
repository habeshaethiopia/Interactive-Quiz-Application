#!/usr/bin/env python3
''' model .py'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
db = SQLAlchemy()

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    questions = relationship('Question', backref='quiz', cascade='all, delete-orphan')
    # questions = db.relationship('Question', backref='quiz', lazy=True)

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    options = db.relationship('Option', backref='question', cascade='all, delete-orphan')
    

class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)