from flask import Flask, render_template, request, redirect, url_for, flash
import os
from controllers.usuario_controller import usuario_blueprint
from controllers.cancion_controller import cancion_controller
from controllers.favorito_controller import favorito_controller

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.register_blueprint(usuario_blueprint)
app.register_blueprint(cancion_controller)
app.register_blueprint(favorito_controller)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

