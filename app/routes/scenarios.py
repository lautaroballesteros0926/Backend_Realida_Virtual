# ===== app/routes/scenarios.py =====
from flask import Blueprint, request, jsonify
from app import db
from app.models.scenario import Scenario

scenarios_bp = Blueprint('scenarios', __name__)

@scenarios_bp.route('/', methods=['GET'])
def get_scenarios():
    """Get all available scenarios (CU2: Seleccionar escenario de entrevista)"""
    try:
        category = request.args.get('category')
        
        query = Scenario.query.filter_by(is_active=True)
        if category:
            query = query.filter_by(category=category)
        
        scenarios = query.all()
        
        return jsonify([scenario.to_dict() for scenario in scenarios]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@scenarios_bp.route('/<int:scenario_id>', methods=['GET'])
def get_scenario(scenario_id):
    """Get specific scenario details"""
    try:
        scenario = Scenario.query.get_or_404(scenario_id)
        return jsonify(scenario.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@scenarios_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all available categories"""
    try:
        categories = db.session.query(Scenario.category).distinct().all()
        return jsonify([cat[0] for cat in categories]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# For developers (CU7: Crear nuevos escenarios)
@scenarios_bp.route('/', methods=['POST'])
def create_scenario():
    """Create new scenario (for developers)"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'description', 'category']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Field {field} is required'}), 400
        
        scenario = Scenario(
            name=data['name'],
            description=data['description'],
            category=data['category'],
            difficulty_levels=data.get('difficulty_levels', ['básico', 'intermedio', 'avanzado']),
            sample_questions=data.get('sample_questions', [])
        )
        
        db.session.add(scenario)
        db.session.commit()
        
        return jsonify({
            'message': 'Scenario created successfully',
            'scenario': scenario.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
