import re
from flask import flash
from usuarios_CR.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
class Usuario:
    db_name = "esquema_usuarios"

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM usuarios;"
        results = connectToMySQL(cls.db_name).query_db(query)
        return [cls(usuario) for usuario in results]

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return cls(result[0]) if result else None

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, created_at, updated_at)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, NOW(), NOW());
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
            UPDATE usuarios
            SET nombre = %(nombre)s, apellido = %(apellido)s, email = %(email)s, updated_at = NOW()
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def validar_usuario(cls, datos):
        es_valido = True

        if len(datos["nombre"].strip()) == 0:
            flash("El nombre no puede estar vacío", "error")
            es_valido = False

        if len(datos["apellido"].strip()) == 0:
            flash("El apellido no puede estar vacío", "error")
            es_valido = False

        if len(datos["email"].strip()) == 0:
            flash("El email no puede estar vacío", "error")
            es_valido = False
        elif not EMAIL_REGEX.match(datos["email"]):
            flash("El formato del email no es válido", "error")
            es_valido = False
        elif cls.email_existe(datos["email"]):
            flash("Este email ya está registrado", "error")
            es_valido = False

        return es_valido

    @classmethod
    def email_existe(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, {"email": email})
        return len(result) > 0