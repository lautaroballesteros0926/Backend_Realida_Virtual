# ===== app/routes/speech.py =====
from flask import Blueprint, request, jsonify
from google.generativeai import GenerativeModel, configure, types
from config import Config

speech_bp = Blueprint('speech', __name__)

# Configura Gemini
configure(api_key=Config.AI_API_KEY)
model = GenerativeModel("gemini-1.5-flash")

@speech_bp.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400

        audio_file = request.files['audio']
        audio_bytes = audio_file.read()

        response = model.generate_content([
            "Dime textualmente el contenido del audio, se encuentra en español.",
            types.Part.from_bytes(data=audio_bytes, mime_type='audio/L16;rate=44100')
        ])

        return jsonify({"text": response.text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500