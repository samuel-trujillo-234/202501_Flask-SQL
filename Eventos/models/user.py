from config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DB = "event_manager_db"
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.DB).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
    
    @classmethod
    def get_by_id(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {'id': user_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if results:
            return cls(results[0])
        return None
    
    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {'email': email}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if results:
            return results[0]
        return None
    
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @staticmethod
    def validate_registration(user):
        is_valid = True
        
        # Validar nombre y apellido
        if len(user['first_name']) < 2:
            flash("El nombre debe tener al menos 2 caracteres", "register")
            is_valid = False
        
        if len(user['last_name']) < 2:
            flash("El apellido debe tener al menos 2 caracteres", "register")
            is_valid = False
        
        # Validar email
        if not EMAIL_REGEX.match(user['email']):
            flash("Email inválido", "register")
            is_valid = False
        
        # Verificar si el email ya existe
        if User.get_by_email(user['email']):
            flash("Este email ya está registrado", "register")
            is_valid = False
        
        # Validar contraseña
        if len(user['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres", "register")
            is_valid = False
        
        # Confirmar contraseña
        if user['password'] != user['confirm_password']:
            flash("Las contraseñas no coinciden", "register")
            is_valid = False
        
        return is_valid
    
    @staticmethod
    def validate_login(user, password):
        # Verificar si el usuario existe
        if not user:
            flash("Email o contraseña incorrectos", "login")
            return False
        
        # Verificar contraseña
        if not bcrypt.check_password_hash(user['password'], password):
            flash("Email o contraseña incorrectos", "login")
            return False
        
        return True
