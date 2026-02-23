import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db, Event, WishlistItem, GroupMember, ChatMessage, User
from discovery_service import DiscoveryService
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        unique_number = request.form.get('unique_number')
        
        user = User.query.filter_by(name=name, unique_number=unique_number).first()
        if user:
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # If not found, let's allow "automatic registration" for this simple app
            # as per user's "Unique number" request
            new_user = User(name=name, unique_number=unique_number)
            try:
                db.session.add(new_user)
                db.session.commit()
                session['user_id'] = new_user.id
                session['user_name'] = new_user.name
                flash('Account created successfully!', 'success')
                return redirect(url_for('dashboard'))
            except:
                db.session.rollback()
                flash('Invalid login or Name/Number already taken.', 'danger')
                
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    events = Event.query.filter_by(creator_id=session['user_id']).order_by(Event.created_at.desc()).all()
    return render_template('index.html', events=events)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        try:
            name = request.form.get('person_name')
            date_str = request.form.get('birthday_date')
            budget = float(request.form.get('total_budget'))
            friends = int(request.form.get('friends_count'))
            location = request.form.get('location')
            sub_location = request.form.get('sub_location', '')
            is_hidden = 'is_hidden' in request.form
            selected_needs = request.form.getlist('needs')
            needs_str = ",".join(selected_needs)
            
            birthday_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            new_event = Event(
                creator_id=session['user_id'],
                person_name=name,
                birthday_date=birthday_date,
                total_budget=budget,
                friends_count=friends,
                location=location,
                sub_location=sub_location,
                is_hidden=is_hidden,
                needs=needs_str,
                invite_code=str(uuid.uuid4())[:8].upper()
            )
            
            db.session.add(new_event)
            db.session.commit()
            
            flash('Secret event created successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating event: {str(e)}', 'danger')
            
    return render_template('create_event.html')

@app.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    days_left = (event.birthday_date - datetime.now().date()).days
    
    # Generate 5-10 smart plans using the DiscoveryService
    smart_plans = DiscoveryService.get_nearby_plans(
        event.location,
        event.sub_location,
        event.total_budget, 
        event.needs
    )
    
    return render_template('event_detail.html', 
                           event=event, 
                           days_left=days_left, 
                           smart_plans=smart_plans)

@app.route('/join/<invite_code>', methods=['GET', 'POST'])
def join_group(invite_code):
    event = Event.query.filter_by(invite_code=invite_code).first_or_404()
    
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        if user_name:
            session['user_name'] = user_name
            session['event_id'] = event.id
            
            # Record guest entry
            member = GroupMember(event_id=event.id, name=user_name)
            db.session.add(member)
            db.session.commit()
            
            return redirect(url_for('event_detail', event_id=event.id))
            
    return render_template('join_group.html', event=event)

@app.route('/join', methods=['POST'])
def join_with_code():
    invite_code = request.form.get('invite_code', '').strip().upper()
    if invite_code:
        event = Event.query.filter_by(invite_code=invite_code).first()
        if event:
            return redirect(url_for('join_group', invite_code=invite_code))
        flash('Invalid invite code. Please try again.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/api/event/<int:event_id>/chat', methods=['GET', 'POST'])
def chat(event_id):
    if request.method == 'POST':
        data = request.get_json()
        sender = session.get('user_name', 'Guest')
        msg_text = data.get('message')
        
        if msg_text:
            msg = ChatMessage(event_id=event_id, sender_name=sender, message=msg_text)
            db.session.add(msg)
            db.session.commit()
            return jsonify({"status": "sent"})
            
    messages = ChatMessage.query.filter_by(event_id=event_id).order_by(ChatMessage.timestamp.asc()).all()
    return jsonify([{
        "sender": m.sender_name,
        "message": m.message,
        "time": m.timestamp.strftime('%H:%M')
    } for m in messages])

@app.route('/api/event/<int:event_id>/update', methods=['POST'])
def update_planning(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.get_json()
    
    if 'budget' in data:
        event.total_budget = float(data['budget'])
    if 'needs' in data:
        event.needs = ",".join(data['needs'])
    if 'location' in data:
        event.location = data['location']
    if 'sub_location' in data:
        event.sub_location = data['sub_location']
        
    db.session.commit()
    return jsonify({"status": "updated"})

@app.route('/api/event/<int:event_id>/select_plan', methods=['POST'])
def select_plan(event_id):
    event = Event.query.get_or_404(event_id)
    data = request.get_json()
    
    # Store the entire plan data for persistence
    event.selected_plan = data.get('plan')
    db.session.commit()
    return jsonify({"status": "selected"})

@app.route('/delete_event/<int:event_id>')
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted.', 'info')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
