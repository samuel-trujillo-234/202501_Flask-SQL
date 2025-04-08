from config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime

class Event:
    DB = "event_manager_db"
    
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.date = data['date']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.participants = []
    
    @classmethod
    def get_all(cls):
        query = """
            SELECT events.*, users.first_name, users.last_name 
            FROM events 
            JOIN users ON events.user_id = users.id
            ORDER BY events.date;
        """
        results = connectToMySQL(cls.DB).query_db(query)
        events = []
        for event in results:
            event_data = {
                'id': event['id'],
                'name': event['name'],
                'location': event['location'],
                'date': event['date'],
                'description': event['description'],
                'user_id': event['user_id'],
                'created_at': event['created_at'],
                'updated_at': event['updated_at'],
                'creator_name': f"{event['first_name']} {event['last_name']}"
            }
            events.append(event_data)
        return events
    
    @classmethod
    def get_by_id(cls, event_id):
        query = """
            SELECT events.*, users.first_name, users.last_name 
            FROM events 
            JOIN users ON events.user_id = users.id
            WHERE events.id = %(id)s;
        """
        data = {'id': event_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        if results:
            event = results[0]
            event_data = {
                'id': event['id'],
                'name': event['name'],
                'location': event['location'],
                'date': event['date'],
                'description': event['description'],
                'user_id': event['user_id'],
                'created_at': event['created_at'],
                'updated_at': event['updated_at'],
                'creator_name': f"{event['first_name']} {event['last_name']}"
            }
            return event_data
        return None
    
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO events (name, location, date, description, user_id, created_at, updated_at)
            VALUES (%(name)s, %(location)s, %(date)s, %(description)s, %(user_id)s, NOW(), NOW());
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def update(cls, data):
        query = """
            UPDATE events 
            SET name = %(name)s, location = %(location)s, date = %(date)s, 
                description = %(description)s, updated_at = NOW()
            WHERE id = %(id)s AND user_id = %(user_id)s;
        """
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete(cls, event_id):
        # Primero eliminar las participaciones
        query1 = "DELETE FROM participants WHERE event_id = %(id)s;"
        data = {'id': event_id}
        connectToMySQL(cls.DB).query_db(query1, data)
        
        # Luego eliminar el evento
        query2 = "DELETE FROM events WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query2, data)
    
    @classmethod
    def get_participants(cls, event_id):
        query = """
            SELECT users.id, users.first_name, users.last_name
            FROM participants
            JOIN users ON participants.user_id = users.id
            WHERE participants.event_id = %(event_id)s;
        """
        data = {'event_id': event_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        participants = []
        for participant in results:
            participants.append({
                'id': participant['id'],
                'name': f"{participant['first_name']} {participant['last_name']}"
            })
        return participants
    
    @classmethod
    def join(cls, event_id, user_id):
        # Verificar si ya está participando
        query1 = """
            SELECT * FROM participants 
            WHERE event_id = %(event_id)s AND user_id = %(user_id)s;
        """
        data = {
            'event_id': event_id,
            'user_id': user_id
        }
        result = connectToMySQL(cls.DB).query_db(query1, data)
        
        if result:
            return False  # Ya está participando
        
        # Agregar participación
        query2 = """
            INSERT INTO participants (event_id, user_id, created_at, updated_at)
            VALUES (%(event_id)s, %(user_id)s, NOW(), NOW());
        """
        return connectToMySQL(cls.DB).query_db(query2, data)
    
    @classmethod
    def leave(cls, event_id, user_id):
        query = """
            DELETE FROM participants 
            WHERE event_id = %(event_id)s AND user_id = %(user_id)s;
        """
        data = {
            'event_id': event_id,
            'user_id': user_id
        }
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def is_participant(cls, event_id, user_id):
        query = """
            SELECT * FROM participants 
            WHERE event_id = %(event_id)s AND user_id = %(user_id)s;
        """
        data = {
            'event_id': event_id,
            'user_id': user_id
        }
        result = connectToMySQL(cls.DB).query_db(query, data)
        return len(result) > 0
    
    @staticmethod
    def validate_event(event):
        is_valid = True
        
        # Validar nombre del evento
        if len(event['name']) < 5:
            flash("El nombre del evento debe tener al menos 5 caracteres")
            is_valid = False
        
        # Validar ubicación
        if len(event['location']) < 2:
            flash("La ubicación debe tener al menos 2 caracteres")
            is_valid = False
        
        # Validar fecha
        if not event['date']:
            flash("La fecha es obligatoria")
            is_valid = False
        else:
            # Verificar que la fecha no sea en el pasado
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
            if event_date < datetime.now():
                flash("La fecha no puede ser en el pasado")
                is_valid = False
        
        # Validar descripción
        if len(event['description']) < 10:
            flash("La descripción debe tener al menos 10 caracteres")
            is_valid = False
        
        return is_valid
