from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.cancion_model import Cancion
from models.favorito_model import Favorito

cancion_controller = Blueprint('cancion', __name__, url_prefix='/canciones')

@cancion_controller.route('/')
def index():
    cancion = Cancion()
    canciones = cancion.get_all()
    return render_template('canciones/index.html', canciones=canciones)

@cancion_controller.route('/nueva', methods=['GET', 'POST'])
def nueva():
    if request.method == 'POST':
        titulo = request.form['titulo']
        artista = request.form['artista']
        
        cancion = Cancion(titulo=titulo, artista=artista)
        cancion.create()
        
        flash('Canción creada exitosamente')
        return redirect(url_for('cancion.index'))
    
    return render_template('canciones/nueva.html')

@cancion_controller.route('/<int:id>')
def mostrar(id):
    cancion = Cancion()
    cancion_data = cancion.get_by_id(id)
    
    favorito = Favorito()
    usuarios_favoritos = favorito.get_usuarios_by_cancion(id)
    
    return render_template('canciones/mostrar.html', 
                        cancion=cancion_data, 
                        usuarios_favoritos=usuarios_favoritos)

@cancion_controller.route('/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    cancion = Cancion()
    
    if request.method == 'POST':
        cancion.id = id
        cancion.titulo = request.form['titulo']
        cancion.artista = request.form['artista']
        
        cancion.update()
        
        flash('Canción actualizada exitosamente')
        return redirect(url_for('cancion.mostrar', id=id))
    
    cancion_data = cancion.get_by_id(id)
    return render_template('canciones/editar.html', cancion=cancion_data)

@cancion_controller.route('/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    cancion = Cancion(id=id)
    cancion.delete()
    
    flash('Canción eliminada exitosamente')
    return redirect(url_for('cancion.index'))

