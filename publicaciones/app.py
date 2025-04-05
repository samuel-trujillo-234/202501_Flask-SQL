from flask import Flask
from publicaciones.controllers.publicaciones_controller import publicaciones_app

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Registra el Blueprint
app.register_blueprint(publicaciones_app)

if __name__ == "__main__":
    app.run(debug=True)