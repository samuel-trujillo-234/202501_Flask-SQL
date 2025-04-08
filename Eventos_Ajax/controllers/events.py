from models.event import Event

class Events:
    def validate_event(self, form_data):
        return Event.validate_event(form_data)
    
    def create_event(self, form_data):
        validation_result = self.validate_event(form_data)
        if not validation_result['is_valid']:
            return False
        
        return Event.save(form_data)
    
    def get_all_events(self):
        return Event.get_all()
    
    def get_event_by_id(self, event_id):
        return Event.get_by_id(event_id)
    
    def update_event(self, form_data):
        validation_result = self.validate_event(form_data)
        if not validation_result['is_valid']:
            return False
        
        return Event.update(form_data)
    
    def delete_event(self, event_id):
        return Event.delete(event_id)
    
    def join_event(self, event_id, user_id):
        return Event.join(event_id, user_id)
    
    def leave_event(self, event_id, user_id):
        return Event.leave(event_id, user_id)
    
    def get_event_participants(self, event_id):
        return Event.get_participants(event_id)
    
    def is_participant(self, event_id, user_id):
        return Event.is_participant(event_id, user_id)
