from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.usuario_model import Usuario

usuario_controller = Blueprint('usuario', __name__, url_prefix='/usuarios')

@usuario_controller.route('/')
def index():
    usuario = Usuario()
    usuarios = usuario.get_all()
    return render_template('usuarios/index.html', usuarios=usuarios)

@usuario_controller.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        
        usuario = Usuario(nombre=nombre, apellido=apellido, email=email)
        usuario.create()
        
        flash('Usuario creado exitosamente ¡Felicidades!')
        return redirect(url_for('usuarios.index'))
    
    return render_template('usuarios/nuevo.html')

@usuario_controller.route('/<int:id>')
def mostrar(id):
    usuario = Usuario()
    usuario_data = usuario.get_by_id(id)
    return render_template('usuarios/mostrar.html', usuario=usuario_data)