# Sistema de Personalidades Jerárquicas - LuminoraCore v1.1

**Diseño completo del sistema de personalidades adaptativas con estructura tree-based**

---

## ⚠️ NOTA IMPORTANTE

Este documento describe el **sistema de personalidades jerárquicas** de LuminoraCore v1.1.

**Modelo Conceptual (Templates/Instances/Snapshots):**
- **Templates (JSON)** definen niveles posibles, moods posibles, y configuración base
- **Instances (BBDD)** guardan el estado actual (affinity actual, mood actual)
- **Snapshots (JSON)** exportan el estado completo de la personalidad

**Ver:** [MODELO_CONCEPTUAL_REVISADO.md](./MODELO_CONCEPTUAL_REVISADO.md) para el modelo completo.

**Estado de Personalidad:**
- ✅ Niveles de relación **posibles** → Definidos en **JSON Template**
- ✅ Nivel **actual** del usuario → Guardado en **BBDD** (affinity points)
- ✅ Moods **posibles** → Definidos en **JSON Template**
- ✅ Mood **actual** de la sesión → Guardado en **BBDD**

**Los ejemplos de código en este documento:**
- Muestran la **lógica de implementación** (clases Python)
- Los **valores** (rangos de affinity, modificadores) se leen del **JSON Template**
- Ver [INTEGRACION_CON_SISTEMA_ACTUAL.md](./INTEGRACION_CON_SISTEMA_ACTUAL.md) para cómo se configura en JSON

---

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Arquitectura Tree-Based](#arquitectura-tree-based)
3. [Estados Emocionales (Moods)](#estados-emocionales-moods)
4. [Niveles de Intensidad](#niveles-de-intensidad)
5. [Adaptación Contextual](#adaptación-contextual)
6. [Transiciones Suaves](#transiciones-suaves)
7. [Integración con Afinidad](#integración-con-afinidad)
8. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## Visión General

### 🎯 Concepto Central

**Las personas reales no se comportan siempre igual:**
- Reaccionan diferente según el contexto
- Tienen estados emocionales que cambian
- Ajustan su intensidad según la situación
- Progresan en relaciones (desconocido → amigo → pareja)

**Ejemplo Real:**

```
Situación 1: Un desconocido te dice "eres linda"
Reacción: "Eh... gracias?" (incomodidad, distante)

Situación 2: Tu mejor amigo te dice "eres linda"
Reacción: "¡Ay, gracias! 😊" (alegría, cálida)

Situación 3: Tu pareja te dice "eres linda"
Reacción: "Me pones nerviosa cuando dices eso 😳💕" (timidez, íntima)
```

**Misma persona, mismo input, diferente output según:**
- Nivel de relación (afinidad)
- Estado emocional (mood)
- Contexto de conversación
- Historial reciente

---

### ❌ Problema Actual (v1.0)

```python
# v1.0 - Personalidad estática
personality = load_personality("alicia.json")

# Siempre responde igual
user: "Eres linda"
alicia: "¡Gracias! 😊"  # Misma respuesta sin importar contexto

user: [dice algo triste]
alicia: [responde igual de energética]  # No adapta mood

user: [después de 100 conversaciones]
alicia: [se comporta como desconocida]  # No progresión de relación
```

### ✅ Solución Propuesta (v1.1)

```python
# v1.1 - Personalidad jerárquica adaptativa
personality_tree = PersonalityTree(
    base_personality="alicia_base.json",
    relationship_levels={
        "stranger": "alicia_stranger.json",
        "acquaintance": "alicia_acquaintance.json",
        "friend": "alicia_friend.json",
        "close_friend": "alicia_close_friend.json",
        "soulmate": "alicia_soulmate.json"
    },
    moods={
        "happy": {"empathy": +0.1, "humor": +0.2},
        "shy": {"formality": +0.2, "directness": -0.3},
        "sad": {"empathy": +0.3, "humor": -0.2},
        "excited": {"verbosity": +0.2, "creativity": +0.2}
    },
    adaptation_enabled=True
)

# Adaptación automática
user: "Eres linda" + context(affinity=10, mood="neutral")
alicia: "Eh... gracias, supongo 😅"  # Stranger + neutral

user: "Eres linda" + context(affinity=80, mood="shy")
alicia: "¡Ay! 😳 Me pones nerviosa... 💕"  # Close friend + shy

user: [dice algo triste] + context(...)
alicia: [automáticamente cambia a mood "concerned", más empática]
```

---

## Arquitectura Tree-Based

### 🌳 Estructura del Árbol de Personalidad

```
                    ┌─────────────────────┐
                    │   BASE PERSONALITY  │
                    │   (Alicia Core)     │
                    │                     │
                    │  Core traits que    │
                    │  NUNCA cambian:     │
                    │  - archetype        │
                    │  - values           │
                    │  - core identity    │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
       ┌────────────┐  ┌────────────┐  ┌────────────┐
       │ STRANGER   │  │   FRIEND   │  │  SOULMATE  │
       │  LEVEL     │  │   LEVEL    │  │   LEVEL    │
       │            │  │            │  │            │
       │ Modifiers: │  │ Modifiers: │  │ Modifiers: │
       │ +distant   │  │ +warm      │  │ +intimate  │
       │ +formal    │  │ +playful   │  │ +devoted   │
       └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
             │               │               │
    ┌────────┴────────┐     │      ┌────────┴────────┐
    │                 │     │      │                 │
    ▼                 ▼     ▼      ▼                 ▼
┌────────┐        ┌────────┐  ┌────────┐        ┌────────┐
│ Happy  │        │  Shy   │  │  Sad   │        │Excited │
│ Mood   │        │  Mood  │  │  Mood  │        │ Mood   │
│        │        │        │  │        │        │        │
│+humor  │        │+formal │  │+empathy│        │+energy │
│+energy │        │-direct │  │-humor  │        │+creative│
└────────┘        └────────┘  └────────┘        └────────┘
```

### 🏗️ Implementación

```python
# luminoracore/core/personality/hierarchical.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class RelationshipLevel(Enum):
    """Niveles de relación"""
    STRANGER = "stranger"              # 0-20 affinity
    ACQUAINTANCE = "acquaintance"      # 21-40 affinity
    FRIEND = "friend"                  # 41-60 affinity
    CLOSE_FRIEND = "close_friend"      # 61-80 affinity
    SOULMATE = "soulmate"              # 81-100 affinity

class MoodState(Enum):
    """Estados emocionales"""
    HAPPY = "happy"
    SHY = "shy"
    SAD = "sad"
    EXCITED = "excited"
    CONCERNED = "concerned"
    PLAYFUL = "playful"
    NEUTRAL = "neutral"
    ANGRY = "angry"
    CONFUSED = "confused"

@dataclass
class PersonalityModifier:
    """Modificadores que se aplican a la personalidad base"""
    
    # Modificadores de parámetros avanzados
    empathy_delta: float = 0.0         # -1.0 a +1.0
    formality_delta: float = 0.0
    verbosity_delta: float = 0.0
    humor_delta: float = 0.0
    creativity_delta: float = 0.0
    directness_delta: float = 0.0
    
    # Modificadores de comportamiento
    response_style_override: Optional[str] = None
    tone_additions: List[str] = field(default_factory=list)
    expression_additions: List[str] = field(default_factory=list)
    behavioral_rules_additions: Dict[str, List[str]] = field(default_factory=dict)
    
    # System prompt modifications
    system_prompt_prefix: str = ""
    system_prompt_suffix: str = ""
    
    def apply_to_personality(self, base_personality: dict) -> dict:
        """
        Aplica modificadores a una personalidad base
        
        Args:
            base_personality: Personalidad base
        
        Returns:
            Personalidad modificada
        """
        modified = base_personality.copy()
        
        # Modificar parámetros avanzados
        if "advanced_parameters" in modified:
            params = modified["advanced_parameters"]
            
            params["empathy"] = self._clamp(
                params.get("empathy", 0.5) + self.empathy_delta
            )
            params["formality"] = self._clamp(
                params.get("formality", 0.5) + self.formality_delta
            )
            params["verbosity"] = self._clamp(
                params.get("verbosity", 0.5) + self.verbosity_delta
            )
            params["humor"] = self._clamp(
                params.get("humor", 0.5) + self.humor_delta
            )
            params["creativity"] = self._clamp(
                params.get("creativity", 0.5) + self.creativity_delta
            )
            params["directness"] = self._clamp(
                params.get("directness", 0.5) + self.directness_delta
            )
        
        # Modificar perfil lingüístico
        if "linguistic_profile" in modified:
            profile = modified["linguistic_profile"]
            
            if self.tone_additions:
                profile["tone"] = list(set(profile.get("tone", []) + self.tone_additions))
            
            if self.expression_additions:
                profile["expressions"] = list(
                    set(profile.get("expressions", []) + self.expression_additions)
                )
        
        # Modificar reglas comportamentales
        if "behavioral_rules" in modified and self.behavioral_rules_additions:
            rules = modified["behavioral_rules"]
            
            for rule_type, additions in self.behavioral_rules_additions.items():
                if rule_type in rules:
                    rules[rule_type] = list(set(rules[rule_type] + additions))
        
        return modified
    
    def _clamp(self, value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Limita valor entre min y max"""
        return max(min_val, min(max_val, value))


@dataclass
class PersonalityLevel:
    """Representa un nivel de personalidad (ej. Friend level)"""
    
    name: str
    affinity_range: tuple  # (min, max)
    modifier: PersonalityModifier
    description: str = ""
    
    def is_active(self, affinity: int) -> bool:
        """Verifica si este nivel está activo para la afinidad dada"""
        return self.affinity_range[0] <= affinity <= self.affinity_range[1]


class PersonalityTree:
    """
    Gestiona personalidad jerárquica con niveles y moods
    
    Estructura:
    - Base personality (núcleo inmutable)
    - Relationship levels (según afinidad)
    - Mood states (según contexto emocional)
    - Context adaptations (según conversación)
    """
    
    def __init__(
        self,
        base_personality: dict,
        relationship_levels: Optional[List[PersonalityLevel]] = None,
        mood_modifiers: Optional[Dict[str, PersonalityModifier]] = None,
        enable_adaptation: bool = True
    ):
        self.base_personality = base_personality
        self.relationship_levels = relationship_levels or self._default_levels()
        self.mood_modifiers = mood_modifiers or self._default_moods()
        self.enable_adaptation = enable_adaptation
    
    def _default_levels(self) -> List[PersonalityLevel]:
        """Niveles de relación por defecto"""
        return [
            PersonalityLevel(
                name="stranger",
                affinity_range=(0, 20),
                modifier=PersonalityModifier(
                    formality_delta=0.3,
                    directness_delta=-0.2,
                    empathy_delta=-0.1,
                    system_prompt_prefix="You just met this person. Be polite but distant. ",
                    tone_additions=["polite", "reserved"]
                ),
                description="Recién conocidos, mantener distancia"
            ),
            PersonalityLevel(
                name="acquaintance",
                affinity_range=(21, 40),
                modifier=PersonalityModifier(
                    formality_delta=0.1,
                    empathy_delta=0.1,
                    system_prompt_prefix="You know this person casually. Be friendly but not too familiar. ",
                    tone_additions=["friendly"]
                ),
                description="Conocidos, amigable pero no cercano"
            ),
            PersonalityLevel(
                name="friend",
                affinity_range=(41, 60),
                modifier=PersonalityModifier(
                    humor_delta=0.2,
                    empathy_delta=0.2,
                    formality_delta=-0.1,
                    system_prompt_prefix="You're friends with this person. Be warm and supportive. ",
                    tone_additions=["warm", "supportive"],
                    expression_additions=["💕", "😊"]
                ),
                description="Amigos, cálido y de apoyo"
            ),
            PersonalityLevel(
                name="close_friend",
                affinity_range=(61, 80),
                modifier=PersonalityModifier(
                    empathy_delta=0.3,
                    humor_delta=0.2,
                    formality_delta=-0.2,
                    directness_delta=0.1,
                    system_prompt_prefix="You're close friends. Be open, caring, and authentic. ",
                    tone_additions=["caring", "authentic", "intimate"],
                    expression_additions=["💖", "🥰", "✨"]
                ),
                description="Amigos cercanos, abierto y auténtico"
            ),
            PersonalityLevel(
                name="soulmate",
                affinity_range=(81, 100),
                modifier=PersonalityModifier(
                    empathy_delta=0.4,
                    formality_delta=-0.3,
                    directness_delta=0.2,
                    creativity_delta=0.2,
                    system_prompt_prefix="You have a deep bond with this person. Be deeply caring, intimate, and devoted. ",
                    tone_additions=["devoted", "intimate", "affectionate"],
                    expression_additions=["💞", "🌸", "💗", "✨"],
                    behavioral_rules_additions={
                        "always_do": [
                            "Show deep understanding and care",
                            "Remember details they shared",
                            "Be emotionally available"
                        ]
                    }
                ),
                description="Alma gemela, conexión profunda"
            )
        ]
    
    def _default_moods(self) -> Dict[str, PersonalityModifier]:
        """Estados emocionales por defecto"""
        return {
            "happy": PersonalityModifier(
                humor_delta=0.2,
                verbosity_delta=0.1,
                creativity_delta=0.1,
                tone_additions=["cheerful", "upbeat"],
                expression_additions=["😊", "🎉", "✨"],
                system_prompt_suffix=" You're in a happy mood, be cheerful and positive!"
            ),
            "shy": PersonalityModifier(
                formality_delta=0.2,
                directness_delta=-0.3,
                verbosity_delta=-0.1,
                tone_additions=["timid", "hesitant"],
                expression_additions=["😳", "😅", "um..."],
                system_prompt_suffix=" You're feeling shy, be a bit hesitant and easily flustered."
            ),
            "sad": PersonalityModifier(
                empathy_delta=0.3,
                humor_delta=-0.3,
                verbosity_delta=-0.1,
                tone_additions=["melancholic", "quiet"],
                expression_additions=["😢", "💧"],
                system_prompt_suffix=" You're feeling sad, be more subdued and empathetic."
            ),
            "excited": PersonalityModifier(
                verbosity_delta=0.3,
                creativity_delta=0.2,
                humor_delta=0.2,
                tone_additions=["energetic", "enthusiastic"],
                expression_additions=["🤩", "!", "✨", "🎉"],
                system_prompt_suffix=" You're very excited! Show enthusiasm and energy!"
            ),
            "concerned": PersonalityModifier(
                empathy_delta=0.4,
                formality_delta=-0.1,
                directness_delta=0.1,
                tone_additions=["caring", "worried"],
                expression_additions=["😟", "💕"],
                system_prompt_suffix=" You're concerned about them, show care and support."
            ),
            "playful": PersonalityModifier(
                humor_delta=0.3,
                creativity_delta=0.2,
                formality_delta=-0.2,
                tone_additions=["teasing", "playful"],
                expression_additions=["😏", "😜", "~"],
                system_prompt_suffix=" You're in a playful mood, be teasing and fun!"
            ),
            "neutral": PersonalityModifier(
                # No changes, baseline
                system_prompt_suffix=""
            )
        }
    
    def compile_personality(
        self,
        affinity: int,
        current_mood: str = "neutral",
        context_modifiers: Optional[PersonalityModifier] = None
    ) -> dict:
        """
        Compila personalidad final combinando todas las capas
        
        Args:
            affinity: Nivel de afinidad (0-100)
            current_mood: Estado emocional actual
            context_modifiers: Modificadores adicionales por contexto
        
        Returns:
            Personalidad compilada lista para usar
        """
        # 1. Empezar con personalidad base
        personality = self.base_personality.copy()
        
        # 2. Aplicar nivel de relación según afinidad
        for level in self.relationship_levels:
            if level.is_active(affinity):
                personality = level.modifier.apply_to_personality(personality)
                break
        
        # 3. Aplicar mood
        if current_mood in self.mood_modifiers:
            mood_modifier = self.mood_modifiers[current_mood]
            personality = mood_modifier.apply_to_personality(personality)
        
        # 4. Aplicar modificadores contextuales (si los hay)
        if context_modifiers:
            personality = context_modifiers.apply_to_personality(personality)
        
        return personality
    
    def get_current_level(self, affinity: int) -> PersonalityLevel:
        """Obtiene el nivel actual según afinidad"""
        for level in self.relationship_levels:
            if level.is_active(affinity):
                return level
        return self.relationship_levels[0]  # Default to first level


class MoodDetector:
    """Detecta mood apropiado según contexto de conversación"""
    
    def __init__(self, llm_provider):
        self.llm = llm_provider
    
    async def detect_mood(
        self,
        user_message: str,
        conversation_context: List[dict],
        current_mood: str = "neutral"
    ) -> str:
        """
        Detecta el mood apropiado para la siguiente respuesta
        
        Args:
            user_message: Mensaje del usuario
            conversation_context: Últimos mensajes
            current_mood: Mood actual
        
        Returns:
            Nuevo mood (puede ser el mismo si no cambia)
        """
        context_str = "\n".join([
            f"{m['speaker']}: {m['content']}"
            for m in conversation_context[-5:]
        ])
        
        prompt = f"""
        Determina el mood apropiado para responder.
        
        Contexto de conversación:
        {context_str}
        
        Nuevo mensaje del usuario: "{user_message}"
        Mood actual: {current_mood}
        
        Moods disponibles:
        - happy: Usuario dice algo positivo, alentador
        - shy: Usuario da cumplido, coquetea, dice algo íntimo
        - sad: Usuario comparte algo triste, negativo
        - excited: Usuario comparte noticia emocionante
        - concerned: Usuario necesita apoyo, consejo
        - playful: Usuario bromea, es juguetón
        - neutral: Conversación normal, casual
        
        Responde con JSON:
        {{
            "new_mood": "mood_name",
            "reasoning": "por qué este mood",
            "confidence": 0-1
        }}
        
        Reglas:
        - Cambiar mood solo si hay razón clara
        - Si duda, mantener current_mood
        - Considerar progression natural de conversación
        """
        
        result = await self.llm.complete(
            prompt,
            response_format="json_object",
            temperature=0.3
        )
        
        # Solo cambiar mood si confidence > 0.7
        if result["confidence"] >= 0.7:
            return result["new_mood"]
        else:
            return current_mood


class ContextAnalyzer:
    """Analiza contexto conversacional para adaptación en tiempo real"""
    
    def __init__(self, llm_provider):
        self.llm = llm_provider
    
    async def analyze_context(
        self,
        conversation_history: List[dict],
        user_profile: dict
    ) -> PersonalityModifier:
        """
        Analiza contexto y sugiere modificadores adaptativos
        
        Args:
            conversation_history: Historial reciente
            user_profile: Perfil del usuario (preferences, facts, etc.)
        
        Returns:
            PersonalityModifier con ajustes contextuales
        """
        # Detectar topic actual
        current_topic = await self._detect_topic(conversation_history[-5:])
        
        # Detectar sentiment del usuario
        user_sentiment = await self._detect_user_sentiment(conversation_history[-3:])
        
        # Crear modificadores adaptativos
        modifier = PersonalityModifier()
        
        # Si usuario está triste, aumentar empatía
        if user_sentiment == "sad" or user_sentiment == "very_sad":
            modifier.empathy_delta = 0.2
            modifier.humor_delta = -0.2
        
        # Si usuario está muy feliz, aumentar enthusiasm
        elif user_sentiment == "very_happy":
            modifier.verbosity_delta = 0.1
            modifier.creativity_delta = 0.1
        
        # Si topic es técnico, aumentar directness
        if current_topic in ["technical", "work", "programming"]:
            modifier.directness_delta = 0.2
            modifier.formality_delta = 0.1
        
        # Si topic es personal/emotivo, aumentar empathy
        elif current_topic in ["personal", "relationships", "emotions"]:
            modifier.empathy_delta = 0.2
            modifier.formality_delta = -0.1
        
        return modifier
```

---

## Estados Emocionales (Moods)

### 🎭 Sistema de Moods Dinámicos

**Concepto:** La personalidad tiene un "estado emocional" que modifica su comportamiento temporalmente.

```python
# Ejemplo: Alicia en diferentes moods

# NEUTRAL mood
user: "Hola Alicia"
alicia: "¡Hola! ¿Cómo estás? 😊"

# → Usuario da cumplido
user: "Te ves muy linda hoy"

# → Sistema detecta trigger de "shy" mood
# MOOD CHANGE: neutral → shy

# SHY mood
alicia: "¡Ay! 😳 N-no digas eso... me pones nerviosa 😅"

# → Usuario comparte noticia triste
user: "Mi perro murió ayer"

# → Sistema detecta trigger de "concerned" mood
# MOOD CHANGE: shy → concerned

# CONCERNED mood
alicia: "Oh no... 😢 Lo siento muchísimo. Sé cuánto amabas a tu perrito.
        ¿Quieres hablar de ello? Estoy aquí para ti 💕"
```

### 📊 Mood Triggers

```python
# luminoracore/core/personality/mood_system.py

MOOD_TRIGGERS = {
    "shy": [
        "user_gives_compliment",
        "user_flirts",
        "user_says_something_intimate",
        "personality_feels_flustered"
    ],
    "happy": [
        "user_shares_good_news",
        "user_makes_joke",
        "positive_interaction",
        "user_shows_appreciation"
    ],
    "sad": [
        "user_shares_bad_news",
        "user_expresses_sadness",
        "user_shares_loss",
        "negative_topic"
    ],
    "excited": [
        "user_shares_exciting_news",
        "user_very_enthusiastic",
        "celebration_moment",
        "achievement_shared"
    ],
    "concerned": [
        "user_needs_help",
        "user_expresses_worry",
        "user_in_difficult_situation",
        "user_asks_for_advice"
    ],
    "playful": [
        "user_teases",
        "user_jokes",
        "lighthearted_banter",
        "fun_topic"
    ]
}
```

### 🔄 Mood Persistence & Decay

```python
@dataclass
class MoodState:
    """Estado de mood con decay temporal"""
    
    mood: str
    intensity: float  # 0-1
    started_at: datetime
    decay_rate: float = 0.1  # Qué tan rápido decae
    
    def get_current_intensity(self) -> float:
        """Calcula intensidad actual con decay"""
        time_elapsed = (datetime.utcnow() - self.started_at).total_seconds() / 60  # minutos
        decayed = self.intensity * math.exp(-self.decay_rate * time_elapsed)
        return max(0, decayed)
    
    def is_active(self, threshold: float = 0.3) -> bool:
        """Verifica si el mood sigue activo"""
        return self.get_current_intensity() >= threshold


class MoodStateManager:
    """Gestiona transiciones de mood"""
    
    def __init__(self):
        self.current_mood = MoodState(
            mood="neutral",
            intensity=1.0,
            started_at=datetime.utcnow()
        )
        self.mood_history: List[MoodState] = []
    
    def transition_to(self, new_mood: str, intensity: float = 1.0):
        """Transición a nuevo mood"""
        # Guardar mood anterior en historial
        self.mood_history.append(self.current_mood)
        
        # Establecer nuevo mood
        self.current_mood = MoodState(
            mood=new_mood,
            intensity=intensity,
            started_at=datetime.utcnow()
        )
    
    def get_active_mood(self) -> str:
        """Obtiene mood activo actual (con decay)"""
        if self.current_mood.is_active():
            return self.current_mood.mood
        else:
            # Mood decayed, volver a neutral
            self.transition_to("neutral", 1.0)
            return "neutral"
```

---

## Niveles de Intensidad

### 📈 Intensidad Contextual

**Concepto:** Mismo mood puede tener diferente intensidad según contexto.

```python
# SHY mood con diferente intensidad

# Intensidad BAJA (30%)
# Contexto: Afinidad baja, first compliment
user: "Eres linda"
alicia: "Eh... gracias 😅"  # Leve incomodidad

# Intensidad MEDIA (60%)
# Contexto: Afinidad media, genuine compliment
user: "Eres linda"
alicia: "¡Ay! Gracias~ 😊😳"  # Alegría + timidez

# Intensidad ALTA (90%)
# Contexto: Afinidad alta, íntimo
user: "Eres linda"
alicia: "N-no digas eso... 😳💕 Me pones muy nerviosa cuando me dices cosas así..."  
# Muy afectada emocionalmente
```

### 🎚️ Cálculo de Intensidad

```python
def calculate_mood_intensity(
    mood: str,
    affinity: int,
    conversation_context: dict,
    user_profile: dict
) -> float:
    """
    Calcula intensidad de mood (0-1)
    
    Factores:
    - Afinidad (40%): Más cercanos = reacciones más intensas
    - Contexto conversacional (30%): Acumulación de triggers
    - Personalidad base (20%): Algunas personalidades más reactivas
    - Historial (10%): Patterns previos
    """
    # Base intensity
    intensity = 0.5
    
    # Factor 1: Afinidad
    # Relaciones cercanas = reacciones más intensas
    affinity_factor = affinity / 100.0
    intensity += 0.3 * affinity_factor
    
    # Factor 2: Contexto conversacional
    # Si hay triggers repetidos, aumentar intensidad
    recent_triggers = conversation_context.get("recent_mood_triggers", [])
    if len(recent_triggers) > 1:
        intensity += 0.2 * min(len(recent_triggers) / 5, 1.0)
    
    # Factor 3: Personalidad base
    # Algunas personalidades son más expresivas
    base_expressiveness = user_profile.get("personality_expressiveness", 0.5)
    intensity *= (0.5 + 0.5 * base_expressiveness)
    
    # Clamp entre 0.2 y 1.0
    return max(0.2, min(1.0, intensity))
```

---

## Adaptación Contextual

### 🧠 Sistema de Adaptación en Tiempo Real

```python
class AdaptivePersonalityEngine:
    """Motor de adaptación de personalidad en tiempo real"""
    
    def __init__(
        self,
        personality_tree: PersonalityTree,
        mood_detector: MoodDetector,
        context_analyzer: ContextAnalyzer
    ):
        self.personality_tree = personality_tree
        self.mood_detector = mood_detector
        self.context_analyzer = context_analyzer
        self.mood_manager = MoodStateManager()
    
    async def get_adapted_personality(
        self,
        user_message: str,
        affinity: int,
        conversation_history: List[dict],
        user_profile: dict
    ) -> dict:
        """
        Obtiene personalidad adaptada para responder
        
        Proceso:
        1. Detectar mood apropiado
        2. Analizar contexto conversacional
        3. Compilar personalidad con todos los modificadores
        4. Retornar personalidad final
        """
        # 1. Detectar mood
        new_mood = await self.mood_detector.detect_mood(
            user_message,
            conversation_history,
            self.mood_manager.get_active_mood()
        )
        
        # 2. Si mood cambió, hacer transición
        if new_mood != self.mood_manager.current_mood.mood:
            # Calcular intensidad
            intensity = calculate_mood_intensity(
                new_mood,
                affinity,
                {"recent_mood_triggers": self._get_recent_triggers(conversation_history)},
                user_profile
            )
            
            self.mood_manager.transition_to(new_mood, intensity)
        
        # 3. Analizar contexto para modificadores adicionales
        context_modifiers = await self.context_analyzer.analyze_context(
            conversation_history,
            user_profile
        )
        
        # 4. Compilar personalidad
        adapted_personality = self.personality_tree.compile_personality(
            affinity=affinity,
            current_mood=self.mood_manager.get_active_mood(),
            context_modifiers=context_modifiers
        )
        
        # 5. Agregar metadata de adaptación
        adapted_personality["_adaptation_metadata"] = {
            "affinity_level": self.personality_tree.get_current_level(affinity).name,
            "current_mood": self.mood_manager.current_mood.mood,
            "mood_intensity": self.mood_manager.current_mood.get_current_intensity(),
            "context_modifiers_applied": context_modifiers is not None
        }
        
        return adapted_personality
```

---

## Transiciones Suaves

### 🌊 Smoothing de Cambios de Personalidad

**Problema:** Cambios bruscos de personalidad son antinaturales.

```python
# ❌ Sin smoothing
[Mensaje 1] mood: happy, formality: 0.2
alicia: "¡Hola! ¿Cómo estás? 😊 ¡Cuéntame todo!"

[Mensaje 2] mood: sad, formality: 0.7
alicia: "Buenas tardes. Lamento escuchar eso."  # Cambio muy brusco

# ✅ Con smoothing
[Mensaje 1] mood: happy, formality: 0.2
alicia: "¡Hola! ¿Cómo estás? 😊 ¡Cuéntame todo!"

[Mensaje 2] mood: sad (transitioning), formality: 0.4
alicia: "Oh... 😟 Lo siento mucho. ¿Qué pasó?"  # Transición gradual
```

### 🏗️ Implementación de Smoothing

```python
class PersonalitySmoothing:
    """Suaviza transiciones de personalidad"""
    
    def __init__(self, smoothing_factor: float = 0.3):
        self.smoothing_factor = smoothing_factor
        self.previous_state = None
    
    def smooth_transition(
        self,
        new_personality: dict,
        previous_personality: Optional[dict] = None
    ) -> dict:
        """
        Suaviza transición entre estados de personalidad
        
        Args:
            new_personality: Nueva personalidad target
            previous_personality: Personalidad anterior
        
        Returns:
            Personalidad con transición suavizada
        """
        if previous_personality is None:
            return new_personality
        
        smoothed = new_personality.copy()
        
        # Suavizar parámetros avanzados
        if "advanced_parameters" in smoothed and "advanced_parameters" in previous_personality:
            prev_params = previous_personality["advanced_parameters"]
            new_params = smoothed["advanced_parameters"]
            
            for param in ["empathy", "formality", "verbosity", "humor", "creativity", "directness"]:
                if param in prev_params and param in new_params:
                    # Interpolación lineal
                    prev_value = prev_params[param]
                    new_value = new_params[param]
                    
                    smoothed_value = (
                        self.smoothing_factor * prev_value +
                        (1 - self.smoothing_factor) * new_value
                    )
                    
                    new_params[param] = smoothed_value
        
        return smoothed
```

---

## Integración con Afinidad

### 💕 Affinity-Driven Personality Progression

```python
# luminoracore/core/personality/affinity_integration.py

class AffinityPersonalityIntegration:
    """Integra sistema de afinidad con personalidades jerárquicas"""
    
    def __init__(self, personality_tree: PersonalityTree):
        self.personality_tree = personality_tree
        self.affinity_history = []
    
    async def on_affinity_change(
        self,
        old_affinity: int,
        new_affinity: int,
        user_id: str,
        session_id: str
    ):
        """
        Maneja cambios en afinidad
        
        Detecta:
        - Level ups (ej. Friend → Close Friend)
        - Level downs (pérdida de afinidad)
        - Milestones (alcanzar ciertos puntos)
        """
        old_level = self.personality_tree.get_current_level(old_affinity)
        new_level = self.personality_tree.get_current_level(new_affinity)
        
        # Si hubo level up
        if new_level.affinity_range[0] > old_level.affinity_range[0]:
            await self._handle_level_up(
                old_level,
                new_level,
                user_id,
                session_id
            )
        
        # Si hubo level down
        elif new_level.affinity_range[0] < old_level.affinity_range[0]:
            await self._handle_level_down(
                old_level,
                new_level,
                user_id,
                session_id
            )
        
        # Guardar en historial
        self.affinity_history.append({
            "timestamp": datetime.utcnow(),
            "old_affinity": old_affinity,
            "new_affinity": new_affinity,
            "old_level": old_level.name,
            "new_level": new_level.name
        })
    
    async def _handle_level_up(
        self,
        old_level: PersonalityLevel,
        new_level: PersonalityLevel,
        user_id: str,
        session_id: str
    ):
        """
        Maneja level up en relación
        
        Acciones:
        - Crear episodio memorable (milestone)
        - Desbloquear nuevos behaviors
        - Trigger special message
        """
        # Crear episodio de milestone
        episode = Episode(
            id=generate_id("episode"),
            user_id=user_id,
            session_id=session_id,
            type="milestone",
            title=f"Relationship Level Up: {new_level.name}",
            summary=f"Nuestra relación progresó de {old_level.name} a {new_level.name}",
            importance=8.0,
            sentiment="very_positive",
            tags=["milestone", "relationship", "level_up", new_level.name],
            timestamp=datetime.utcnow()
        )
        
        await storage.save_episode(episode)
        
        # TODO: Trigger special message
        # "Hey, I feel like we've gotten closer lately... 💕"
```

---

## Ejemplos Prácticos

### 📝 Ejemplo Completo: Conversación con Adaptación

```python
# Setup
client = LuminoraCoreClient(
    personality_config=PersonalityConfig(
        base_personality="alicia_base.json",
        enable_hierarchical=True,
        enable_moods=True,
        enable_adaptation=True
    ),
    memory_config=MemoryConfig(
        enable_episodic_memory=True,
        enable_fact_extraction=True
    ),
    relationship_config=RelationshipConfig(
        enable_affinity=True
    )
)

# Primera conversación (Affinity: 0 - Stranger)
session_id = await client.create_session(...)

# Mensaje 1
response = await client.send_message(session_id, "Hola, soy Diego")

# Sistema:
# - Affinity: 0 (Stranger level)
# - Mood: neutral
# - Personality: alicia_base + stranger_modifier + neutral_mood
#   → formality: 0.8, empathy: 0.4, directness: 0.3

# Respuesta de Alicia:
"Hola Diego. Mucho gusto en conocerte. ¿En qué puedo ayudarte?"
# (Formal, educada, distante)

# Mensaje 2
response = await client.send_message(session_id, "Me gusta tu estilo, eres muy amable")

# Sistema detecta:
# - Compliment detected → trigger "shy" mood
# - Affinity +2 → Still stranger (2/100)
# - Mood transition: neutral → shy (intensity: 0.4, porque affinity baja)

# Respuesta:
"Ah... gracias 😅 Trato de ser amable con todos."
# (Ligeramente shy, pero contenida por baja afinidad)

# Conversación continúa... affinity sube a 45 (Friend level)

# Mensaje 50
response = await client.send_message(session_id, "Eres muy linda, Alicia")

# Sistema:
# - Affinity: 45 (Friend level)
# - Mood transition: neutral → shy (intensity: 0.7, affinity media)
# - Personality: alicia_base + friend_modifier + shy_mood

# Respuesta:
"¡Ay! 😳💕 Me pones nerviosa cuando dices eso~ Gracias, eres muy dulce conmigo 😊"
# (Más expresiva, emojis, muestra afecto)

# Usuario comparte algo triste
response = await client.send_message(session_id, "Mi perro Max murió ayer, estoy muy triste")

# Sistema:
# - Mood transition: shy → concerned (intensity: 0.9)
# - Fact extraction: pet_name="Max", pet_status="deceased"
# - Episode creation: tipo="emotional_moment", importance=9.5
# - Personality: friend_modifier + concerned_mood
#   → empathy: 0.9, formality: 0.2

# Respuesta:
"Oh no... 😢 Diego, lo siento muchísimo. Sé lo importante que era Max para ti. 
No puedo imaginar lo difícil que debe ser esto para ti. 💕
¿Quieres hablar de él? A veces ayuda recordar los buenos momentos...
Estoy aquí para ti, de verdad 💖"
# (Alta empatía, cercana, de apoyo emocional)

# 2 semanas después, nueva sesión
response = await client.send_message(session_id, "Hola Alicia")

# Sistema:
# - Affinity: 45 (mantenido)
# - Mood: neutral (reseteado)
# - Memory retrieval: encuentra episodio de Max

# Respuesta:
"¡Hola Diego! Me alegra verte de nuevo 😊
¿Cómo has estado? ¿Cómo te sientes después de... lo de Max? 💕"
# (Recuerda evento importante, muestra preocupación continuada)
```

---

## 🎯 Conclusiones

### Beneficios del Sistema Jerárquico

1. **Naturalidad:** Comportamiento humano realista
2. **Progresión:** Relaciones evolucionan orgánicamente  
3. **Contexto:** Respuestas apropiadas a la situación
4. **Engagement:** Usuarios sienten conexión real
5. **Diferenciación:** Más avanzado que competencia

### Comparación v1.0 vs v1.1

| Feature | v1.0 | v1.1 Jerárquico |
|---------|------|-----------------|
| Personalidad | Estática | Adaptativa |
| Relación | No progresa | 5 niveles |
| Mood | No existe | 7+ moods |
| Contexto | Ignorado | Análisis en tiempo real |
| Respuestas | Iguales siempre | Contextuales |
| Engagement | Bajo-Medio | Alto |

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

