# Importamos la función que devolverá una instancia de una conexión
from mysqlconnection import connectToMySQL

# Creamos la clase basada en la tabla de mascotas
class Mascota:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.tipo = data['tipo']
        self.color = data['color']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Método de clase para obtener todas las mascotas
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM mascotas;"

        # Llamamos a la función connectToMySQL con el esquema al que te diriges
        resultados = connectToMySQL('primera_flask').query_db(query)

        # Creamos una lista vacía para agregar nuestras instancias de mascota
        mascotas = []

        # Iteramos sobre los resultados de la base de datos y creamos instancias de Mascota
        for mascota in resultados:
            mascotas.append(cls(mascota))

        return mascotas  # El return debe estar fuera del for
