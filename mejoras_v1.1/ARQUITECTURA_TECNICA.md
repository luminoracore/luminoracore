# Arquitectura Técnica - LuminoraCore v1.1

**Diseño detallado de implementación: clases, módulos, APIs, y esquemas de base de datos**

---

## ⚠️ DISCLAIMER IMPORTANTE

**Los ejemplos de código Python en este documento muestran valores como `affinity_range=(0, 20)` en código.**

**ESTO NO SIGNIFICA QUE ESTÉN HARDCODEADOS.**

Estos valores son **ejemplos de defaults** que el código usa **SOLO SI el JSON no los especifica**.

**EN PRODUCCIÓN:**
- Todos los valores se leen del JSON de personalidad
- El código solo tiene defaults de fallback
- Ver [INTEGRACION_CON_SISTEMA_ACTUAL.md](./INTEGRACION_CON_SISTEMA_ACTUAL.md) para aclaración completa
- Ver [EJEMPLOS_PERSONALIDADES_JSON.md](./EJEMPLOS_PERSONALIDADES_JSON.md) para templates JSON reales

---

## 📋 Tabla de Contenidos

1. [Visión General de Arquitectura](#visión-general)
2. [Estructura de Módulos](#estructura-de-módulos)
3. [Esquemas de Base de Datos](#esquemas-de-base-de-datos)
4. [APIs y Interfaces](#apis-y-interfaces)
5. [Flujos de Datos](#flujos-de-datos)
6. [Configuración](#configuración)
7. [Integración con v1.0](#integración-con-v10)

---

## Visión General

### 💡 Cómo se Usa Realmente (Ejemplo Completo)

```python
# ============================================
# EJEMPLO REAL: De JSON a Ejecución
# ============================================

# 1. Desarrollador crea personalidad en JSON
# alicia.json contiene:
# {
#   "persona": {...},
#   "hierarchical_config": {
#     "enabled": true,
#     "relationship_levels": [
#       {"name": "stranger", "affinity_range": [0, 20], "modifiers": {...}},
#       {"name": "friend", "affinity_range": [41, 60], "modifiers": {...}}
#     ]
#   }
# }

# 2. Sistema carga JSON
personality_json = load_json("alicia.json")

# 3. Crear PersonalityTree DESDE JSON (no hardcoded)
tree = PersonalityTree.from_json(personality_json)  # ← Lee valores del JSON

# 4. Usuario conversa
affinity = await db.get_affinity(session_id)  # Ej: 45 (de BBDD)
mood = await db.get_mood(session_id)          # Ej: "shy" (de BBDD)

# 5. Compilar dinámicamente
compiled = tree.compile(affinity=45, mood="shy")
# Aplica modificadores que están en el JSON

# 6. Generar respuesta
response = await llm.generate(compiled + message)
```

**Los valores NO están en código, están en el JSON.**

---

### 🏗️ Arquitectura Modular

```
luminoracore/
├── core/
│   ├── personality/
│   │   ├── __init__.py
│   │   ├── base.py                    # Personalidad base (v1.0)
│   │   ├── hierarchical.py            # NEW: Sistema jerárquico
│   │   ├── mood_system.py             # NEW: Sistema de moods
│   │   ├── adaptation.py              # NEW: Adaptación contextual
│   │   └── compiler.py                # Compilador de personalidades
│   │
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── storage.py                 # Storage base (v1.0)
│   │   ├── episodic.py                # NEW: Memoria episódica
│   │   ├── semantic.py                # NEW: Vector search
│   │   ├── classifier.py              # NEW: Clasificación inteligente
│   │   ├── fact_extractor.py          # NEW: Extracción de facts
│   │   └── retrieval.py               # NEW: Recuperación contextual
│   │
│   ├── relationship/
│   │   ├── __init__.py
│   │   ├── affinity.py                # NEW: Sistema de afinidad
│   │   ├── events.py                  # NEW: Eventos de relación
│   │   └── progression.py             # NEW: Progresión de relación
│   │
│   └── analytics/
│       ├── __init__.py
│       ├── conversation_analytics.py  # NEW: Análisis conversacional
│       └── metrics.py                 # NEW: Métricas y tracking
│
├── providers/
│   └── embeddings/
│       ├── __init__.py
│       ├── openai_embeddings.py       # NEW: OpenAI embeddings
│       ├── cohere_embeddings.py       # NEW: Cohere embeddings
│       └── local_embeddings.py        # NEW: Sentence transformers
│
└── storage/
    └── vector/
        ├── __init__.py
        ├── pgvector.py                # NEW: PostgreSQL pgvector
        ├── pinecone.py                # NEW: Pinecone
        └── weaviate.py                # NEW: Weaviate
```

---

## Estructura de Módulos

### 1. Core - Personality

#### `hierarchical.py`

```python
"""
luminoracore/core/personality/hierarchical.py

Sistema de personalidades jerárquicas con niveles de relación y moods
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import json

# ============================================================================
# ENUMS
# ============================================================================

class RelationshipLevel(Enum):
    """Niveles de relación usuario-personalidad"""
    STRANGER = "stranger"
    ACQUAINTANCE = "acquaintance"
    FRIEND = "friend"
    CLOSE_FRIEND = "close_friend"
    SOULMATE = "soulmate"

class MoodState(Enum):
    """Estados emocionales de la personalidad"""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SHY = "shy"
    SAD = "sad"
    EXCITED = "excited"
    CONCERNED = "concerned"
    PLAYFUL = "playful"
    ANGRY = "angry"
    CONFUSED = "confused"

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class PersonalityModifier:
    """
    Modificadores que se aplican a la personalidad base
    
    Attributes:
        empathy_delta: Cambio en empatía (-1.0 a +1.0)
        formality_delta: Cambio en formalidad
        verbosity_delta: Cambio en verbosidad
        humor_delta: Cambio en humor
        creativity_delta: Cambio en creatividad
        directness_delta: Cambio en directness
        tone_additions: Tonos adicionales para agregar
        expression_additions: Expresiones adicionales
        system_prompt_prefix: Prefijo para system prompt
        system_prompt_suffix: Sufijo para system prompt
    """
    empathy_delta: float = 0.0
    formality_delta: float = 0.0
    verbosity_delta: float = 0.0
    humor_delta: float = 0.0
    creativity_delta: float = 0.0
    directness_delta: float = 0.0
    
    tone_additions: List[str] = field(default_factory=list)
    expression_additions: List[str] = field(default_factory=list)
    behavioral_rules_additions: Dict[str, List[str]] = field(default_factory=dict)
    
    system_prompt_prefix: str = ""
    system_prompt_suffix: str = ""
    
    def apply_to(self, base_personality: dict) -> dict:
        """Aplica modificadores a personalidad base"""
        modified = base_personality.copy()
        
        # Modificar advanced_parameters
        if "advanced_parameters" in modified:
            params = modified["advanced_parameters"]
            for param in ["empathy", "formality", "verbosity", "humor", "creativity", "directness"]:
                delta = getattr(self, f"{param}_delta")
                if delta != 0.0:
                    current = params.get(param, 0.5)
                    params[param] = self._clamp(current + delta)
        
        # Modificar linguistic_profile
        if "linguistic_profile" in modified:
            profile = modified["linguistic_profile"]
            
            if self.tone_additions:
                profile["tone"] = list(set(profile.get("tone", []) + self.tone_additions))
            
            if self.expression_additions:
                profile["expressions"] = list(set(
                    profile.get("expressions", []) + self.expression_additions
                ))
        
        return modified
    
    @staticmethod
    def _clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Limita valor entre min y max"""
        return max(min_val, min(max_val, value))

@dataclass
class PersonalityLevel:
    """
    Nivel de personalidad (ej. Friend, Soulmate)
    
    Attributes:
        name: Nombre del nivel
        affinity_range: Rango de afinidad (min, max)
        modifier: Modificadores a aplicar
        description: Descripción del nivel
    """
    name: str
    affinity_range: tuple
    modifier: PersonalityModifier
    description: str = ""
    
    def is_active(self, affinity: int) -> bool:
        """Verifica si este nivel está activo"""
        return self.affinity_range[0] <= affinity <= self.affinity_range[1]

# ============================================================================
# MAIN CLASSES
# ============================================================================

class PersonalityTree:
    """
    Árbol de personalidad jerárquica
    
    Gestiona:
    - Base personality (inmutable)
    - Relationship levels (según afinidad)
    - Mood states (según contexto emocional)
    - Context adaptations (según conversación)
    
    IMPORTANTE: Los valores se cargan del JSON de personalidad.
    Ver método from_json() para carga desde JSON.
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
    
    @classmethod
    def from_json(cls, personality_json: dict) -> 'PersonalityTree':
        """
        Crea PersonalityTree desde JSON de personalidad
        
        ESTE ES EL MÉTODO REAL que se usa en producción.
        Lee TODOS los valores del JSON.
        
        Args:
            personality_json: Personalidad cargada desde alicia.json
        
        Returns:
            PersonalityTree configurado desde el JSON
        """
        # Extraer config jerárquica del JSON
        hierarchical_config = personality_json.get("hierarchical_config", {})
        
        if not hierarchical_config.get("enabled", False):
            # Si no está habilitado, usar defaults
            return cls(base_personality=personality_json)
        
        # Leer niveles del JSON
        levels_json = hierarchical_config.get("relationship_levels", [])
        levels = [
            PersonalityLevel(
                name=level["name"],
                affinity_range=tuple(level["affinity_range"]),  # Del JSON!
                modifier=PersonalityModifier(
                    empathy_delta=level["modifiers"].get("advanced_parameters", {}).get("empathy", 0.0),
                    formality_delta=level["modifiers"].get("advanced_parameters", {}).get("formality", 0.0),
                    # ... etc, todos del JSON
                ),
                description=level.get("description", "")
            )
            for level in levels_json
        ]
        
        # Leer moods del JSON
        mood_config = personality_json.get("mood_config", {})
        moods = {}  # Similar parsing desde JSON
        
        return cls(
            base_personality=personality_json,
            relationship_levels=levels if levels else None,
            mood_modifiers=moods if moods else None,
            enable_adaptation=hierarchical_config.get("enabled", True)
        )
    
    def compile(
        self,
        affinity: int,
        current_mood: str = "neutral",
        context_modifiers: Optional[PersonalityModifier] = None
    ) -> dict:
        """
        Compila personalidad final
        
        Args:
            affinity: Nivel de afinidad 0-100
            current_mood: Estado emocional actual
            context_modifiers: Modificadores contextuales adicionales
        
        Returns:
            Personalidad compilada
        """
        # 1. Base
        personality = self.base_personality.copy()
        
        # 2. Relationship level
        for level in self.relationship_levels:
            if level.is_active(affinity):
                personality = level.modifier.apply_to(personality)
                break
        
        # 3. Mood
        if current_mood in self.mood_modifiers:
            personality = self.mood_modifiers[current_mood].apply_to(personality)
        
        # 4. Context
        if context_modifiers:
            personality = context_modifiers.apply_to(personality)
        
        return personality
    
    def _default_levels(self) -> List[PersonalityLevel]:
        """
        Niveles por defecto (SOLO si JSON no los especifica)
        
        IMPORTANTE: Estos son FALLBACK defaults.
        En producción, los niveles se leen del JSON de personalidad:
        personality_json["hierarchical_config"]["relationship_levels"]
        """
        return [
            PersonalityLevel(
                name="stranger",
                affinity_range=(0, 20),  # Del JSON, este es default
                modifier=PersonalityModifier(
                    formality_delta=0.3,
                    directness_delta=-0.2,
                    system_prompt_prefix="You just met this person. Be polite but distant. "
                ),
                description="Recién conocidos"
            ),
            PersonalityLevel(
                name="friend",
                affinity_range=(41, 60),  # Del JSON, este es default
                modifier=PersonalityModifier(
                    empathy_delta=0.2,
                    humor_delta=0.2,
                    formality_delta=-0.1,
                    system_prompt_prefix="You're friends. Be warm and supportive. "
                ),
                description="Amigos"
            ),
            PersonalityLevel(
                name="soulmate",
                affinity_range=(81, 100),  # Del JSON, este es default
                modifier=PersonalityModifier(
                    empathy_delta=0.4,
                    formality_delta=-0.3,
                    system_prompt_prefix="Deep bond. Be intimate and devoted. "
                ),
                description="Alma gemela"
            )
        ]
    
    def _default_moods(self) -> Dict[str, PersonalityModifier]:
        """
        Moods por defecto (SOLO si JSON no los especifica)
        
        IMPORTANTE: Estos son FALLBACK defaults.
        En producción, los moods se leen del JSON de personalidad:
        personality_json["mood_config"]["moods"]
        """
        return {
            "neutral": PersonalityModifier(),
            "happy": PersonalityModifier(
                humor_delta=0.2,
                system_prompt_suffix=" You're in a happy mood!"
            ),
            "shy": PersonalityModifier(
                formality_delta=0.2,
                directness_delta=-0.3,
                system_prompt_suffix=" You're feeling shy and flustered."
            ),
            "sad": PersonalityModifier(
                empathy_delta=0.3,
                humor_delta=-0.3,
                system_prompt_suffix=" You're feeling sad and subdued."
            )
        }


class MoodDetector:
    """Detecta mood apropiado según contexto"""
    
    def __init__(self, llm_provider):
        self.llm = llm_provider
    
    async def detect(
        self,
        user_message: str,
        conversation_context: List[dict],
        current_mood: str = "neutral"
    ) -> str:
        """Detecta mood para siguiente respuesta"""
        # Implementación con LLM
        # Ver SISTEMA_PERSONALIDADES_JERARQUICAS.md para detalles
        pass
```

---

### 2. Core - Memory

#### `episodic.py`

```python
"""
luminoracore/core/memory/episodic.py

Sistema de memoria episódica para recordar momentos importantes
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import numpy as np

@dataclass
class Episode:
    """
    Episodio memorable en la conversación
    
    Attributes:
        id: ID único
        user_id: ID del usuario
        session_id: ID de sesión
        type: Tipo de episodio (emotional_moment, milestone, etc.)
        title: Título corto
        summary: Resumen del episodio
        importance: Importancia 0-10
        sentiment: Sentimiento principal
        tags: Tags para búsqueda
        context_messages: IDs de mensajes relacionados
        timestamp: Cuándo ocurrió
        temporal_decay: Factor de decay temporal (1.0 = reciente)
        embedding: Vector para búsqueda semántica
    """
    id: str
    user_id: str
    session_id: str
    type: str
    title: str
    summary: str
    importance: float
    sentiment: str
    tags: List[str]
    context_messages: List[str]
    timestamp: datetime
    temporal_decay: float = 1.0
    related_facts: List[str] = None
    related_episodes: List[str] = None
    embedding: np.ndarray = None
    
    def get_current_importance(self) -> float:
        """Importancia actual con decay temporal"""
        return self.importance * self.temporal_decay
    
    def update_decay(self, days_passed: int):
        """Actualiza decay temporal"""
        import math
        decay_rate = 0.1
        self.temporal_decay = 1.0 / (1.0 + decay_rate * math.log(days_passed + 1))


class EpisodicMemoryManager:
    """
    Gestiona memoria episódica
    
    Funciones:
    - Detectar episodios automáticamente
    - Clasificar por importancia
    - Almacenar en DB
    - Recuperar episodios relevantes
    """
    
    def __init__(
        self,
        storage_backend,
        llm_provider,
        importance_threshold: float = 7.0
    ):
        self.storage = storage_backend
        self.llm = llm_provider
        self.importance_threshold = importance_threshold
    
    async def detect_episode(
        self,
        messages: List,
        context: dict
    ) -> Optional[Episode]:
        """
        Detecta si los mensajes forman un episodio memorable
        
        Args:
            messages: Últimos mensajes (3-10)
            context: Contexto adicional (afinidad, mood, etc.)
        
        Returns:
            Episode si se detecta, None si no
        """
        # 1. Analizar sentimiento
        sentiment = await self._analyze_sentiment(messages)
        
        # 2. Scoring de importancia
        importance = await self._score_importance(messages, sentiment, context)
        
        # 3. Si no alcanza threshold, no crear
        if importance < self.importance_threshold:
            return None
        
        # 4. Crear episodio
        # ... (ver SISTEMA_MEMORIA_AVANZADO.md para detalles)
        pass
    
    async def retrieve_relevant(
        self,
        query: str,
        user_id: str,
        top_k: int = 5
    ) -> List[Episode]:
        """Recupera episodios relevantes"""
        # Búsqueda semántica + temporal decay
        # ... (ver SISTEMA_MEMORIA_AVANZADO.md)
        pass
```

#### `semantic.py`

```python
"""
luminoracore/core/memory/semantic.py

Sistema de búsqueda semántica con vector embeddings
"""

from typing import List, Optional
import numpy as np

class SemanticMemoryManager:
    """
    Gestiona búsqueda semántica
    
    Funciones:
    - Indexar mensajes con embeddings
    - Búsqueda por similitud
    - Filtrado por metadata
    """
    
    def __init__(
        self,
        embedding_provider: str = "openai",
        vector_store: str = "pgvector",
        similarity_threshold: float = 0.75
    ):
        self.embedding_provider = self._init_embedding_provider(embedding_provider)
        self.vector_store = self._init_vector_store(vector_store)
        self.similarity_threshold = similarity_threshold
    
    async def index_message(
        self,
        message: dict,
        metadata: dict
    ) -> str:
        """
        Indexa mensaje para búsqueda semántica
        
        Args:
            message: Mensaje a indexar
            metadata: Metadata (timestamp, tags, etc.)
        
        Returns:
            ID del vector
        """
        # Crear embedding
        embedding = await self.embedding_provider.create_embedding(message["content"])
        
        # Indexar
        vector_id = await self.vector_store.upsert(
            id=f"vec_{message['id']}",
            vector=embedding,
            metadata={
                "message_id": message["id"],
                "user_id": message["user_id"],
                "content": message["content"],
                **metadata
            }
        )
        
        return vector_id
    
    async def search(
        self,
        query: str,
        user_id: str,
        top_k: int = 10,
        filter: Optional[dict] = None
    ) -> List[dict]:
        """
        Búsqueda semántica
        
        Args:
            query: Consulta en lenguaje natural
            user_id: ID del usuario
            top_k: Número de resultados
            filter: Filtros adicionales
        
        Returns:
            Lista de resultados ordenados por relevancia
        """
        # Crear embedding de query
        query_embedding = await self.embedding_provider.create_embedding(query)
        
        # Búsqueda vectorial
        results = await self.vector_store.query(
            vector=query_embedding,
            top_k=top_k,
            filter={"user_id": user_id, **(filter or {})},
            include_metadata=True
        )
        
        # Filtrar por threshold
        filtered = [r for r in results if r["score"] >= self.similarity_threshold]
        
        return filtered
```

---

## Esquemas de Base de Datos

### PostgreSQL Schema

```sql
-- ============================================================================
-- FACTS TABLE
-- ============================================================================

CREATE TABLE user_facts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,  -- personal_info, preferences, etc.
    key VARCHAR(255) NOT NULL,
    value JSONB NOT NULL,  -- Soporta strings, numbers, objects
    confidence FLOAT DEFAULT 1.0,  -- 0.0 - 1.0
    source_message_id VARCHAR(255),
    first_mentioned TIMESTAMP DEFAULT NOW(),
    last_updated TIMESTAMP DEFAULT NOW(),
    mention_count INTEGER DEFAULT 1,
    tags TEXT[],
    context TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT unique_user_fact UNIQUE(user_id, category, key)
);

CREATE INDEX idx_user_facts_user_id ON user_facts(user_id);
CREATE INDEX idx_user_facts_category ON user_facts(category);
CREATE INDEX idx_user_facts_tags ON user_facts USING GIN(tags);

-- ============================================================================
-- EPISODES TABLE
-- ============================================================================

CREATE TABLE episodes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,  -- emotional_moment, milestone, etc.
    title VARCHAR(500) NOT NULL,
    summary TEXT NOT NULL,
    importance FLOAT NOT NULL,  -- 0-10
    sentiment VARCHAR(50) NOT NULL,  -- very_positive, positive, etc.
    tags TEXT[],
    context_messages TEXT[],  -- Array de message IDs
    timestamp TIMESTAMP NOT NULL,
    temporal_decay FLOAT DEFAULT 1.0,
    related_facts UUID[],
    related_episodes UUID[],
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_episodes_user_id ON episodes(user_id);
CREATE INDEX idx_episodes_importance ON episodes(importance);
CREATE INDEX idx_episodes_timestamp ON episodes(timestamp);
CREATE INDEX idx_episodes_type ON episodes(type);
CREATE INDEX idx_episodes_tags ON episodes USING GIN(tags);

-- ============================================================================
-- VECTOR EMBEDDINGS (pgvector)
-- ============================================================================

-- Requiere extensión pgvector
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE message_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    session_id VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1536),  -- OpenAI text-embedding-3-small
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_message_embeddings_user_id ON message_embeddings(user_id);
CREATE INDEX idx_message_embeddings_embedding ON message_embeddings 
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Función de búsqueda
CREATE OR REPLACE FUNCTION search_similar_messages(
    query_embedding vector(1536),
    query_user_id VARCHAR(255),
    similarity_threshold FLOAT DEFAULT 0.75,
    max_results INT DEFAULT 10
)
RETURNS TABLE (
    message_id VARCHAR(255),
    content TEXT,
    similarity FLOAT,
    metadata JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.message_id,
        m.content,
        1 - (m.embedding <=> query_embedding) as similarity,
        m.metadata
    FROM message_embeddings m
    WHERE m.user_id = query_user_id
        AND 1 - (m.embedding <=> query_embedding) >= similarity_threshold
    ORDER BY m.embedding <=> query_embedding
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- AFFINITY TABLE
-- ============================================================================

CREATE TABLE user_affinity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    personality_name VARCHAR(255) NOT NULL,
    affinity_points INTEGER DEFAULT 0,  -- 0-100
    current_level VARCHAR(50) DEFAULT 'stranger',  -- stranger, friend, etc.
    total_messages INTEGER DEFAULT 0,
    positive_interactions INTEGER DEFAULT 0,
    negative_interactions INTEGER DEFAULT 0,
    last_interaction TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    CONSTRAINT unique_user_personality UNIQUE(user_id, personality_name)
);

CREATE INDEX idx_affinity_user_id ON user_affinity(user_id);

-- ============================================================================
-- AFFINITY EVENTS TABLE
-- ============================================================================

CREATE TABLE affinity_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    personality_name VARCHAR(255) NOT NULL,
    event_type VARCHAR(100) NOT NULL,  -- mention_preference, share_personal_info, etc.
    affinity_delta INTEGER NOT NULL,  -- +/- points
    new_affinity INTEGER NOT NULL,
    old_level VARCHAR(50),
    new_level VARCHAR(50),
    context JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_affinity_events_user_id ON affinity_events(user_id);
CREATE INDEX idx_affinity_events_created_at ON affinity_events(created_at);

-- ============================================================================
-- SESSION MOOD STATE
-- ============================================================================

CREATE TABLE session_moods (
    session_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    current_mood VARCHAR(50) DEFAULT 'neutral',
    mood_intensity FLOAT DEFAULT 1.0,
    mood_started_at TIMESTAMP DEFAULT NOW(),
    mood_history JSONB DEFAULT '[]'::jsonb,
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_session_moods_user_id ON session_moods(user_id);

-- ============================================================================
-- MEMORY CLASSIFICATIONS
-- ============================================================================

CREATE TABLE memory_classifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    importance FLOAT NOT NULL,
    sentiment VARCHAR(50) NOT NULL,
    privacy_level VARCHAR(50) NOT NULL,
    temporal_relevance FLOAT NOT NULL,
    confidence FLOAT NOT NULL,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_memory_classifications_user_id ON memory_classifications(user_id);
CREATE INDEX idx_memory_classifications_importance ON memory_classifications(importance);
```

---

## APIs y Interfaces

### Client API (Python SDK)

```python
"""
luminoracore_sdk/client.py

API del cliente con nuevas features v1.1
"""

from typing import List, Optional, Dict
from .types import (
    Message,
    Episode,
    Fact,
    MemorySearchResult,
    AffinityInfo,
    SessionAnalytics
)

class LuminoraCoreClient:
    """Cliente mejorado v1.1"""
    
    def __init__(
        self,
        personality_config: Optional[PersonalityConfig] = None,
        memory_config: Optional[MemoryConfig] = None,
        relationship_config: Optional[RelationshipConfig] = None,
        **kwargs
    ):
        """
        Inicializa cliente
        
        Args:
            personality_config: Configuración de personalidades
            memory_config: Configuración de memoria
            relationship_config: Configuración de relaciones
        """
        pass
    
    # ========================================================================
    # CONVERSACIÓN (v1.0 + mejoras)
    # ========================================================================
    
    async def send_message(
        self,
        session_id: str,
        message: str,
        extract_facts: bool = True,  # NEW
        detect_episode: bool = True,  # NEW
        update_affinity: bool = True  # NEW
    ) -> Message:
        """
        Envía mensaje (mejorado con auto-extraction)
        
        Args:
            session_id: ID de sesión
            message: Mensaje del usuario
            extract_facts: Extraer facts automáticamente
            detect_episode: Detectar episodios automáticamente
            update_affinity: Actualizar afinidad automáticamente
        
        Returns:
            Respuesta de la personalidad
        """
        pass
    
    # ========================================================================
    # MEMORIA (NEW en v1.1)
    # ========================================================================
    
    async def search_memories(
        self,
        session_id: str,
        query: str,
        top_k: int = 10,
        include_episodes: bool = True,
        include_facts: bool = True,
        include_messages: bool = True
    ) -> List[MemorySearchResult]:
        """
        Búsqueda semántica en memoria
        
        Args:
            session_id: ID de sesión
            query: Consulta en lenguaje natural
            top_k: Número de resultados
            include_episodes: Incluir episodios
            include_facts: Incluir facts
            include_messages: Incluir mensajes
        
        Returns:
            Resultados ordenados por relevancia
        
        Example:
            >>> results = await client.search_memories(
            ...     session_id=sid,
            ...     query="cuando hablamos de mi perro"
            ... )
            >>> for result in results:
            ...     print(f"{result.type}: {result.content} (score: {result.score})")
        """
        pass
    
    async def get_episodes(
        self,
        session_id: str,
        min_importance: float = 5.0,
        limit: int = 20
    ) -> List[Episode]:
        """
        Obtiene episodios memorables
        
        Args:
            session_id: ID de sesión
            min_importance: Importancia mínima
            limit: Máximo de episodios
        
        Returns:
            Lista de episodios ordenados por importancia
        """
        pass
    
    async def get_facts(
        self,
        session_id: str,
        category: Optional[str] = None
    ) -> List[Fact]:
        """
        Obtiene facts del usuario
        
        Args:
            session_id: ID de sesión
            category: Filtrar por categoría
        
        Returns:
            Lista de facts
        """
        pass
    
    # ========================================================================
    # AFINIDAD (NEW en v1.1)
    # ========================================================================
    
    async def get_affinity(
        self,
        session_id: str
    ) -> AffinityInfo:
        """
        Obtiene información de afinidad
        
        Returns:
            AffinityInfo con puntos, nivel, etc.
        
        Example:
            >>> affinity = await client.get_affinity(session_id)
            >>> print(f"Level: {affinity.level} ({affinity.points}/100)")
            Level: friend (58/100)
        """
        pass
    
    async def update_affinity(
        self,
        session_id: str,
        event_type: str,
        custom_delta: Optional[int] = None
    ) -> AffinityInfo:
        """
        Actualiza afinidad manualmente
        
        Args:
            session_id: ID de sesión
            event_type: Tipo de evento (mention_preference, etc.)
            custom_delta: Delta personalizado (+/- puntos)
        
        Returns:
            AffinityInfo actualizado
        """
        pass
    
    # ========================================================================
    # ANALYTICS (NEW en v1.1)
    # ========================================================================
    
    async def get_session_analytics(
        self,
        session_id: str
    ) -> SessionAnalytics:
        """
        Obtiene analytics de la sesión
        
        Returns:
            SessionAnalytics con métricas
        
        Example:
            >>> analytics = await client.get_session_analytics(session_id)
            >>> print(f"Messages: {analytics.total_messages}")
            >>> print(f"Sentiment: {analytics.sentiment_distribution}")
            >>> print(f"Engagement: {analytics.engagement_score}/10")
        """
        pass
```

### Configuration Types

```python
"""
luminoracore_sdk/types/config.py

Configuraciones para v1.1
"""

from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class MemoryConfig:
    """Configuración de memoria"""
    
    # Memoria episódica
    enable_episodic_memory: bool = True
    episode_importance_threshold: float = 7.0
    episode_detection_frequency: int = 5  # Cada N mensajes
    max_episodes_per_session: int = 50
    
    # Búsqueda semántica
    enable_semantic_search: bool = True
    embedding_provider: str = "openai"  # openai, cohere, local
    vector_store: str = "pgvector"  # pgvector, pinecone, weaviate
    similarity_threshold: float = 0.75
    
    # Extracción de facts
    enable_fact_extraction: bool = True
    fact_confidence_threshold: float = 0.7
    fact_extraction_frequency: int = 1  # Cada N mensajes
    
    # Clasificación
    memory_classification: str = "automatic"  # automatic, manual
    
    # Storage
    storage_backend: str = "postgresql"
    storage_config: Optional[Dict] = None


@dataclass
class PersonalityConfig:
    """Configuración de personalidad"""
    
    # Personalidad base
    base_personality: str  # Ruta o nombre
    
    # Sistema jerárquico
    enable_hierarchical: bool = True
    relationship_levels: Optional[List[Dict]] = None  # Custom levels
    
    # Moods
    enable_moods: bool = True
    mood_modifiers: Optional[Dict] = None  # Custom moods
    mood_detection_frequency: int = 1  # Cada N mensajes
    
    # Adaptación
    enable_adaptation: bool = True
    adaptation_strength: float = 0.5  # 0-1, qué tan fuerte adaptar
    
    # Smoothing
    enable_smoothing: bool = True
    smoothing_factor: float = 0.3  # 0-1, qué tan suave transicionar


@dataclass
class RelationshipConfig:
    """Configuración de relaciones"""
    
    # Afinidad
    enable_affinity: bool = True
    affinity_rules: Optional[Dict[str, int]] = None  # event_type: delta
    affinity_decay_enabled: bool = True
    affinity_decay_rate: float = 1.0  # Puntos por día de inactividad
    
    # Eventos
    track_relationship_events: bool = True
    milestone_detection: bool = True
```

---

## Flujos de Datos

### Flujo de Envío de Mensaje

```
User sends message
       │
       ▼
┌─────────────────────────────────────────┐
│ 1. Pre-processing                       │
│    - Detect mood trigger                │
│    - Analyze sentiment                  │
│    - Extract context                    │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ 2. Memory Processing (Parallel)         │
│    ┌───────────────────────────────┐    │
│    │ a) Fact Extraction            │    │
│    │    - NLP extraction           │    │
│    │    - Store facts in DB        │    │
│    └───────────────────────────────┘    │
│    ┌───────────────────────────────┐    │
│    │ b) Semantic Indexing          │    │
│    │    - Create embedding         │    │
│    │    - Index in vector store    │    │
│    └───────────────────────────────┘    │
│    ┌───────────────────────────────┐    │
│    │ c) Classification             │    │
│    │    - Classify memory          │    │
│    │    - Store classification     │    │
│    └───────────────────────────────┘    │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ 3. Retrieve Relevant Context            │
│    - Semantic search for relevant       │
│      memories                           │
│    - Get recent messages                │
│    - Get user facts                     │
│    - Get relevant episodes              │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ 4. Compile Personality                  │
│    - Get current affinity               │
│    - Detect/update mood                 │
│    - Get relationship level             │
│    - Apply modifiers                    │
│    - Compile final personality          │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ 5. Generate Response (LLM)              │
│    - Build enhanced prompt with:        │
│      * Compiled personality             │
│      * Retrieved context                │
│      * User message                     │
│    - Call LLM provider                  │
│    - Get response                       │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│ 6. Post-processing                      │
│    ┌───────────────────────────────┐    │
│    │ a) Update Affinity            │    │
│    │    - Analyze interaction      │    │
│    │    - Apply affinity rules     │    │
│    │    - Update DB                │    │
│    └───────────────────────────────┘    │
│    ┌───────────────────────────────┐    │
│    │ b) Episode Detection          │    │
│    │    - Check if episode worthy  │    │
│    │    - Create episode if yes    │    │
│    │    - Store in DB              │    │
│    └───────────────────────────────┘    │
│    ┌───────────────────────────────┐    │
│    │ c) Index Response             │    │
│    │    - Create embedding         │    │
│    │    - Index in vector store    │    │
│    └───────────────────────────────┘    │
└────────────┬────────────────────────────┘
             │
             ▼
     Return response to user
```

---

## Integración con v1.0

### Backward Compatibility

```python
"""
Garantizar compatibilidad con código v1.0 existente
"""

# v1.0 code sigue funcionando
client = LuminoraCoreClient()  # Sin configs nuevos
session_id = await client.create_session(...)
response = await client.send_message(session_id, "Hello")

# Pero features v1.1 están deshabilitados por defecto
# Para habilitar, usar configs explícitos:

client = LuminoraCoreClient(
    memory_config=MemoryConfig(
        enable_episodic_memory=True,  # Opt-in
        enable_semantic_search=True,
        enable_fact_extraction=True
    ),
    personality_config=PersonalityConfig(
        enable_hierarchical=True,  # Opt-in
        enable_moods=True
    )
)
```

### Migration Path

```python
"""
Path de migración de v1.0 a v1.1
"""

# 1. Instalar v1.1
pip install luminoracore-sdk==1.1.0

# 2. Migrar base de datos
luminora-cli migrate --from 1.0 --to 1.1

# 3. Actualizar código gradualmente
# Paso 1: Habilitar solo memoria episódica
client = LuminoraCoreClient(
    memory_config=MemoryConfig(enable_episodic_memory=True)
)

# Paso 2: Agregar búsqueda semántica
client = LuminoraCoreClient(
    memory_config=MemoryConfig(
        enable_episodic_memory=True,
        enable_semantic_search=True
    )
)

# Paso 3: Full v1.1
client = LuminoraCoreClient(
    memory_config=MemoryConfig(enable_all=True),
    personality_config=PersonalityConfig(enable_all=True),
    relationship_config=RelationshipConfig(enable_affinity=True)
)
```

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

