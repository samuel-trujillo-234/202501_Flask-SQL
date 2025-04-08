from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_bcrypt import Bcrypt
import os
from datetime import datetime

# Importar los controladores
from controllers.users import Users
from controllers.events import Events

app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)


users_controller = Users()
events_controller = Events()


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not users_controller.validate_registration(request.form):
        return redirect('/')
    
    # Registrar usuario
    user_id = users_controller.register(request.form)
    if user_id:
        session['user_id'] = user_id
        session['first_name'] = request.form['first_name']
        return redirect('/dashboard')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    # Validar login
    user = users_controller.login(request.form)
    if user:
        session['user_id'] = user['id']
        session['first_name'] = user['first_name']
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    

    events = events_controller.get_all_events()
    return render_template('dashboard.html', events=events, user_name=session['first_name'])


@app.route('/events/new')
def new_event():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_event.html')

@app.route('/events/create', methods=['POST'])
def create_event():
    if 'user_id' not in session:
        return redirect('/')
    

    if not events_controller.validate_event(request.form):
        return redirect('/events/new')
    

    event_data = {
        **request.form,
        'user_id': session['user_id']
    }
    events_controller.create_event(event_data)
    return redirect('/dashboard')

@app.route('/events/<int:event_id>')
def show_event(event_id):
    if 'user_id' not in session:
        return redirect('/')
    

    event = events_controller.get_event_by_id(event_id)
    if not event:
        return redirect('/dashboard')
    

    participants = events_controller.get_event_participants(event_id)
    
    return render_template('show_event.html', event=event, participants=participants)

@app.route('/events/edit/<int:event_id>')
def edit_event(event_id):
    if 'user_id' not in session:
        return redirect('/')
    

    event = events_controller.get_event_by_id(event_id)
    if not event or event['user_id'] != session['user_id']:
        flash("No tienes permiso para editar este evento")
        return redirect('/dashboard')
    
    return render_template('edit_event.html', event=event)

@app.route('/events/update/<int:event_id>', methods=['POST'])
def update_event(event_id):
    if 'user_id' not in session:
        return redirect('/')
    

    if not events_controller.validate_event(request.form):
        return redirect(f'/events/edit/{event_id}')
    

    event_data = {
        **request.form,
        'id': event_id,
        'user_id': session['user_id']
    }
    events_controller.update_event(event_data)
    return redirect('/dashboard')

@app.route('/events/join/<int:event_id>')
def join_event(event_id):
    if 'user_id' not in session:
        return redirect('/')
    

    events_controller.join_event(event_id, session['user_id'])
    return redirect(f'/events/{event_id}')

@app.route('/events/leave/<int:event_id>')
def leave_event(event_id):
    if 'user_id' not in session:
        return redirect('/')
    
    events_controller.leave_event(event_id, session['user_id'])
    return redirect(f'/events/{event_id}')

@app.route('/events/delete/<int:event_id>')
def delete_event(event_id):
    if 'user_id' not in session:
        return redirect('/')
    
    event = events_controller.get_event_by_id(event_id)
    if not event or event['user_id'] != session['user_id']:
        flash("No tienes permiso para eliminar este evento")
        return redirect('/dashboard')
    

    events_controller.delete_event(event_id)
    return redirect('/dashboard')

if __name__ == "__main__":
    app.run(debug=True)
