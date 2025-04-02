from flask_app import app

from flask import render_template, request, redirect

from flask_app.models.estudiante import Estudiante
from flask_app.models.curso import Curso

@app.route("/estudiantes")
def estudiantes():
    estudiantes = Estudiante.get_all()
    return render_template("estudiantes/estudantes.html", estudiantes=estudiantes)


@app.route('/crear_estudiante')
def criar_estudiante():
    cursos = Curso.get_all()
    return render_template("estudiantes/criar.html", cursos=cursos)


@app.route('/incluir_estudiante', methods=['POST'])
def incluir_estudiante():
    data = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'ciudad': request.form['ciudad'],
        'created_at': 'NOW()',
        'updated_at': 'NOW()',
        'curso_id': request.form['curso']
        }
    if data['nombre'] != "" and data['apellido'] != "" and data['email'] != "" and data['ciudad'] != "":
        Estudiante.save(data)
        return redirect ('/estudiantes')
    else:
        flash ("Dados incompletos")
    return redirect ('/criar_estudiante')


@app.route('/agregar_estudiante_curso/<int:id>')
def incluir_estudiante_curso(id):
    curso = Curso.get_one(id)
    return render_template("estudiantes/incluir.html", curso=curso, id=id)


@app.route("/editar_estudiante/<int:id>")
def editar_estudiante(id):
    estudiante=Estudiante.get_one(id)
    cursos = Curso.get_all()
    return render_template('estudiantes/editar.html/', estudiante=estudiante, cursos=cursos)


@app.route("/atualizar_estudiante/<int:id>", methods=['POST'])
def atualizar_estudiante(id):
    estudiante = Estudiante.get_one(id)
    estudiante.nombre = request.form['nombre']
    estudiante.apellido = request.form['apellido'] 
    estudiante.email = request.form['email'] 
    estudiante.ciudad = request.form['ciudad'] 
    estudiante.curso_id = request.form['curso'] 
    if estudiante.nombre != "" and estudiante.apellido != "" and estudiante.email != "" and estudiante.ciudad  != "":
        Estudiante.update(estudiante)
        return redirect ('/estudiantes')
    return redirect (f"/editar_estudiante/{id}")


@app.route("/eliminar_estudiante/<int:id>")
def eliminar_estudiante(id):
    Estudiante.delete(id)
    return redirect ('/estudiantes')


@app.route("/cancelar_matricula/<int:id_curso>/<int:id_estudiante>")
def cancelar_matricula(id_curso, id_estudiante):
    Estudiante.delete(id_estudiante)
    return redirect (f'/curso/{id_curso}')