from flask import Flask, render_template, request, redirect
from mascota import Mascota  

app = Flask(__name__)

@app.route("/")
def index():
    mascotas = Mascota.get_all()
    print(mascotas) 
    return render_template("index.html", todas_mascotas=mascotas)

@app.route("/crear_mascota", methods=['POST'])

def crear_mascota():
    
    datos = {
    "nombre": request.form['nombre'],
    "tipo": request.form['tipo'],
    "color": request.form['color']
    }
    
    Mascota.save(datos)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
