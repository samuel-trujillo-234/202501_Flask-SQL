from flask import Blueprint, render_template, request, redirect
from models.usuario import Usuario

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route("/usuarios")
def mostrar_usuarios():
    usuarios = Usuario.get_all()
    return render_template("usuarios.html", todos_usuarios=usuarios)

@usuarios_bp.route("/usuarios/<int:id>")
def ver_usuario(id):
    usuario = Usuario.get_one({"id": id})
    return render_template("ver_usuario.html", usuario=usuario)

@usuarios_bp.route("/usuarios/nuevo")
def formulario_usuario():
    return render_template("nuevo_usuario.html")

@usuarios_bp.route("/nuevos", methods=['POST'])
def crear_usuario():
    datos = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "email": request.form['email']
    }
    if not Usuario.validar_usuario(datos):
        session["form_data"] = datos
        return redirect("/usuarios/nuevo")
    Usuario.save(datos)
    session.pop("form_data", None) 
    return redirect('/usuarios')

@usuarios_bp.route("/usuarios/editar/<int:id>")
def editar_usuario(id):
    usuario = Usuario.get_one({"id": id})
    return render_template("editar_usuario.html", usuario=usuario)

@usuarios_bp.route("/usuarios/actualizar/<int:id>", methods=["POST"])
def actualizar_usuario(id):
    datos = {
        "id": id,
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "email": request.form["email"]
    }
    Usuario.update(datos)
    return redirect("/usuarios")

@usuarios_bp.route("/usuarios/borrar/<int:id>")
def borrar_usuario(id):
    Usuario.delete({"id": id})
    return redirect("/usuarios")
