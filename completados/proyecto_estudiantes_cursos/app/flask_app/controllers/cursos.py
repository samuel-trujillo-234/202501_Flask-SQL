from flask_app import app

from flask import render_template, request, redirect, flash

from flask_app.models.estudiantes import Estudiantes
from flask_app.models.curso import Curso

@app.route("/")
def cursos():
    cursos = Curso.get_all()
    return render_template("cursos/cursos.html", cursos=cursos)

@app.route('/crear_curso')
def crear_curso():
    return render_template("cursos/crear.html")

@app.route('/agregar_curso', methods=['POST'])
def agregar_curso():
    data = {
        'nombre': request.form['niombre'],
        'created_at': 'NOW()',
        'updated_at': 'NOW()',
    }
    if data['nombre'] != "":
        Curso.save(data)
    return redirect ('/')



@app.route('/curso/<int:id>')
def detalhar_curso(id):
    curso=Curso.get_one(id)
    estudiantes=Estudiante.select(id)
    print("Estudiantes: ", estudiantes)
    return render_template('cursos/mostrar.html', curso=curso, estudiantes=estudiantes)


@app.route("/editar_curso/<int:id>")
def editar_curso(id):
    curso=Curso.get_one(id)
    return render_template('cursos/editar.html', curso=curso)


@app.route("/actualizar_curso/<int:id>", methods=['POST'])
def actualizar_curso(id):
    curso = Curso.get_one(id)
    curso.nombre = request.form['nombre']
    Curso.update(curso)
    return redirect ('/')


@app.route("/eliminar_curso/<int:id>")
def eliminar_curso(id):
    Curso.delete(id)
    return redirect ('/')