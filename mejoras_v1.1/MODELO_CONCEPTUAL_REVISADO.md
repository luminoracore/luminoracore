# Modelo Conceptual Revisado - LuminoraCore v1.1

**Reconciliando la propuesta de valor original con las mejoras propuestas**

---

## ⚠️ PROBLEMA IDENTIFICADO

### Propuesta de Valor Original de LuminoraCore

> **"Define personalidades AI complejas en JSON estándar que funcionan con cualquier LLM"**

**Implica:**
- ✅ El JSON ES la personalidad
- ✅ El JSON es portable
- ✅ El JSON es el estándar

### Lo que Propuse en v1.1

> **"JSON estático + Estado en BBDD"**

**Implica:**
- ❌ El JSON es solo un template
- ❌ La evolución está en BBDD (no portable)
- ❌ El JSON no representa el estado completo

### 🔴 INCONSISTENCIA

**Si el JSON nunca evoluciona, ¿entonces qué estamos estandarizando?**

---

## ✅ SOLUCIÓN: Modelo de Tres Capas

### Concepto: Template → Instance → Snapshot

```
┌─────────────────────────────────────────────────────────┐
│ CAPA 1: PERSONALITY TEMPLATE (JSON Base)                │
│ - alicia_base.json                                      │
│ - Define comportamiento "de fábrica"                    │
│ - Inmutable, compartido entre todos los usuarios        │
│ - Es el ESTÁNDAR que estamos creando                    │
└─────────────────────────────────────────────────────────┘
              │ Instancia
              ▼
┌─────────────────────────────────────────────────────────┐
│ CAPA 2: PERSONALITY INSTANCE (Estado en BBDD + RAM)     │
│ - Estado del usuario X con personalidad Alicia          │
│ - Evoluciona con cada interacción                       │
│ - Privado por usuario/sesión                            │
│ - Se guarda en BBDD (affinity, facts, mood, etc.)       │
└─────────────────────────────────────────────────────────┘
              │ Exporta
              ▼
┌─────────────────────────────────────────────────────────┐
│ CAPA 3: PERSONALITY SNAPSHOT (JSON Exportado) [OPCIONAL]│
│ - alicia_user_diego_snapshot_2025-10-14.json           │
│ - Estado completo en un momento dado                    │
│ - Portable, puede compartirse/importarse                │
│ - Recrea la experiencia exacta                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Nuevo Modelo Conceptual

### 1. Personality Template (JSON Base)

**Qué es:** Blueprint de la personalidad, configurable, portable, estándar.

```json
// alicia_base.json (TEMPLATE)
{
  "persona": {...},
  "core_traits": {...},
  "advanced_parameters": {...},
  
  // v1.1: Define comportamientos POSIBLES
  "hierarchical_config": {
    "enabled": true,
    "relationship_levels": [...]  // Niveles posibles
  },
  "mood_config": {
    "enabled": true,
    "moods": {...}  // Moods posibles
  }
}
```

**Propósito:**
- Define la "personalidad de fábrica"
- Portable entre proyectos
- El ESTÁNDAR que publicamos
- Inmutable (no cambia con uso)

**Analogía:** Es como la "ISO de una personalidad" - el estándar oficial.

---

### 2. Personality Instance (Estado Runtime)

**Qué es:** Estado actual de la personalidad para un usuario específico.

```python
# En runtime (RAM + BBDD)
instance = PersonalityInstance(
    template=alicia_base,           # Referencia al template
    user_id="diego",
    session_id="session_123",
    
    # Estado actual (en BBDD)
    current_state={
        "affinity": 45,
        "current_level": "friend",
        "current_mood": "shy",
        "mood_intensity": 0.7,
        "learned_facts": {...},
        "episodes": [...],
        "conversation_history": [...]
    }
)
```

**Propósito:**
- Estado vivo de la conversación
- Evoluciona con cada mensaje
- Específico por usuario
- Se guarda en BBDD

**Analogía:** Es como tu "instalación" de un software - el template es el instalador, la instance es tu copia corriendo.

---

### 3. Personality Snapshot (JSON Exportado) - NUEVO

**Qué es:** Exportación del estado completo como JSON.

```json
// alicia_user_diego_snapshot.json (EXPORTADO)
{
  // ========================================
  // METADATA DEL SNAPSHOT
  // ========================================
  "_snapshot_info": {
    "created_at": "2025-10-14T15:30:00Z",
    "template_name": "alicia_base",
    "template_version": "1.1.0",
    "user_id": "diego",
    "session_id": "session_123",
    "total_messages": 150,
    "days_active": 30
  },

  // ========================================
  // PERSONALIDAD BASE (del template)
  // ========================================
  "persona": {...},  // Copiado del template
  "core_traits": {...},
  "linguistic_profile": {...},
  "behavioral_rules": {...},
  "advanced_parameters": {...},

  // ========================================
  // ESTADO ACTUAL (de BBDD)
  // ========================================
  "current_state": {
    "affinity": {
      "points": 45,
      "level": "friend",
      "progression_history": [
        {"date": "2025-09-14", "points": 0, "level": "stranger"},
        {"date": "2025-09-21", "points": 25, "level": "acquaintance"},
        {"date": "2025-10-01", "points": 45, "level": "friend"}
      ]
    },
    
    "mood": {
      "current": "shy",
      "intensity": 0.7,
      "started_at": "2025-10-14T15:25:00Z",
      "history": [
        {"mood": "neutral", "duration": "15m"},
        {"mood": "happy", "duration": "5m"},
        {"mood": "shy", "duration": "current"}
      ]
    },
    
    "learned_facts": [
      {
        "category": "personal_info",
        "key": "name",
        "value": "Diego",
        "confidence": 0.99,
        "first_mentioned": "2025-09-14T10:00:00Z"
      },
      {
        "category": "preferences",
        "key": "favorite_anime",
        "value": "Naruto",
        "confidence": 0.90,
        "first_mentioned": "2025-09-14T10:05:00Z"
      }
    ],
    
    "memorable_episodes": [
      {
        "type": "emotional_moment",
        "title": "Pérdida de mascota Max",
        "summary": "Usuario compartió que su perro Max falleció",
        "importance": 9.5,
        "date": "2025-10-01T14:30:00Z",
        "tags": ["sad", "loss", "pet"]
      }
    ],
    
    "conversation_summary": {
      "total_messages": 150,
      "main_topics": ["anime", "work", "pets"],
      "sentiment_overall": "positive",
      "engagement_score": 8.5
    }
  },

  // ========================================
  // CONFIGURACIÓN ACTIVA (compilada)
  // ========================================
  "active_configuration": {
    // Personalidad compilada actual (con modificadores aplicados)
    "compiled_parameters": {
      "empathy": 1.0,       // Base 0.95 + friend 0.2 + shy 0.0 = CLAMP(1.15) = 1.0
      "formality": 0.4,     // Base 0.3 + friend -0.1 + shy 0.2 = 0.4
      "verbosity": 0.6,     // Base 0.7 + friend 0.0 + shy -0.1 = 0.6
      "humor": 0.5,
      "creativity": 0.6,
      "directness": 0.1     // Base 0.4 + friend 0.0 + shy -0.3 = 0.1
    },
    "active_level": "friend",
    "active_mood": "shy",
    "active_modifiers_applied": ["friend_level", "shy_mood"]
  }
}
```

**Propósito:**
- Captura el estado COMPLETO en un momento dado
- Portable (puede importarse en otro sistema)
- Reproducible (recrea la experiencia exacta)
- Compartible (puede guardarse, transferirse)

**Analogía:** Es como un "save game" - guarda el progreso completo.

---

## 🔄 Flujos con Tres Capas

### Flujo 1: Primera Vez (Template → Instance)

```python
# 1. Usuario crea sesión con template
session_id = await client.create_session(
    personality_template="alicia_base.json",  # Template
    user_id="diego"
)

# Sistema internamente:
# 1. Carga template
template = load_json("alicia_base.json")

# 2. Crea instance nueva
instance = PersonalityInstance.create_from_template(
    template=template,
    user_id="diego",
    initial_state={
        "affinity": 0,
        "current_level": "stranger",
        "current_mood": "neutral",
        "learned_facts": [],
        "episodes": []
    }
)

# 3. Guarda instance en BBDD
await db.save_instance(instance)
```

### Flujo 2: Conversación (Instance Evoluciona)

```python
# Usuario envía mensaje
response = await client.send_message(session_id, "Eres linda")

# Sistema:
# 1. Carga instance desde BBDD
instance = await db.load_instance(session_id)
# instance.affinity = 45
# instance.current_mood = "neutral"

# 2. Procesa mensaje
# - Detecta mood trigger → nuevo mood = "shy"
# - Actualiza affinity → 45 + 2 = 47
# - Extrae facts (si los hay)

# 3. Actualiza instance
instance.current_mood = "shy"
instance.affinity = 47

# 4. Guarda instance actualizada en BBDD
await db.save_instance(instance)

# 5. Compila personalidad dinámica
compiled = instance.compile_current_state()

# 6. Genera respuesta
response = await llm.generate(compiled + message)
```

### Flujo 3: Exportar Snapshot (Instance → JSON)

```python
# Usuario quiere guardar su progreso como JSON
snapshot_json = await client.export_personality_snapshot(
    session_id=session_id,
    include_conversation=True,
    include_facts=True,
    include_episodes=True
)

# Guarda en archivo
with open("my_alicia_snapshot.json", "w") as f:
    json.dump(snapshot_json, f, indent=2)

# Ahora tiene un JSON COMPLETO con todo el estado
# Puede compartirlo, guardarlo, importarlo en otro sistema
```

### Flujo 4: Importar Snapshot (JSON → Instance)

```python
# Usuario importa un snapshot guardado
session_id = await client.import_personality_snapshot(
    snapshot_file="my_alicia_snapshot.json",
    user_id="nuevo_usuario"
)

# Sistema recrea EXACTAMENTE el estado:
# - Affinity: 45
# - Mood: "shy"
# - Facts aprendidos
# - Episodios
# - Todo!

# Usuario continúa donde lo dejó
```

---

## 💡 Propuesta de Valor REVISADA

### LuminoraCore v1.1 es:

**1. Un Estándar para Definir Personalidades (Templates)**
```json
// El estándar: cómo DEFINIR una personalidad
alicia_base.json  ← Template oficial, portable, compartible
```

**2. Un Sistema de Gestión de Instancias**
```python
# Cada usuario tiene su propia instancia
diego_instance → affinity=45, mood="shy", facts=[...]
maria_instance → affinity=10, mood="neutral", facts=[...]
```

**3. Un Formato de Intercambio (Snapshots)**
```json
// Snapshots: estado completo exportable
alicia_diego_snapshot.json  ← Incluye template + estado
```

---

## 🎯 Tres Tipos de JSON

### Tipo 1: Personality Template (Compartible)

```json
// alicia_base.json
// Tipo: Template
// Uso: Base para crear instances
// Compartible: ✅ SÍ
// Mutable: ❌ NO
{
  "persona": {...},
  "core_traits": {...},
  "hierarchical_config": {...},
  "mood_config": {...}
}
```

**Se publica en:**
- GitHub
- Personality Marketplace
- PyPI packages
- Documentación

---

### Tipo 2: Personality Snapshot (Personal)

```json
// alicia_user_diego_snapshot.json  
// Tipo: Snapshot completo
// Uso: Guardar/restaurar estado
// Compartible: ⚠️ Opcional (privado por defecto)
// Mutable: ✅ SÍ (al exportar)
{
  "_snapshot_info": {...},
  "template_base": {...},      // Template original
  "current_state": {...},      // Estado actual
  "learned_facts": [...],
  "episodes": [...],
  "conversation_summary": {...}
}
```

**Se usa para:**
- Backup de conversaciones
- Migración entre sistemas
- Compartir experiencias (opcional)
- Testing/debugging

---

### Tipo 3: Personality Config (Configuración de App)

```json
// config/personalities.json
// Tipo: Configuración de app
// Uso: Qué personalidades usar en tu app
{
  "available_personalities": [
    {
      "id": "alicia",
      "template": "luminoracore/personalities/alicia_base.json",
      "display_name": "Alicia - La Dulce Soñadora",
      "features_enabled": {
        "hierarchical": true,
        "moods": true,
        "memory": true
      }
    }
  ]
}
```

---

## 🏗️ Arquitectura Revisada

### Separación Clara de Responsabilidades

```
┌──────────────────────────────────────────────────────────┐
│ LUMINORACORE CORE (El Estándar)                          │
│                                                          │
│ Responsabilidad:                                         │
│ 1. Definir schema JSON para templates                   │
│ 2. Validar templates                                    │
│ 3. Compilar templates para LLMs                         │
│ 4. Gestionar instances (create, update, compile)        │
│ 5. Exportar/importar snapshots                          │
│                                                          │
│ NO responsable de:                                       │
│ - Dónde se guarda el estado (usuario elige backend)     │
│ - UI/UX de aplicación                                   │
│ - Lógica de negocio específica                          │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ TU APLICACIÓN (Usuario de LuminoraCore)                 │
│                                                          │
│ Responsabilidad:                                         │
│ 1. Elegir qué templates usar                            │
│ 2. Elegir dónde guardar instances (SQLite/PostgreSQL)   │
│ 3. Gestionar usuarios y sesiones                        │
│ 4. UI/UX                                                │
│ 5. Lógica de negocio (gamificación, monetización, etc.) │
└──────────────────────────────────────────────────────────┘
```

---

## 📝 Estándar JSON Extendido

### Template Structure v1.1

```json
{
  // ========================================
  // CORE DEFINITION (v1.0, required)
  // ========================================
  "schema_version": "1.1.0",
  "template_info": {
    "name": "alicia_base",
    "version": "1.0.0",
    "author": "Ereace",
    "license": "MIT",
    "description": "Dulce soñadora que ama el anime",
    "tags": ["anime", "caregiver", "empathetic"],
    "language": "es"
  },
  
  "persona": {...},
  "core_traits": {...},
  "linguistic_profile": {...},
  "behavioral_rules": {...},
  "response_patterns": {...},
  "advanced_parameters": {...},

  // ========================================
  // DYNAMIC BEHAVIOR CONFIG (v1.1, optional)
  // ========================================
  
  "hierarchical_config": {
    "enabled": true,
    "metric": "affinity",  // "affinity" | "knowledge" | "custom"
    "relationship_levels": [...]
  },
  
  "mood_config": {
    "enabled": true,
    "moods": {...},
    "mood_triggers": {...}
  },
  
  "memory_config": {
    "episodic_memory": {
      "enabled": true,
      "importance_threshold": 7.0
    },
    "fact_extraction": {
      "enabled": true,
      "auto_extract_categories": ["personal_info", "preferences"]
    },
    "semantic_search": {
      "enabled": true,
      "similarity_threshold": 0.75
    }
  },

  // ========================================
  // INSTANCE DEFAULTS (v1.1, optional)
  // ========================================
  
  "instance_defaults": {
    "initial_affinity": 0,
    "initial_mood": "neutral",
    "initial_level": "stranger"
  }
}
```

### Snapshot Structure v1.1

```json
{
  // ========================================
  // SNAPSHOT METADATA
  // ========================================
  "_snapshot_info": {
    "type": "personality_snapshot",
    "version": "1.1.0",
    "created_at": "2025-10-14T15:30:00Z",
    "template_reference": {
      "name": "alicia_base",
      "version": "1.0.0",
      "source": "luminoracore/personalities/alicia_base.json"
    },
    "user_info": {
      "user_id": "diego",  // Opcional, puede anonimizarse
      "session_id": "session_123"
    },
    "statistics": {
      "total_messages": 150,
      "days_active": 30,
      "engagement_score": 8.5
    }
  },

  // ========================================
  // TEMPLATE BASE (referencia)
  // ========================================
  "template": {
    // Puede ser referencia:
    "$ref": "alicia_base.json"
    
    // O copia completa (para portabilidad):
    // "persona": {...},
    // "core_traits": {...},
    // etc.
  },

  // ========================================
  // CURRENT STATE (estado exportado)
  // ========================================
  "state": {
    "affinity": 45,
    "current_level": "friend",
    "current_mood": "shy",
    "mood_intensity": 0.7,
    
    "facts": [...],      // Todos los facts aprendidos
    "episodes": [...],   // Todos los episodios
    
    // OPCIONAL: incluir conversación completa
    "conversation_history": [...]
  },

  // ========================================
  // COMPILED STATE (para debugging)
  // ========================================
  "compiled_snapshot": {
    // Personalidad compilada con estado actual
    "advanced_parameters": {
      "empathy": 1.0,    // Compilado final
      "formality": 0.4,
      "verbosity": 0.6,
      "humor": 0.5,
      "creativity": 0.6,
      "directness": 0.1
    },
    "active_modifiers": ["friend_level", "shy_mood"]
  }
}
```

---

## 🎯 Casos de Uso de Snapshots

### Caso 1: Backup de Conversación

```python
# Usuario quiere guardar su progreso
snapshot = await client.export_snapshot(session_id)

# Guardar localmente
with open("my_alicia_backup.json", "w") as f:
    json.dump(snapshot, f)

# Días después, restaurar
new_session = await client.import_snapshot("my_alicia_backup.json")
# Continúa exactamente donde lo dejó
```

### Caso 2: Migrar entre Dispositivos

```python
# Dispositivo 1 (PC)
snapshot = await client.export_snapshot(session_id)
upload_to_cloud(snapshot)

# Dispositivo 2 (Móvil)
snapshot = download_from_cloud()
session_id = await client.import_snapshot(snapshot)
# Misma conversación, diferente dispositivo
```

### Caso 3: Compartir Experiencias (Comunidad)

```python
# Usuario A: "Mi conversación con Alicia fue increíble"
snapshot = await client.export_snapshot(
    session_id,
    anonymize=True,  # Remueve datos personales
    include_conversation=True
)

# Comparte en foro/comunidad
post_to_community(snapshot)

# Usuario B: "Quiero experimentar esta conversación"
imported_session = await client.import_snapshot(snapshot)
# Experimenta la misma progresión que Usuario A
```

### Caso 4: A/B Testing

```python
# Crear snapshot de baseline
baseline = await client.export_snapshot(session_id)

# Variar personalidad A
session_a = await client.import_snapshot(baseline)
# ... conversar ...
metrics_a = await client.get_analytics(session_a)

# Variar personalidad B
session_b = await client.import_snapshot(baseline)
# ... conversar ...
metrics_b = await client.get_analytics(session_b)

# Comparar
compare(metrics_a, metrics_b)
```

---

## 🎯 Propuesta de Valor RECONCILIADA

### Lo Que LuminoraCore Estandariza

#### 1. **Template Format** (El Estándar Principal)

**Definición oficial de personalidades AI:**
- Schema JSON validado
- Compatible con múltiples LLMs
- Portable entre proyectos
- Versionado semántico

**Ejemplo:**
```json
// Este es el ESTÁNDAR que creamos
{
  "schema_version": "1.1.0",
  "persona": {...},
  "core_traits": {...},
  "hierarchical_config": {...}
}
```

#### 2. **Instance Format** (Extensión del Estándar)

**Cómo representar el estado de una instance:**
- Estructura estandarizada para affinity, mood, facts
- Compatible con el template base
- Exportable/importable

#### 3. **Snapshot Format** (Formato de Intercambio)

**Cómo guardar/compartir experiencias completas:**
- Template + State en un solo JSON
- Portable, reproducible
- Puede compartirse en comunidad

---

## 📊 Qué se Guarda Dónde (Tabla Definitiva)

| Dato | Template JSON | Instance (BBDD) | Snapshot JSON | Mutable |
|------|---------------|-----------------|---------------|---------|
| **Nombre de personalidad** | ✅ | - | ✅ | ❌ |
| **Core traits** | ✅ | - | ✅ | ❌ |
| **Niveles posibles** | ✅ | - | ✅ | ❌ |
| **Moods posibles** | ✅ | - | ✅ | ❌ |
| **Affinity actual** | - | ✅ | ✅ | ✅ |
| **Mood actual** | - | ✅ | ✅ | ✅ |
| **Facts aprendidos** | - | ✅ | ✅ | ✅ |
| **Episodios** | - | ✅ | ✅ | ✅ |
| **Mensajes** | - | ✅ | ✅ (opcional) | ✅ |
| **Personalidad compilada** | - | - | ✅ (snapshot) | - |

---

## 🔧 APIs Propuestas v1.1

### Working with Templates

```python
# Cargar template (estándar)
template = Personality.load_template("alicia_base.json")

# Validar template
is_valid = template.validate()

# Publicar template
await marketplace.publish_template(template)

# Buscar templates
templates = await marketplace.search(tags=["anime", "caregiver"])
```

### Working with Instances

```python
# Crear instance desde template
session_id = await client.create_session(
    template="alicia_base",
    user_id="diego"
)

# Obtener instance actual
instance = await client.get_instance(session_id)
# instance.affinity = 45
# instance.mood = "shy"

# Actualizar instance (automático al enviar mensajes)
response = await client.send_message(session_id, "Hola")
# instance se actualiza automáticamente en BBDD
```

### Working with Snapshots

```python
# Exportar snapshot
snapshot = await client.export_snapshot(
    session_id=session_id,
    format="json",
    include_options={
        "conversation_history": True,
        "facts": True,
        "episodes": True,
        "embeddings": False,  # Demasiado pesado
        "anonymize_user_data": False
    }
)

# Guardar snapshot
with open("snapshot.json", "w") as f:
    json.dump(snapshot, f)

# Importar snapshot
new_session = await client.import_snapshot(
    snapshot_file="snapshot.json",
    user_id="nuevo_usuario",  # Opcional, para re-asociar
    restore_options={
        "restore_affinity": True,
        "restore_mood": True,
        "restore_facts": True,
        "restore_conversation": False  # Empezar conversación limpia
    }
)
```

---

## 💾 Sistema de Persistencia Híbrido

### Opción A: BBDD + Snapshots Periódicos (Recomendado)

```python
# Configuración
client = LuminoraCoreClient(
    storage_config={
        "backend": "postgresql",  # Estado activo
        "snapshot_config": {
            "enabled": True,
            "auto_snapshot_interval": "daily",  # Snapshot automático diario
            "snapshot_storage": "s3://my-bucket/snapshots/"
        }
    }
)

# Uso normal: estado en PostgreSQL
response = await client.send_message(session_id, "Hola")

# Sistema automáticamente crea snapshots diarios
# snapshots/session_123/2025-10-14.json
# snapshots/session_123/2025-10-15.json
# ...

# Restaurar de snapshot si BBDD falla
await client.restore_from_snapshot("2025-10-14.json")
```

### Opción B: Solo JSON (Simple, para apps pequeñas)

```python
# Configuración
client = LuminoraCoreClient(
    storage_config={
        "backend": "json_snapshots",
        "snapshot_dir": "./user_data/"
    }
)

# Cada usuario tiene su JSON
# user_data/
# ├── diego_alicia.json    ← Snapshot que se actualiza
# ├── maria_mika.json
# └── carlos_yumi.json

# Al enviar mensaje:
# 1. Carga snapshot del usuario
# 2. Procesa mensaje
# 3. Actualiza snapshot
# 4. Guarda snapshot actualizado
```

**Ventajas:**
- ✅ Simple, no requiere BBDD
- ✅ Portable (archivos JSON)
- ✅ Fácil de respaldar

**Desventajas:**
- ❌ Más lento (I/O de disco cada mensaje)
- ❌ Concurrencia limitada
- ❌ No vector search eficiente

---

## 🎯 Respuesta a tu Pregunta Original

### "¿Esto casa con la propuesta de valor de LuminoraCore?"

**Respuesta:** SÍ, pero necesitamos CLARIFICAR el modelo:

#### Antes (confuso):
> "Define personalidades en JSON"
> - ¿Pero el JSON nunca cambia?
> - ¿Entonces cómo evoluciona la personalidad?
> - ¿Dónde está el estándar?

#### Ahora (claro):
> **"LuminoraCore define el ESTÁNDAR para:**
> 1. **Templates de personalidades** (JSON base, portable, compartible)
> 2. **Instances de personalidades** (estado runtime, en BBDD)
> 3. **Snapshots de personalidades** (estado exportado, JSON completo)
> 
> **El JSON puede ser:**
> - Template (inmutable, compartido) ← El estándar principal
> - Snapshot (mutable, privado) ← Exportación de estado
> 
> **Ambos usan el mismo schema JSON estándar."**

---

## 🔄 Flujo Completo Revisado

```python
# ============================================
# PASO 1: Desarrollador crea TEMPLATE
# ============================================

# Crear personalidad base (TEMPLATE)
template = {
    "schema_version": "1.1.0",
    "template_info": {...},
    "persona": {...},
    "hierarchical_config": {...},
    "mood_config": {...}
}

# Guardar como JSON estándar
with open("alicia_base.json", "w") as f:
    json.dump(template, f)

# Validar contra schema oficial
luminora-cli validate alicia_base.json
# ✅ Valid personality template v1.1.0

# Publicar (opcional)
await marketplace.publish("alicia_base.json")

# ============================================
# PASO 2: Usuario usa TEMPLATE en app
# ============================================

# App carga template
client = LuminoraCoreClient()
await client.load_template("alicia_base.json")

# Crear INSTANCE para usuario Diego
session_diego = await client.create_instance(
    template="alicia_base",
    user_id="diego"
)

# Estado inicial (en BBDD):
# - affinity: 0
# - mood: "neutral"
# - facts: []

# ============================================
# PASO 3: Instance EVOLUCIONA
# ============================================

# Conversación
await client.send_message(session_diego, "Hola, soy Diego")
# Estado actualizado en BBDD:
# - affinity: 1
# - facts: [{key: "name", value: "Diego"}]

await client.send_message(session_diego, "Eres linda")
# Estado actualizado:
# - affinity: 3
# - mood: "shy"

# El TEMPLATE sigue igual (inmutable)
# La INSTANCE evoluciona (en BBDD)

# ============================================
# PASO 4: Exportar SNAPSHOT (opcional)
# ============================================

# Usuario quiere backup
snapshot = await client.export_snapshot(session_diego)

# snapshot.json contiene:
# - Template base (referencia o copia)
# - Estado actual (affinity=3, mood="shy", facts=[...])
# - Historial completo

# Guardar
save_json("diego_alicia_snapshot.json", snapshot)

# ============================================
# PASO 5: Importar SNAPSHOT (recuperación)
# ============================================

# Nuevo dispositivo o después de reinstalar
restored_session = await client.import_snapshot(
    "diego_alicia_snapshot.json"
)

# Session restaurada EXACTAMENTE como estaba:
# - affinity: 3
# - mood: "shy"
# - facts: [...]
# - Todo!
```

---

## ✅ Propuesta de Valor FINAL

### LuminoraCore v1.1 es:

**"El estándar open-source para definir, gestionar, y compartir personalidades AI con memoria y adaptación."**

#### Tres Componentes del Estándar:

1. **Template Standard** (JSON Schema oficial)
   - Cómo DEFINIR una personalidad
   - Portable, validable, versionado
   - Marketplace de templates

2. **Instance Management** (Runtime system)
   - Cómo EJECUTAR personalidades con estado
   - Adaptación dinámica (affinity, moods)
   - Backend-agnostic (SQLite, PostgreSQL, etc.)

3. **Snapshot Format** (Interchange format)
   - Cómo EXPORTAR/IMPORTAR estados completos
   - Backup, migración, compartición
   - Reproducibilidad

---

## 📊 Comparación Final

### Propuesta Original (v1.0)

```
Template JSON → Compile → Use
(Estático)
```

**Problema:** No evoluciona

### Propuesta Inicial v1.1 (Confusa)

```
Template JSON (inmutable) → BBDD (estado) → Compile dinámico
```

**Problema:** ¿Dónde está el estándar para el estado?

### Propuesta REVISADA v1.1 (Clara)

```
Template JSON (estándar) → Instance (BBDD) → Snapshot JSON (exportable)
      ↓                         ↓                    ↓
  Portable              Evoluciona            Portable again
  Compartible           Privado               Compartible
  Inmutable             Mutable               Inmutable (snapshot)
```

**Solución:** El estándar cubre TEMPLATES y SNAPSHOTS (ambos JSON)

---

## 🎯 Conclusión

### ¿Casa con la propuesta de valor?

**SÍ, con aclaración:**

**LuminoraCore v1.0:**
- Estándar para definir personalidades (Templates)

**LuminoraCore v1.1:**
- Estándar para definir personalidades (Templates) ← Mismo
- **+** Sistema para gestionar instances que evolucionan (BBDD) ← Nuevo
- **+** Estándar para exportar estados (Snapshots) ← Nuevo

**El estándar JSON se EXTIENDE para cubrir más casos de uso, no se abandona.**

---

### Templates vs Instances vs Snapshots

| | Template | Instance | Snapshot |
|---|----------|----------|----------|
| **Formato** | JSON | BBDD + RAM | JSON |
| **Propósito** | Blueprint | Estado vivo | Backup/compartir |
| **Mutable** | ❌ NO | ✅ SÍ | ❌ NO |
| **Compartible** | ✅ SÍ | ❌ NO | ✅ SÍ |
| **Portable** | ✅ SÍ | ❌ NO | ✅ SÍ |
| **Parte del estándar** | ✅ SÍ | ⚠️ Implementación | ✅ SÍ |

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

**LuminoraCore v1.1 - Templates, Instances & Snapshots**

</div>

