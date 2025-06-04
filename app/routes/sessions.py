# ===== app/routes/sessions.py =====
from flask import Blueprint, request, jsonify
from app import db
from app.models.session import Session
from app.models.user import User
from app.models.scenario import Scenario
from datetime import datetime

sessions_bp = Blueprint('sessions', __name__)

@sessions_bp.route('/', methods=['POST'])
def create_session():
    """Create new interview session (CU4: Participar en la entrevista simulada)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'scenario_id', 'difficulty_level']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Field {field} is required'}), 400
        
        # Validate user and scenario exist
        user = User.query.get_or_404(data['user_id'])
        scenario = Scenario.query.get_or_404(data['scenario_id'])
        
        # Validate difficulty level
        if data['difficulty_level'] not in scenario.get_difficulty_levels():
            return jsonify({'error': 'Invalid difficulty level for this scenario'}), 400
        
        session = Session(
            user_id=data['user_id'],
            scenario_id=data['scenario_id'],
            difficulty_level=data['difficulty_level'],
            interviewer_avatar=data.get('interviewer_avatar', 'profesional'),
            environment=data.get('environment', 'oficina'),
            custom_description=data.get('custom_description')
        )
        
        db.session.add(session)
        db.session.commit()
        
        return jsonify({
            'message': 'Session created successfully',
            'session': session.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@sessions_bp.route('/<int:session_id>', methods=['GET'])
def get_session(session_id):
    """Get session details"""
    try:
        session = Session.query.get_or_404(session_id)
        return jsonify(session.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@sessions_bp.route('/<int:session_id>/conversation', methods=['POST'])
def add_conversation_turn():
    """Add a conversation turn to the session"""
    try:
        data = request.get_json()
        session = Session.query.get_or_404(session_id)
        
        if not data.get('speaker') or not data.get('message'):
            return jsonify({'error': 'Speaker and message are required'}), 400
        
        session.add_conversation_turn(
            speaker=data['speaker'],
            message=data['message'],
            response_time=data.get('response_time')
        )
        
        db.session.commit()
        
        return jsonify({
            'message': 'Conversation turn added successfully',
            'conversation_history': session.get_conversation_history()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@sessions_bp.route('/<int:session_id>/end', methods=['POST'])
def end_session(session_id):
    """End interview session"""
    try:
        session = Session.query.get_or_404(session_id)
        
        if session.status != 'active':
            return jsonify({'error': 'Session is not active'}), 400
        
        session.ended_at = datetime.utcnow()
        session.status = 'completed'
        
        # Calculate performance metrics
        conversation = session.get_conversation_history()
        user_responses = [turn for turn in conversation if turn['speaker'] == 'user']
        
        metrics = {
            'total_responses': len(user_responses),
            'total_words': sum(len(response['message'].split()) for response in user_responses),
            'avg_response_time': sum(response.get('response_time', 0) for response in user_responses) / len(user_responses) if user_responses else 0,
            'session_duration': session.get_duration_minutes()
        }
        
        session.update_performance_metrics(metrics)
        db.session.commit()
        
        return jsonify({
            'message': 'Session ended successfully',
            'session': session.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@sessions_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_sessions(user_id):
    """Get user's session history (CU6: Revisar historial de desempeño)"""
    try:
        user = User.query.get_or_404(user_id)
        
        # Query parameters for filtering
        limit = request.args.get('limit', 10, type=int)
        status = request.args.get('status', 'completed')
        
        sessions = Session.query.filter_by(user_id=user_id, status=status)\
                                .order_by(Session.started_at.desc())\
                                .limit(limit).all()
        
        return jsonify([session.to_dict() for session in sessions]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500