from flask_app.config.mysqlconnection import connectToMySQL

class Curso:

    def __init__( self , data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']



    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cursos;"
        results = connectToMySQL('estudiantes_cursos').query_db(query)
        cursos = []
        for curso in results:
            cursos.append( cls(curso) )
        return cursos


    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM cursos WHERE id = %(id)s;"
        data = { "id": id }
        curso = connectToMySQL('estudiantes_cursos').query_db(query, data)
        return cls(curso[0])


    @classmethod
    def save(cls, data):
        query = "INSERT INTO cursos (nombre, created_at, updated_at) VALUES (%(nombre)s,  NOW(), NOW())"
        return connectToMySQL('estudiantes_cursos').query_db(query, data)


    @classmethod
    def delete(cls, id):
        query = "DELETE FROM cursos WHERE id = %(id)s;"
        data = { "id": id }
        return connectToMySQL('estudiantes_cursos').query_db(query, data)


    @classmethod
    def update(cls, curso):
        query = "UPDATE cursos SET nombre = %(nombre)s, updated_at = NOW() WHERE id = %(id)s"
        data = {
            "id": curso.id,
            "nombre": curso.nombre,
            }
        return connectToMySQL('estudiantes_cursos').query_db(query, data)