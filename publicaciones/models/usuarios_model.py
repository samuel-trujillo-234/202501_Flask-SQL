from publicaciones.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    db_name = "esquema_publicaciones"
    
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password, created_at, updated_at)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW())
        """
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL(cls.db_name).query_db(query)
        usuarios = []
        for usuario in results:
            usuarios.append(cls(usuario))
        return usuarios
    
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, {'id': id})
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL(cls.db_name).query_db(query, {'email': email})
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @staticmethod
    def validar(usuario):
        is_valid = True
        
        if len(usuario['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteres", "registro")
            is_valid = False
        
        if len(usuario['apellido']) < 2:
            flash("El apellido debe tener al menos 2 caracteres", "registro")
            is_valid = False
        
        if not EMAIL_REGEX.match(usuario['email']):
            flash("El email debe tener un formato válido", "registro")
            is_valid = False
        
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        results = connectToMySQL(Usuario.db_name).query_db(query, {'email': usuario['email']})
        if len(results) >= 1:
            flash("El email no puede repetirse en la BD", "registro")
            is_valid = False
        
        if usuario['password'] != usuario['confirm_password']:
            flash("La password y la confirmación deben ser iguales", "registro")
            is_valid = False
        
        return is_valid