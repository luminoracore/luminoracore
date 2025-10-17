# 🔧 Complete CLI and Configuration Guide - LuminoraCore v1.1

**Complete guide for CLI commands, personality enrichment, sentiment analysis, and configuration**

---

## 🎭 **PERSONALIDAD ENRIQUECIDA (JSON GENERADO)**

### **📍 ¿Dónde se genera el JSON de personalidad enriquecida?**

El JSON de personalidad enriquecida se genera en **`conversation_export.json`** en la sección `final_personality`:

```json
{
  "final_personality": {
    "core_traits": {
      "professionalism": 1.0,
      "efficiency": 1.0,
      "empathy": 1.0,
      "directness": 0.736
    },
    "communication_style": {
      "formality": 0.4000000000000001,
      "warmth": 1.0,
      "humor": 0.9,
      "patience": 0.836
    }
  }
}
```

### **🔄 Evolución de Personalidad (3 Recalculaciones):**

```json
{
  "personality_evolution": [
    {
      "message_count": 3,
      "affinity": 19,
      "relationship_level": "acquaintance",
      "personality_before": { /* personalidad inicial */ },
      "personality_after": { /* personalidad después del mensaje 3 */ },
      "changes": {
        "professionalism": 0.019,
        "efficiency": 0.038,
        "empathy": 0.057,
        "directness": 0.019,
        "patience": 0.019
      }
    }
    // ... más recalculaciones
  ]
}
```

### **📁 Archivos Generados en la Simulación:**

1. **`conversation_export.json`** - JSON completo con:
   - `session_info`: Información de la sesión
   - `conversation`: Los 10 mensajes completos
   - `personality_evolution`: 3 recalculaciones de personalidad
   - `memory_classification`: Hechos y episodios clasificados
   - `final_personality`: Personalidad final enriquecida

2. **`conversation_memory.db`** - Base de datos SQLite con:
   - Tabla `sessions`: Información de sesiones
   - Tabla `conversations`: Mensajes y contexto
   - Tabla `personality_evolution`: Evolución de personalidad
   - Tabla `memory_facts`: Hechos clasificados
   - Tabla `memory_episodes`: Episodios memorables

---

## 📊 **ANÁLISIS SENTIMENTAL Y CONFIGURACIÓN**

### **⚙️ ¿Dónde se configura cuándo hacer análisis sentimental?**

En el archivo de configuración de personalidad:

```json
{
  "memory_preferences": {
    "fact_retention": 0.9,
    "episodic_memory": 0.8,
    "preference_learning": 0.9,
    "goal_tracking": 0.8,
    "recalculation_frequency": 3,  // ← AQUÍ: Cada 3 mensajes
    "sentiment_analysis_frequency": 5  // ← AQUÍ: Cada 5 mensajes
  }
}
```

### **🧠 Configuración Completa de Análisis Sentimental:**

```json
{
  "sentiment_config": {
    "enabled": true,
    "frequency": 5,  // Cada 5 mensajes
    "provider": "deepseek",  // o "openai", "anthropic", etc.
    "analysis_types": [
      "emotional_tone",
      "user_satisfaction", 
      "relationship_health",
      "conversation_mood"
    ],
    "triggers": [
      "message_count_threshold",
      "affinity_change_detected",
      "negative_sentiment_detected",
      "relationship_level_change"
    ],
    "actions": {
      "on_negative_sentiment": "adjust_empathy_up",
      "on_positive_sentiment": "maintain_or_enhance_warmth",
      "on_neutral_sentiment": "increase_engagement"
    }
  }
}
```

### **📈 Ejemplo de Análisis Sentimental:**

```json
{
  "sentiment_analysis": {
    "message_count": 5,
    "timestamp": "2025-10-16T22:47:39.064316",
    "analysis": {
      "overall_sentiment": 0.8,  // Positivo
      "emotional_tone": "enthusiastic",
      "user_satisfaction": 0.85,
      "relationship_health": "improving",
      "conversation_mood": "collaborative"
    },
    "recommendations": [
      "maintain_current_warmth_level",
      "increase_technical_detail",
      "continue_direct_communication"
    ],
    "personality_adjustments": {
      "warmth": +0.1,
      "technical_depth": +0.05
    }
  }
}
```

### **🔧 Comando CLI para Análisis Sentimental:**

```bash
# Analizar sentimientos de una sesión (futuro comando)
luminoracore sentiment analyze user_123        # Analizar sentimientos
luminoracore sentiment history user_123        # Historial de sentimientos
luminoracore sentiment dashboard user_123      # Dashboard de sentimientos
```

---

## 🖥️ **COMANDOS CLI COMPLETOS**

### **📋 Lista de Comandos CLI v1.1 (REAL):**

```bash
# COMANDOS BÁSICOS v1.0 (11 comandos)
luminoracore validate <personality_file>     # Validar personalidad
luminoracore compile <personality_file>      # Compilar personalidad  
luminoracore blend <file1> <file2>           # Mezclar personalidades
luminoracore test <personality_file>         # Probar personalidad
luminoracore create <template>               # Crear nueva personalidad
luminoracore list                            # Listar personalidades
luminoracore serve                           # Servidor web
luminoracore update <personality_file>       # Actualizar personalidad
luminoracore init <project_name>             # Inicializar proyecto
luminoracore info <personality_file>         # Información de personalidad

# COMANDOS NUEVOS v1.1 (3 comandos)
luminoracore migrate [db_path]               # Migrar base de datos
luminoracore memory facts <session_id>       # Gestionar hechos de memoria
luminoracore memory episodes <session_id>    # Gestionar episodios
luminoracore memory search <session_id>      # Buscar en memoria
luminoracore snapshot <session_id>           # Exportar snapshot
```

### **📖 Guía de Uso de Comandos CLI:**

#### **🔧 Comandos Básicos:**

```bash
# 1. Validar personalidad
luminoracore validate luminoracore/luminoracore/personalities/dr_luna.json

# 2. Compilar personalidad para OpenAI
luminoracore compile luminoracore/luminoracore/personalities/dr_luna.json --provider openai

# 3. Mezclar dos personalidades
luminoracore blend dr_luna.json victoria_sterling.json --output mixed_personality.json

# 4. Probar personalidad
luminoracore test dr_luna.json --provider deepseek --api-key $DEEPSEEK_API_KEY

# 5. Analizar personalidad
luminoracore analyze dr_luna.json --detailed
```

#### **🆕 Comandos v1.1:**

```bash
# 1. Migrar base de datos a v1.1
luminoracore migrate                          # Migrar con configuración por defecto
luminoracore migrate custom.db                # Migrar base de datos específica
luminoracore migrate --dry-run                # Ver qué se haría sin aplicar
luminoracore migrate --status                 # Ver estado de migraciones
luminoracore migrate --history                # Ver historial de migraciones

# 2. Gestionar memoria de sesión
luminoracore memory facts user_123            # Listar hechos de la sesión
luminoracore memory facts user_123 --category personal_info  # Filtrar por categoría
luminoracore memory facts user_123 --format json            # Formato JSON
luminoracore memory episodes user_123         # Listar episodios memorables
luminoracore memory search user_123 "Carlos"  # Buscar en memoria

# 3. Exportar snapshot completo
luminoracore snapshot user_123                # Exportar snapshot de sesión
luminoracore snapshot user_123 --format json  # Formato JSON
luminoracore snapshot user_123 --format sqlite # Formato SQLite
```

### **📚 Ayuda de Comandos:**

```bash
# Ayuda general
luminoracore --help

# Ayuda específica de comando
luminoracore validate --help
luminoracore migrate --help
luminoracore memory --help
luminoracore snapshot --help
```

---

## ⚙️ **CONFIGURACIÓN AVANZADA**

### **🎯 Configuración de Frecuencias:**

```json
{
  "luminora_config": {
    "personality_recalculation": {
      "frequency": 3,  // Cada 3 mensajes
      "triggers": [
        "message_count",
        "affinity_change",
        "relationship_level_change"
      ]
    },
    "sentiment_analysis": {
      "frequency": 5,  // Cada 5 mensajes
      "triggers": [
        "message_count",
        "negative_sentiment_detected",
        "conversation_quality_drop"
      ]
    },
    "memory_consolidation": {
      "frequency": 10,  // Cada 10 mensajes
      "triggers": [
        "message_count",
        "memory_size_threshold",
        "conversation_end"
      ]
    }
  }
}
```

### **🔧 Variables de Entorno:**

```bash
# Configuración de frecuencias
export LUMINORA_RECALCULATION_FREQUENCY=3
export LUMINORA_SENTIMENT_FREQUENCY=5
export LUMINORA_MEMORY_CONSOLIDATION_FREQUENCY=10

# Configuración de análisis sentimental
export LUMINORA_SENTIMENT_PROVIDER=deepseek
export LUMINORA_SENTIMENT_MODEL=deepseek-chat
export LUMINORA_SENTIMENT_ENABLED=true

# Configuración de memoria
export LUMINORA_MEMORY_RETENTION_DAYS=30
export LUMINORA_MEMORY_MAX_FACTS=1000
export LUMINORA_MEMORY_MAX_EPISODES=500
```

---

## 🚀 **COMANDOS FUTUROS (v1.2+)**

### **📋 Comandos Planificados (v1.2+):**

```bash
# Análisis avanzado
luminoracore sentiment analyze <session_id>      # Analizar sentimientos
luminoracore sentiment history <session_id>      # Historial de sentimientos
luminoracore analytics dashboard <session_id>    # Dashboard analítico
luminoracore insights generate <session_id>      # Generar insights automáticos

# Gestión de datos
luminoracore backup all-sessions                 # Backup completo
luminoracore restore from-backup <file>          # Restaurar backup
luminoracore sync cloud <provider>               # Sincronizar con cloud
luminoracore export all-formats <session_id>     # Exportar todos los formatos

# Desarrollo
luminoracore dev create-personality              # Crear personalidad interactivo
luminoracore dev test-scenarios                  # Probar escenarios
luminoracore dev benchmark                       # Benchmark de rendimiento
luminoracore dev validate-performance           # Validar rendimiento

# Integración
luminoracore integrate webhook <url>             # Configurar webhooks
luminoracore integrate api generate-keys         # Generar API keys
luminoracore integrate monitoring setup          # Configurar monitoreo
luminoracore integrate discord setup             # Configurar Discord bot
luminoracore integrate telegram setup            # Configurar Telegram bot

# Análisis de calidad
luminoracore quality check <personality_file>    # Verificar calidad
luminoracore quality optimize <personality_file> # Optimizar personalidad
luminoracore quality compare <file1> <file2>     # Comparar personalidades
```

---

## 📊 **EJEMPLO COMPLETO DE USO**

### **🔧 Configuración Completa:**

```python
# config.py
PERSONALITY_CONFIG = {
    "name": "Victoria Sterling",
    "version": "1.1.0",
    "base_personality": {
        "core_traits": {
            "professionalism": 0.9,
            "efficiency": 0.8,
            "empathy": 0.7,
            "directness": 0.6
        }
    },
    "hierarchical_config": {
        "relationship_levels": {
            "stranger": {"affinity_threshold": 0},
            "acquaintance": {"affinity_threshold": 10},
            "friend": {"affinity_threshold": 25},
            "close_friend": {"affinity_threshold": 50}
        }
    },
    "memory_preferences": {
        "recalculation_frequency": 3,      # Cada 3 mensajes
        "sentiment_analysis_frequency": 5,  # Cada 5 mensajes
        "memory_consolidation_frequency": 10 # Cada 10 mensajes
    },
    "sentiment_config": {
        "enabled": True,
        "provider": "deepseek",
        "frequency": 5,
        "analysis_types": [
            "emotional_tone",
            "user_satisfaction",
            "relationship_health"
        ]
    }
}
```

### **🖥️ Uso de Comandos CLI:**

```bash
# 1. Validar configuración
luminoracore validate victoria_sterling.json

# 2. Migrar a v1.1
luminoracore migrate --to-v1.1 --input victoria_sterling.json

# 3. Probar con DeepSeek
luminoracore test victoria_sterling_v1_1.json --provider deepseek

# 4. Gestionar memoria
luminoracore memory --session user_123 --action list

# 5. Exportar snapshot
luminoracore snapshot --export user_123 --format json
```

---

## 🎯 **RESUMEN COMPLETO DE RESPUESTAS**

### **📄 JSON de Personalidad Enriquecida:**
✅ **Generado en**: `conversation_export.json` → sección `final_personality`
✅ **Contiene**: Evolución completa de personalidad con 3 recalculaciones
✅ **Incluye**: Hechos, episodios, afinidad y cambios de personalidad

### **📊 Análisis Sentimental:**
✅ **Configurado en**: `memory_preferences.sentiment_analysis_frequency: 5`
✅ **Se ejecuta**: Cada 5 mensajes (configurable)
✅ **Proveedores**: DeepSeek, OpenAI, Anthropic (configurable)
✅ **Comandos**: `luminoracore sentiment analyze <session_id>` (futuro)

### **🖥️ Comandos CLI:**
✅ **Comandos v1.0**: 10 comandos básicos (validate, compile, blend, test, create, list, serve, update, init, info)
✅ **Comandos v1.1**: 4 comandos nuevos (migrate, memory facts, memory episodes, memory search, snapshot)
✅ **Comandos futuros**: 15+ comandos planificados para v1.2+

### **⚙️ Configuración:**
✅ **Frecuencias**: Configurables en JSON y variables de entorno
✅ **Proveedores**: DeepSeek, OpenAI, Anthropic, etc.
✅ **Personalizable**: Cada aspecto es configurable
✅ **Base de datos**: SQLite, PostgreSQL, Redis, MongoDB

### **📁 Archivos Generados:**
✅ **JSON**: `conversation_export.json` con toda la información
✅ **SQLite**: `conversation_memory.db` con estructura de tablas
✅ **Logs**: Información detallada de cada proceso

### **🔄 Proceso de Recalculación:**
✅ **Frecuencia**: Cada 3 mensajes (configurable)
✅ **Triggers**: Cambios de afinidad, nivel de relación, nuevos hechos
✅ **Algoritmo**: Linear mapping + smooth transition
✅ **Export**: JSON, prompt, system prompt para LLMs

---

**🎊 ¡LuminoraCore v1.1 tiene todo lo que necesitas para personalidades inteligentes, análisis sentimental y gestión avanzada de memoria!**
