import sys
import os

# Agregar el directorio raíz al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from publicaciones.controllers.publicaciones_controller import publicaciones_app

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Registra el Blueprint
app.register_blueprint(publicaciones_app)

if __name__ == "__main__":
    app.run(debug=True)