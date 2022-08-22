from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(250))
    email = db.Column(db.String(100), unique=True)
    ci = db.Column (db.Integer, unique =True)
    password = db.Column (db.String(100))

    def __init__(self, fullname, email, ci):
        self.fullname = fullname
        self.email = email
        self.ci = ci


    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def set_password(self, password):
        self.password = generate_password_hash(password) 
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_by_ci(ci):
        return User.query.filter_by(ci = ci). first()

    @staticmethod
    def get_by_id(id):
        return User.query.filter_by(id = id). first()

    @staticmethod
    def get_all():
        return User.query.all()