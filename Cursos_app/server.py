from models.database import app  # Usa la instancia de Flask que ya tienes
from controllers.cursos_controller import cursos_bp
from controllers.estudiantes_controller import estudiantes_bp

# Registra los Blueprints correctamente
app.register_blueprint(cursos_bp)
app.register_blueprint(estudiantes_bp)

if __name__ == '__main__':
    app.run(debug=True)