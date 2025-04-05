from flask_app.models import taco  # Importamos la clase Taco
from publicaciones.config.mysqlconnection import connectToMySQL  # Importamos la conexión a MySQL

class Restaurante:
    @classmethod
    def get_restaurante_y_tacos(cls, datos):
        query = """
            SELECT * FROM restaurantes 
            LEFT JOIN tacos ON tacos.restaurante_id = restaurantes.id 
            WHERE restaurantes.id = %(id)s;
        """

        # Obtenemos los resultados de la base de datos
        resultados = connectToMySQL('esquema_tacos').query_db(query, datos)

        # Creamos el objeto Restaurante con los datos del primer registro
        restaurante = cls(resultados[0])

        # Iteramos sobre los resultados para agregar los tacos
        for fila_en_db in resultados:
            datos_taco = {
                "id": fila_en_db['tacos.id'],
                "tortilla": fila_en_db['tortilla'],
                "guiso": fila_en_db['guiso'],
                "salsa": fila_en_db['salsa'],
                "created_at": fila_en_db['tacos.created_at'],
                "updated_at": fila_en_db['tacos.updated_at'],
            }
            restaurante.tacos.append(taco.Taco(datos_taco))

        return restaurante
