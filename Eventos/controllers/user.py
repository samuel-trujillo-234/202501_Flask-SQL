from flask import flash
from models.user import User
from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
bcrypt = Bcrypt(app)

class Users:
    def validate_registration(self, form_data):
        return User.validate_registration(form_data)
    
    def register(self, form_data):
        if not self.validate_registration(form_data):
            return False

        pw_hash = bcrypt.generate_password_hash(form_data['password'])
        

        data = {
            'first_name': form_data['first_name'],
            'last_name': form_data['last_name'],
            'email': form_data['email'],
            'password': pw_hash
        }
        

        return User.save(data)
    
    def login(self, form_data):

        user = User.get_by_email(form_data['email'])
        

        if User.validate_login(user, form_data['password']):
            return user
        
        return False
    
    def get_user_by_id(self, user_id):
        return User.get_by_id(user_id)
