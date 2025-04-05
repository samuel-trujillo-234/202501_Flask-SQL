from flask import Flask
from controllers.usuarios import usuarios_bp

app = Flask(__name__)

# Registrar Blueprint de usuarios
app.register_blueprint(usuarios_bp)

if __name__ == "__main__":
    app.run(debug=True)
