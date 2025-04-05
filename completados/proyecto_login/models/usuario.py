from utils.db import obtener_conexion

class Usuario:
    def __init__(self, id=None, nombre=None, apellido=None, email=None, password=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.password = password
    
    @classmethod
    def buscar_por_email(cls, email):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                sql = "SELECT * FROM usuarios WHERE email = %s"
                cursor.execute(sql, (email,))
                resultado = cursor.fetchone()
                
                if resultado:
                    return cls(
                        id=resultado['id'],
                        nombre=resultado['nombre'],
                        apellido=resultado['apellido'],
                        email=resultado['email'],
                        password=resultado['password']
                    )
                return None
        except Exception as e:
            print(f"Error al buscar usuario por email: {e}")
            return None
        finally:
            conexion.close()
    
    @classmethod
    def crear(cls, nombre, apellido, email, password):
        try:
            conexion = obtener_conexion()
            with conexion.cursor() as cursor:
                sql = """
                INSERT INTO usuarios (nombre, apellido, email, password) 
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (nombre, apellido, email, password))
                conexion.commit()
                
                return cursor.lastrowid
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return None
        finally:
            conexion.close()

