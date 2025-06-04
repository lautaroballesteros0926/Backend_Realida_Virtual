# ===== app/__init__.py =====
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.scenarios import scenarios_bp
    from app.routes.sessions import sessions_bp
    from app.routes.feedback import feedback_bp
    from app.routes.interviewer import interviewer_bp
    from app.routes.test import test_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(scenarios_bp, url_prefix='/api/scenarios')
    app.register_blueprint(sessions_bp, url_prefix='/api/sessions')
    app.register_blueprint(feedback_bp, url_prefix='/api/feedback')
    app.register_blueprint(interviewer_bp, url_prefix='/api/interviewer')
    app.register_blueprint(test_bp, url_prefix='/api')
    # Create tables
    with app.app_context():
        db.create_all()
        
        # Initialize default scenarios
        from app.models.scenario import Scenario
        if Scenario.query.count() == 0:
            init_default_scenarios()
    
    return app

def init_default_scenarios():
    """Initialize default interview scenarios"""
    from app.models.scenario import Scenario
    
    scenarios = [
        {
            'name': 'Programador Junior',
            'description': 'Entrevista técnica para posición de desarrollo de software',
            'category': 'Tecnología',
            'difficulty_levels': ['básico', 'intermedio', 'avanzado'],
            'sample_questions': [
                '¿Cuéntame sobre tu experiencia en programación?',
                '¿Qué lenguajes de programación dominas?',
                '¿Cómo resuelves un problema técnico complejo?'
            ]
        },
        {
            'name': 'Atención al Cliente',
            'description': 'Entrevista para posiciones de servicio y atención al cliente',
            'category': 'Servicios',
            'difficulty_levels': ['básico', 'intermedio', 'avanzado'],
            'sample_questions': [
                '¿Cómo manejarías a un cliente molesto?',
                '¿Qué significa para ti un buen servicio al cliente?',
                'Describe una situación difícil que hayas resuelto'
            ]
        },
        {
            'name': 'Marketing Digital',
            'description': 'Entrevista para especialistas en marketing y publicidad',
            'category': 'Marketing',
            'difficulty_levels': ['básico', 'intermedio', 'avanzado'],
            'sample_questions': [
                '¿Cómo medirías el éxito de una campaña digital?',
                '¿Qué redes sociales consideras más efectivas?',
                'Describe tu experiencia con análisis de datos'
            ]
        }
    ]
    
    for scenario_data in scenarios:
        scenario = Scenario(
            name=scenario_data['name'],
            description=scenario_data['description'],
            category=scenario_data['category'],
            difficulty_levels=scenario_data['difficulty_levels'],
            sample_questions=scenario_data['sample_questions']
        )
        db.session.add(scenario)
    
    db.session.commit()

