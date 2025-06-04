from flask import Blueprint, request, jsonify
from app.services.interviewer_ai import InterviewerAI
from app.models.session import Session
from app.models.scenario import Scenario
from app import db
import time

interviewer_bp = Blueprint('interviewer', __name__)

@interviewer_bp.route('/question', methods=['POST'])
def get_next_question():
    """Get next question from AI interviewer (CU4: Participar en la entrevista simulada)"""
    try:
        data = request.get_json()
        
        if not data.get('session_id'):
            return jsonify({'error': 'Session ID is required'}), 400
        
        session = Session.query.get_or_404(data['session_id'])
        scenario = session.scenario
        
        # Get conversation history
        conversation_history = session.get_conversation_history()
        
        # Initialize AI interviewer
        ai_interviewer = InterviewerAI()
        
        # Get context for AI
        context = {
            'scenario_name': scenario.name,
            'scenario_description': scenario.description,
            'difficulty_level': session.difficulty_level,
            'interviewer_avatar': session.interviewer_avatar,
            'custom_description': session.custom_description,
            'conversation_history': conversation_history
        }
        
        # Get next question from AI
        start_time = time.time()
        ai_response = ai_interviewer.get_next_question(context)
        response_time = time.time() - start_time
        
        if ai_response:
            # Add AI response to conversation history
            session.add_conversation_turn(
                speaker='interviewer',
                message=ai_response,
                response_time=response_time
            )
            db.session.commit()
            
            return jsonify({
                'question': ai_response,
                'response_time': response_time
            }), 200
        else:
            return jsonify({'error': 'Failed to generate question'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@interviewer_bp.route('/response', methods=['POST'])
def process_user_response():
    """Process user response and update session (CU4: Participar en la entrevista simulada)"""
    try:
        data = request.get_json()
        
        required_fields = ['session_id', 'user_response']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Field {field} is required'}), 400
        
        session = Session.query.get_or_404(data['session_id'])
        
        # Add user response to conversation history
        session.add_conversation_turn(
            speaker='user',
            message=data['user_response'],
            response_time=data.get('response_time', 0)
        )
        
        # Update performance metrics
        conversation = session.get_conversation_history()
        user_responses = [turn for turn in conversation if turn['speaker'] == 'user']
        
        # Calculate updated metrics
        total_words = sum(len(response['message'].split()) for response in user_responses)
        avg_response_time = sum(response.get('response_time', 0) for response in user_responses) / len(user_responses)
        
        session.update_performance_metrics({
            'total_responses': len(user_responses),
            'total_words': total_words,
            'avg_response_time': avg_response_time
        })
        
        db.session.commit()
        
        return jsonify({
            'message': 'Response processed successfully',
            'conversation_length': len(conversation)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
