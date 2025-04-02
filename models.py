import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Create a base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Create db instance
db = SQLAlchemy(model_class=Base)

class ChatHistory(db.Model):
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    detected_mood = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChatHistory id={self.id} mood={self.detected_mood}>'

class MoodStatistics(db.Model):
    __tablename__ = 'mood_statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(50), nullable=False, unique=True)
    count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<MoodStatistics mood={self.mood} count={self.count}>'
        
class MoodHistory(db.Model):
    __tablename__ = 'mood_history'
    
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(50), nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MoodHistory mood={self.mood} recorded_at={self.recorded_at}>'