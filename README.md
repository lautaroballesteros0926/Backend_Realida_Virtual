# API Sistema de Entrevistas Virtuales

## Descripción General

El Sistema de Entrevistas Virtuales es una aplicación web desarrollada en Flask que permite a los usuarios practicar entrevistas laborales en un entorno virtual simulado. La plataforma utiliza inteligencia artificial para generar preguntas dinámicas y proporcionar retroalimentación personalizada sobre el desempeño del usuario.

### Características Principales

- **Registro y autenticación de usuarios**
- **Múltiples escenarios de entrevista** (Programador, Atención al Cliente, Marketing, etc.)
- **Entrevistador virtual con IA** que adapta las preguntas según el contexto
- **Sistema de retroalimentación detallado** con puntuaciones y sugerencias
- **Historial de sesiones** para seguimiento del progreso
- **Personalización de dificultad** y configuraciones del entorno

### Tecnologías Utilizadas

- **Backend**: Flask 2.3.3
- **Base de Datos**: SQLAlchemy con SQLite
- **Autenticación**: bcrypt para hash de contraseñas
- **IA**: Integración con APIs de modelos de lenguaje (OpenAI GPT)
- **CORS**: Flask-CORS para comunicación cross-origin

---

## Configuración y Instalación

### Requisitos del Sistema

```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
requests==2.31.0
python-dotenv==1.0.0
bcrypt==4.0.1
```

### Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
SECRET_KEY=tu-clave-secreta-aqui
DATABASE_URL=sqlite:///vr_interviews.db
AI_API_URL=https://api.openai.com/v1/chat/completions
AI_API_KEY=tu-api-key-de-openai
```

### Ejecución

```bash
python run.py
```

La aplicación se ejecutará en `http://localhost:5000`

---

## Arquitectura del Sistema

### Modelos de Datos

#### Usuario (User)
- **id**: Identificador único
- **email**: Correo electrónico (único)
- **password_hash**: Hash de la contraseña
- **first_name, last_name**: Nombres del usuario
- **preferred_difficulty**: Nivel de dificultad preferido
- **anxiety_level**: Nivel de ansiedad (1-10)
- **created_at, last_login**: Timestamps

#### Escenario (Scenario)
- **id**: Identificador único
- **name**: Nombre del escenario
- **description**: Descripción detallada
- **category**: Categoría profesional
- **difficulty_levels**: Niveles disponibles (JSON)
- **sample_questions**: Preguntas de ejemplo (JSON)
- **interviewer_avatars**: Avatares disponibles (JSON)
- **environments**: Entornos virtuales (JSON)

#### Sesión (Session)
- **id**: Identificador único
- **user_id**: Referencia al usuario
- **scenario_id**: Referencia al escenario
- **difficulty_level**: Nivel de dificultad seleccionado
- **interviewer_avatar**: Avatar del entrevistador
- **environment**: Entorno virtual
- **started_at, ended_at**: Timestamps de inicio y fin
- **conversation_history**: Historial de conversación (JSON)
- **performance_metrics**: Métricas de rendimiento (JSON)

#### Retroalimentación (Feedback)
- **id**: Identificador único
- **session_id**: Referencia a la sesión
- **overall_score**: Puntuación general (1-10)
- **communication_score**: Puntuación de comunicación
- **confidence_score**: Puntuación de confianza
- **technical_score**: Puntuación técnica
- **strengths**: Fortalezas identificadas (JSON)
- **areas_for_improvement**: Áreas de mejora (JSON)
- **specific_suggestions**: Sugerencias específicas (JSON)

---

## Endpoints de la API

### 🔐 Autenticación

#### POST /api/auth/register
**Descripción**: Registra un nuevo usuario en el sistema

**Cuerpo de la Solicitud**:
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123",
  "first_name": "Juan",
  "last_name": "Pérez",
  "preferred_difficulty": "básico",
  "anxiety_level": 5
}
```

**Respuesta Exitosa (201)**:
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "email": "usuario@ejemplo.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "preferred_difficulty": "básico",
    "anxiety_level": 5,
    "created_at": "2024-01-15T10:30:00",
    "last_login": null
  }
}
```

**Errores Posibles**:
- `400`: Campos requeridos faltantes
- `409`: Email ya registrado
- `500`: Error interno del servidor

---

#### POST /api/auth/login
**Descripción**: Autentica un usuario existente

**Cuerpo de la Solicitud**:
```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123"
}
```

**Respuesta Exitosa (200)**:
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "email": "usuario@ejemplo.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "preferred_difficulty": "básico",
    "anxiety_level": 5,
    "created_at": "2024-01-15T10:30:00",
    "last_login": "2024-01-15T14:20:00"
  }
}
```

**Errores Posibles**:
- `400`: Email y contraseña requeridos
- `401`: Credenciales inválidas
- `500`: Error interno del servidor

---

### 👤 Gestión de Usuarios

#### GET /api/users/{user_id}
**Descripción**: Obtiene el perfil de un usuario específico

**Parámetros de Ruta**:
- `user_id` (integer): ID del usuario

**Respuesta Exitosa (200)**:
```json
{
  "id": 1,
  "email": "usuario@ejemplo.com",
  "first_name": "Juan",
  "last_name": "Pérez",
  "preferred_difficulty": "básico",
  "anxiety_level": 5,
  "created_at": "2024-01-15T10:30:00",
  "last_login": "2024-01-15T14:20:00"
}
```

**Errores Posibles**:
- `404`: Usuario no encontrado
- `500`: Error interno del servidor

---

#### PUT /api/users/{user_id}
**Descripción**: Actualiza el perfil de un usuario

**Parámetros de Ruta**:
- `user_id` (integer): ID del usuario

**Cuerpo de la Solicitud**:
```json
{
  "first_name": "Juan Carlos",
  "last_name": "Pérez González",
  "preferred_difficulty": "intermedio",
  "anxiety_level": 3,
  "password": "nueva_contraseña123"
}
```

**Respuesta Exitosa (200)**:
```json
{
  "message": "User updated successfully",
  "user": {
    "id": 1,
    "email": "usuario@ejemplo.com",
    "first_name": "Juan Carlos",
    "last_name": "Pérez González",
    "preferred_difficulty": "intermedio",
    "anxiety_level": 3,
    "created_at": "2024-01-15T10:30:00",
    "last_login": "2024-01-15T14:20:00"
  }
}
```

---

#### GET /api/users/{user_id}/stats
**Descripción**: Obtiene estadísticas de rendimiento del usuario

**Parámetros de Ruta**:
- `user_id` (integer): ID del usuario

**Respuesta Exitosa (200)**:
```json
{
  "user_id": 1,
  "stats": {
    "total_sessions": 15,
    "avg_score": 7.8,
    "total_hours": 12.5,
    "improvement_trend": 1.2
  },
  "recent_scores": [7.5, 8.0, 8.2, 7.9, 8.5],
  "last_session": {
    "id": 25,
    "scenario_id": 1,
    "difficulty_level": "intermedio",
    "started_at": "2024-01-14T15:30:00",
    "ended_at": "2024-01-14T16:15:00",
    "status": "completed"
  }
}
```

---

### 🎭 Gestión de Escenarios

#### GET /api/scenarios/
**Descripción**: Obtiene todos los escenarios de entrevista disponibles

**Parámetros de Consulta Opcionales**:
- `category` (string): Filtrar por categoría específica

**Ejemplo de Solicitud**:
```
GET /api/scenarios/?category=Tecnología
```

**Respuesta Exitosa (200)**:
```json
[
  {
    "id": 1,
    "name": "Programador Junior",
    "description": "Entrevista técnica para posición de desarrollo de software",
    "category": "Tecnología",
    "difficulty_levels": ["básico", "intermedio", "avanzado"],
    "sample_questions": [
      "¿Cuéntame sobre tu experiencia en programación?",
      "¿Qué lenguajes de programación dominas?",
      "¿Cómo resuelves un problema técnico complejo?"
    ],
    "interviewer_avatars": ["profesional", "amigable", "serio"],
    "environments": ["oficina", "sala_reuniones", "espacio_moderno"],
    "is_active": true,
    "created_at": "2024-01-01T00:00:00"
  },
  {
    "id": 2,
    "name": "Atención al Cliente",
    "description": "Entrevista para posiciones de servicio y atención al cliente",
    "category": "Servicios",
    "difficulty_levels": ["básico", "intermedio", "avanzado"],
    "sample_questions": [
      "¿Cómo manejarías a un cliente molesto?",
      "¿Qué significa para ti un buen servicio al cliente?",
      "Describe una situación difícil que hayas resuelto"
    ],
    "interviewer_avatars": ["profesional", "amigable", "serio"],
    "environments": ["oficina", "sala_reuniones", "espacio_moderno"],
    "is_active": true,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

#### GET /api/scenarios/{scenario_id}
**Descripción**: Obtiene detalles de un escenario específico

**Parámetros de Ruta**:
- `scenario_id` (integer): ID del escenario

**Respuesta Exitosa (200)**:
```json
{
  "id": 1,
  "name": "Programador Junior",
  "description": "Entrevista técnica para posición de desarrollo de software",
  "category": "Tecnología",
  "difficulty_levels": ["básico", "intermedio", "avanzado"],
  "sample_questions": [
    "¿Cuéntame sobre tu experiencia en programación?",
    "¿Qué lenguajes de programación dominas?",
    "¿Cómo resuelves un problema técnico complejo?"
  ],
  "interviewer_avatars": ["profesional", "amigable", "serio"],
  "environments": ["oficina", "sala_reuniones", "espacio_moderno"],
  "is_active": true,
  "created_at": "2024-01-01T00:00:00"
}
```

---

#### GET /api/scenarios/categories
**Descripción**: Obtiene todas las categorías disponibles

**Respuesta Exitosa (200)**:
```json
["Tecnología", "Servicios", "Marketing", "Ventas", "Recursos Humanos"]
```

---

#### POST /api/scenarios/
**Descripción**: Crea un nuevo escenario de entrevista (para desarrolladores)

**Cuerpo de la Solicitud**:
```json
{
  "name": "Analista de Datos",
  "description": "Entrevista para posiciones de análisis y ciencia de datos",
  "category": "Tecnología",
  "difficulty_levels": ["básico", "intermedio", "avanzado"],
  "sample_questions": [
    "¿Qué herramientas de análisis de datos utilizas?",
    "¿Cómo abordarías un problema de datos faltantes?",
    "Explica la diferencia entre correlación y causalidad"
  ]
}
```

**Respuesta Exitosa (201)**:
```json
{
  "message": "Scenario created successfully",
  "scenario": {
    "id": 4,
    "name": "Analista de Datos",
    "description": "Entrevista para posiciones de análisis y ciencia de datos",
    "category": "Tecnología",
    "difficulty_levels": ["básico", "intermedio", "avanzado"],
    "sample_questions": [
      "¿Qué herramientas de análisis de datos utilizas?",
      "¿Cómo abordarías un problema de datos faltantes?",
      "Explica la diferencia entre correlación y causalidad"
    ],
    "interviewer_avatars": ["profesional", "amigable", "serio"],
    "environments": ["oficina", "sala_reuniones", "espacio_moderno"],
    "is_active": true,
    "created_at": "2024-01-15T16:45:00"
  }
}
```

---

### 🎯 Gestión de Sesiones

#### POST /api/sessions/
**Descripción**: Crea una nueva sesión de entrevista

**Cuerpo de la Solicitud**:
```json
{
  "user_id": 1,
  "scenario_id": 1,
  "difficulty_level": "intermedio",
  "interviewer_avatar": "profesional",
  "environment": "oficina",
  "custom_description": "Enfoque especial en frameworks de JavaScript"
}
```

**Respuesta Exitosa (201)**:
```json
{
  "message": "Session created successfully",
  "session": {
    "id": 15,
    "user_id": 1,
    "scenario_id": 1,
    "difficulty_level": "intermedio",
    "interviewer_avatar": "profesional",
    "environment": "oficina",
    "custom_description": "Enfoque especial en frameworks de JavaScript",
    "started_at": "2024-01-15T14:30:00",
    "ended_at": null,
    "status": "active",
    "duration_minutes": 0,
    "conversation_history": [],
    "performance_metrics": {}
  }
}
```

**Errores Posibles**:
- `400`: Campos requeridos faltantes o nivel de dificultad inválido
- `404`: Usuario o escenario no encontrado
- `500`: Error interno del servidor

---

#### GET /api/sessions/{session_id}
**Descripción**: Obtiene detalles de una sesión específica

**Parámetros de Ruta**:
- `session_id` (integer): ID de la sesión

**Respuesta Exitosa (200)**:
```json
{
  "id": 15,
  "user_id": 1,
  "scenario_id": 1,
  "difficulty_level": "intermedio",
  "interviewer_avatar": "profesional",
  "environment": "oficina",
  "custom_description": "Enfoque especial en frameworks de JavaScript",
  "started_at": "2024-01-15T14:30:00",
  "ended_at": "2024-01-15T15:15:00",
  "status": "completed",
  "duration_minutes": 45,
  "conversation_history": [
    {
      "speaker": "interviewer",
      "message": "¡Hola! Me complace conocerte. ¿Podrías presentarte y contarme sobre tu experiencia en programación?",
      "timestamp": "2024-01-15T14:30:15",
      "response_time": 2.3
    },
    {
      "speaker": "user",
      "message": "¡Hola! Soy Juan Pérez, tengo 3 años de experiencia desarrollando aplicaciones web principalmente con JavaScript y Python...",
      "timestamp": "2024-01-15T14:30:45",
      "response_time": 8.5
    }
  ],
  "performance_metrics": {
    "total_responses": 8,
    "total_words": 342,
    "avg_response_time": 6.8,
    "session_duration": 45
  }
}
```

---

#### POST /api/sessions/{session_id}/conversation
**Descripción**: Añade un turno de conversación a la sesión

**Parámetros de Ruta**:
- `session_id` (integer): ID de la sesión

**Cuerpo de la Solicitud**:
```json
{
  "speaker": "user",
  "message": "Tengo experiencia con React, Node.js y bases de datos MongoDB. He trabajado en varios proyectos de e-commerce...",
  "response_time": 12.5
}
```

**Respuesta Exitosa (200)**:
```json
{
  "message": "Conversation turn added successfully",
  "conversation_length": 5
}
```

**Errores Posibles**:
- `400`: Speaker y mensaje son requeridos
- `404`: Sesión no encontrada
- `500`: Error interno del servidor

---

#### POST /api/sessions/{session_id}/end
**Descripción**: Finaliza una sesión de entrevista

**Parámetros de Ruta**:
- `session_id` (integer): ID de la sesión

**Respuesta Exitosa (200)**:
```json
{
  "message": "Session ended successfully",
  "session": {
    "id": 15,
    "user_id": 1,
    "scenario_id": 1,
    "difficulty_level": "intermedio",
    "started_at": "2024-01-15T14:30:00",
    "ended_at": "2024-01-15T15:15:00",
    "status": "completed",
    "duration_minutes": 45,
    "performance_metrics": {
      "total_responses": 8,
      "total_words": 342,
      "avg_response_time": 6.8,
      "session_duration": 45
    }
  }
}
```

**Errores Posibles**:
- `400`: La sesión no está activa
- `404`: Sesión no encontrada
- `500`: Error interno del servidor

---

#### GET /api/sessions/user/{user_id}
**Descripción**: Obtiene el historial de sesiones de un usuario

**Parámetros de Ruta**:
- `user_id` (integer): ID del usuario

**Parámetros de Consulta Opcionales**:
- `limit` (integer): Número máximo de sesiones a retornar (por defecto: 10)
- `status` (string): Filtrar por estado (por defecto: "completed")

**Ejemplo de Solicitud**:
```
GET /api/sessions/user/1?limit=5&status=completed
```

**Respuesta Exitosa (200)**:
```json
[
  {
    "id": 15,
    "user_id": 1,
    "scenario_id": 1,
    "difficulty_level": "intermedio",
    "started_at": "2024-01-15T14:30:00",
    "ended_at": "2024-01-15T15:15:00",
    "status": "completed",
    "duration_minutes": 45
  },
  {
    "id": 14,
    "user_id": 1,
    "scenario_id": 2,
    "difficulty_level": "básico",
    "started_at": "2024-01-14T10:00:00",
    "ended_at": "2024-01-14T10:30:00",
    "status": "completed",
    "duration_minutes": 30
  }
]
```

---

### 🎤 Entrevistador Virtual (IA)

#### POST /api/interviewer/question
**Descripción**: Obtiene la siguiente pregunta del entrevistador virtual

**Cuerpo de la Solicitud**:
```json
{
  "session_id": 15
}
```

**Respuesta Exitosa (200)**:
```json
{
  "question": "Excelente, me parece muy interesante tu experiencia. ¿Podrías contarme sobre algún desafío técnico específico que hayas enfrentado en uno de tus proyectos de e-commerce y cómo lo resolviste?",
  "response_time": 1.8
}
```

**Errores Posibles**:
- `400`: Session ID es requerido
- `404`: Sesión no encontrada
- `500`: Error al generar pregunta con IA

**Notas Importantes**:
- El sistema utiliza el historial de conversación para generar preguntas contextuales
- Las preguntas se adaptan al nivel de dificultad y al avatar del entrevistador seleccionado
- Si la API de IA falla, se utilizan preguntas de respaldo predefinidas

---

#### POST /api/interviewer/response
**Descripción**: Procesa la respuesta del usuario y actualiza métricas

**Cuerpo de la Solicitud**:
```json
{
  "session_id": 15,
  "user_response": "En mi último proyecto tuvimos un problema de rendimiento con las consultas a la base de datos. Lo que hice fue implementar un sistema de caché con Redis y optimizar las consultas más lentas...",
  "response_time": 18.7
}
```

**Respuesta Exitosa (200)**:
```json
{
  "message": "Response processed successfully",
  "conversation_length": 6
}
```

**Errores Posibles**:
- `400`: Session ID y respuesta del usuario son requeridos
- `404`: Sesión no encontrada
- `500`: Error interno del servidor

---

### 📊 Sistema de Retroalimentación

#### POST /api/feedback/
**Descripción**: Genera retroalimentación automática para una sesión completada

**Cuerpo de la Solicitud**:
```json
{
  "session_id": 15
}
```

**Respuesta Exitosa (201)**:
```json
{
  "message": "Feedback generated successfully",
  "feedback": {
    "id": 8,
    "session_id": 15,
    "overall_score": 8.2,
    "communication_score": 8.5,
    "confidence_score": 7.8,
    "technical_score": 8.4,
    "strengths": [
      "Excelente conocimiento técnico en frameworks modernos",
      "Respuestas bien estructuradas y claras",
      "Buena capacidad para explicar conceptos complejos"
    ],
    "areas_for_improvement": [
      "Reducir ligeramente el tiempo de respuesta",
      "Incluir más ejemplos específicos en las respuestas"
    ],
    "specific_suggestions": [
      "Practica respuestas a preguntas técnicas comunes para mejorar fluidez",
      "Prepara anecdotas específicas que demuestren tus habilidades",
      "Continuar practicando con diferentes tipos de entrevistas"
    ],
    "avg_response_time": 6.8,
    "total_words_spoken": 342,
    "hesitation_count": 0,
    "created_at": "2024-01-15T15:20:00"
  }
}
```

**Errores Posibles**:
- `400`: Session ID es requerido
- `404`: Sesión no encontrada
- `409`: Ya existe retroalimentación para esta sesión
- `500`: Error interno del servidor

---

#### GET /api/feedback/{feedback_id}
**Descripción**: Obtiene retroalimentación específica por ID

**Parámetros de Ruta**:
- `feedback_id` (integer): ID de la retroalimentación

**Respuesta Exitosa (200)**:
```json
{
  "id": 8,
  "session_id": 15,
  "overall_score": 8.2,
  "communication_score": 8.5,
  "confidence_score": 7.8,
  "technical_score": 8.4,
  "strengths": [
    "Excelente conocimiento técnico en frameworks modernos",
    "Respuestas bien estructuradas y claras",
    "Buena capacidad para explicar conceptos complejos"
  ],
  "areas_for_improvement": [
    "Reducir ligeramente el tiempo de respuesta",
    "Incluir más ejemplos específicos en las respuestas"
  ],
  "specific_suggestions": [
    "Practica respuestas a preguntas técnicas comunes para mejorar fluidez",
    "Prepara anecdotas específicas que demuestren tus habilidades",
    "Continuar practicando con diferentes tipos de entrevistas"
  ],
  "avg_response_time": 6.8,
  "total_words_spoken": 342,
  "hesitation_count": 0,
  "created_at": "2024-01-15T15:20:00"
}
```

---

#### GET /api/feedback/session/{session_id}
**Descripción**: Obtiene retroalimentación de una sesión específica

**Parámetros de Ruta**:
- `session_id` (integer): ID de la sesión

**Respuesta Exitosa (200)**:
```json
{
  "id": 8,
  "session_id": 15,
  "overall_score": 8.2,
  "communication_score": 8.5,
  "confidence_score": 7.8,
  "technical_score": 8.4,
  "strengths": [
    "Excelente conocimiento técnico en frameworks modernos",
    "Respuestas bien estructuradas y claras",
    "Buena capacidad para explicar conceptos complejos"
  ],
  "areas_for_improvement": [
    "Reducir ligeramente el tiempo de respuesta",
    "Incluir más ejemplos específicos en las respuestas"
  ],
  "specific_suggestions": [
    "Practica respuestas a preguntas técnicas comunes para mejorar fluidez",
    "Prepara anecdotas específicas que demuestren tus habilidades",
    "Continuar practicando con diferentes tipos de entrevistas"
  ],
  "avg_response_time": 6.8,
  "total_words_spoken": 342,
  "hesitation_count": 0,
  "created_at": "2024-01-15T15:20:00"
}
```

**Errores Posibles**:
- `404`: No se encontró retroalimentación para esta sesión
- `500`: Error interno del servidor

---

## Sistema de Puntuación

### Algoritmo de Calificación

El sistema utiliza un algoritmo de puntuación multifactorial que evalúa:

1. **Puntuación General (Overall Score)**: Promedio ponderado de todas las categorías
2. **Comunicación**: Claridad, estructura y coherencia de las respuestas
3. **Confianza**: Tiempo de respuesta y fluidez
4. **Técnica**: Precisión y profundidad del conocimiento específico

### Factores de Evaluación

- **Tiempo de Respuesta Promedio**:
  - Óptimo: 2-8 segundos
  - Penalización por > 10 segundos (falta de preparación)
  - Penalización leve por < 2 segundos (respuestas apresuradas)

- **Extensión de Respuestas**:
  - Óptimo: 15-80 palabras por respuesta
  - Penalización por < 10 palabras (respuestas muy breves)
  - Penalización leve por > 100 palabras (verbosidad excesiva)

- **Duración de la Sesión**:
  - Penalización por < 5 minutos (sesión muy corta)
  - Bonificación por > 15 minutos (buen engagement)

### Escala de Puntuación

- **9.0 - 10.0**: Excelente - Desempeño sobresaliente
- **8.0 - 8.9**: Muy Bueno - Desempeño sólido con mínimas áreas de mejora
- **7.0 - 7.9**: Bueno - Desempeño competente con algunas oportunidades de mejora
- **6.0 - 6.9**: Satisfactorio - Desempeño aceptable con varias áreas de mejora
- **5.0 - 5.9**: Necesita Mejora - Desempeño por debajo del estándar
- **1.0 - 4.9**: Deficiente - Requiere preparación significativa

---

## Integración con IA

### Configuración del Entrevistador Virtual

El sistema se integra con APIs de modelos de lenguaje para generar preguntas dinámicas y contextualmente relevantes.

#### Personalidades del Entrevistador

- **Profesional**: Formal pero amigable, enfoque equilibrado
- **Amigable**: Relajado y acogedor, busca hacer sentir cómodo al candidato
- **Serio**: Directo y formal, va al grano en las preguntas

#### Adaptación Contextual

El sistema considera múltiples factores para generar preguntas apropiadas:

- **Historial de conversación**: Utiliza las últimas 6 interacciones para mantener contexto
- **Nivel de dificultad**: Adapta la complejidad de las preguntas
- **Tipo de escenario**: Personaliza preguntas según el área profesional
- **Personalidad del avatar**: Ajusta el tono y estilo de las preguntas
- **Descripción personalizada**: Incorpora requisitos específicos del usuario

#### Sistema de Respaldo (Fallback)

En caso de fallo de la API de IA, el sistema utiliza preguntas predefinidas organizadas por categorías:

**Programador/Tecnología**:
- ¿Podrías contarme sobre tu experiencia en programación?
- ¿Qué lenguajes de programación dominas mejor?
- ¿Cómo enfrentas los desafíos técnicos en tus proyectos?

**Atención al Cliente**:
- ¿Qué te motiva a trabajar en atención al cliente?
- ¿Cómo manejarías a un cliente molesto o insatisfecho?
- ¿Qué consideras más importante en el servicio al cliente?

**Marketing**:
- ¿Cuál es tu experiencia en marketing digital?
- ¿Cómo medirías el éxito de una campaña publicitaria?
- ¿Qué redes sociales consideras más efectivas y por qué?

---

## Algoritmos de Evaluación

### 📊 Sistema de Puntuación Detallado

#### Función de Cálculo Principal

```python
def calculate_scores(metrics, conversation):
    # Puntuaciones base
    overall_score = 7.0
    communication_score = 7.0
    confidence_score = 7.0
    technical_score = 7.0
    
    # Ajustes basados en tiempo de respuesta
    avg_response_time = metrics.get('avg_response_time', 0)
    if avg_response_time > 10:  # Muy lento
        confidence_score -= 2
        overall_score -= 1
    elif avg_response_time < 2:  # Muy rápido (apresurado)
        confidence_score -= 0.5
    
    # Ajustes basados en cantidad de palabras
    total_words = metrics.get('total_words', 0)
    total_responses = metrics.get('total_responses', 1)
    avg_words_per_response = total_words / total_responses
    
    if avg_words_per_response < 10:  # Muy breve
        communication_score -= 1.5
        overall_score -= 1
    elif avg_words_per_response > 100:  # Muy extenso
        communication_score -= 0.5
    
    # Ajustes basados en duración de sesión
    session_duration = metrics.get('session_duration', 0)
    if session_duration < 5:  # Muy corto
        overall_score -= 2
    elif session_duration > 30:  # Buen engagement
        overall_score += 0.5
    
    # Mantener puntuaciones en rango 1-10
    scores = [overall_score, communication_score, confidence_score, technical_score]
    return [max(1.0, min(10.0, score)) for score in scores]
```

#### Métricas de Evaluación

**Tiempo de Respuesta**:
- **Óptimo**: 2-8 segundos
- **Penalización alta**: > 10 segundos (indica falta de preparación)
- **Penalización leve**: < 2 segundos (respuestas apresuradas)

**Extensión de Respuestas**:
- **Óptimo**: 15-80 palabras por respuesta
- **Penalización**: < 10 palabras (respuestas muy breves)
- **Penalización leve**: > 100 palabras (verbosidad excesiva)

**Duración de Sesión**:
- **Penalización**: < 5 minutos (sesión muy corta)
- **Bonificación**: > 15 minutos (buen engagement)

#### Generación de Retroalimentación

El sistema genera automáticamente tres tipos de feedback:

**Fortalezas** (basadas en desempeño):
- Desempeño general excelente (puntuación ≥ 8)
- Tiempo de respuesta apropiado (< 5 segundos)
- Buena participación (duración > 15 minutos)

**Áreas de Mejora**:
- Claridad de comunicación (puntuación comunicación < 7)
- Confianza y seguridad (puntuación confianza < 7)
- Conocimientos técnicos (puntuación técnica < 7)

**Sugerencias Específicas**:
- Elaborar respuestas con ejemplos (< 15 palabras promedio)
- Practicar fluidez (tiempo respuesta > 8 segundos)
- Continuar practicando diferentes tipos de entrevista

---

## Utilidades y Funciones de Apoyo

### 🔧 Funciones de Validación

#### Validación de Email
```python
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

#### Validación de Contraseña
```python
def validate_password(password):
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, "Password is valid"
```

### 📈 Cálculo de Estadísticas

#### Estadísticas de Usuario
```python
def calculate_session_stats(sessions):
    # Estadísticas básicas
    total_sessions = len(sessions)
    scores = [s.feedback.overall_score for s in sessions if s.feedback]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Cálculo de horas totales
    total_minutes = sum(s.get_duration_minutes() for s in sessions)
    total_hours = total_minutes / 60
    
    # Tendencia de mejora (últimas 3 vs primeras 3 sesiones)
    improvement_trend = 0
    if len(scores) >= 6:
        first_three = sum(scores[:3]) / 3
        last_three = sum(scores[-3:]) / 3
        improvement_trend = last_three - first_three
    
    return {
        'total_sessions': total_sessions,
        'avg_score': round(avg_score, 2),
        'total_hours': round(total_hours, 2),
        'improvement_trend': round(improvement_trend, 2)
    }
```

#### Análisis de Calidad de Respuesta
```python
def analyze_response_quality(response_text):
    words = response_text.split()
    word_count = len(words)
    
    # Puntuación base de calidad
    quality_score = 5
    
    # Ajustes por longitud
    if word_count > 20: quality_score += 1
    if word_count > 50: quality_score += 1
    if word_count < 5: quality_score -= 2
    
    # Indicadores positivos
    positive_words = ['experiencia', 'aprendí', 'logré', 'desarrollé', 'implementé']
    if any(word in response_text.lower() for word in positive_words):
        quality_score += 1
    
    return {
        'word_count': word_count,
        'quality_score': max(1, min(10, quality_score))
    }
```

---

## Manejo de Errores y Casos Especiales

### 🚨 Códigos de Error Estándar

#### Errores de Autenticación (4xx)
- **400 Bad Request**: Datos de entrada inválidos o faltantes
- **401 Unauthorized**: Credenciales inválidas
- **404 Not Found**: Recurso no encontrado
- **409 Conflict**: Recurso ya existe (ej: email duplicado, feedback existente)

#### Errores del Servidor (5xx)
- **500 Internal Server Error**: Error interno del sistema
- **503 Service Unavailable**: API de IA no disponible

### 🔄 Manejo de Fallos de IA

#### Estrategia de Respaldo
1. **Timeout**: Si la API de IA no responde en tiempo límite
2. **Error de API**: Si la API devuelve error
3. **Respuesta inválida**: Si la respuesta no cumple criterios

#### Implementación
```python
try:
    response = requests.post(self.api_url, headers=headers, json=payload, timeout=self.max_response_time)
    if response.status_code == 200:
        return result['choices'][0]['message']['content'].strip()
    else:
        return self._get_fallback_question(context)
except requests.exceptions.Timeout:
    return self._get_fallback_question(context)
except Exception as e:
    return self._get_fallback_question(context)
```

---

## Configuración y Variables de Entorno

### 🔧 Archivo de Configuración (.env)

```env
# Configuración principal
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DATABASE_URL=sqlite:///vr_interviews.db
FLASK_ENV=development

# API de Inteligencia Artificial
AI_API_URL=https://api.openai.com/v1/chat/completions
AI_API_KEY=sk-tu-api-key-de-openai-aqui
MAX_RESPONSE_TIME=10

# Configuración de base de datos
SQLALCHEMY_DATABASE_URI=sqlite:///vr_interviews.db
SQLALCHEMY_TRACK_MODIFICATIONS=False

# Configuración de CORS
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log
```

### ⚙️ Configuración de Desarrollo

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///vr_interviews.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # AI Configuration
    AI_API_URL = os.environ.get('AI_API_URL')
    AI_API_KEY = os.environ.get('AI_API_KEY')
    MAX_RESPONSE_TIME = int(os.environ.get('MAX_RESPONSE_TIME', 10))
    
    # Scoring Configuration
    DEFAULT_SCORES = {
        'overall': 7.0,
        'communication': 7.0,
        'confidence': 7.0,
        'technical': 7.0
    }
```

---

## Testing y Casos de Prueba

### 🧪 Ejemplos de Pruebas de API

#### Prueba de Registro de Usuario
```python
def test_user_registration():
    response = client.post('/api/auth/register', json={
        'email': 'test@example.com',
        'password': 'password123',
        'first_name': 'Test',
        'last_name': 'User',
        'preferred_difficulty': 'básico',
        'anxiety_level': 5
    })
    assert response.status_code == 201
    assert 'user' in response.json
```

#### Prueba de Creación de Sesión
```python
def test_create_session():
    response = client.post('/api/sessions/', json={
        'user_id': 1,
        'scenario_id': 1,
        'difficulty_level': 'intermedio',
        'interviewer_avatar': 'profesional',
        'environment': 'oficina'
    })
    assert response.status_code == 201
    assert response.json['session']['status'] == 'active'
```

#### Prueba de Generación de Retroalimentación
```python
def test_generate_feedback():
    response = client.post('/api/feedback/', json={
        'session_id': 1
    })
    assert response.status_code == 201
    assert 'overall_score' in response.json['feedback']
    assert 1 <= response.json['feedback']['overall_score'] <= 10
```

---

## Monitoreo y Logging

### 📊 Métricas Importantes a Monitorear

#### Métricas de Performance
- **Tiempo de respuesta de API**: < 2 segundos promedio
- **Tasa de éxito de IA**: > 95%
- **Tiempo de generación de feedback**: < 5 segundos

#### Métricas de Usuario
- **Sesiones completadas vs iniciadas**: Tasa de abandono
- **Duración promedio de sesión**: Engagement del usuario
- **Puntuaciones promedio**: Efectividad del sistema

#### Métricas del Sistema
- **Uptime**: > 99.9%
- **Errores de base de datos**: < 0.1%
- **Fallos de API externa**: Seguimiento de dependencias

### 📝 Configuración de Logging

```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    if not app.debug:
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('VR Interviews application startup')
```

---

## Deployment y Producción

### 🚀 Consideraciones para Producción

#### Variables de Entorno de Producción
```env
FLASK_ENV=production
SECRET_KEY=clave-super-segura-generada-aleatoriamente
DATABASE_URL=postgresql://usuario:password@host:puerto/database
AI_API_KEY=clave-api-real-de-produccion
CORS_ORIGINS=["https://tu-dominio.com"]
```

#### Configuración de Base de Datos
Para producción, se recomienda PostgreSQL:
```python
# requirements.txt adicional para producción
psycopg2-binary==2.9.7
gunicorn==21.2.0
```

#### Docker Configuration
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

### 🔒 Consideraciones de Seguridad

#### Validación de Entrada
- Validación estricta de todos los inputs
- Sanitización de datos antes de almacenamiento
- Límites de rate limiting por IP/usuario

#### Protección de APIs
- Implementar autenticación JWT para endpoints sensibles
- CORS configurado apropiadamente
- Headers de seguridad (HSTS, CSP, etc.)

#### Datos Sensibles
- Encriptación de contraseñas con bcrypt
- API keys almacenadas como variables de entorno
- Logs sin información sensible

---

## Mantenimiento y Actualizaciones

### 🔄 Migraciones de Base de Datos

#### Comando de Migración
```bash
flask db migrate -m "Descripción del cambio"
flask db upgrade
```

#### Backup de Base de Datos
```bash
# SQLite
cp vr_interviews.db vr_interviews_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump database_name > backup_$(date +%Y%m%d).sql
```

### 📊 Métricas de Mantenimiento

#### Limpieza de Datos
- Sesiones no completadas > 7 días
- Logs antiguos > 30 días
- Datos de prueba en desarrollo

#### Actualizaciones del Sistema
- Dependencias de Python (mensual)
- Modelos de IA (según disponibilidad)
- Configuraciones de seguridad (trimestral)

---

## Anexos

### 📚 Recursos Adicionales

#### Documentación Externa
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

#### Herramientas Recomendadas
- **Testing**: pytest, unittest
- **Monitoring**: Prometheus, Grafana
- **Deployment**: Docker, Kubernetes
- **CI/CD**: GitHub Actions, Jenkins

#### Contacto y Soporte
- **Documentación del proyecto**: README.md
- **Issues y bugs**: GitHub Issues
- **Mejoras y features**: GitHub Discussions