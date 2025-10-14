# Quick Reference - LuminoraCore v1.1

**Respuestas rápidas a las preguntas más comunes**

---

## 🎯 Modelo en Una Frase

> **LuminoraCore define Templates JSON (estándar compartible), ejecuta Instances (estado en BBDD), y exporta Snapshots (backup JSON).**

---

## ❓ Preguntas Frecuentes

### 1. ¿El JSON de personalidad se actualiza?

**NO.** El template JSON es **inmutable**.

```
Template (alicia.json)  → NO cambia nunca
Estado (PostgreSQL)     → SÍ cambia constantemente
Snapshot (backup.json)  → Foto del estado, NO cambia después de exportar
```

---

### 2. ¿Dónde persiste el estado?

**En BBDD** (tu elección: SQLite, PostgreSQL, MongoDB, etc.)

```sql
-- Estado del usuario Diego con Alicia
SELECT * FROM user_affinity WHERE user_id='diego';
→ affinity: 45, level: "friend"

SELECT * FROM session_moods WHERE session_id='session_123';
→ mood: "shy", intensity: 0.7

SELECT * FROM user_facts WHERE user_id='diego';
→ name: "Diego", favorite_anime: "Naruto"
```

---

### 3. ¿Se recompila con cada mensaje?

**SÍ, pero toma solo 5ms** (el LLM toma 1500ms, la compilación es irrelevante).

```
Compilar: 5ms (0.3% del tiempo)
LLM: 1500ms (99.7% del tiempo)
```

---

### 4. ¿Es más lento que v1.0?

**NO.** Overhead de solo ~55ms (3.5%), y el procesamiento pesado va en background.

```
v1.0: 1500ms (solo LLM)
v1.1: 1555ms (LLM + compilación + caché)
      + 400ms background (no bloquea)

Usuario ve respuesta igual de rápido
```

---

### 5. ¿Qué pasa con mis BBDD actuales?

**Siguen funcionando.** Solo se agregan tablas nuevas.

```
Antes (v1.0):
- sessions
- messages

Después (v1.1):
- sessions ← Sin cambios
- messages ← Sin cambios
- user_affinity ← NUEVA
- user_facts ← NUEVA
- episodes ← NUEVA
- (opcionales: message_embeddings, session_moods)
```

---

### 6. ¿BBDD vectorial reemplaza SQLite/JSON?

**NO.** Es **adicional** (solo para semantic search).

```
SQLite/PostgreSQL → Guarda mensajes, facts, episodios (SIEMPRE)
pgvector/Pinecone → Solo para búsqueda semántica (OPCIONAL)
```

Puedes usar v1.1 sin vector search ✅

---

### 7. ¿Cómo recupera recuerdos?

**Multi-source** (combina varias fuentes):

```python
# Usuario pregunta: "Recuerdas cuando hablamos de mi perro?"

# Sistema busca en paralelo:
1. Mensajes recientes (últimos 10) ← Siempre
2. Facts del usuario (pet_name="Max") ← Si existen
3. Episodios (búsqueda por tags) ← Si existen
4. Vector search (similitud semántica) ← Si habilitado

# Combina todo y lo envía al LLM
```

---

### 8. ¿Memoria del LLM o de LuminoraCore?

**Ambas se complementan:**

```
LLM Context Window (corto plazo):
- Últimos 10-20 mensajes
- Rápido, siempre disponible
- Limitado a ventana reciente

LuminoraCore Memory (largo plazo):
- Todos los mensajes (ilimitado)
- Facts, episodios, embeddings
- Búsqueda cuando se necesita

JUNTOS:
LLM recibe: mensajes recientes + memoria relevante de LuminoraCore
```

---

### 9. ¿Cómo se exporta el estado?

**Snapshots** (JSON exportado):

```python
# Exportar estado completo
snapshot = await client.export_snapshot(session_id)

# Guardar
save_json("backup.json", snapshot)

# Importar
new_session = await client.import_snapshot("backup.json")
# Restaura exactamente el estado guardado
```

---

### 10. ¿Casa con la propuesta de valor original?

**SÍ.** El estándar JSON ahora cubre:

1. **Templates** (v1.0) - Cómo definir personalidades
2. **Snapshots** (v1.1 nuevo) - Cómo exportar estados
3. **Instances** (v1.1 nuevo) - Cómo ejecutar personalidades

**El JSON sigue siendo el corazón del sistema.**

---

## 📊 Tres Capas (Resumen)

| | Template | Instance | Snapshot |
|---|----------|----------|----------|
| **Qué es** | Blueprint | Estado vivo | Foto del estado |
| **Formato** | JSON | BBDD | JSON |
| **Mutable** | ❌ | ✅ | ❌ |
| **Compartible** | ✅ | ❌ | ✅ |
| **Ejemplo** | alicia_base.json | affinity=45 en PostgreSQL | diego_backup.json |

---

## ⚡ Configuraciones Rápidas

### Mínima (Simple)

```python
LuminoraCoreClient(
    storage_config={"backend": "sqlite"},
    personality_config={"enable_hierarchical": True},
    memory_config={"enable_all": False}
)
```

**Requiere:** Template JSON + SQLite

---

### Recomendada (Balanceada)

```python
LuminoraCoreClient(
    storage_config={"backend": "postgresql"},
    personality_config={
        "enable_hierarchical": True,
        "enable_moods": True
    },
    memory_config={
        "enable_episodic_memory": True,
        "enable_fact_extraction": True,
        "enable_semantic_search": False
    }
)
```

**Requiere:** Template JSON + PostgreSQL

---

### Completa (Full Features)

```python
LuminoraCoreClient(
    storage_config={
        "backend": "postgresql",
        "cache": "redis",
        "vector_store": "pgvector"
    },
    personality_config={"enable_all": True},
    memory_config={"enable_all": True}
)
```

**Requiere:** Template JSON + PostgreSQL + Redis + pgvector

---

## 🔧 Comandos Útiles

```bash
# Crear template desde wizard
luminora-cli create-personality --version 1.1 --interactive

# Validar template
luminora-cli validate alicia.json

# Exportar snapshot
luminora-cli export-snapshot --session session_123 --output backup.json

# Importar snapshot
luminora-cli import-snapshot backup.json --user nuevo_usuario

# Migrar BBDD de v1.0 a v1.1
luminora-cli migrate --from 1.0 --to 1.1
```

---

## 📚 Documentos por Prioridad

### 🔥 DEBE LEER (Críticos)

1. [`RESUMEN_VISUAL.md`](./RESUMEN_VISUAL.md) (15 min) ⭐⭐⭐
2. [`MODELO_CONCEPTUAL_REVISADO.md`](./MODELO_CONCEPTUAL_REVISADO.md) (20 min) ⭐⭐⭐
3. [`FLUJO_DATOS_Y_PERSISTENCIA.md`](./FLUJO_DATOS_Y_PERSISTENCIA.md) (25 min) ⭐⭐⭐

**Total: 1 hora**

---

### 📖 DEBERÍA LEER (Importantes)

4. [`INTEGRACION_CON_SISTEMA_ACTUAL.md`](./INTEGRACION_CON_SISTEMA_ACTUAL.md) (20 min) ⭐⭐
5. [`EJEMPLOS_PERSONALIDADES_JSON.md`](./EJEMPLOS_PERSONALIDADES_JSON.md) (15 min) ⭐⭐

**Total: +35 min**

---

### 📚 LECTURA COMPLETA (Para implementar)

6. [`SISTEMA_MEMORIA_AVANZADO.md`](./SISTEMA_MEMORIA_AVANZADO.md) (45 min)
7. [`SISTEMA_PERSONALIDADES_JERARQUICAS.md`](./SISTEMA_PERSONALIDADES_JERARQUICAS.md) (40 min)
8. [`ARQUITECTURA_TECNICA.md`](./ARQUITECTURA_TECNICA.md) (35 min)
9. [`PLAN_IMPLEMENTACION.md`](./PLAN_IMPLEMENTACION.md) (30 min)
10. [`CASOS_DE_USO.md`](./CASOS_DE_USO.md) (25 min)

**Total: +2.75 horas**

---

## 💡 Conceptos Clave

### Template = Receta de Cocina

```
La receta de un pastel:
- Define ingredientes y pasos
- NO cambia cuando cocinas
- Puedes compartirla
- Múltiples personas pueden usarla

Template JSON:
- Define personalidad y comportamientos
- NO cambia con uso
- Puedes compartirlo
- Múltiples usuarios pueden usarlo
```

### Instance = Tu Pastel

```
Cuando cocinas:
- Sigues la receta
- Haces ajustes (más azúcar, menos harina)
- Tu pastel es único
- No modificas la receta original

Instance de personalidad:
- Sigue el template
- Aplica modificadores (affinity, mood)
- Tu conversación es única
- No modifica el template original
```

### Snapshot = Foto del Pastel

```
Sacas una foto:
- Captura cómo quedó
- Puedes compartirla
- Otros pueden intentar replicarlo
- La foto no cambia

Snapshot JSON:
- Captura estado completo
- Puedes compartirlo
- Otros pueden importarlo
- El snapshot no cambia
```

---

## ✅ Para Recordar

### El JSON Template NO se actualiza

```python
# ❌ NUNCA
personality_json["affinity"] = 45
save(personality_json)

# ✅ SIEMPRE
await db.update_affinity(session_id, 45)
```

### La Compilación es Rápida

```
Compilar: 5ms ≈ Irrelevante
LLM: 1500ms ≈ 99% del tiempo
```

### Background Tasks No Bloquean

```python
# Foreground (bloquea)
response = await llm.generate()  # 1500ms
return response  # Usuario ve aquí ✅

# Background (no bloquea)
asyncio.create_task(extract_facts())  # 300ms async
# Usuario NO espera esto
```

### Todo es Opcional

```python
# Puedes habilitar solo lo que necesites
enable_moods = True           # ✅
enable_hierarchical = True    # ✅
enable_semantic_search = False  # ❌ Disabled
enable_episodic_memory = True  # ✅
```

---

## 🎯 Próximos Pasos

1. **Si tienes dudas conceptuales:** Lee [`MODELO_CONCEPTUAL_REVISADO.md`](./MODELO_CONCEPTUAL_REVISADO.md)
2. **Si tienes dudas de performance:** Lee [`FLUJO_DATOS_Y_PERSISTENCIA.md`](./FLUJO_DATOS_Y_PERSISTENCIA.md)
3. **Si quieres ver código:** Lee [`EJEMPLOS_PERSONALIDADES_JSON.md`](./EJEMPLOS_PERSONALIDADES_JSON.md)
4. **Si quieres implementar:** Lee [`PLAN_IMPLEMENTACION.md`](./PLAN_IMPLEMENTACION.md)

---

<div align="center">

**Made with ❤️ by Ereace - Ruly Altamirano**

</div>

