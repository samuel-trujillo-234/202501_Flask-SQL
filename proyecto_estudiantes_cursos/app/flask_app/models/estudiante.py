from flask_app.config.mysqlconnection import connectToMySQL

class Estudiante:

    def __init__(self , data):
        self.id = data['id']
        self.nombre = data['nome']
        self.apellido = data['apellido']
        self.email = data['email']
        self.ciudad = data['ciudad']
        self.curso_id = data['curso_id']
        self.curso = data['curso']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = """
        SELECT estudiante.id as id, estudiante.nombre as nombre, estudiante.apellido as apellido, estudiante.email as email, estudiante.ciudad as ciudad, estudiante.created_at as created_at, estudiante.updated_at as updated_at, estudiante.curso_id as curso_id, cursos.nombre as curso 
        FROM estudiantes
        LEFT JOIN cursos
        ON estudiantes.curso_id = cursos.id;"""

        results = connectToMySQL('estudiantes_cursos').query_db(query)
        estudiantes = []
        for estudiante in results:
            print (estudiante)
            estudiantes.append( cls(estudiante) )
        return estudiantes


    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM estudiantes WHERE id = %(id)s;"
        data = { "id": id }
        estudiante = connectToMySQL('estudiantes_cursos').query_db(query, data)
        estudiante[0]['curso'] = ''
        return cls(estudiante[0])


    @classmethod
    def select(cls, curso_id):
        query = "SELECT * FROM estudiantes WHERE curso_id = %(id)s;"
        data = { "id": curso_id }
        results = connectToMySQL('estudiantes_cursos').query_db(query, data)
        estudiantes = []
        for estudiante in results:
            estudiante['curso'] = ''
            estudiantes.append( cls(estudiante) )
        return estudiantes


    @classmethod
    def save(cls, data):
        query = "INSERT INTO estudiantes (nombre, apellido, email, ciudad, created_at, updated_at, curso_id) VALUES (%(nombre)s, %(apellido)s, %(email)s, %(ciudad)s, NOW(), NOW(), %(curso_id)s)"
        return connectToMySQL('estudiantes_cursos').query_db(query, data)


    @classmethod
    def delete(cls, id):
        query = "DELETE FROM estudiantes WHERE id = %(id)s;"
        data = { "id": id }
        return connectToMySQL('estudiantes_cursos').query_db(query, data)


    @classmethod
    def update(cls, estudiantes):
        query = "UPDATE estudiante SET nombre = %(nombre)s, apellido = %(apellido)s, email = %(email)s, ciudad = %(ciudad)s, updated_at = NOW(), curso_id = %(curso_id)s WHERE id = %(id)s"
        data = {
            "id": estudiantes.id,
            "nombre": estudiantes.nombre,
            "apellido": estudiantes.apellido,
            "email": estudiantes.email,
            "ciudad": estudiantes.ciudad,
            "curso_id": estudiantes.curso_id,
            }
        return connectToMySQL('estudiantes_cursos').query_db(query, data)