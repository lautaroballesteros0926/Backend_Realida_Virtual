# ===== app/models/session.py =====
from app import db
from datetime import datetime
import json

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'), nullable=False)
    
    # Session configuration
    difficulty_level = db.Column(db.String(20), nullable=False)
    interviewer_avatar = db.Column(db.String(50), default='profesional')
    environment = db.Column(db.String(50), default='oficina')
    custom_description = db.Column(db.Text)  # User's custom scenario description
    
    # Session data
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='active')  # active, completed, abandoned
    
    # Conversation and performance data (JSON)
    conversation_history = db.Column(db.Text)  # JSON string
    performance_metrics = db.Column(db.Text)   # JSON string
    
    # Relationships
    feedback = db.relationship('Feedback', backref='session', uselist=False, cascade='all, delete-orphan')
    
    def __init__(self, user_id, scenario_id, difficulty_level, **kwargs):
        self.user_id = user_id
        self.scenario_id = scenario_id
        self.difficulty_level = difficulty_level
        self.conversation_history = json.dumps([])
        self.performance_metrics = json.dumps({})
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def add_conversation_turn(self, speaker, message, timestamp=None, response_time=None):
        """Add a turn to the conversation history"""
        history = self.get_conversation_history()
        turn = {
            'speaker': speaker,  # 'user' or 'interviewer'
            'message': message,
            'timestamp': (timestamp or datetime.utcnow()).isoformat(),
            'response_time': response_time  # Time taken to respond (seconds)
        }
        history.append(turn)
        self.conversation_history = json.dumps(history)
    
    def get_conversation_history(self):
        return json.loads(self.conversation_history) if self.conversation_history else []
    
    def update_performance_metrics(self, metrics):
        """Update performance metrics"""
        current_metrics = self.get_performance_metrics()
        current_metrics.update(metrics)
        self.performance_metrics = json.dumps(current_metrics)
    
    def get_performance_metrics(self):
        return json.loads(self.performance_metrics) if self.performance_metrics else {}
    
    def get_duration_minutes(self):
        """Get session duration in minutes"""
        if self.ended_at and self.started_at:
            return (self.ended_at - self.started_at).total_seconds() / 60
        elif self.started_at:
            return (datetime.utcnow() - self.started_at).total_seconds() / 60
        else:
            return 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'scenario_id': self.scenario_id,
            'difficulty_level': self.difficulty_level,
            'interviewer_avatar': self.interviewer_avatar,
            'environment': self.environment,
            'custom_description': self.custom_description,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'status': self.status,
            'duration_minutes': self.get_duration_minutes(),
            'conversation_history': self.get_conversation_history(),
            'performance_metrics': self.get_performance_metrics()
        }
