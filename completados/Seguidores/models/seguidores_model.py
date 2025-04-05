from models.db import Database

class Seguidores:
    def __init__(self, usuario_id=None, seguidor_id=None):
        self.usuario_id = usuario_id
        self.seguidor_id = seguidor_id
        self.db = Database()

    def get_followers(self, usuario_id):
        """ Obtiene todos los seguidores de un usuario """
        query = """
        SELECT u.id, u.nombre, u.apellido, u.email 
        FROM seguidores s
        JOIN usuarios u ON s.seguidor_id = u.id
        WHERE s.usuario_id = %s
        """
        return self.db.fetch_all(query, (usuario_id,))

    def add_follower(self):
        """ Agrega un seguidor a un usuario, evitando duplicados """
        check_query = "SELECT * FROM seguidores WHERE usuario_id = %s AND seguidor_id = %s"
        exists = self.db.fetch_one(check_query, (self.usuario_id, self.seguidor_id))
        
        if exists:
            return False 

        query = "INSERT INTO seguidores (usuario_id, seguidor_id) VALUES (%s, %s)"
        self.db.execute_query(query, (self.usuario_id, self.seguidor_id))
        return True

    def remove_follower(self):
        """ Elimina una relación de seguidor-usuario """
        query = "DELETE FROM seguidores WHERE usuario_id = %s AND seguidor_id = %s"
        self.db.execute_query(query, (self.usuario_id, self.seguidor_id))
        return True
