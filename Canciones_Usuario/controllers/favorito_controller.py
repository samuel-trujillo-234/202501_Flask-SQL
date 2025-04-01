from flask import Blueprint, redirect, url_for, flash, request
from models.favorito_model import Favorito
from models.usuario_model import Usuario
from models.cancion_model import Cancion

favorito_controller = Blueprint('favorito', __name__, url_prefix='/favoritos')

@favorito_controller.route('/agregar', methods=['POST'])
def agregar():
    usuario_id = request.form['usuario_id']
    cancion_id = request.form['cancion_id']
    
    # Validar que existan usuario y canción
    usuario = Usuario()
    usuario_data = usuario.get_by_id(usuario_id)
    
    cancion = Cancion()
    cancion_data = cancion.get_by_id(cancion_id)
    
    if not usuario_data or not cancion_data:
        flash('Usuario o canción no encontrados')
        return redirect(url_for('index'))
    
    favorito = Favorito(usuario_id=usuario_id, cancion_id=cancion_id)
    favorito.create()
    
    flash('Favorito agregado exitosamente')
    
    # Redireccionar a la página desde donde se hizo la solicitud
    referer = request.referrer
    if 'usuarios' in referer:
        return redirect(url_for('usuario.mostrar', id=usuario_id))
    else:
        return redirect(url_for('cancion.mostrar', id=cancion_id))

@favorito_controller.route('/eliminar', methods=['POST'])
def eliminar():
    usuario_id = request.form['usuario_id']
    cancion_id = request.form['cancion_id']
    
    favorito = Favorito(usuario_id=usuario_id, cancion_id=cancion_id)
    favorito.delete()
    
    flash('Favorito eliminado exitosamente')
    
    # Redireccionar a la página desde donde se hizo la solicitud
    referer = request.referrer
    if 'usuarios' in referer:
        return redirect(url_for('usuario.mostrar', id=usuario_id))
    else:
        return redirect(url_for('cancion.mostrar', id=cancion_id))

