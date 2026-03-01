import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from forms import PiezaForm, RegistroForm, LoginForm
from functools import wraps
import bcrypt

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Conexión a MongoDB
MONGO_URI = os.getenv('MONGO_URI')
cliente = MongoClient(MONGO_URI)
db = cliente['autopartes']          # Base de datos
coleccion = db['piezas']             # Colección de piezas
usuarios = db['usuarios']            # Colección para autenticación

# Decorador para rutas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# -------------------- RUTAS PÚBLICAS --------------------

@app.route('/')
def inicio():
    # Estadística: número de piezas en catálogo
    total_piezas = coleccion.count_documents({})
    return render_template('inicio.html', total=total_piezas)

@app.route('/catalogo')
def catalogo():
    piezas = list(coleccion.find({}, {'_id': 0}))  # Excluimos _id para simplificar
    return render_template('read.html', piezas=piezas)

# -------------------- CRUD (solo para usuarios autenticados) --------------------

@app.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva():
    form = PiezaForm()
    if form.validate_on_submit():
        pieza = {
            'nombre': form.nombre.data,
            'descripcion': form.descripcion.data,
            'precio': float(form.precio.data),
            'stock': int(form.stock.data),
            'categoria': form.categoria.data
        }
        coleccion.insert_one(pieza)
        flash('Pieza añadida correctamente', 'success')
        return redirect(url_for('catalogo'))
    return render_template('add.html', form=form)

@app.route('/editar/<nombre>', methods=['GET', 'POST'])
@login_required
def editar(nombre):
    pieza = coleccion.find_one({'nombre': nombre})
    if not pieza:
        flash('Pieza no encontrada', 'danger')
        return redirect(url_for('catalogo'))
    form = PiezaForm(data=pieza)
    if form.validate_on_submit():
        nuevos_valores = {
            'nombre': form.nombre.data,
            'descripcion': form.descripcion.data,
            'precio': float(form.precio.data),
            'stock': int(form.stock.data),
            'categoria': form.categoria.data
        }
        coleccion.update_one({'nombre': nombre}, {'$set': nuevos_valores})
        flash('Pieza actualizada', 'success')
        return redirect(url_for('catalogo'))
    return render_template('update.html', form=form, pieza=pieza)

@app.route('/eliminar/<nombre>')
@login_required
def eliminar(nombre):
    pieza = coleccion.find_one({'nombre': nombre})
    if not pieza:
        flash('Pieza no encontrada', 'danger')
        return redirect(url_for('catalogo'))
    return render_template('remove.html', pieza=pieza)

@app.route('/confirmar_eliminar/<nombre>', methods=['POST'])
@login_required
def confirmar_eliminar(nombre):
    coleccion.delete_one({'nombre': nombre})
    flash('Pieza eliminada', 'success')
    return redirect(url_for('catalogo'))

# -------------------- AUTENTICACIÓN --------------------

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        if usuarios.find_one({'usuario': form.usuario.data}):
            flash('El nombre de usuario ya está registrado', 'danger')
        else:
            hashed = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
            usuarios.insert_one({
                'usuario': form.usuario.data,
                'password': hashed
            })
            flash('Registro exitoso, ya puedes iniciar sesión', 'success')
            return redirect(url_for('login'))
    return render_template('registro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = usuarios.find_one({'usuario': form.usuario.data})
        if usuario and bcrypt.checkpw(form.password.data.encode('utf-8'), usuario['password']):
            session['usuario'] = form.usuario.data
            flash('Sesión iniciada', 'success')
            return redirect(url_for('inicio'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada', 'info')
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)