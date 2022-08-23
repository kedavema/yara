from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "user"
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


class Emprendimiento(db.Model): 
    __tablename__ = "emprendimiento"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    imagen = db.Column(db.String )
    nombre = db.Column(db.String(250),nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    descripcion = db.Column(db.String(1000), nullable=False) 
    whatsapp = db.Column(db.String(10))
    telefono = db.Column(db.String(10), nullable=False)
    facebook = db.Column(db.String(100))
    instagram = db.Column(db.String(100))
    latitud = db.Column(db.String, nullable=False)
    longitud = db.Column(db.String, nullable=False)
    
    def __init__(self, user_id, imagen, nombre, categoria_id, descripcion, whatsapp, telefono, facebook, instagram, latitud, longitud):
        self.user_id = user_id
        self.imagen = imagen
        self.nombre = nombre
        self.categoria_id = categoria_id
        self.descripcion = descripcion
        self.whatsapp = whatsapp
        self.telefono = telefono
        self.facebook = facebook
        self.instagram = instagram
        self.latitud = latitud
        self.longitud = longitud
    
    @classmethod
    def create(cls, user_id, imagen, nombre, categoria_id, descripcion, whatsapp, telefono, facebook, instagram, latitud, longitud):
        emp = Emprendimiento(user_id, imagen, nombre, categoria_id, descripcion, whatsapp, telefono, facebook, instagram, latitud, longitud)
        return emp.save()

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Emprendimiento.query.all()

class Categoria(db.Model): 
    __tablename__ = "categoria"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(), nullable=False)
    
    def __init__(self, nombre):
        self.nombre = nombre

    @classmethod
    def create(cls, nombre):
        cat = Categoria(nombre=nombre)
        return cat.save()
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Categoria.query.all()
