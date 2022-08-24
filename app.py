from flask import Flask, render_template, redirect, url_for, request
from flask_login import current_user, LoginManager, login_manager, login_user, logout_user, login_required
from config import config
from models import Categoria, db, User, Emprendimiento
from forms import LoginForm, SignupForm
import os 


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(environment)
    SECRET_KEY = os.urandom(32)
    app.config["SECRET_KEY"] = SECRET_KEY
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app
    
environment = "config.DevelopmentConfig"
app =create_app(environment)


# Ruta principal
@app.route("/")
#@login_required
def index():
    emprendimientos = Emprendimiento.get_all()
    return render_template("index.html", emprendimientos=emprendimientos)


# Ruta para el registro de las emprendedoras
@app.route("/signup", methods = ["POST", "GET"])
def signup ():
    # si el usuario ya esta registrado se lo redirige al inicio
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form =SignupForm()
    if form.validate_on_submit():
        #capturamos los datos del usuario
        fullname = form.fullname.data
        email = form.email.data
        ci = form.ci.data
        password = form.password.data
        #creamos usuario y guardamos en la base de datos
        user = User(fullname=fullname, email=email,ci=ci)
        user.set_password(password)
        user.save()
        return redirect(url_for("index"))    
    return render_template("signup.html", form=form)

@app.login_manager.user_loader
def load_user(user_id):
    return User.get_by_id((user_id))


# Ruta para el login
@app.route("/login", methods = ["POST", "GET"])
def login ():
    if current_user.is_authenticated:
        return redirect(url_for("index")) 
    form = LoginForm()
    if form.validate_on_submit:
        ci = form.ci.data
        user = User.get_by_ci(ci)
        password = form.password.data
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
        
    return render_template("login.html", form=form)


# Ruta para logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect (url_for("index"))


# Ruta para crear un emprendimiento
@app.route('/crear-emprendimiento', methods = ['GET', 'POST'])
def registros():
    if request.method == 'POST':
        user_id = current_user.id
        imagen = request.files['imagen']
        filename = imagen.filename
        nombre = request.form['nombre']
        categoria_id = request.form['categoria']
        descripcion = request.form['descripcion']
        whatsapp = request.form['whatsapp']
        telefono = request.form['telefono']
        facebook = request.form['facebook']
        instagram = request.form['instagram']
        latitud = request.form['latitud']
        longitud = request.form['longitud']
        
        Emprendimiento.create(user_id, filename, nombre, categoria_id, descripcion, whatsapp, telefono, facebook, instagram, latitud, longitud)
        imagen.save(f"static/emprendimientos/{filename}")
        return redirect(url_for('index')) #mientras redireccionamos al index donde luego listaremos todos los emprendimientos
    categorias = Categoria.get_all()
    return render_template("crear_emprendimiento.html", categorias=categorias)


# Ruta para listar los emprendimientos
@app.route('/emprendimientos')
def emprendimientos():
    emprendimiento = Emprendimiento.query.all() 
    return render_template('emprendimientos.html, emprendimientos = emprendimientos')
