# Sistema de Memoria Avanzado - LuminoraCore v1.1

**Diseño completo del sistema de memoria episódica, clasificación inteligente y recuperación contextual**

---

## ⚠️ NOTA IMPORTANTE

Este documento describe el **sistema de memoria** de LuminoraCore v1.1.

**Modelo Conceptual (Templates/Instances/Snapshots):**
- **Templates (JSON)** definen qué memoria está habilitada (configuración)
- **Instances (BBDD)** guardan los datos reales (facts, episodios, mensajes)
- **Snapshots (JSON)** exportan todo el estado incluyendo memoria

**Ver:** [MODELO_CONCEPTUAL_REVISADO.md](./MODELO_CONCEPTUAL_REVISADO.md) para entender cómo se integra la memoria con el modelo completo.

**Datos de Memoria:**
- ✅ Facts → Se guardan en **BBDD** (NO en JSON Template)
- ✅ Episodios → Se guardan en **BBDD** (NO en JSON Template)
- ✅ Embeddings → Se guardan en **Vector Store** (NO en JSON Template)
- ✅ El JSON Template solo define **configuración** de memoria (qué features están habilitadas)

---

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Arquitectura de Memoria](#arquitectura-de-memoria)
3. [Tipos de Memoria](#tipos-de-memoria)
4. [Memoria Episódica](#memoria-episódica)
5. [Búsqueda Semántica (Vector Search)](#búsqueda-semántica)
6. [Clasificación Inteligente](#clasificación-inteligente)
7. [Extracción Automática de Facts](#extracción-automática-de-facts)
8. [Almacenamiento a Largo Plazo](#almacenamiento-a-largo-plazo)
9. [Recuperación Contextual](#recuperación-contextual)
10. [Optimización y Performance](#optimización-y-performance)

---

## Visión General

### 🎯 Objetivo

**Crear un sistema de memoria que permita a las personalidades recordar conversaciones de forma humana:**
- Recordar momentos importantes (memoria episódica)
- Buscar por significado, no solo palabras exactas (vector search)
- Clasificar automáticamente información (facts, episodios, eventos)
- Recuperar contexto relevante automáticamente

### ❌ Problemas Actuales (v1.0)

```python
# v1.0 - Memoria básica
await client.store_memory(session_id, "favorite_anime", "Naruto")  # Manual
await client.get_memory(session_id, "favorite_anime")  # Solo key-value

# Problemas:
# 1. ❌ Extracción manual de facts
# 2. ❌ No diferencia información importante de trivial
# 3. ❌ No puede buscar "recuerdas cuando hablamos de mi perro?"
# 4. ❌ No guarda "momentos especiales" automáticamente
# 5. ❌ Almacenamiento sin priorización
```

### ✅ Solución Propuesta (v1.1)

```python
# v1.1 - Memoria inteligente
client = LuminoraCoreClient(
    memory_config=MemoryConfig(
        enable_episodic_memory=True,       # ← Episodios automáticos
        enable_fact_extraction=True,        # ← Extracción automática
        enable_semantic_search=True,        # ← Búsqueda por significado
        memory_classification="automatic"   # ← Clasificación IA
    )
)

# Todo es automático
response = await client.send_message(
    session_id,
    "Mi perro Max murió ayer, estoy destrozado"
)

# Sistema automáticamente:
# 1. ✅ Extrae facts: pet_name="Max", pet_status="deceased"
# 2. ✅ Detecta importancia: 9/10 (momento emocional crítico)
# 3. ✅ Crea episodio: tipo="loss", tags=["sad", "pet", "grief"]
# 4. ✅ Genera embedding para búsqueda semántica
# 5. ✅ Almacena con prioridad alta
```

---

## Arquitectura de Memoria

### 🏗️ Capas del Sistema

```
┌────────────────────────────────────────────────────────────┐
│                    CONVERSACIÓN (LLM)                      │
│  "Recuerdas cuando hablamos de mi perro?"                  │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│              CAPA DE RECUPERACIÓN INTELIGENTE              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Vector Search│  │ Episodic     │  │ Fact Retrieval  │  │
│  │ (Semántica)  │  │ Memory Query │  │ (Key-Value)     │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│            CAPA DE CLASIFICACIÓN Y PROCESAMIENTO           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Importance   │  │ Category     │  │ Sentiment       │  │
│  │ Scoring      │  │ Classification│  │ Analysis        │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│                 CAPA DE EXTRACCIÓN                         │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Fact         │  │ Episode      │  │ Entity          │  │
│  │ Extraction   │  │ Detection    │  │ Recognition     │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│                CAPA DE ALMACENAMIENTO                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Short-term Memory (Redis)          │ Rolling window  │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ Long-term Memory (PostgreSQL)      │ Facts + Episodes│  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ Vector Store (Pinecone/pgvector)   │ Embeddings     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

---

## Tipos de Memoria

### 1. **Memoria de Corto Plazo (Working Memory)**

**Duración:** Sesión actual (hasta cierre)  
**Storage:** Redis / Memory  
**Contenido:** Últimos N mensajes de la conversación

```python
# Configuración
working_memory_config = {
    "max_messages": 50,              # Últimos 50 mensajes
    "max_tokens": 4000,              # O 4000 tokens (lo que ocurra primero)
    "compression": "automatic",      # Comprimir automáticamente si excede
    "backend": "redis"               # Redis para velocidad
}
```

**Uso:**
- Contexto inmediato de conversación
- Referencia a mensajes recientes
- No requiere búsqueda, está siempre disponible

---

### 2. **Memoria Semántica (Facts)**

**Duración:** Permanente (hasta que se actualice)  
**Storage:** PostgreSQL / MongoDB  
**Contenido:** Información factual sobre el usuario

```python
# Estructura de un Fact
{
    "id": "fact_123",
    "user_id": "user_456",
    "session_id": "session_789",
    "category": "personal_info",        # personal_info, preferences, relationships, etc.
    "key": "favorite_anime",
    "value": "Naruto",
    "confidence": 0.95,                 # Qué tan seguro está el sistema
    "source_message_id": "msg_555",
    "first_mentioned": "2025-10-14T10:30:00Z",
    "last_updated": "2025-10-14T10:30:00Z",
    "mention_count": 1,
    "tags": ["anime", "entertainment", "preference"],
    "context": "Usuario mencionó que le encanta Naruto"
}
```

**Categorías de Facts:**
- `personal_info`: Nombre, edad, profesión, ubicación
- `preferences`: Gustos, disgustos, favoritos
- `relationships`: Familia, amigos, parejas, mascotas
- `hobbies`: Actividades, intereses
- `goals`: Objetivos, aspiraciones
- `health`: Salud física, mental
- `work`: Trabajo, estudios, carrera
- `events`: Eventos importantes ya ocurridos

**Extracción Automática:**
```python
# Input: "Soy Diego, tengo 28 años y trabajo en IT. Me encanta Naruto."

# Output automático:
facts_extracted = [
    {
        "category": "personal_info",
        "key": "name",
        "value": "Diego",
        "confidence": 0.99
    },
    {
        "category": "personal_info",
        "key": "age",
        "value": 28,
        "confidence": 0.99
    },
    {
        "category": "work",
        "key": "profession",
        "value": "IT",
        "confidence": 0.95
    },
    {
        "category": "preferences",
        "key": "favorite_anime",
        "value": "Naruto",
        "confidence": 0.90
    }
]
```

---

### 3. **Memoria Episódica (Episodes)**

**Duración:** Permanente  
**Storage:** PostgreSQL / MongoDB  
**Contenido:** Momentos importantes de la relación

```python
# Estructura de un Episodio
{
    "id": "episode_123",
    "user_id": "user_456",
    "session_id": "session_789",
    "type": "emotional_moment",      # emotional_moment, milestone, confession, conflict, achievement
    "title": "Pérdida de mascota Max",
    "summary": "Usuario compartió la triste noticia de que su perro Max falleció ayer. Está muy afectado emocionalmente.",
    "importance": 9.5,               # 0-10 (10 = más importante)
    "sentiment": "very_sad",         # very_happy, happy, neutral, sad, very_sad, angry
    "tags": ["sad", "loss", "pet", "grief", "max"],
    "participants": ["user_456", "personality_alicia"],
    "context_messages": [            # Mensajes que forman el episodio
        "msg_100",
        "msg_101",
        "msg_102"
    ],
    "timestamp": "2025-10-14T10:30:00Z",
    "temporal_decay": 1.0,          # Empieza en 1.0, decae con tiempo
    "related_facts": ["fact_pet_max", "fact_pet_status"],
    "related_episodes": [],
    "embedding": [0.234, -0.567, ...] # Para búsqueda semántica
}
```

**Tipos de Episodios:**

| Tipo | Descripción | Importancia Base | Ejemplos |
|------|-------------|------------------|----------|
| `emotional_moment` | Momentos de alta carga emocional | 7-10 | Pérdidas, rupturas, confesiones |
| `milestone` | Hitos en la relación | 6-9 | Primera conversación, aniversarios |
| `confession` | Usuario comparte algo personal | 6-8 | Secretos, miedos, sueños |
| `conflict` | Desacuerdos o tensiones | 5-7 | Discusiones, malentendidos |
| `achievement` | Logros del usuario | 5-8 | Promoción, graduación, éxito |
| `bonding` | Momentos de conexión especial | 6-8 | Risas compartidas, apoyo mutuo |
| `routine` | Conversaciones cotidianas | 1-3 | Saludos, clima, small talk |

**Detección Automática:**
```python
# Sistema analiza cada N mensajes (ej. cada 5 mensajes)
def detect_episode(messages: List[Message]) -> Optional[Episode]:
    # 1. Análisis de sentimiento
    sentiment_score = analyze_sentiment(messages)
    
    # 2. Análisis de importancia
    importance = score_importance(messages, sentiment_score)
    
    # 3. Si importancia > threshold, crear episodio
    if importance >= 7.0:
        episode_type = classify_episode_type(messages, sentiment_score)
        summary = generate_summary(messages)
        tags = extract_tags(messages)
        
        return Episode(
            type=episode_type,
            summary=summary,
            importance=importance,
            sentiment=sentiment_score,
            tags=tags,
            context_messages=messages
        )
    
    return None
```

---

### 4. **Memoria de Vector (Semantic Memory)**

**Duración:** Permanente  
**Storage:** Pinecone / Weaviate / PostgreSQL pgvector  
**Contenido:** Embeddings de mensajes para búsqueda semántica

```python
# Cada mensaje se convierte en vector
{
    "id": "vec_msg_123",
    "message_id": "msg_123",
    "user_id": "user_456",
    "session_id": "session_789",
    "content": "Mi perro Max murió ayer",
    "embedding": [0.234, -0.567, 0.123, ...],  # 1536 dimensiones (OpenAI)
    "metadata": {
        "timestamp": "2025-10-14T10:30:00Z",
        "speaker": "user",
        "sentiment": "very_sad",
        "importance": 9.5,
        "tags": ["pet", "loss", "sad"]
    }
}
```

**Búsqueda Semántica:**
```python
# Query: "Recuerdas cuando hablamos de mi perro?"
query_embedding = create_embedding("Recuerdas cuando hablamos de mi perro?")

# Búsqueda por similitud coseno
results = vector_store.query(
    vector=query_embedding,
    top_k=5,
    filter={"user_id": "user_456"}
)

# Resultados similares semánticamente:
# 1. "Mi perro Max murió ayer" (similitud: 0.92)
# 2. "Max era mi mejor amigo" (similitud: 0.87)
# 3. "Extraño mucho a mi perrito" (similitud: 0.84)
```

---

## Memoria Episódica

### 🎯 Concepto

**Inspirado en memoria humana:**  
Los humanos no recordamos cada conversación palabra por palabra, pero sí recordamos **momentos especiales**.

**Ejemplos:**
- "Recuerdo cuando me contaste que tu perro murió"
- "Aquella vez que te sentiste tan feliz por tu promoción"
- "Cuando me confesaste tus miedos sobre tu relación"

### 🏗️ Implementación

```python
# luminoracore/core/memory/episodic.py

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import numpy as np

@dataclass
class Episode:
    """Representa un episodio memorable en la conversación"""
    
    id: str
    user_id: str
    session_id: str
    type: str  # emotional_moment, milestone, confession, etc.
    title: str
    summary: str
    importance: float  # 0-10
    sentiment: str
    tags: List[str]
    context_messages: List[str]  # IDs de mensajes
    timestamp: datetime
    temporal_decay: float = 1.0
    related_facts: List[str] = None
    related_episodes: List[str] = None
    embedding: np.ndarray = None
    
    def get_current_importance(self) -> float:
        """Importancia actual considerando decay temporal"""
        return self.importance * self.temporal_decay
    
    def update_decay(self, days_passed: int):
        """Actualiza decay temporal (memories fade over time)"""
        # Decay logarítmico: eventos recientes decaen lento
        decay_rate = 0.1
        self.temporal_decay = 1.0 / (1.0 + decay_rate * np.log(days_passed + 1))


class EpisodicMemoryManager:
    """Gestiona memoria episódica"""
    
    def __init__(
        self,
        storage_backend,
        llm_provider,
        importance_threshold: float = 7.0,
        max_episodes_per_session: int = 50
    ):
        self.storage = storage_backend
        self.llm = llm_provider
        self.importance_threshold = importance_threshold
        self.max_episodes = max_episodes_per_session
    
    async def detect_episode(
        self,
        messages: List[Message],
        context: dict
    ) -> Optional[Episode]:
        """
        Detecta si los mensajes recientes forman un episodio memorable
        
        Args:
            messages: Últimos 3-10 mensajes
            context: Contexto adicional (afinidad, mood, etc.)
        
        Returns:
            Episode si se detecta, None si no
        """
        # 1. Análisis de sentimiento
        sentiment_analysis = await self._analyze_sentiment(messages)
        
        # 2. Scoring de importancia
        importance = await self._score_importance(
            messages,
            sentiment_analysis,
            context
        )
        
        # 3. Si no alcanza threshold, no crear episodio
        if importance < self.importance_threshold:
            return None
        
        # 4. Clasificar tipo de episodio
        episode_type = await self._classify_episode_type(
            messages,
            sentiment_analysis
        )
        
        # 5. Generar resumen
        summary = await self._generate_summary(messages)
        
        # 6. Extraer tags
        tags = await self._extract_tags(messages, sentiment_analysis)
        
        # 7. Crear embedding
        embedding = await self._create_embedding(summary)
        
        # 8. Crear episodio
        episode = Episode(
            id=generate_id("episode"),
            user_id=context["user_id"],
            session_id=context["session_id"],
            type=episode_type,
            title=self._generate_title(episode_type, summary),
            summary=summary,
            importance=importance,
            sentiment=sentiment_analysis["primary_emotion"],
            tags=tags,
            context_messages=[msg.id for msg in messages],
            timestamp=datetime.utcnow(),
            embedding=embedding
        )
        
        return episode
    
    async def _score_importance(
        self,
        messages: List[Message],
        sentiment: dict,
        context: dict
    ) -> float:
        """
        Calcula importancia del episodio (0-10)
        
        Factores:
        - Intensidad emocional (40%)
        - Revelación personal (30%)
        - Impacto en relación (20%)
        - Singularidad del tema (10%)
        """
        # Usar LLM para scoring
        prompt = f"""
        Analiza la importancia de esta conversación en una escala de 0-10.
        
        Conversación:
        {format_messages(messages)}
        
        Factores a considerar:
        - Intensidad emocional: {sentiment['intensity']}
        - Emoción principal: {sentiment['primary_emotion']}
        - Contexto: Nivel de afinidad {context.get('affinity', 0)}/100
        
        Responde con JSON:
        {{
            "importance_score": 0-10,
            "reasoning": "explicación breve",
            "key_factors": ["factor1", "factor2"]
        }}
        """
        
        result = await self.llm.complete(
            prompt,
            response_format="json_object"
        )
        
        return result["importance_score"]
    
    async def retrieve_relevant_episodes(
        self,
        query: str,
        user_id: str,
        top_k: int = 5,
        min_importance: float = 5.0
    ) -> List[Episode]:
        """
        Recupera episodios relevantes para una query
        
        Args:
            query: Consulta del usuario (ej. "cuando hablamos de mi perro")
            user_id: ID del usuario
            top_k: Cuántos episodios retornar
            min_importance: Importancia mínima a considerar
        
        Returns:
            Lista de episodios relevantes ordenados por relevancia
        """
        # 1. Crear embedding de la query
        query_embedding = await self._create_embedding(query)
        
        # 2. Buscar episodios similares
        similar_episodes = await self.storage.vector_search(
            collection="episodes",
            vector=query_embedding,
            filter={
                "user_id": user_id,
                "current_importance": {"$gte": min_importance}
            },
            top_k=top_k * 2  # Obtener más para re-ranking
        )
        
        # 3. Re-ranking considerando temporal decay
        current_time = datetime.utcnow()
        for episode in similar_episodes:
            days_passed = (current_time - episode.timestamp).days
            episode.update_decay(days_passed)
        
        # 4. Ordenar por importancia actual
        sorted_episodes = sorted(
            similar_episodes,
            key=lambda e: e.get_current_importance(),
            reverse=True
        )
        
        return sorted_episodes[:top_k]
```

### 📊 Ejemplo de Uso

```python
# Configuración
client = LuminoraCoreClient(
    memory_config=MemoryConfig(
        enable_episodic_memory=True,
        episode_importance_threshold=7.0,
        episode_detection_frequency=5  # Cada 5 mensajes
    )
)

# Conversación
session_id = await client.create_session(...)

# Mensaje 1
await client.send_message(session_id, "Hola, ¿cómo estás?")
# → No se detecta episodio (rutina)

# Mensaje 2-6 (conversación emocional)
await client.send_message(session_id, "Tengo que contarte algo triste")
await client.send_message(session_id, "Mi perro Max murió ayer")
await client.send_message(session_id, "Estoy destrozado, era mi mejor amigo")
await client.send_message(session_id, "No sé cómo superarlo")
# → Sistema detecta episodio de importancia 9.5/10

# Weeks later...
await client.send_message(session_id, "Recuerdas cuando te hablé de Max?")

# Sistema automáticamente:
# 1. Busca episodios semánticamente similares
# 2. Encuentra episodio "Pérdida de mascota Max"
# 3. Lo incluye en contexto del LLM
# 4. LLM puede referirse específicamente al episodio

# Respuesta: "Claro que sí, recuerdo cuando me contaste de Max hace 2 semanas.
#             Sé que era muy importante para ti. ¿Cómo te sientes ahora?"
```

---

## Búsqueda Semántica

### 🔍 Vector Search

**Problema:** Búsqueda exacta no funciona para memoria conversacional

```python
# ❌ Búsqueda exacta
user: "cuando hablamos de mi perro"
system.search("perro")  # Solo encuentra mensajes con palabra "perro"

user: "aquella vez que te conté de mi mascota"
system.search("mascota")  # No encuentra nada si dijiste "perro" antes
```

**Solución:** Búsqueda semántica por embeddings

```python
# ✅ Búsqueda semántica
user: "cuando hablamos de mi perro"
embedding = create_embedding("cuando hablamos de mi perro")
results = vector_search(embedding)
# → Encuentra: "mi perro Max", "mi mascota", "mi perrito", etc.

user: "aquella vez que te conté de mi mascota"
embedding = create_embedding("aquella vez que te conté de mi mascota")
results = vector_search(embedding)
# → Encuentra conversaciones sobre perros, gatos, pets en general
```

### 🏗️ Implementación

```python
# luminoracore/core/memory/semantic.py

from typing import List, Optional
import numpy as np

class SemanticMemoryManager:
    """Gestiona búsqueda semántica en memoria"""
    
    def __init__(
        self,
        embedding_provider: str = "openai",  # openai, cohere, sentence-transformers
        vector_store: str = "pgvector",      # pgvector, pinecone, weaviate
        embedding_model: str = "text-embedding-3-small",
        similarity_threshold: float = 0.75
    ):
        self.embedding_provider = self._init_embedding_provider(
            embedding_provider,
            embedding_model
        )
        self.vector_store = self._init_vector_store(vector_store)
        self.similarity_threshold = similarity_threshold
    
    async def index_message(
        self,
        message: Message,
        metadata: dict
    ) -> str:
        """
        Indexa un mensaje para búsqueda semántica
        
        Args:
            message: Mensaje a indexar
            metadata: Metadata adicional (timestamp, speaker, sentiment, etc.)
        
        Returns:
            ID del vector indexado
        """
        # 1. Crear embedding
        embedding = await self.embedding_provider.create_embedding(
            message.content
        )
        
        # 2. Preparar metadata
        full_metadata = {
            "message_id": message.id,
            "user_id": message.user_id,
            "session_id": message.session_id,
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
            "speaker": message.speaker,
            **metadata
        }
        
        # 3. Indexar en vector store
        vector_id = await self.vector_store.upsert(
            id=f"vec_{message.id}",
            vector=embedding,
            metadata=full_metadata
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
        Busca mensajes semánticamente similares
        
        Args:
            query: Consulta en lenguaje natural
            user_id: ID del usuario
            top_k: Número de resultados
            filter: Filtros adicionales (tiempo, tags, etc.)
        
        Returns:
            Lista de mensajes ordenados por relevancia
        """
        # 1. Crear embedding de la query
        query_embedding = await self.embedding_provider.create_embedding(query)
        
        # 2. Preparar filtros
        search_filter = {"user_id": user_id}
        if filter:
            search_filter.update(filter)
        
        # 3. Búsqueda vectorial
        results = await self.vector_store.query(
            vector=query_embedding,
            top_k=top_k,
            filter=search_filter,
            include_metadata=True
        )
        
        # 4. Filtrar por threshold de similitud
        filtered_results = [
            r for r in results
            if r["score"] >= self.similarity_threshold
        ]
        
        return filtered_results
    
    async def search_with_temporal_boost(
        self,
        query: str,
        user_id: str,
        top_k: int = 10,
        recency_weight: float = 0.3
    ) -> List[dict]:
        """
        Búsqueda semántica con boost por recencia
        
        Mensajes recientes tienen score boost
        """
        results = await self.search(query, user_id, top_k * 2)
        
        current_time = datetime.utcnow()
        
        for result in results:
            # Calcular recencia (0-1, más reciente = mayor)
            timestamp = datetime.fromisoformat(result["metadata"]["timestamp"])
            days_ago = (current_time - timestamp).days
            recency_score = 1.0 / (1.0 + 0.1 * days_ago)
            
            # Combinar similarity + recency
            original_score = result["score"]
            boosted_score = (
                (1 - recency_weight) * original_score +
                recency_weight * recency_score
            )
            result["score"] = boosted_score
        
        # Re-ordenar por score boosted
        sorted_results = sorted(
            results,
            key=lambda r: r["score"],
            reverse=True
        )
        
        return sorted_results[:top_k]
```

### 🎯 Ejemplo de Uso

```python
# Indexar mensajes automáticamente
@client.on_message
async def on_new_message(message: Message):
    # Automático en v1.1
    await semantic_memory.index_message(
        message,
        metadata={
            "sentiment": analyze_sentiment(message),
            "tags": extract_tags(message),
            "importance": score_importance(message)
        }
    )

# Búsqueda semántica
results = await client.search_memories(
    session_id=session_id,
    query="cuando hablamos de mi perro",
    top_k=5
)

# Resultados:
# [
#   {
#     "content": "Mi perro Max murió ayer",
#     "score": 0.92,
#     "timestamp": "2025-10-01T10:30:00Z"
#   },
#   {
#     "content": "Max era un golden retriever de 10 años",
#     "score": 0.88,
#     "timestamp": "2025-10-01T10:35:00Z"
#   },
#   ...
# ]
```

---

## Clasificación Inteligente

### 📊 Sistema de Clasificación Multi-dimensional

**Cada memoria se clasifica en:**

1. **Categoría** (qué tipo de información)
2. **Importancia** (qué tan relevante)
3. **Sentimiento** (qué emoción)
4. **Temporalidad** (cuándo ocurrió / validez temporal)
5. **Privacidad** (qué tan sensible)

```python
# luminoracore/core/memory/classifier.py

from enum import Enum
from dataclasses import dataclass

class MemoryCategory(Enum):
    PERSONAL_INFO = "personal_info"      # Nombre, edad, profesión
    PREFERENCES = "preferences"          # Gustos, disgustos
    RELATIONSHIPS = "relationships"      # Familia, amigos, pareja
    HOBBIES = "hobbies"                 # Actividades, intereses
    GOALS = "goals"                     # Objetivos, aspiraciones
    HEALTH = "health"                   # Salud física, mental
    WORK = "work"                       # Trabajo, estudios
    EVENTS = "events"                   # Eventos pasados
    ROUTINE = "routine"                 # Hábitos, rutinas
    OTHER = "other"

class ImportanceLevel(Enum):
    CRITICAL = 9-10      # Eventos life-changing
    HIGH = 7-8           # Muy importante
    MEDIUM = 5-6         # Moderadamente importante
    LOW = 3-4            # Poco importante
    TRIVIAL = 0-2        # Irrelevante

class SentimentLevel(Enum):
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"

class PrivacyLevel(Enum):
    PUBLIC = "public"            # Info pública
    PRIVATE = "private"          # Info personal no sensible
    SENSITIVE = "sensitive"      # Info sensible (salud, finanzas)
    CONFIDENTIAL = "confidential"  # Info muy privada (secretos)

@dataclass
class MemoryClassification:
    category: MemoryCategory
    importance: float  # 0-10
    sentiment: SentimentLevel
    privacy: PrivacyLevel
    temporal_relevance: float  # 0-1 (1 = siempre relevante, 0 = ya no relevante)
    confidence: float  # 0-1 (confianza en la clasificación)
    tags: List[str]


class MemoryClassifier:
    """Clasifica memories automáticamente usando LLM"""
    
    def __init__(self, llm_provider):
        self.llm = llm_provider
    
    async def classify(
        self,
        content: str,
        context: Optional[dict] = None
    ) -> MemoryClassification:
        """
        Clasifica un contenido de memoria
        
        Args:
            content: Texto a clasificar
            context: Contexto adicional
        
        Returns:
            MemoryClassification con todos los atributos
        """
        prompt = f"""
        Clasifica la siguiente información de memoria del usuario.
        
        Contenido: "{content}"
        {f"Contexto: {context}" if context else ""}
        
        Responde con JSON:
        {{
            "category": "personal_info | preferences | relationships | hobbies | goals | health | work | events | routine | other",
            "importance": 0-10,
            "importance_reasoning": "explicación breve",
            "sentiment": "very_positive | positive | neutral | negative | very_negative",
            "privacy": "public | private | sensitive | confidential",
            "temporal_relevance": 0-1,
            "tags": ["tag1", "tag2", "tag3"],
            "confidence": 0-1
        }}
        
        Criterios de importancia:
        - 9-10: Eventos life-changing (muerte, nacimiento, matrimonio, divorcio)
        - 7-8: Muy importante (cambio de trabajo, mudanza, enfermedad seria)
        - 5-6: Moderadamente importante (nueva relación, hobby nuevo)
        - 3-4: Poco importante (preferencia de comida, opinión)
        - 0-2: Trivial (clima, saludo)
        
        Criterios de privacidad:
        - Confidential: Secretos, traumas, info financiera sensible
        - Sensitive: Salud mental, problemas personales
        - Private: Info personal normal (edad, trabajo, gustos)
        - Public: Info que el usuario compartiría públicamente
        
        Temporal relevance:
        - 1.0: Siempre relevante (nombre, profesión, valores)
        - 0.7: Relevante por años (trabajo actual, relación actual)
        - 0.5: Relevante por meses (proyecto actual, meta a corto plazo)
        - 0.3: Relevante por semanas (mood temporal, evento próximo)
        - 0.0: Ya no relevante (evento pasado único, mood pasajero)
        """
        
        result = await self.llm.complete(
            prompt,
            response_format="json_object",
            temperature=0.1  # Baja temperatura para consistencia
        )
        
        return MemoryClassification(
            category=MemoryCategory(result["category"]),
            importance=result["importance"],
            sentiment=SentimentLevel(result["sentiment"]),
            privacy=PrivacyLevel(result["privacy"]),
            temporal_relevance=result["temporal_relevance"],
            confidence=result["confidence"],
            tags=result["tags"]
        )
```

### 🎯 Uso de Clasificación

```python
# Automático al guardar memoria
async def store_memory_with_classification(
    content: str,
    user_id: str,
    session_id: str
):
    # 1. Clasificar
    classification = await classifier.classify(content)
    
    # 2. Decidir storage strategy según clasificación
    if classification.importance >= 7.0:
        # Alta importancia → crear episodio
        episode = await episodic_memory.create_episode(content, classification)
    
    if classification.category == MemoryCategory.PERSONAL_INFO:
        # Info personal → extraer facts
        facts = await fact_extractor.extract(content)
        await storage.save_facts(facts)
    
    # 3. Indexar para búsqueda semántica
    await semantic_memory.index(
        content,
        metadata={
            "category": classification.category.value,
            "importance": classification.importance,
            "sentiment": classification.sentiment.value,
            "privacy": classification.privacy.value,
            "tags": classification.tags
        }
    )
    
    # 4. Guardar clasificación
    await storage.save_classification(content, classification)
```

---

## Extracción Automática de Facts

### 🤖 NLP-Based Fact Extraction

```python
# luminoracore/core/memory/fact_extractor.py

class FactExtractor:
    """Extrae facts automáticamente de conversaciones"""
    
    def __init__(self, llm_provider, confidence_threshold: float = 0.7):
        self.llm = llm_provider
        self.confidence_threshold = confidence_threshold
    
    async def extract_from_message(
        self,
        message: str,
        context: Optional[List[Message]] = None
    ) -> List[Fact]:
        """
        Extrae facts de un mensaje
        
        Args:
            message: Mensaje del usuario
            context: Mensajes anteriores para contexto
        
        Returns:
            Lista de facts extraídos
        """
        context_str = ""
        if context:
            context_str = "\n".join([f"{m.speaker}: {m.content}" for m in context[-5:]])
        
        prompt = f"""
        Extrae información factual sobre el usuario del siguiente mensaje.
        
        {f"Contexto previo:\n{context_str}\n" if context else ""}
        
        Mensaje del usuario: "{message}"
        
        Responde con JSON:
        {{
            "facts": [
                {{
                    "category": "personal_info | preferences | relationships | hobbies | goals | health | work",
                    "key": "nombre_descriptivo_del_fact",
                    "value": "valor_extraído",
                    "confidence": 0-1,
                    "reasoning": "por qué extraíste este fact"
                }}
            ]
        }}
        
        Reglas:
        - Solo extrae facts EXPLÍCITOS, no infieras
        - Confidence alto (>0.9) solo si es statement directo
        - Key debe ser descriptivo (ej. "favorite_anime", "pet_name", "age")
        - Si no hay facts, retorna array vacío
        
        Ejemplos:
        
        Input: "Soy Diego, tengo 28 años y trabajo en IT"
        Output:
        {{
            "facts": [
                {{"category": "personal_info", "key": "name", "value": "Diego", "confidence": 0.99, "reasoning": "Usuario declaró su nombre directamente"}},
                {{"category": "personal_info", "key": "age", "value": 28, "confidence": 0.99, "reasoning": "Usuario declaró su edad directamente"}},
                {{"category": "work", "key": "profession", "value": "IT", "confidence": 0.95, "reasoning": "Usuario declaró su profesión"}}
            ]
        }}
        
        Input: "Me encanta Naruto"
        Output:
        {{
            "facts": [
                {{"category": "preferences", "key": "favorite_anime", "value": "Naruto", "confidence": 0.90, "reasoning": "Usuario expresó fuerte preferencia"}}
            ]
        }}
        
        Input: "Hace calor hoy"
        Output:
        {{
            "facts": []
        }}
        """
        
        result = await self.llm.complete(
            prompt,
            response_format="json_object",
            temperature=0.1
        )
        
        # Filtrar por confidence threshold
        facts = [
            Fact(**f)
            for f in result["facts"]
            if f["confidence"] >= self.confidence_threshold
        ]
        
        return facts
    
    async def extract_from_conversation(
        self,
        messages: List[Message],
        batch_size: int = 10
    ) -> List[Fact]:
        """
        Extrae facts de una conversación completa
        
        Procesa en batches para no exceder context window
        """
        all_facts = []
        
        for i in range(0, len(messages), batch_size):
            batch = messages[i:i+batch_size]
            batch_text = "\n".join([f"{m.speaker}: {m.content}" for m in batch])
            
            facts = await self.extract_from_message(
                batch_text,
                context=messages[max(0, i-5):i] if i > 0 else None
            )
            
            all_facts.extend(facts)
        
        # Deduplicar facts
        deduplicated = self._deduplicate_facts(all_facts)
        
        return deduplicated
    
    def _deduplicate_facts(self, facts: List[Fact]) -> List[Fact]:
        """
        Elimina facts duplicados, manteniendo el de mayor confidence
        """
        facts_by_key = {}
        
        for fact in facts:
            key = f"{fact.category}:{fact.key}"
            
            if key not in facts_by_key or fact.confidence > facts_by_key[key].confidence:
                facts_by_key[key] = fact
        
        return list(facts_by_key.values())
```

### 🎯 Ejemplo de Uso

```python
# Habilitado por defecto en v1.1
client = LuminoraCoreClient(
    memory_config=MemoryConfig(
        enable_fact_extraction=True,
        fact_confidence_threshold=0.7
    )
)

# El usuario habla
response = await client.send_message(
    session_id,
    "Hola! Soy Diego, tengo 28 años. Trabajo en IT y me encanta Naruto. Tengo un perro llamado Max."
)

# Sistema automáticamente extrae:
# Facts:
# 1. {category: "personal_info", key: "name", value: "Diego", confidence: 0.99}
# 2. {category: "personal_info", key: "age", value: 28, confidence: 0.99}
# 3. {category: "work", key: "profession", value: "IT", confidence: 0.95}
# 4. {category: "preferences", key: "favorite_anime", value: "Naruto", confidence: 0.90}
# 5. {category: "relationships", key: "pet_name", value: "Max", confidence: 0.95}
# 6. {category: "relationships", key: "pet_type", value: "dog", confidence: 0.95}

# Guardar facts
await storage.save_facts(facts, user_id, session_id)

# Luego, en conversación futura:
response = await client.send_message(
    session_id,
    "¿Cómo está tu perro?"
)

# Sistema automáticamente:
# 1. Recupera fact: pet_name = "Max"
# 2. Inyecta en contexto: "El usuario tiene un perro llamado Max"
# 3. LLM responde: "¿Cómo está Max? 🐶"
```

---

**(Continúa en siguiente mensaje debido a límite de longitud...)**


