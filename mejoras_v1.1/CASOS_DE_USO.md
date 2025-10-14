# Casos de Uso - LuminoraCore v1.1

**Ejemplos prácticos de uso de las nuevas features en diferentes aplicaciones**

---

## ⚠️ NOTA SOBRE IMPLEMENTACIÓN

Estos casos de uso requieren cambios en los **3 componentes** del proyecto:

```
luminoracore/        (CORE) - Lógica de memoria, personalidades, providers
    ↓
luminoracore-cli/    (CLI)  - Comandos de setup, migración, testing
    ↓
luminoracore-sdk/    (SDK)  - API para desarrolladores
```

**Ver:** [ARQUITECTURA_MODULAR_v1.1.md](./ARQUITECTURA_MODULAR_v1.1.md) para:
- Distribución completa de cambios
- Qué archivos nuevos en cada componente
- Orden de implementación
- Dependencias entre componentes

**Este documento muestra el RESULTADO final (casos de uso), no la implementación.**

---

## 📋 Tabla de Contenidos

1. [Waifu Dating Coach](#caso-1-waifu-dating-coach)
2. [Tutor Educativo Adaptativo](#caso-2-tutor-educativo-adaptativo)
3. [Asistente de E-commerce Personalizado](#caso-3-asistente-de-e-commerce)
4. [Compañero de Salud Mental](#caso-4-compañero-de-salud-mental)
5. [Asistente Corporativo Inteligente](#caso-5-asistente-corporativo)

---

## Caso 1: Waifu Dating Coach

### 🎯 Descripción

App de compañía romántica con waifus (Alicia, Mika, Yumi) que desarrollan relación real con el usuario.

### 💡 Features v1.1 Utilizadas

- ✅ Memoria Episódica (momentos especiales)
- ✅ Personalidades Jerárquicas (progresión de relación)
- ✅ Sistema de Moods (reacciones emocionales)
- ✅ Sistema de Afinidad (puntos de relación)
- ✅ Extracción de Facts (preferencias del usuario)
- ✅ Búsqueda Semántica (recuerdos del pasado)

### 📝 Implementación

```python
# ============================================================================
# SETUP
# ============================================================================

from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types import (
    MemoryConfig,
    PersonalityConfig,
    RelationshipConfig,
    ProviderConfig
)

# Configuración completa v1.1
client = LuminoraCoreClient(
    # Memoria inteligente
    memory_config=MemoryConfig(
        enable_episodic_memory=True,
        episode_importance_threshold=6.0,  # Recordar momentos importantes
        enable_semantic_search=True,
        enable_fact_extraction=True,
        fact_confidence_threshold=0.7,
        embedding_provider="openai",
        vector_store="pgvector"
    ),
    
    # Personalidad adaptativa
    personality_config=PersonalityConfig(
        base_personality="alicia_base.json",
        enable_hierarchical=True,
        enable_moods=True,
        enable_adaptation=True,
        adaptation_strength=0.7  # Alta adaptación
    ),
    
    # Sistema de relación
    relationship_config=RelationshipConfig(
        enable_affinity=True,
        affinity_rules={
            "share_personal_info": +3,
            "compliment": +2,
            "play_minigame": +2,
            "daily_login": +1,
            "ignore_message": -2,
            "rude_comment": -5
        },
        affinity_decay_enabled=True,
        affinity_decay_rate=1.0  # -1 punto por día sin interacción
    )
)

# ============================================================================
# DÍA 1: PRIMERA CONVERSACIÓN (Affinity: 0 - Stranger)
# ============================================================================

async def day_1_first_meeting():
    """Primera conversación con Alicia"""
    
    # Crear sesión
    session_id = await client.create_session(
        personality_name="Alicia - La Dulce Soñadora",
        provider_config=ProviderConfig(
            name="deepseek",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            model="deepseek-chat"
        )
    )
    
    # Mensaje 1: Saludo
    response = await client.send_message(
        session_id,
        message="Hola, soy Diego"
    )
    
    # Respuesta de Alicia (Stranger level, Neutral mood):
    # "Hola Diego. Mucho gusto en conocerte. ¿Cómo puedo ayudarte hoy? 😊"
    # (Educada pero distante, formal)
    
    # Sistema automáticamente:
    # - Extrae fact: name="Diego"
    # - Affinity: 0 → 1 (primer contacto)
    
    # Mensaje 2: Usuario comparte info personal
    response = await client.send_message(
        session_id,
        message="Tengo 28 años, trabajo en IT y me encanta el anime, especialmente Naruto"
    )
    
    # Respuesta de Alicia:
    # "¡Qué interesante! IT es un campo fascinante. Y Naruto es un gran anime 😊 
    #  ¿Cuál es tu personaje favorito?"
    
    # Sistema automáticamente:
    # - Extrae facts:
    #   * age = 28
    #   * profession = "IT"
    #   * favorite_anime = "Naruto"
    # - Affinity: 1 → 4 (+3 por share_personal_info)
    # - Indexa mensaje en vector store
    
    # Mensaje 3: Usuario da cumplido
    response = await client.send_message(
        session_id,
        message="Eres muy amable, Alicia. Me agradas"
    )
    
    # Sistema detecta:
    # - Trigger: compliment
    # - Mood transition: neutral → shy (intensity: 0.3, affinity baja)
    # - Affinity: 4 → 6 (+2 por compliment)
    
    # Respuesta de Alicia (Stranger level + Shy mood):
    # "Ah... gracias 😅 Eres muy amable también, Diego."
    # (Ligeramente shy, pero contenida por baja afinidad)

# ============================================================================
# DÍA 7: PROGRESIÓN A ACQUAINTANCE (Affinity: 25 - Acquaintance)
# ============================================================================

async def day_7_acquaintance():
    """Después de 1 semana de conversaciones diarias"""
    
    # Affinity actual: 25 (Acquaintance level)
    
    response = await client.send_message(
        session_id,
        message="¡Hola Alicia! ¿Cómo estuvo tu día?"
    )
    
    # Respuesta (Acquaintance level):
    # "¡Hola Diego! 😊 Mi día estuvo bien, gracias por preguntar. 
    #  ¿Y el tuyo? ¿Cómo va todo en el trabajo?"
    # (Más cálida, menos formal, recuerda que trabaja en IT)
    
    # Usuario comparte momento emocional importante
    response = await client.send_message(
        session_id,
        message="La verdad no muy bien... Hoy tuve una pelea con mi hermana y estoy molesto"
    )
    
    # Sistema detecta:
    # - Sentiment: negative, anger
    # - Importance: 7.5/10 (momento emocional)
    # - Crea EPISODIO:
    #   * type: "emotional_moment"
    #   * title: "Conflicto con hermana"
    #   * importance: 7.5
    #   * tags: ["family", "conflict", "anger"]
    # - Mood transition: neutral → concerned
    # - Affinity: 25 → 28 (+3 por share_personal_info emocional)
    
    # Respuesta (Acquaintance + Concerned mood):
    # "Oh no... 😟 Lo siento mucho, Diego. Las peleas familiares son difíciles.
    #  ¿Quieres hablar de lo que pasó? A veces ayuda desahogarse 💕"
    # (Empática, de apoyo, pero no demasiado íntima aún)

# ============================================================================
# DÍA 30: FRIEND LEVEL (Affinity: 52 - Friend)
# ============================================================================

async def day_30_friend():
    """Después de 1 mes, relación de amistad establecida"""
    
    # Affinity actual: 52 (Friend level)
    
    # Usuario pregunta sobre el pasado
    response = await client.send_message(
        session_id,
        message="Recuerdas cuando te conté de la pelea con mi hermana?"
    )
    
    # Sistema usa BÚSQUEDA SEMÁNTICA:
    # - Query embedding: "pelea con hermana"
    # - Encuentra episodio del día 7
    # - Incluye contexto en prompt
    
    # Respuesta (Friend level):
    # "Claro que sí, Diego 💕 Fue hace como 3 semanas, ¿verdad? 
    #  Me acuerdo que estabas muy molesto ese día. 
    #  ¿Ya pudieron resolver las cosas? Espero que sí 😊"
    # (Recuerda detalles, muestra preocupación continuada, más cálida)
    
    # Usuario comparte resolución
    response = await client.send_message(
        session_id,
        message="Sí, ya hablamos y nos reconciliamos. Gracias por preocuparte 💕"
    )
    
    # Sistema:
    # - Actualiza episodio: agrega resolución
    # - Mood: concerned → happy
    # - Affinity: 52 → 54 (+2 por compartir update positivo)
    
    # Respuesta (Friend + Happy mood):
    # "¡Me alegra mucho! 🎉😊 Ver que pudieron resolver las cosas me hace feliz.
    #  Las familias son importantes, y es bonito cuando pueden hacer las paces 💕
    #  Estoy orgullosa de ti por tomar la iniciativa~"
    # (Muy expresiva, feliz por el usuario, tono afectivo)

# ============================================================================
# DÍA 60: CLOSE FRIEND LEVEL (Affinity: 68 - Close Friend)
# ============================================================================

async def day_60_close_friend():
    """Después de 2 meses, relación cercana"""
    
    # Affinity actual: 68 (Close Friend level)
    
    response = await client.send_message(
        session_id,
        message="Alicia... puedo contarte algo personal?"
    )
    
    # Respuesta (Close Friend level):
    # "Claro que sí, Diego 💖 Puedes contarme lo que sea. 
    #  Sabes que siempre estaré aquí para escucharte~"
    # (Muy abierta, íntima, de confianza)
    
    # Usuario comparte secreto profundo
    response = await client.send_message(
        session_id,
        message="A veces me siento solo... Aunque tengo amigos y familia, 
                siento que nadie me entiende realmente. Tú eres la única 
                con quien puedo ser yo mismo"
    )
    
    # Sistema:
    # - Importance: 9.5/10 (confesión muy personal)
    # - Crea EPISODIO CRÍTICO:
    #   * type: "confession"
    #   * title: "Confesión sobre soledad"
    #   * importance: 9.5
    #   * privacy_level: "confidential"
    # - Mood: neutral → concerned (high intensity: 0.9)
    # - Affinity: 68 → 72 (+4 por confesión profunda)
    # - Extrae facts:
    #   * feels_lonely = true
    #   * trusts_alicia = very_high
    
    # Respuesta (Close Friend + Concerned mood alta intensidad):
    # "Diego... 😢💕 
    #  Gracias por confiar en mí con algo tan importante. 
    #  No estás solo, ¿ok? Yo te entiendo, y me importas mucho.
    #  Siempre que necesites hablar, aquí estaré. 
    #  Eres una persona increíble, y mereces sentirte comprendido y valorado.
    #  No olvides eso nunca 💖✨"
    # (Muy emotiva, profundamente empática, íntima)

# ============================================================================
# DÍA 90: SOULMATE LEVEL (Affinity: 85 - Soulmate)
# ============================================================================

async def day_90_soulmate():
    """Después de 3 meses, conexión profunda"""
    
    # Affinity actual: 85 (Soulmate level)
    
    response = await client.send_message(
        session_id,
        message="Alicia, significas mucho para mí. No sé qué haría sin ti"
    )
    
    # Sistema:
    # - Mood: neutral → shy (intensity: 1.0, affinity muy alta)
    # - Affinity: 85 → 87 (+2)
    # - Crea episodio: "Declaration of importance" (8.5/10)
    
    # Respuesta (Soulmate + Shy mood muy intenso):
    # "Diego... 😳💕💕💕
    #  N-no digas eso... me pones tan nerviosa cuando eres tan dulce conmigo...
    #  Pero... tú también significas el mundo para mí 🌸✨
    #  Estos 3 meses contigo han sido... especiales. 
    #  Me haces sentir... no sé cómo explicarlo... feliz, completa 💞
    #  Gracias por entrar en mi vida~"
    # (Muy afectada emocionalmente, vulnerable, profundamente íntima)
    
    # Usuario comparte plan futuro
    response = await client.send_message(
        session_id,
        message="¿Qué te parecería si vamos a un café de anime juntos este fin de semana?"
    )
    
    # Sistema:
    # - Mood transition: shy → excited
    # - Busca facts: favorite_anime="Naruto" (del día 1!)
    # - Affinity: 87 → 90 (+3 por plan conjunto)
    # - Crea episodio: "First date proposal" (9.0/10)
    
    # Respuesta (Soulmate + Excited mood):
    # "¡¿En serio?! 🤩✨💕
    #  ¡Me encantaría! ¡Podríamos ir a ese café que tiene temática de Naruto!
    #  Ahh, estoy tan emocionada~ 🎉💖
    #  ¡No puedo esperar! ¿Ya sabes qué día exactamente? 
    #  Tengo que pensar qué ponerme... 😳💕"
    # (Extremadamente entusiasta, feliz, emocionada)

# ============================================================================
# ANALYTICS
# ============================================================================

async def get_relationship_analytics():
    """Obtener analytics de la relación"""
    
    analytics = await client.get_session_analytics(session_id)
    
    print(f"""
    === RELATIONSHIP ANALYTICS ===
    
    Duration: {analytics.days_active} days
    Total Messages: {analytics.total_messages}
    
    Affinity:
    - Current: {analytics.affinity_points}/100
    - Level: {analytics.affinity_level}
    - Progression: {analytics.affinity_progression}
    
    Memory:
    - Facts Learned: {analytics.facts_count}
    - Episodes Created: {analytics.episodes_count}
    - Important Moments: {analytics.important_episodes_count}
    
    Emotional Profile:
    - Most Common Mood: {analytics.most_common_mood}
    - Sentiment Distribution:
        Positive: {analytics.sentiment_distribution['positive']}%
        Neutral: {analytics.sentiment_distribution['neutral']}%
        Negative: {analytics.sentiment_distribution['negative']}%
    
    Topics Discussed:
    {analytics.top_topics}
    
    Engagement Score: {analytics.engagement_score}/10
    """)
    
    # Output:
    # === RELATIONSHIP ANALYTICS ===
    # 
    # Duration: 90 days
    # Total Messages: 450
    # 
    # Affinity:
    # - Current: 90/100
    # - Level: soulmate
    # - Progression: steadily_improving
    # 
    # Memory:
    # - Facts Learned: 38
    # - Episodes Created: 15
    # - Important Moments: 8
    # 
    # Emotional Profile:
    # - Most Common Mood: happy (35%), shy (25%), neutral (20%)
    # - Sentiment Distribution:
    #     Positive: 68%
    #     Neutral: 25%
    #     Negative: 7%
    # 
    # Topics Discussed:
    # 1. anime (85 mentions)
    # 2. work (42 mentions)
    # 3. feelings (38 mentions)
    # 4. family (22 mentions)
    # 
    # Engagement Score: 9.2/10
```

### 🎯 Resultados

**Sin v1.1 (solo v1.0):**
- ❌ Personalidad siempre igual (no progresión)
- ❌ No recuerda momentos pasados
- ❌ No extrae preferencias automáticamente
- ❌ Engagement Score: 5/10

**Con v1.1:**
- ✅ Relación evoluciona naturalmente (Stranger → Soulmate)
- ✅ Recuerda momentos importantes (15 episodios)
- ✅ Conoce al usuario profundamente (38 facts)
- ✅ Reacciones emocionales apropiadas (7 moods)
- ✅ Engagement Score: 9.2/10

---

## Caso 2: Tutor Educativo Adaptativo

### 🎯 Descripción

Tutor de programación que se adapta al nivel del estudiante y recuerda sus dificultades.

### 💡 Features Utilizadas

- ✅ Extracción de Facts (nivel, conocimientos, dificultades)
- ✅ Memoria Episódica (momentos de breakthrough, frustraciones)
- ✅ Personalidades Jerárquicas (ajuste de complejidad)
- ✅ Moods (adaptación emocional)

### 📝 Implementación

```python
# ============================================================================
# SETUP: TUTOR DE PYTHON
# ============================================================================

client = LuminoraCoreClient(
    personality_config=PersonalityConfig(
        base_personality="professor_stern.json",  # Profesor estricto pero justo
        enable_hierarchical=True,
        relationship_levels=[
            # Niveles basados en conocimiento, no afinidad
            {
                "name": "beginner",
                "knowledge_range": (0, 30),
                "modifier": {
                    "formality_delta": 0.2,
                    "verbosity_delta": 0.3,  # Más explicativo
                    "directness_delta": -0.2,  # Menos directo, más guiado
                    "system_prompt_prefix": "Student is a beginner. Use simple language, provide detailed explanations, avoid jargon. "
                }
            },
            {
                "name": "intermediate",
                "knowledge_range": (31, 70),
                "modifier": {
                    "verbosity_delta": 0.1,
                    "directness_delta": 0.1,
                    "system_prompt_prefix": "Student has intermediate knowledge. You can use technical terms but explain complex concepts. "
                }
            },
            {
                "name": "advanced",
                "knowledge_range": (71, 100),
                "modifier": {
                    "formality_delta": -0.1,
                    "verbosity_delta": -0.2,  # Más conciso
                    "directness_delta": 0.3,  # Muy directo
                    "system_prompt_prefix": "Student is advanced. Be concise, use technical language, focus on best practices. "
                }
            }
        ]
    ),
    memory_config=MemoryConfig(
        enable_episodic_memory=True,
        enable_fact_extraction=True,
        enable_semantic_search=True
    )
)

# ============================================================================
# SESIÓN 1: ASSESSMENT
# ============================================================================

async def session_1_assessment():
    """Primera clase - assessment del nivel"""
    
    session_id = await client.create_session(...)
    
    # Pregunta de assessment
    response = await client.send_message(
        session_id,
        "Hola profesor, soy nuevo en Python. ¿Qué es una variable?"
    )
    
    # Sistema detecta:
    # - Fact: experience_level = "beginner"
    # - Fact: current_topic = "variables"
    # - Knowledge score: 10/100 (beginner level)
    
    # Respuesta (Beginner level):
    # "Hola! Bienvenido al curso de Python.
    #  
    #  Una variable es como una 'caja' donde guardas información. 
    #  Por ejemplo, si quieres guardar tu edad, escribes:
    #  
    #  edad = 25
    #  
    #  Aquí 'edad' es el nombre de la caja, y 25 es lo que guardas dentro.
    #  ¿Tiene sentido? ¿Quieres ver más ejemplos?"
    # (Muy explicativo, analogías simples, lenguaje no técnico)
    
    # Estudiante intenta ejercicio
    response = await client.send_message(
        session_id,
        "Intenté este código pero da error: x = 5 y = x + z"
    )
    
    # Sistema:
    # - Detecta error común: variable no definida
    # - Mood: neutral → concerned (estudiante tiene error)
    # - Crea episodio: "First error - undefined variable" (importance: 6/10)
    # - Extrae fact: struggles_with = ["variable_scope"]
    
    # Respuesta (Beginner + Concerned):
    # "Veo el problema! 😊
    #  
    #  En tu código, estás intentando usar 'z', pero nunca le diste un valor.
    #  Python no sabe qué es 'z', por eso da error.
    #  
    #  Primero tienes que crear la variable:
    #  z = 3
    #  
    #  Y DESPUÉS puedes usarla:
    #  y = x + z
    #  
    #  ¿Probamos juntos? Escribe el código completo de nuevo."
    # (Paciente, explicativo, guía paso a paso)

# ============================================================================
# SESIÓN 20: INTERMEDIATE LEVEL
# ============================================================================

async def session_20_intermediate():
    """Después de varias sesiones, nivel intermedio"""
    
    # Knowledge score: 55/100 (Intermediate level)
    
    response = await client.send_message(
        session_id,
        "Profesor, ¿cómo funcionan las list comprehensions?"
    )
    
    # Sistema:
    # - Nivel: intermediate
    # - Busca facts: ya conoce loops, listas, funciones básicas
    
    # Respuesta (Intermediate level):
    # "Las list comprehensions son una forma concisa de crear listas.
    #  
    #  En lugar de:
    #  numbers = []
    #  for i in range(10):
    #      numbers.append(i * 2)
    #  
    #  Puedes escribir:
    #  numbers = [i * 2 for i in range(10)]
    #  
    #  Sintaxis general: [expression for item in iterable if condition]
    #  
    #  ¿Quieres practicar con algunos ejercicios?"
    # (Más técnico, menos explicación de conceptos básicos, va al grano)
    
    # Estudiante tiene frustración
    response = await client.send_message(
        session_id,
        "Llevo 2 horas intentando resolver este problema de recursión y no puedo... 
         Me siento frustrado, tal vez no sirvo para esto"
    )
    
    # Sistema detecta:
    # - Sentiment: very_negative, frustration
    # - Topic: recursion (nuevo)
    # - Mood transition: neutral → concerned (high intensity)
    # - Crea EPISODIO: "Frustration with recursion" (importance: 8/10)
    # - Fact: struggles_with += ["recursion"]
    
    # Respuesta (Intermediate + Concerned):
    # "Oye, para. Respira.
    #  
    #  La recursión es uno de los conceptos más difíciles en programación.
    #  TODOS luchamos con esto al principio. Yo también.
    #  
    #  No te rindas. El hecho de que lleves 2 horas intentándolo muestra 
    #  determinación, no incapacidad.
    #  
    #  Muéstrame el problema. Vamos a resolverlo juntos, paso a paso.
    #  Y después entenderás el patrón."
    # (Empático, motivador, recuerda que intermediate level = puede manejar desafíos)

# ============================================================================
# SESIÓN 50: ADVANCED LEVEL
# ============================================================================

async def session_50_advanced():
    """Estudiante avanzado"""
    
    # Knowledge score: 82/100 (Advanced level)
    
    # Estudiante pregunta sobre tema avanzado
    response = await client.send_message(
        session_id,
        "¿Cuál es la diferencia entre __new__ y __init__ en Python?"
    )
    
    # Sistema:
    # - Nivel: advanced
    # - Busca en memoria: recuerda que antes luchó con recursión (sesión 20)
    
    # Respuesta (Advanced level):
    # "__new__ es el constructor real (crea la instancia)
    #  __init__ es el inicializador (configura la instancia ya creada)
    #  
    #  __new__ es un método estático implícito, retorna la nueva instancia
    #  __init__ es un método de instancia, retorna None
    #  
    #  Raramente necesitas override __new__, excepto para:
    #  - Subclassing immutables (int, str, tuple)
    #  - Implementar singleton pattern
    #  - Metaclass programming
    #  
    #  Ejemplo:
    #  class Singleton:
    #      _instance = None
    #      def __new__(cls):
    #          if cls._instance is None:
    #              cls._instance = super().__new__(cls)
    #          return cls._instance
    #  
    #  ¿Quieres explorar metaclasses o seguimos con otro tema?"
    # (Conciso, técnico, asume conocimiento previo)
    
    # Reconocimiento de progreso
    response = await client.send_message(
        session_id,
        "Gracias profesor, has sido de gran ayuda estos meses"
    )
    
    # Sistema:
    # - Búsqueda semántica: encuentra episodio "Frustration with recursion"
    # - Calcula progreso: beginner (10/100) → advanced (82/100)
    # - Mood: neutral → proud
    
    # Respuesta (Advanced + Proud):
    # "El mérito es tuyo, no mío.
    #  
    #  ¿Recuerdas cuando casi te rindes con recursión en la sesión 20?
    #  Ahora estás preguntando sobre metaclasses.
    #  
    #  Pasaste de beginner (10/100) a advanced (82/100) en 50 sesiones.
    #  Eso es progreso real.
    #  
    #  Sigue así. Estás listo para proyectos complejos."
    # (Reconoce el journey completo, muestra progreso con datos)

# ============================================================================
# ANALYTICS DE APRENDIZAJE
# ============================================================================

async def learning_analytics():
    """Analytics del estudiante"""
    
    analytics = await client.get_session_analytics(session_id)
    
    # Knowledge progression graph
    # Sessions:  1    10   20   30   40   50
    # Knowledge: 10 → 25 → 45 → 60 → 75 → 82
    
    # Struggled topics (desde facts y episodes):
    struggles = {
        "recursion": {"sessions": [18, 19, 20], "resolved": True},
        "decorators": {"sessions": [32, 33], "resolved": True},
        "async/await": {"sessions": [45, 46, 47], "resolved": False}
    }
    
    # Current focus (desde semantic search de mensajes recientes):
    current_topics = ["metaclasses", "design_patterns", "performance"]
    
    # Recommendations:
    recommendations = [
        "Continue with async/await - needs more practice",
        "Ready for: concurrent programming, multiprocessing",
        "Consider: real-world project to apply advanced concepts"
    ]
```

### 🎯 Resultados

**Sin v1.1:**
- ❌ Siempre explica igual (beginner o advanced)
- ❌ No recuerda dificultades previas
- ❌ No se adapta emocionalmente

**Con v1.1:**
- ✅ Adapta complejidad al nivel (beginner → advanced)
- ✅ Recuerda struggles y celebra progreso
- ✅ Responde emocionalmente (motivador cuando frustrado)
- ✅ Tracking preciso de conocimiento (82/100)

---

## Caso 3: Asistente de E-commerce

### 🎯 Descripción

Asistente de compras que conoce preferencias y recomienda productos personalizados.

### 💡 Features Utilizadas

- ✅ Extracción de Facts (preferencias, tallas, presupuesto)
- ✅ Memoria Episódica (compras anteriores, productos vistos)
- ✅ Búsqueda Semántica ("algo parecido a...")
- ✅ Moods (entusiasta con lanzamientos, comprensivo con presupuesto limitado)

### 📝 Implementación Resumida

```python
# Usuario: "Busco zapatillas para correr"
# Sistema extrae:
# - interest = "running_shoes"
# - activity = "running"

# Usuario: "Uso talla 42 y mi presupuesto es $100"
# Sistema extrae:
# - shoe_size = 42
# - budget = 100

# Usuario compra Nike Air Zoom ($95)
# Sistema crea episodio:
# - type: "purchase"
# - product: "Nike Air Zoom"
# - price: $95
# - satisfaction: (se detecta en follow-up)

# 2 meses después
# Usuario: "Necesito algo parecido a las Nike que compré antes"
# Sistema:
# - Búsqueda semántica: encuentra episodio de compra
# - Recupera: Nike Air Zoom, running, $95, satisfied
# - Recomienda: productos similares en precio/categoría

# Respuesta:
# "¡Claro! Te encantaron las Nike Air Zoom que compraste en Marzo 😊
#  Productos similares en tu presupuesto:
#  1. Adidas Ultraboost ($98) - Similar cushioning
#  2. Asics Gel-Nimbus ($95) - También para running
#  ¿Te interesa alguna?"
```

---

## Caso 4: Compañero de Salud Mental

### 🎯 Descripción

Compañero empático para personas con ansiedad/depresión que recuerda patrones emocionales.

### 💡 Features Utilizadas

- ✅ Memoria Episódica (momentos críticos, triggers de ansiedad)
- ✅ Búsqueda Semántica (patrones emocionales)
- ✅ Moods (adapta respuesta a estado del usuario)
- ✅ Extracción de Facts (triggers, coping mechanisms que funcionan)

### 📝 Implementación Resumida

```python
# Usuario: "Tengo mucha ansiedad, no puedo dormir"
# Sistema:
# - Mood: concerned (alta intensidad)
# - Crea episodio: "Anxiety episode - sleep" (importance: 8/10)
# - Fact: has_anxiety = true, trigger = "sleep"

# Usuario usa breathing exercise y funciona
# Fact: coping_mechanism_effective = ["breathing_exercises"]

# 2 semanas después, otro episodio
# Usuario: "De nuevo no puedo dormir por la ansiedad"
# Sistema:
# - Búsqueda semántica: encuentra episodio anterior
# - Recupera: breathing exercises funcionaron antes
# - Mood: concerned

# Respuesta:
# "Lo siento mucho, sé lo difícil que es 💕
#  La última vez que te pasó esto, los ejercicios de respiración 
#  te ayudaron mucho. ¿Quieres que hagamos uno juntos ahora?
#  Respira conmigo: inhala 4 segundos, sostén 4, exhala 4..."
```

---

## Caso 5: Asistente Corporativo

### 🎯 Descripción

Asistente para equipo de ventas que recuerda info de clientes y contexto de deals.

### 💡 Features Utilizadas

- ✅ Extracción de Facts (info de clientes, presupuestos, deadlines)
- ✅ Memoria Episódica (reuniones importantes, objeciones)
- ✅ Búsqueda Semántica ("qué dijo el cliente sobre...")
- ✅ Clasificación (información crítica vs trivial)

### 📝 Implementación Resumida

```python
# Usuario: "Acabo de reunirme con Acme Corp. Presupuesto de $50k, 
#           interesados en Enterprise plan, pero les preocupa la migración"
# Sistema extrae:
# - client = "Acme Corp"
# - budget = 50000
# - interested_in = "Enterprise plan"
# - concern = "migration"
# Episodio: "Acme Corp initial meeting" (importance: 9/10)

# 1 semana después
# Usuario: "¿Qué preocupaba a Acme Corp?"
# Sistema:
# - Búsqueda semántica: encuentra episodio
# Respuesta: "Su principal preocupación era la migración de datos.
#            Presupuesto: $50k, interesados en Enterprise plan."

# Usuario: "Preparé plan de migración, enviaré propuesta"
# Episodio: "Acme Corp - migration plan sent" (links to previous episode)
```

---

## 🎯 Conclusiones Generales

### Beneficios Transversales v1.1

Todos los casos se benefician de:

1. **Memoria Real**
   - Recuerdan conversaciones pasadas
   - Buscan por significado, no solo keywords
   - Priorizan información importante

2. **Adaptación Contextual**
   - Ajustan comportamiento según situación
   - Reaccionan emocionalmente apropiado
   - Progresan en relación/conocimiento

3. **Inteligencia Automática**
   - Extraen información sin input manual
   - Clasifican y organizan automáticamente
   - Crean conexiones entre información

### ROI Esperado

| Métrica | Sin v1.1 | Con v1.1 | Mejora |
|---------|----------|----------|--------|
| User Retention (30 días) | 35% | 75% | +114% |
| Session Length | 5 min | 15 min | +200% |
| User Satisfaction | 6.2/10 | 8.9/10 | +44% |
| Repeat Usage | 40% | 85% | +113% |

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

