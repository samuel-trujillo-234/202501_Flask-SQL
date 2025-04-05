from flask import Blueprint, redirect, url_for, flash, request, render_template
from models.seguidores_model import Seguidores

seguidores_controller = Blueprint('seguidores', __name__, url_prefix='/seguidores')

@seguidores_controller.route('/<int:usuario_id>')
def index(usuario_id):
    seguidor = Seguidores()
    seguidores = seguidor.get_followers(usuario_id)
    return render_template('seguidores/index.html', seguidores=seguidores, usuario_id=usuario_id)

@seguidores_controller.route('/<int:usuario_id>/nuevo', methods=['GET', 'POST'])
def nuevo(usuario_id):
    if request.method == 'POST':
        seguidor_id = request.form['seguidor_id']
        
        seguidor = Seguidores(usuario_id=usuario_id, seguidor_id=seguidor_id)
        if seguidor.add_follower():
            flash('Seguidor añadido exitosamente.')
        else:
            flash('Este seguidor ya existe.')
        
        return redirect(url_for('seguidores.index', usuario_id=usuario_id))
    
    return render_template('seguidores/nuevo.html', usuario_id=usuario_id)