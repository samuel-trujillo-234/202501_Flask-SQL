from models.db import Database

class Usuario:
    def __init__(self, id=None, nombre=None, email=None, password=None):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.password = password
        self.db = Database()
    
    def get_all(self):
        return self.db.fetch_all("SELECT * FROM usuarios")
    
    def get_by_id(self, id):
        return self.db.fetch_one("SELECT * FROM usuarios WHERE id = %s", (id,))
    
    def create(self):
        query = "INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)"
        params = (self.nombre, self.email, self.password)
        cursor = self.db.execute_query(query, params)
        self.id = cursor.lastrowid
        return self.id
    
    def update(self):
        query = "UPDATE usuarios SET nombre = %s, email = %s, password = %s WHERE id = %s"
        params = (self.nombre, self.email, self.password, self.id)
        self.db.execute_query(query, params)
        return True
    
    def delete(self):
        query = "DELETE FROM usuarios WHERE id = %s"
        self.db.execute_query(query, (self.id,))
        return True

