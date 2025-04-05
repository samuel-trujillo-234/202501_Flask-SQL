from flask import render_template, request, redirect
from flask_app import app
from flask_app.models.taco import Taco

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/crear", methods=["POST"])
def crear_taco():
    Taco.save(request.form)
    return redirect("/tacos")

@app.route("/tacos")
def mostrar_tacos():
    tacos = Taco.get_all()
    return render_template("resultados.html", todos_tacos=tacos)

@app.route("/mostrar/<int:id>")
def mostrar_taco(id):
    datos = {"id": id}
    taco = Taco.get_one(datos)
    return render_template("detalle.html", taco=taco)

@app.route("/editar/<int:id>")
def editar_taco(id):
    datos = {"id": id}
    taco = Taco.get_one(datos)
    return render_template("editar.html", taco=taco)

@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar_taco(id):
    datos = {**request.form, "id": id}
    Taco.update(datos)
    return redirect("/tacos")

@app.route("/borrar/<int:id>")
def borrar_taco(id):
    datos = {"id": id}
    Taco.delete(datos)
    return redirect("/tacos")

@app.route('/crear',methods=['POST'])

def crear():
    datos = {
    "tortilla":request.form['tortilla'],
    "guiso": request.form['guiso'],
    "salsa": request.form['salsa'],
    "restaurante_id": request.form['restaurante_id']
}
    if not Taco.validar_taco(datos):
        return redirect('/') 
    Taco.save(datos)
    return redirect('/tacos')