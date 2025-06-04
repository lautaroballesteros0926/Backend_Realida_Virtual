# ===== app/models/scenario.py =====
from app import db
import json

class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    
    # JSON fields for complex data
    difficulty_levels = db.Column(db.Text)  # Stored as JSON string
    sample_questions = db.Column(db.Text)   # Stored as JSON string
    
    # Configuration options
    interviewer_avatars = db.Column(db.Text)  # JSON: available avatar options
    environments = db.Column(db.Text)         # JSON: available environments
    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    sessions = db.relationship('Session', backref='scenario', lazy=True)
    
    def __init__(self, name, description, category, difficulty_levels=None, sample_questions=None, **kwargs):
        self.name = name
        self.description = description
        self.category = category
        self.difficulty_levels = json.dumps(difficulty_levels or ['básico', 'intermedio', 'avanzado'])
        self.sample_questions = json.dumps(sample_questions or [])
        self.interviewer_avatars = json.dumps(['profesional', 'amigable', 'serio'])
        self.environments = json.dumps(['oficina', 'sala_reuniones', 'espacio_moderno'])
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def get_difficulty_levels(self):
        return json.loads(self.difficulty_levels) if self.difficulty_levels else []
    
    def get_sample_questions(self):
        return json.loads(self.sample_questions) if self.sample_questions else []
    
    def get_interviewer_avatars(self):
        return json.loads(self.interviewer_avatars) if self.interviewer_avatars else []
    
    def get_environments(self):
        return json.loads(self.environments) if self.environments else []
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'difficulty_levels': self.get_difficulty_levels(),
            'sample_questions': self.get_sample_questions(),
            'interviewer_avatars': self.get_interviewer_avatars(),
            'environments': self.get_environments(),
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
