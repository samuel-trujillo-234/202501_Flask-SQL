import pymysql.cursors

class MySQLConnection:
    def __init__(self, db):
        connection = pymysql.connect(
            host = 'localhost',
            user = 'root',
            password = '2005', 
            db = db,
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor,
            autocommit = True
        )
        self.connection = connection
    
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    # Si es INSERT, devuelve el ID del último row insertado
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # Si es SELECT, devuelve los datos
                    result = cursor.fetchall()
                    return result
                else:
                    # Si es UPDATE o DELETE, devuelve nada
                    self.connection.commit()
            except Exception as e:
                print("Algo salió mal", e)
                return False
            finally:
                self.connection.close()

def connectToMySQL(db):
    return MySQLConnection(db)
