import pymysql.cursors
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def obtener_conexion():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def crear_tablas():
    try:
        conexion = obtener_conexion()
        with conexion.cursor() as cursor:
            sql = """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            cursor.execute(sql)
            conexion.commit()
            print("Tablas creadas correctamente")
    except Exception as e:
        print(f"Error al crear tablas: {e}")
    finally:
        conexion.close()

