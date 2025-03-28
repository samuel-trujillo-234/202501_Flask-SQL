from mysqlconnection import connectToMySQL

class estudiantes_cursos:
    def __init__( self , data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.tipo = data['tipo']
        self.color = data['color']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
@classmethod
def get_all(cls):
    query = "SELECT * FROM cursos;"
    resultados = connectToMySQL('estudiantes_cursos').query_db(query)
    
    usuarios = []
    for usuario in resultados:
        usuario.append( cls(usuario) )
    return usuarios