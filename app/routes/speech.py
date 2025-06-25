# ===== app/routes/speech.py =====
from flask import Blueprint, request, jsonify
from google.generativeai import GenerativeModel, configure
from google.genai import types
from config import Config
import base64

speech_bp = Blueprint('speech', __name__)  # Corrige _name a _name_

# Configura Gemini
configure(api_key=Config.AI_API_KEY)
model = GenerativeModel("gemini-2.5-flash")

@speech_bp.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        data = request.get_json()
        if not data or 'base64_audio' not in data:
            return jsonify({'error': 'Missing "base64_audio" field in JSON'}), 400

        # Decodifica base64 a bytes
        audio_bytes = data['base64_audio']

        audio_part = {
            "mime_type": "audio/wav",  # Usa 24000 si ese es tu sample rate
            "data": audio_bytes
        }

        # Envia el audio al modelo
        response = model.generate_content(contents=[
            "Por favor, transcribe este audio, está en español",
            audio_part
        ])

        return jsonify({"text": response.text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500