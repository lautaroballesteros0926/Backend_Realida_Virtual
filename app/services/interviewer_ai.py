import google.generativeai as genai
from flask import current_app
from config import Config

class InterviewerAI:
    def __init__(self):
        genai.configure(api_key=Config.AI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.max_response_time = Config.MAX_RESPONSE_TIME

    def get_next_question(self, context):
        try:
            prompt = self._build_prompt(context)
            system_prompt = self._get_system_prompt(context)

            full_prompt = f"{system_prompt}\n\n{prompt}"

            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 150
                }
            )

            return response.text.strip()

        except Exception as e:
            current_app.logger.error(f"Gemini API error: {str(e)}")
            return self._get_fallback_question(context)

    def _get_system_prompt(self, context):
        avatar_personality = {
            'profesional': 'Eres un entrevistador profesional, formal pero amigable.',
            'amigable': 'Eres un entrevistador muy amigable y relajado que busca hacer sentir cómodo al candidato.',
            'serio': 'Eres un entrevistador serio y directo, que va al grano en sus preguntas.'
        }

        personality = avatar_personality.get(context.get('interviewer_avatar', 'profesional'))

        return f"""
        {personality}

        Estás conduciendo una entrevista para el puesto de: {context.get('scenario_name', 'Trabajo general')}
        Descripción del escenario: {context.get('scenario_description', '')}
        Nivel de dificultad: {context.get('difficulty_level', 'básico')}

        Instrucciones:
        - Haz preguntas relevantes al puesto y nivel de dificultad
        - Mantén un tono {context.get('interviewer_avatar', 'profesional')}
        - Las preguntas deben ser en español
        - Sé conciso en tus preguntas (máximo 2-3 oraciones)
        - Adapta las preguntas según las respuestas previas del candidato
        """

    def _build_prompt(self, context):
        conversation_history = context.get('conversation_history', [])
        custom_description = context.get('custom_description', '')

        prompt = f"Escenario de entrevista: {context.get('scenario_name')}\n"

        if custom_description:
            prompt += f"Descripción personalizada: {custom_description}\n"

        if conversation_history:
            prompt += "\nConversación previa:\n"
            for turn in conversation_history[-6:]:
                speaker = "Entrevistador" if turn['speaker'] == 'interviewer' else "Candidato"
                prompt += f"{speaker}: {turn['message']}\n"

        if not conversation_history:
            prompt += "\nEsta es la primera pregunta de la entrevista. Comienza con una pregunta de presentación apropiada."
        else:
            prompt += "\nGenera la siguiente pregunta apropiada para continuar la entrevista."

        return prompt

    def _get_fallback_question(self, context):
        """Get fallback question if AI API fails"""
        scenario_name = context.get('scenario_name', '').lower()
        conversation_history = context.get('conversation_history', [])
        
        # Fallback questions by scenario
        fallback_questions = {
            'programador': [
                "¿Podrías contarme sobre tu experiencia en programación?",
                "¿Qué lenguajes de programación dominas mejor?",
                "¿Cómo enfrentas los desafíos técnicos en tus proyectos?",
                "¿Puedes describir un proyecto del que te sientas orgulloso?"
            ],
            'atención al cliente': [
                "¿Qué te motiva a trabajar en atención al cliente?",
                "¿Cómo manejarías a un cliente molesto o insatisfecho?",
                "¿Qué consideras más importante en el servicio al cliente?",
                "Cuéntame sobre una situación difícil que hayas resuelto"
            ],
            'marketing': [
                "¿Cuál es tu experiencia en marketing digital?",
                "¿Cómo medirías el éxito de una campaña publicitaria?",
                "¿Qué redes sociales consideras más efectivas y por qué?",
                "¿Cómo te mantienes actualizado con las tendencias del marketing?"
            ]
        }
        
        # Determine which set of questions to use
        questions = None
        for key in fallback_questions:
            if key in scenario_name:
                questions = fallback_questions[key]
                break
        
        if not questions:
            questions = [
                "¿Podrías presentarte y contarme sobre tu experiencia?",
                "¿Qué te interesa de esta posición?",
                "¿Cuáles consideras que son tus principales fortalezas?",
                "¿Cómo te ves en 5 años?"
            ]
        
        # Return question based on conversation progress
        question_index = len(conversation_history) // 2  # Every 2 turns (user + interviewer)
        if question_index >= len(questions):
            question_index = len(questions) - 1
        
        return questions[question_index]
