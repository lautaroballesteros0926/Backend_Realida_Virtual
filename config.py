# ===== config.py =====
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///vr_interviews.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # IA API Configuration
    AI_API_KEY = os.environ.get('AI_API_KEY') or 'AIzaSyAUOl7tx3q4atsrHUuuVDusqxwDIE5KZpM'
    
    # Response time limit (seconds)
    MAX_RESPONSE_TIME = 3
