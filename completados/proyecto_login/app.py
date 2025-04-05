from flask import Flask
from controllers.auth_controller import auth_bp
from utils.db import crear_tablas

app = Flask(__name__)

app.config.from_pyfile('config.py')

app.register_blueprint(auth_bp)

crear_tablas()

if __name__ == '__main__':
    app.run(debug=True)

