# Resumen Visual - LuminoraCore v1.1

**Explicación visual y concisa del sistema completo**

---

## 🎯 El Modelo en 3 Conceptos

```
┌─────────────────────────────────────────────────────────────┐
│ 1. TEMPLATE = Blueprint de personalidad (JSON base)        │
│    - Define CÓMO es la personalidad                        │
│    - Inmutable, compartible, portable                       │
│    - Ejemplo: alicia_base.json                             │
│    - Es el ESTÁNDAR que publicamos                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Instancia para usuario
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. INSTANCE = Estado vivo de conversación (BBDD + RAM)     │
│    - Define el ESTADO ACTUAL para un usuario               │
│    - Mutable, privado, evoluciona                          │
│    - Ejemplo: Diego conversando con Alicia                  │
│    - Guarda: affinity=45, mood="shy", facts=[...]          │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Exporta cuando necesitas
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. SNAPSHOT = Foto del estado completo (JSON exportado)    │
│    - Template + Estado en un solo JSON                     │
│    - Portable, compartible, reproducible                    │
│    - Ejemplo: diego_alicia_dia30.json                      │
│    - Usa: backup, migración, compartir                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 💾 Qué se Guarda Dónde (Tabla Simple)

| Tipo de Dato | Archivo JSON | BBDD | RAM | Mutable |
|--------------|--------------|------|-----|---------|
| **Personalidad base** | ✅ Template | - | ✅ Caché | ❌ |
| **Niveles posibles** | ✅ Template | - | - | ❌ |
| **Moods posibles** | ✅ Template | - | - | ❌ |
| **Affinity actual** | - | ✅ | ✅ Caché | ✅ |
| **Mood actual** | - | ✅ | ✅ Caché | ✅ |
| **Facts** | - | ✅ | - | ✅ |
| **Episodios** | - | ✅ | - | ✅ |
| **Mensajes** | - | ✅ | - | ✅ |
| **Estado completo** | ✅ Snapshot | - | - | ❌ |

---

## 🔄 Flujo de un Mensaje (Simplificado)

```
Usuario: "Eres linda"
    │
    ▼
┌─────────────────────────────┐
│ 1. Cargar contexto (50ms)   │
│    ├─ Template (caché)      │  ← alicia_base.json
│    ├─ Affinity (BBDD)       │  ← PostgreSQL: affinity=45
│    └─ Mood (BBDD)           │  ← PostgreSQL: mood="neutral"
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│ 2. Compilar (5ms)           │
│    Base + Friend + Neutral  │  ← En RAM, temporal
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│ 3. LLM (1500ms) ← LENTO     │
│    Generar respuesta        │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│ 4. Retornar (INMEDIATO)     │  Usuario ve respuesta ✅
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│ 5. Background (no bloquea)  │
│    ├─ Detectar mood: "shy"  │  ← En paralelo
│    ├─ Actualizar affinity   │  ← Guardar en BBDD
│    ├─ Extraer facts         │  ← Guardar en BBDD
│    └─ Crear embeddings      │  ← Guardar en BBDD
└─────────────────────────────┘

Usuario vio respuesta en 1.5s
Sistema procesó memoria en background (no le afecta)
```

---

## 📝 Los 3 Tipos de JSON

### Template JSON (Compartible)

```json
// alicia_base.json
{
  "persona": {"name": "Alicia"},
  "core_traits": {...},
  "hierarchical_config": {
    "relationship_levels": [
      {"name": "stranger", "affinity_range": [0, 20]},
      {"name": "friend", "affinity_range": [41, 60]}
    ]
  }
}
```

**Uso:**
- ✅ Publicar en GitHub
- ✅ Compartir en comunidad
- ✅ Usar como base para múltiples usuarios
- ❌ NO se actualiza con uso

---

### Snapshot JSON (Backup)

```json
// diego_alicia_snapshot.json
{
  "_snapshot_info": {
    "user_id": "diego",
    "created_at": "2025-10-14"
  },
  "template": "alicia_base.json",  // Referencia al template
  "state": {
    "affinity": 45,
    "mood": "shy",
    "facts": [
      {"key": "name", "value": "Diego"},
      {"key": "favorite_anime", "value": "Naruto"}
    ],
    "episodes": [...]
  }
}
```

**Uso:**
- ✅ Backup de conversación
- ✅ Migrar entre dispositivos
- ✅ Compartir experiencia (opcional)
- ❌ NO se actualiza con cada mensaje (solo al exportar)

---

### Config JSON (App)

```json
// config/app_config.json
{
  "personalities": [
    {"id": "alicia", "template": "alicia_base.json"},
    {"id": "mika", "template": "mika_base.json"}
  ],
  "storage": {
    "backend": "postgresql",
    "snapshot_enabled": true
  }
}
```

**Uso:**
- ✅ Configurar qué personalidades usar
- ✅ Configurar backends
- ❌ NO define personalidades (solo referencias)

---

## ⚡ Performance (Números Reales)

### Latencia Total por Mensaje

```
┌──────────────────────────────────────┐
│ Componente         │ Tiempo          │
├────────────────────┼─────────────────┤
│ Cargar contexto    │ 50ms (1ª vez)   │
│                    │ 1ms (caché)     │
├────────────────────┼─────────────────┤
│ Compilar           │ 5ms             │
├────────────────────┼─────────────────┤
│ LLM (DeepSeek)     │ 1500ms ← 96%    │
├────────────────────┼─────────────────┤
│ Guardar mensaje    │ 20ms            │
├────────────────────┼─────────────────┤
│ TOTAL (usuario)    │ 1575ms          │
├────────────────────┼─────────────────┤
│ Background tasks   │ 400ms (async)   │
│ (no bloquea)       │ Usuario no nota │
└────────────────────┴─────────────────┘
```

**Conclusión: La compilación dinámica agrega solo 5ms (0.3% overhead)**

---

## 🗄️ BBDD: Actuales vs Nuevas

### Tu BBDD Actual (v1.0) - NO CAMBIA

```sql
-- Tablas existentes (siguen igual)
sessions
messages
-- Tus tablas custom
```

### Nuevas Tablas v1.1 - SE AGREGAN

```sql
-- Nuevas tablas (se agregan, no reemplazan)
user_affinity       -- Puntos de relación
session_moods       -- Mood actual
user_facts          -- Facts aprendidos
episodes            -- Momentos importantes
message_embeddings  -- Vectores (opcional)
```

**Total: +5 tablas (o +4 si no usas vector search)**

---

## 🎯 Casos de Uso de Cada Componente

### Templates

```python
# Desarrollador crea personalidad
template = create_template("alicia_base.json")

# Publica en marketplace
marketplace.publish(template)

# Otros desarrolladores usan
template = marketplace.download("alicia_base")
```

**Analogía:** Es como una "app" en App Store - se crea una vez, se usa muchas veces.

---

### Instances

```python
# Usuario A conversa con Alicia
session_a = create_instance("alicia_base", user="userA")
# state: affinity=20, mood="neutral"

# Usuario B conversa con Alicia (diferente instance)
session_b = create_instance("alicia_base", user="userB")
# state: affinity=60, mood="happy"

# Misma personalidad, diferente estado
```

**Analogía:** Es como "instalar una app" - cada usuario tiene su propia instalación.

---

### Snapshots

```python
# Usuario quiere backup
snapshot = export_snapshot(session_a)
save("backup_oct_14.json", snapshot)

# Semanas después, restaurar
session_restored = import_snapshot("backup_oct_14.json")
# Exactamente como estaba el 14 de octubre
```

**Analogía:** Es como un "save game" - guardas el progreso.

---

## 📊 Propuesta de Valor Completa

### LuminoraCore v1.0

> **"Estándar JSON para definir personalidades AI"**

**Ofrecía:**
- ✅ Templates de personalidades
- ✅ Validación de schema
- ✅ Compilación para LLMs
- ❌ No evolución de personalidad

---

### LuminoraCore v1.1

> **"Estándar completo para personalidades AI adaptativas con memoria"**

**Ofrece:**
- ✅ **Templates** - Define personalidades (como v1.0)
- ✅ **Instances** - Gestiona estado y evolución (NUEVO)
- ✅ **Snapshots** - Exporta/importa estados completos (NUEVO)
- ✅ **Memory System** - Memoria episódica + semantic search (NUEVO)
- ✅ **Adaptive Personalities** - Moods + niveles (NUEVO)

**El estándar JSON ahora cubre:**
1. Cómo DEFINIR personalidades (Templates)
2. Cómo CONFIGURAR comportamiento adaptativo (Template extensions)
3. Cómo EXPORTAR estados (Snapshots)

---

## ✅ Respuestas Rápidas

### "¿El JSON se actualiza?"

**Templates: NO**
**Snapshots: NO (son fotos, inmutables)**
**Estado: SÍ, pero en BBDD (no en JSON)**

---

### "¿Recompila cada mensaje?"

**SÍ, pero toma solo 5ms (irrelevante vs 1500ms del LLM)**

---

### "¿Personalidad evoluciona?"

**SÍ:**
- Template define comportamientos POSIBLES
- Instance evoluciona con uso (affinity, facts, mood)
- Snapshot captura evolución en JSON

---

### "¿Dónde persiste?"

- **Templates:** Archivos JSON (inmutables)
- **Instances:** BBDD (tu elección: SQLite, PostgreSQL, etc.)
- **Snapshots:** Archivos JSON (exportados cuando quieras)

---

### "¿Qué pasa con BBDD actuales?"

**Se agregan tablas nuevas, NO se reemplazan las existentes.**

```sql
-- Antes (v1.0)
sessions
messages

-- Después (v1.1)
sessions            ← Sin cambios
messages            ← Sin cambios
user_affinity       ← NUEVA
session_moods       ← NUEVA
user_facts          ← NUEVA
episodes            ← NUEVA
message_embeddings  ← NUEVA (opcional)
```

---

### "¿Vector search reemplaza SQLite/JSON?"

**NO. Es ADICIONAL (opcional).**

```
SQLite/PostgreSQL → Almacena mensajes, facts, episodios
pgvector/Pinecone → Solo para búsqueda semántica

Puedes usar SQLite sin vector search ✅
O usar PostgreSQL con pgvector ✅
O usar MongoDB sin vector search ✅
```

---

### "¿Es más lento?"

**NO. Background tasks no bloquean.**

```
Sin v1.1:
Usuario → LLM → Respuesta
          1500ms

Con v1.1:
Usuario → LLM → Respuesta (1555ms)
          Background tasks (400ms, async)
          
Overhead: 55ms en foreground (3.5%)
```

---

## 🎨 Visualización del Sistema

```
                    DESARROLLADOR
                         │
                         │ Crea
                         ▼
                  ┌──────────────┐
                  │  TEMPLATE    │
                  │ alicia.json  │
                  │  (Estándar)  │
                  └──────┬───────┘
                         │
                         │ Usa en app
                         ▼
                    APLICACIÓN
                         │
           ┌─────────────┼─────────────┐
           │             │             │
           ▼             ▼             ▼
      ┌─────────┐  ┌─────────┐  ┌─────────┐
      │Instance │  │Instance │  │Instance │
      │ Diego   │  │ María   │  │ Carlos  │
      │ aff=45  │  │ aff=10  │  │ aff=80  │
      │ mood=shy│  │mood=neu │  │mood=hap │
      └────┬────┘  └────┬────┘  └────┬────┘
           │            │            │
           │ Exporta    │            │
           ▼            │            │
      ┌─────────┐       │            │
      │Snapshot │       │            │
      │backup   │       │            │
      └─────────┘       │            │
                        │            │
                        ▼            ▼
                  ┌──────────────────────┐
                  │   BBDD (Shared)      │
                  │   PostgreSQL/SQLite  │
                  │                      │
                  │ - Affinity de todos  │
                  │ - Facts de todos     │
                  │ - Episodes de todos  │
                  └──────────────────────┘
```

---

## 📋 Checklist: ¿Qué Necesito?

### Para Usar LuminoraCore v1.1

- [ ] **Template JSON** (una o varias personalidades)
  - Puedes usar las incluidas (alicia, mika, etc.)
  - O crear tus propias

- [ ] **BBDD** (para guardar estado)
  - Opción 1: SQLite (simple)
  - Opción 2: PostgreSQL (producción)
  - Opción 3: MongoDB (flexible)

- [ ] **Caché** (opcional pero recomendado)
  - Redis (velocidad)
  - O memoria local

- [ ] **Vector Search** (OPCIONAL)
  - pgvector (PostgreSQL extension)
  - O Pinecone (cloud)
  - O sin vector search (semantic search deshabilitado)

---

### Mínimo para Funcionar

```python
# Configuración mínima v1.1
client = LuminoraCoreClient(
    storage_config={
        "backend": "sqlite",
        "database": "luminora.db"
    }
)

# Cargar template
template = "alicia_base.json"

# Crear session
session = await client.create_session(template, user_id="diego")

# Chatear
response = await client.send_message(session, "Hola")

# ✅ Funciona!
# - Template: alicia_base.json (archivo)
# - Estado: luminora.db (SQLite)
# - Sin Redis: OK (más lento pero funciona)
# - Sin pgvector: OK (sin semantic search)
```

---

## 🎯 Decisión: ¿Qué Features Habilitar?

### Configuración Mínima (Simple)

```python
memory_config = MemoryConfig(
    enable_episodic_memory=False,   # No episodios
    enable_fact_extraction=False,   # No extracción automática
    enable_semantic_search=False    # No vector search
)

personality_config = PersonalityConfig(
    enable_hierarchical=True,       # SÍ niveles (no requiere nada extra)
    enable_moods=False,             # No moods (más simple)
    enable_adaptation=False         # No adaptación contextual
)
```

**Requiere:**
- Template JSON ✅
- SQLite ✅
- Nada más

**Ventajas:**
- Simple
- Rápido
- Sin dependencias extra

**Desventajas:**
- No memoria de largo plazo
- No búsqueda semántica
- Solo niveles de relación

---

### Configuración Media (Balanceada)

```python
memory_config = MemoryConfig(
    enable_episodic_memory=True,    # Episodios importantes
    enable_fact_extraction=True,    # Extracción automática
    enable_semantic_search=False    # Sin vector search (por ahora)
)

personality_config = PersonalityConfig(
    enable_hierarchical=True,       # Niveles de relación
    enable_moods=True,              # Moods dinámicos
    enable_adaptation=True          # Adaptación contextual
)
```

**Requiere:**
- Template JSON ✅
- SQLite o PostgreSQL ✅
- API de LLM (para extracción) ✅

**Ventajas:**
- Memoria episódica funcional
- Personalidades adaptativas
- Sin vector search (más simple)

**Desventajas:**
- No semantic search ("recuerdas cuando...")

---

### Configuración Full (Máximo)

```python
memory_config = MemoryConfig(
    enable_episodic_memory=True,
    enable_fact_extraction=True,
    enable_semantic_search=True     # Vector search habilitado
)

personality_config = PersonalityConfig(
    enable_hierarchical=True,
    enable_moods=True,
    enable_adaptation=True
)
```

**Requiere:**
- Template JSON ✅
- PostgreSQL con pgvector ✅ (o Pinecone)
- API de embeddings (OpenAI) ✅
- Redis (recomendado) ✅

**Ventajas:**
- Todas las features
- Mejor experiencia de usuario
- Semantic search completo

**Desventajas:**
- Más complejo
- Más costos (embeddings API)

---

## 🚀 Conclusión

### LuminoraCore v1.1 es:

**Un sistema de TRES capas:**

1. **Templates (JSON)** - El estándar para DEFINIR personalidades
2. **Instances (BBDD)** - El runtime que EJECUTA personalidades
3. **Snapshots (JSON)** - El formato para EXPORTAR estados

**Todo sigue siendo JSON-based:**
- Templates son JSON ✅
- Snapshots son JSON ✅
- Estado runtime está en BBDD (por performance) ✅

**El estándar JSON se EXTIENDE, no se abandona.**

---

## 📊 Tabla Comparativa Final

| Aspecto | v1.0 | v1.1 | ¿Mantiene propuesta de valor? |
|---------|------|------|-------------------------------|
| **Templates JSON** | ✅ | ✅ | ✅ SÍ |
| **Portable** | ✅ | ✅ Templates + Snapshots | ✅ SÍ |
| **Estándar** | ✅ | ✅ Extendido | ✅ SÍ |
| **Evolución** | ❌ | ✅ Via instances | ✅ MEJORA |
| **Memoria** | ⚠️ Básica | ✅ Avanzada | ✅ MEJORA |
| **Exportable** | ⚠️ Solo template | ✅ Template + Snapshots | ✅ MEJORA |

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

**LuminoraCore v1.1 - Templates, Instances & Snapshots**

</div>

