# ===== app/routes/speech.py =====
from flask import Blueprint, request, jsonify
from google.generativeai import GenerativeModel, configure
from google.genai import types
from config import Config
import base64

speech_bp = Blueprint('speech', __name__)  # Corrige _name a _name_

# Configura Gemini
configure(api_key=Config.AI_API_KEY)
model = GenerativeModel("gemini-1.5-flash")

@speech_bp.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        data = request.get_json()
        print(data)
        if not data or 'base64_audio' not in data:
            return jsonify({'error': 'Missing "base64_audio" field in JSON'}), 400

        # Decodifica base64 a bytes
        audio_bytes = base64.b64decode(data['base64_audio'])

        # Envia el audio al modelo
        response = model.generate_content([
            {"role": "user", "parts":[
                "Dime textualmente el contenido del audio, se encuentra en español.",
                {
                    "inline_data": {
                        "mime_type": "audio/L16;rate=44100",
                        "data": audio_bytes
                }
            }]
}  # Ajusta el rate si es necesario
        ])

        return jsonify({"text": response.text}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500