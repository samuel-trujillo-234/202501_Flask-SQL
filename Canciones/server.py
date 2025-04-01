from flask_app import app

from flask_app.controllers import canciones
from flask_app.controllers import favoritos


if __name__ == "__main__":
    
    app.run(debug=True)