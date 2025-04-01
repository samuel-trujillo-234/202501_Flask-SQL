from flask_app.config.mysqlconnection import connectToMySQL

class Cancion:
    def __init__(self, data):
        self.id =data['id']
        self.nombre = data['nombre']
        self.artista = data['artista']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']        

@classmethod
def get_all(cls):
    query = "SELECT * FROM canciones;"
    results = connectToMySQL('canciones').query_db(query)
    canciones = []
    for cancion in results:
        canciones.append( cls(cancion) )
    return canciones

    results = connectToMySQL('bd_canciones').query_db(query)
    canciones = []
    for cancion in resultados:
        canciones.append(cls(cancion))
    return canciones

