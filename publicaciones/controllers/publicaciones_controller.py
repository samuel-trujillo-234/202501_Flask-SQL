from flask import Blueprint, render_template, redirect, request, session, flash
from publicaciones.models.publicaciones_model import Publicacion
from publicaciones.models.usuarios_model import Usuario

publicaciones_app = Blueprint('publicaciones', __name__)

@publicaciones_app.route('/nueva')
def nueva_publicacion():
    if 'usuario_id' not in session:
        flash("El usuario debe haber iniciado sesión para ver esta página", "info")
        return redirect('/login')
    
    usuarios = Usuario.get_all()

    autores = [u for u in usuarios if u.id != session['usuario_id']]
    return render_template('nueva_publicacion.html', autores=autores)

@publicaciones_app.route('/crear_publicacion', methods=['POST'])
def crear_publicacion():
    if 'usuario_id' not in session:
        return redirect('/login')
    
    if not Publicacion.validar(request.form):
        return redirect('/nueva')
    
    data = {
        'titulo': request.form['titulo'],
        'contenido': request.form['contenido'],
        'fecha': request.form['fecha'],
        'usuario_id': session['usuario_id'],
        'autor_id': request.form['autor_id'] if 'autor_id' in request.form else None
    }
    Publicacion.save(data)
    
    return redirect('/dashboard')

@publicaciones_app.route('/editar/<int:id>')
def editar_publicacion(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    
    publicacion = Publicacion.get_by_id(id)
    
    if not publicacion:
        return redirect('/dashboard')
    
    if publicacion['usuario_id'] != session['usuario_id']:
        flash("No puedes editar una publicación que no creaste", "info")
        return redirect('/dashboard')
    
    usuarios = Usuario.get_all()
    autores = [u for u in usuarios if u.id != session['usuario_id']]
    
    return render_template('editar_publicacion.html', publicacion=publicacion, autores=autores)

@publicaciones_app.route('/actualizar_publicacion', methods=['POST'])
def actualizar_publicacion():
    if 'usuario_id' not in session:
        return redirect('/login')
    
    if not Publicacion.validar(request.form):
        return redirect(f'/editar/{request.form["id"]}')
    
    data = {
        'id': request.form['id'],
        'titulo': request.form['titulo'],
        'contenido': request.form['contenido'],
        'fecha': request.form['fecha'],
        'autor_id': request.form['autor_id'] if 'autor_id' in request.form else None
    }
    
    Publicacion.update(data)
    
    return redirect('/dashboard')

@publicaciones_app.route('/borrar/<int:id>')
def borrar_publicacion(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    
    publicacion = Publicacion.get_by_id(id)
    
    if not publicacion:
        return redirect('/dashboard')
    
    if publicacion['usuario_id'] != session['usuario_id']:
        flash("No puedes borrar una publicación que no creaste", "info")
        return redirect('/dashboard')
    
    Publicacion.delete(id)
    
    return redirect('/dashboard')

@publicaciones_app.route('/ver/<int:id>')
def ver_publicacion(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    
    publicacion = Publicacion.get_by_id(id)
    
    if not publicacion:
        return redirect('/dashboard')
    
    usuarios = Usuario.get_all()
    autores = [u for u in usuarios if u.id != publicacion['usuario_id']]
    
    return render_template('ver_publicacion.html', publicacion=publicacion, autores=autores)

@publicaciones_app.route('/cambiar_autor', methods=['POST'])
def cambiar_autor():
    if 'usuario_id' not in session:
        return redirect('/login')
    
    data = {
        'id': request.form['id'],
        'autor_id': request.form['autor_id']
    }
    Publicacion.update_autor(data)
    
    return redirect(f'/ver/{request.form["id"]}')