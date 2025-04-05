from flask import Flask
from controllers.usuario_controller import usuario_controller
from controllers.seguidores_controller import seguidores_controller

app = Flask(__name__)
app.secret_key = "snoop-dog"

app.register_blueprint(usuario_controller)
app.register_blueprint(seguidores_controller)

if __name__ == '__main__':
    app.run(debug=True)
