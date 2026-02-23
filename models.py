from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unique_number = db.Column(db.String(20), unique=True, nullable=False) # PIN/Unique ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Link to user
    person_name = db.Column(db.String(100), nullable=False)
    birthday_date = db.Column(db.Date, nullable=False)
    total_budget = db.Column(db.Float, nullable=False)
    friends_count = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    sub_location = db.Column(db.String(100), default="") # Specific area like Koramangala
    is_hidden = db.Column(db.Boolean, default=False)
    invite_code = db.Column(db.String(20), unique=True, nullable=True) # Unique join code
    needs = db.Column(db.String(500), default="") # comma separated needs: food,cake,decor,venue
    selected_plan = db.Column(db.JSON, nullable=True) # Stored selected plan data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def invite_link(self):
        return f"/join/{self.invite_code}"

    @property
    def cost_per_person(self):
        if self.friends_count > 0:
            return self.total_budget / self.friends_count
        return self.total_budget

    @property
    def budget_breakdown(self):
        needs_list = self.needs.split(',') if self.needs else []
        breakdown = {}
        
        # Calculate total weighted parts based on selected needs
        weights = {
            "cake": 0.30 if "cake" in needs_list else 0,
            "decor": 0.20 if "decor" in needs_list else 0,
            "food": 0.50 if "food" in needs_list else 0
        }
        
        total_weight = sum(weights.values())
        if total_weight == 0: # Default if nothing selected
            return {"cake": self.total_budget * 0.3, "decor": self.total_budget * 0.2, "food": self.total_budget * 0.5}
            
        for key, weight in weights.items():
            if weight > 0:
                # Redistribute budget based on selected items
                breakdown[key] = (weight / total_weight) * self.total_budget
            else:
                breakdown[key] = 0
        return breakdown

    @property
    def package_suggestion(self):
        if self.total_budget < 5000:
            return {
                "name": "Basic Package",
                "venue": "Home / Local Park",
                "cake": "Small Custom Cake",
                "decor": "DIY Balloons & Streamers",
                "food": "Snacks & Drinks"
            }
        elif self.total_budget < 15000:
            return {
                "name": "Standard Package",
                "venue": "Cafe / Restaurant Party Room",
                "cake": "Medium Themed Cake",
                "decor": "Professional Balloon Backdrop",
                "food": "Full Meal + Starters"
            }
        else:
            return {
                "name": "Premium Package",
                "venue": "Banquet Hall / Rooftop",
                "cake": "Large Multi-tier Designer Cake",
                "decor": "Full Theme Decor + Photo Booth",
                "food": "Buffet with Multiple Cuisines"
            }

class GroupMember(db.Model):
    __tablename__ = 'group_members'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    sender_name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class WishlistItem(db.Model):
    __tablename__ = 'wishlist_items'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    is_purchased = db.Column(db.Boolean, default=False)
