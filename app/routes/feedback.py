# ===== app/routes/feedback.py =====
from flask import Blueprint, request, jsonify
from app import db
from app.models.feedback import Feedback
from app.models.session import Session

feedback_bp = Blueprint('feedback', __name__)


def calculate_scores(metrics, conversation):
    """Calculate performance scores based on metrics and conversation"""
    # Simplified scoring algorithm - can be enhanced with ML
    
    # Base scores
    overall_score = 7.0
    communication_score = 7.0
    confidence_score = 7.0
    technical_score = 7.0
    
    # Adjust based on response time
    avg_response_time = metrics.get('avg_response_time', 0)
    if avg_response_time > 10:  # Too slow
        confidence_score -= 2
        overall_score -= 1
    elif avg_response_time < 2:  # Too fast (might be rushed)
        confidence_score -= 0.5
    
    # Adjust based on word count
    total_words = metrics.get('total_words', 0)
    total_responses = metrics.get('total_responses', 1)
    avg_words_per_response = total_words / total_responses if total_responses > 0 else 0
    
    if avg_words_per_response < 10:  # Too brief
        communication_score -= 1.5
        overall_score -= 1
    elif avg_words_per_response > 100:  # Too verbose
        communication_score -= 0.5
    
    # Adjust based on session duration
    session_duration = metrics.get('session_duration', 0)
    if session_duration < 5:  # Too short
        overall_score -= 2
    elif session_duration > 30:  # Good engagement
        overall_score += 0.5
    
    # Ensure scores are within 1-10 range
    scores = [overall_score, communication_score, confidence_score, technical_score]
    scores = [max(1.0, min(10.0, score)) for score in scores]
    
    return scores

def generate_feedback_content(scores, metrics, conversation):
    """Generate detailed feedback content"""
    strengths = []
    improvements = []
    suggestions = []
    
    overall_score = scores[0]
    
    # Generate strengths based on performance
    if overall_score >= 8:
        strengths.append("Excelente desempeño general en la entrevista")
    if metrics.get('avg_response_time', 0) < 5:
        strengths.append("Tiempo de respuesta apropiado y natural")
    if metrics.get('session_duration', 0) > 15:
        strengths.append("Buena participación durante toda la sesión")
    
    # Generate improvement areas
    if scores[1] < 7:  # Communication
        improvements.append("Mejorar la claridad y estructura de las respuestas")
    if scores[2] < 7:  # Confidence
        improvements.append("Trabajar en la confianza y seguridad al responder")
    if scores[3] < 7:  # Technical
        improvements.append("Fortalecer conocimientos técnicos específicos del área")
    
    # Generate specific suggestions
    avg_words = metrics.get('total_words', 0) / metrics.get('total_responses', 1) if metrics.get('total_responses', 0) > 0 else 0
    if avg_words < 15:
        suggestions.append("Elaborar más las respuestas con ejemplos específicos")
    if metrics.get('avg_response_time', 0) > 8:
        suggestions.append("Practicar respuestas a preguntas comunes para mejorar fluidez")
    
    suggestions.append("Continuar practicando con diferentes tipos de entrevistas")
    
    return strengths, improvements, suggestions

@feedback_bp.route('/', methods=['POST'])
def create_feedback():
    """Generate feedback for a session (CU5: Recibir retroalimentación)"""
    try:
        data = request.get_json()
        
        if not data.get('session_id'):
            return jsonify({'error': 'Session ID is required'}), 400
        
        session = Session.query.get_or_404(data['session_id'])
        
        # Check if feedback already exists
        if session.feedback:
            return jsonify({'error': 'Feedback already exists for this session'}), 409
        
        # Generate automated feedback based on performance metrics
        metrics = session.get_performance_metrics()
        conversation = session.get_conversation_history()
        
        # Calculate scores
        scores = calculate_scores(metrics, conversation)
        overall_score, communication_score, confidence_score, technical_score = scores
        
        # Generate detailed feedback content
        strengths, improvements, suggestions = generate_feedback_content(scores, metrics, conversation)
        
        feedback = Feedback(
            session_id=data['session_id'],
            overall_score=overall_score,
            communication_score=communication_score,
            confidence_score=confidence_score,
            technical_score=technical_score,
            avg_response_time=metrics.get('avg_response_time', 0),
            total_words_spoken=metrics.get('total_words', 0),
            hesitation_count=0  # This would need speech analysis to calculate
        )
        
        feedback.set_strengths(strengths)
        feedback.set_areas_for_improvement(improvements)
        feedback.set_specific_suggestions(suggestions)
        
        db.session.add(feedback)
        db.session.commit()
        
        return jsonify({
            'message': 'Feedback generated successfully',
            'feedback': feedback.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@feedback_bp.route('/<int:feedback_id>', methods=['GET'])
def get_feedback(feedback_id):
    """Get specific feedback"""
    try:
        feedback = Feedback.query.get_or_404(feedback_id)
        return jsonify(feedback.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@feedback_bp.route('/session/<int:session_id>', methods=['GET'])
def get_session_feedback(session_id):
    """Get feedback for a specific session"""
    try:
        session = Session.query.get_or_404(session_id)
        if not session.feedback:
            return jsonify({'error': 'No feedback found for this session'}), 404
        
        return jsonify(session.feedback.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
