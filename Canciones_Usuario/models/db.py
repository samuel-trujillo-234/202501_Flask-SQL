import pymysql

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='12345678',
            db='esquema_canciones',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()
    
    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor
        except Exception as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            raise e
    
    def fetch_all(self, query, params=None):
        cursor = self.execute_query(query, params)
        return cursor.fetchall()
    
    def fetch_one(self, query, params=None):
        cursor = self.execute_query(query, params)
        return cursor.fetchone()
    
    def close(self):
        self.connection.close()

