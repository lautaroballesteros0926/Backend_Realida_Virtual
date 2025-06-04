# routes/test.py
from flask import Blueprint, jsonify
from app import db
from app.models.session import Session
from app.models.scenario import Scenario
from app.models.user import User
import uuid

test_bp = Blueprint('test', __name__)

@test_bp.route('/test/create_session', methods=['POST'])
def create_test_session():
    try:
        # Buscar o crear un usuario de prueba
        user = User.query.first()
        if not user:
            user = User(
                email='testuser@example.com',
                first_name='Test',
                last_name='User',
                preferred_difficulty='intermedio',
                anxiety_level=2
            )
            user.set_password('test123')
            db.session.add(user)
            db.session.commit()  # Commitea para guardar y tener ID asignado

        # Buscar un escenario
        scenario = Scenario.query.first()
        if not scenario:
            return jsonify({'error': 'No scenarios found in the database'}), 404

        # Crear la sesión SIN definir id
        session = Session(
            user_id=user.id,
            scenario_id=scenario.id,
            difficulty_level='intermedio',
            interviewer_avatar='default_avatar',
            custom_description='Eres un entrevistador amable pero exigente.',
            conversation_history='[]',  # Campo JSON string
            performance_metrics='{}'    # Inicializa performance_metrics también
        )

        db.session.add(session)
        db.session.commit()  # Guarda y asigna el ID autoincremental

        return jsonify({
            'session_id': session.id,
            'user_id': user.id,
            'scenario_id': scenario.id
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500