from flask import Flask, render_template
# Importamos la clase Mascota desde el archivo mascota.py
from mascota import Mascota  

app = Flask(__name__)

@app.route("/")
def index():
    # Invocamos el método de clase get_all para obtener todas las mascotas
    mascotas = Mascota.get_all()
    print(mascotas)  # Para depuración, puedes eliminarlo después
    return render_template("index.html", todas_mascotas=mascotas)

if __name__ == "__main__":
    app.run(debug=True)
