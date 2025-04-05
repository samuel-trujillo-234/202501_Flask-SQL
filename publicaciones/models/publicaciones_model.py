from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime

class Publicacion:
    db_name = "esquema_publicaciones"
    
    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.contenido = data['contenido']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO publicaciones (titulo, descripcion, fecha_publicacion, usuario_id, created_at, updated_at)
            VALUES (%(titulo)s, %(descripcion)s, %(fecha_publicacion)s, %(usuario_id)s, NOW(), NOW())
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM publicaciones;"
        results = connectToMySQL(cls.db_name).query_db(query)
        publicaciones = []
        for publicacion in results:
            publicaciones.append(cls(publicacion))
        return publicaciones

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM publicaciones WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db({'id': id})
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = """
            UPDATE publicaciones
            SET titulo = %(titulo)s, contenido = %(contenido)s, updated_at = NOW()
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, id):
        query = "DELETE FROM publicaciones WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db({'id': id})