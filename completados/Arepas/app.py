from flask import Flask
from controllers.pedidos_controller import pedidos_controller

app = Flask(__name__)
app.secret_key = "eminem"

app.register_blueprint(pedidos_controller)

if __name__ == '__main__':
    app.run(debug=True)
