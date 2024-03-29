from flask import Flask, render_template, jsonify, flash
from flask import redirect, url_for
from flask_login import current_user,LoginManager, UserMixin,login_user, login_required, logout_user
from App.model import db, Quiz, Question, Option, User
app = Flask(__name__)
login_manager = LoginManager(app)

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
from App import route