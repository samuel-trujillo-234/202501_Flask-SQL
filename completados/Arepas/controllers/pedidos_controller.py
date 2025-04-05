from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.pedidos_model import Pedidos

pedidos_controller = Blueprint('pedido', __name__, url_prefix='/pedidos')

@pedidos_controller.route('/')
def index():
    pedido = Pedidos
    pedidos = pedido.get_all()
    return render_template('pedidos/index.html', pedidos=pedidos)

@pedidos_controller.route('/<int:id>')
def mostrar(id):
    pedido = Pedidos().get_by_id(id)
    return render_template('pedidos/mostrar.html', pedido=pedido)

@pedidos_controller.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        relleno = request.form['relleno']
        
        pedido = Pedidos(nombre=nombre, cantidad=cantidad, relleno=relleno)
        pedido.create()
        
    if not Pedidos.validar_usuario(datos):
        return redirect('/') 
        Pedidos.save(datos)
        return redirect('/nuevo')
        
        flash('Pedido de arepa creado exitosamente!')
        return redirect(url_for('pedidos.index'))
    
    return render_template('pedidos/nuevo.html')
