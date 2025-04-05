from models.db import Database

class Favorito:
    def __init__(self, id=None, usuario_id=None, cancion_id=None):
        self.id = id
        self.usuario_id = usuario_id
        self.cancion_id = cancion_id
        self.db = Database()
    
    def get_favoritos_by_usuario(self, usuario_id):
        query = """
            SELECT c.* FROM canciones c
            JOIN favoritos f ON c.id = f.cancion_id
            WHERE f.usuario_id = %s
        """
        return self.db.fetch_all(query, (usuario_id,))
    
    def get_usuarios_by_cancion(self, cancion_id):
        query = """
            SELECT u.* FROM usuarios u
            JOIN favoritos f ON u.id = f.usuario_id
            WHERE f.cancion_id = %s
        """
        return self.db.fetch_all(query, (cancion_id,))
    
    def create(self):
        check_query = "SELECT id FROM favoritos WHERE usuario_id = %s AND cancion_id = %s"
        existing = self.db.fetch_one(check_query, (self.usuario_id, self.cancion_id))
        
        if existing:
            return existing['id']
        
        query = "INSERT INTO favoritos (usuario_id, cancion_id) VALUES (%s, %s)"
        params = (self.usuario_id, self.cancion_id)
        cursor = self.db.execute_query(query, params)
        self.id = cursor.lastrowid
        return self.id
    
    def delete(self):
        query = "DELETE FROM favoritos WHERE usuario_id = %s AND cancion_id = %s"
        self.db.execute_query(query, (self.usuario_id, self.cancion_id))
        return True

