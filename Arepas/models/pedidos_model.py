from models.db import Database

class Pedidos:
        
        def __init__(self, id=None, nombre=None, cantidad=None, relleno=None):
                self.id = id
                self.nombre = nombre
                self.cantidad = cantidad
                self.relleno = relleno
                self.db = Database()
        
def get_all(self):
        return self.db.fetch_all("SELECT * FROM pedidos")

def get_by_id(self, id):
        return self.db.fetch_one("SELECT * FROM pedidos WHERE id = %s", (id,))

def create(self):
        query = "INSERT INTO pedidos (nombre, cantidad, relleno) VALUES (%s, %s, %s)"
        params = (self.nombre, self.cantidad, self.relleno)
        cursor = self.db.execute_query(query, params)
        self.id = cursor.lastrowid
        return self.id

def update(self):
        query = "UPDATE pedidos SET nombre = %s, cantidad = %s, relleno = %s WHERE id = %s"
        params = (self.nombre, self.cantidad, self.relleno, self.id)
        self.db.execute_query(query, params)
        return True
