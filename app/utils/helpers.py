# ===== app/utils/helpers.py =====
from datetime import datetime
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, "Password is valid"

def calculate_session_stats(sessions):
    """Calculate user session statistics"""
    if not sessions:
        return {
            'total_sessions': 0,
            'avg_score': 0,
            'total_hours': 0,
            'improvement_trend': 0
        }
    
    total_sessions = len(sessions)
    scores = [s.feedback.overall_score for s in sessions if s.feedback]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    total_minutes = sum(s.get_duration_minutes() for s in sessions)
    total_hours = total_minutes / 60
    
    # Calculate improvement trend (last 3 vs first 3 sessions)
    improvement_trend = 0
    if len(scores) >= 6:
        first_three = sum(scores[:3]) / 3
        last_three = sum(scores[-3:]) / 3
        improvement_trend = last_three - first_three
    
    return {
        'total_sessions': total_sessions,
        'avg_score': round(avg_score, 2),
        'total_hours': round(total_hours, 2),
        'improvement_trend': round(improvement_trend, 2)
    }

def format_datetime(dt):
    """Format datetime for API responses"""
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt

def analyze_response_quality(response_text):
    """Analyze quality of user response"""
    if not response_text:
        return {'word_count': 0, 'quality_score': 0}
    
    words = response_text.split()
    word_count = len(words)
    
    # Simple quality scoring
    quality_score = 5  # Base score
    
    if word_count > 20:
        quality_score += 1
    if word_count > 50:
        quality_score += 1
    if word_count < 5:
        quality_score -= 2
    
    # Look for positive indicators
    positive_words = ['experiencia', 'aprendí', 'logré', 'desarrollé', 'implementé']
    if any(word in response_text.lower() for word in positive_words):
        quality_score += 1
    
    quality_score = max(1, min(10, quality_score))
    
    return {
        'word_count': word_count,
        'quality_score': quality_score
    }

