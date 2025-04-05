from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.usuario import Usuario
from functools import wraps


auth_bp = Blueprint('auth', __name__)

def login_requerido(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Por favor inicia sesión para acceder a esta página', 'error')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/')
def index():

    if 'usuario_id' in session:
        return redirect(url_for('auth.dashboard'))
    return render_template('index.html')


@auth_bp.route('/registro', methods=['POST'])
def registro():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    errores = []
    
    if not nombre:
        errores.append('El nombre es obligatorio')
    elif len(nombre) < 2:
        errores.append('El nombre debe tener al menos 2 caracteres')
    elif not nombre.replace(' ', '').isalpha():
        errores.append('El nombre solo debe contener letras')
    
    if not apellido:
        errores.append('El apellido es obligatorio')
    elif len(apellido) < 2:
        errores.append('El apellido debe tener al menos 2 caracteres')
    elif not apellido.replace(' ', '').isalpha():
        errores.append('El apellido solo debe contener letras')
    
    if not email:
        errores.append('El email es obligatorio')
    elif '@' not in email or '.' not in email:
        errores.append('El formato del email no es válido')
    
    if not password:
        errores.append('La contraseña es obligatoria')
    elif len(password) < 8:
        errores.append('La contraseña debe tener al menos 8 caracteres')
    
    if password != confirm_password:
        errores.append('Las contraseñas no coinciden')
    
    if errores:
        for error in errores:
            flash(error, 'error')
        return redirect(url_for('auth.index'))
    
    usuario_existente = Usuario.buscar_por_email(email)
    if usuario_existente:
        flash('El email ya está registrado', 'error')
        return redirect(url_for('auth.index'))
    
    usuario_id = Usuario.crear(nombre, apellido, email, password)
    
    if usuario_id:
        session['usuario_id'] = usuario_id
        session['nombre'] = nombre
        
        flash('¡Registro exitoso!', 'success')
        return redirect(url_for('auth.dashboard'))
    else:
        flash('Ocurrió un error al registrar el usuario', 'error')
        return redirect(url_for('auth.index'))

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    if not email or not password:
        flash('Por favor ingresa email y contraseña', 'error')
        return redirect(url_for('auth.index'))
    
    usuario = Usuario.buscar_por_email(email)
    
    if not usuario or usuario.password != password:  
        flash('Credenciales inválidas', 'error')
        return redirect(url_for('auth.index'))
    
    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    
    flash('¡Inicio de sesión exitoso!', 'success')
    return redirect(url_for('auth.dashboard'))

@auth_bp.route('/dashboard')
@login_requerido
def dashboard():
    return render_template('dashboard.html', nombre=session['nombre'])

@auth_bp.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('nombre', None)
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('auth.index'))

