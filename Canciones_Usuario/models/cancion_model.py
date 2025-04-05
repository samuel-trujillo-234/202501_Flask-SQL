from models.db import Database

class Cancion:
    def __init__(self, id=None, titulo=None, artista=None):
        self.id = id
        self.titulo = titulo
        self.artista = artista
        self.db = Database()
    
    def get_all(self):
        return self.db.fetch_all("SELECT * FROM canciones")
    
    def get_by_id(self, id):
        return self.db.fetch_one("SELECT * FROM canciones WHERE id = %s", (id,))
    
    def create(self):
        query = "INSERT INTO canciones (titulo, artista) VALUES (%s, %s)"
        params = (self.titulo, self.artista)
        cursor = self.db.execute_query(query, params)
        self.id = cursor.lastrowid
        return self.id
    
    def update(self):
        query = "UPDATE canciones SET titulo = %s, artista = %s WHERE id = %s"
        params = (self.titulo, self.artista, self.id)
        self.db.execute_query(query, params)
        return True
    
    def delete(self):
        query = "DELETE FROM canciones WHERE id = %s"
        self.db.execute_query(query, (self.id,))
        return True

