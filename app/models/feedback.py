# ===== app/models/feedback.py =====
from app import db
from datetime import datetime
import json

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    
    # Overall scores (1-10 scale)
    overall_score = db.Column(db.Float, nullable=False)
    communication_score = db.Column(db.Float, nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    technical_score = db.Column(db.Float, nullable=False)
    
    # Detailed feedback (JSON)
    strengths = db.Column(db.Text)           # JSON array of strengths
    areas_for_improvement = db.Column(db.Text)  # JSON array of improvement areas
    specific_suggestions = db.Column(db.Text)   # JSON array of specific suggestions
    
    # Metrics analysis
    avg_response_time = db.Column(db.Float)  # Average response time in seconds
    total_words_spoken = db.Column(db.Integer)
    hesitation_count = db.Column(db.Integer)  # Number of "um", "eh", etc.
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, session_id, overall_score, communication_score, confidence_score, technical_score, **kwargs):
        self.session_id = session_id
        self.overall_score = overall_score
        self.communication_score = communication_score
        self.confidence_score = confidence_score
        self.technical_score = technical_score
        
        # Initialize JSON fields as empty arrays
        self.strengths = json.dumps([])
        self.areas_for_improvement = json.dumps([])
        self.specific_suggestions = json.dumps([])
        
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def set_strengths(self, strengths_list):
        self.strengths = json.dumps(strengths_list)
    
    def get_strengths(self):
        return json.loads(self.strengths) if self.strengths else []
    
    def set_areas_for_improvement(self, areas_list):
        self.areas_for_improvement = json.dumps(areas_list)
    
    def get_areas_for_improvement(self):
        return json.loads(self.areas_for_improvement) if self.areas_for_improvement else []
    
    def set_specific_suggestions(self, suggestions_list):
        self.specific_suggestions = json.dumps(suggestions_list)
    
    def get_specific_suggestions(self):
        return json.loads(self.specific_suggestions) if self.specific_suggestions else []
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'overall_score': self.overall_score,
            'communication_score': self.communication_score,
            'confidence_score': self.confidence_score,
            'technical_score': self.technical_score,
            'strengths': self.get_strengths(),
            'areas_for_improvement': self.get_areas_for_improvement(),
            'specific_suggestions': self.get_specific_suggestions(),
            'avg_response_time': self.avg_response_time,
            'total_words_spoken': self.total_words_spoken,
            'hesitation_count': self.hesitation_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }