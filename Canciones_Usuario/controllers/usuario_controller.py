from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.usuario_model import Usuario
from models.favorito_model import Favorito

usuario_blueprint = Blueprint('usuario', __name__, url_prefix='/usuarios')

@usuario_blueprint.route('/')
def index():
    usuario = Usuario()
    usuarios = usuario.get_all()
    return render_template('usuarios/index.html', usuarios=usuarios)

@usuario_blueprint.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        
        usuario = Usuario(nombre=nombre, email=email, password=password)
        usuario.create()
        
        flash('Usuario creado exitosamente')
        return redirect(url_for('usuario.index'))
    
    return render_template('usuarios/nuevo.html')

@usuario_blueprint.route('/<int:id>')
def mostrar(id):
    usuario = Usuario()
    usuario_data = usuario.get_by_id(id)
    
    favorito = Favorito()
    canciones_favoritas = favorito.get_favoritos_by_usuario(id)
    
    return render_template('usuarios/mostrar.html', 
                        usuario=usuario_data, 
                        canciones_favoritas=canciones_favoritas)

@usuario_blueprint.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    usuario = Usuario()
    
    if request.method == 'POST':
        usuario.id = id
        usuario.nombre = request.form['nombre']
        usuario.email = request.form['email']
        usuario.password = request.form['password']
        
        usuario.update()
        
        flash('Usuario actualizado exitosamente')
        return redirect(url_for('usuario.mostrar', id=id))
    
    usuario_data = usuario.get_by_id(id)
    return render_template('usuarios/editar.html', usuario=usuario_data)

@usuario_blueprint.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    usuario = Usuario(id=id)
    usuario.delete()
    
    flash('Usuario eliminado exitosamente')
    return redirect(url_for('usuario.index'))

