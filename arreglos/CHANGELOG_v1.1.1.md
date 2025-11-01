# Changelog - Versión 1.1.1

**Fecha:** 2025-01-27  
**Tipo:** Patch Release (Bug Fixes)

---

## 🔧 Fixes Críticos

### 1. Normalización de Fact Value

**Problema:** El frontend recibía facts con `value` como objeto (dict/list) en lugar de string, causando errores de renderizado.

**Solución:**
- Normalización automática de `value` a string durante la extracción de facts
- Normalización al leer facts desde DynamoDB
- Objetos y listas se serializan como JSON string

**Archivos afectados:**
- `conversation_memory_manager.py`
- `storage_dynamodb_flexible.py`

**Impacto:** ⚠️ **CRÍTICO** - Sin esto, el frontend falla al renderizar facts.

---

### 2. Filtro de Conversation History

**Problema:** Los turns de conversación (`conversation_history`) aparecían en `user_facts`, causando confusión en el frontend.

**Solución:**
- Filtrado automático para excluir `conversation_history` de `user_facts`
- Aplicado en todos los métodos de export y en el contexto de conversación

**Archivos afectados:**
- `conversation_memory_manager.py`
- `client_v1_1.py` (4 métodos: export_conversation, export_user_conversations, export_session, export_user_data)

**Impacto:** ⚠️ **IMPORTANTE** - El frontend espera solo facts reales del usuario.

---

### 3. Cálculo Correcto de context_used

**Problema:** `context_used` siempre era `True`, incluso en la primera conversación sin contexto previo.

**Solución:**
- Cálculo dinámico basado en existencia real de contexto
- `False` cuando no hay conversación previa ni facts del usuario
- `True` cuando hay conversación previa o facts existentes

**Archivos afectados:**
- `conversation_memory_manager.py`

**Impacto:** ⚠️ **MEDIO** - Mejora UX pero no bloquea funcionalidad.

---

## 📊 Estadísticas

- **Archivos modificados:** 3
- **Métodos modificados:** 7
- **Líneas modificadas:** ~62
- **Tests ejecutados:** 13
- **Tests pasados:** 13 ✅
- **Errores de linter:** 0 ✅

---

## ✅ Validaciones

Todos los fixes han sido validados con tests automatizados:

- ✅ Normalización de value (6 casos)
- ✅ Filtro conversation_history (5 casos)
- ✅ Cálculo context_used (8 casos)
- ✅ Imports y estructura del código
- ✅ Serialización JSON

---

## 🔄 Compatibilidad

**NO hay breaking changes.** Estos son fixes de bugs que mejoran el comportamiento sin cambiar la API.

**Compatibilidad:**
- ✅ API mantiene la misma estructura
- ✅ Los campos de respuesta son los mismos
- ✅ Solo cambia el contenido/valores de algunos campos
- ✅ Compatible con código existente del backend

---

## 📝 Notas para Usuarios

### Para el Equipo del Backend:

1. **Workaround de context_used:**
   - Si tenían un workaround calculando `context_used` en `chat.py`, pueden revisarlo
   - El framework ahora calcula correctamente, pueden usar el valor directamente

2. **Facts con value como objeto:**
   - Ya no ocurrirá, `value` siempre será string
   - Si tenían código manejando objetos, ya no es necesario

3. **Conversation history en user_facts:**
   - Ya no ocurrirá, `user_facts` solo contiene facts reales
   - Si tenían código filtrando esto, ya no es necesario

### Para el Frontend:

1. **value siempre será string:**
   - Pueden remover validaciones/convertidores de objeto a string
   - Si esperaban objetos, ahora recibirán JSON strings

2. **user_facts limpio:**
   - Ya no necesitan filtrar `conversation_history` manualmente
   - Solo recibirán facts reales del usuario

---

## 🚀 Upgrade Guide

**De 1.1.0 a 1.1.1:**

1. Actualizar el SDK/layer Lambda a versión 1.1.1
2. No se requieren cambios en el código
3. Opcional: Remover workarounds mencionados arriba
4. Ejecutar tests para verificar

---

## 📋 Referencias

- **Fix 1 y 2:** `arreglos/FIXES_FRONTEND_ISSUES_APLICADOS.md`
- **Fix 3:** `arreglos/FIX_CONTEXT_USED_APLICADO.md`
- **Validación:** `arreglos/VALIDACION_COMPLETA.md`
- **Resumen:** `arreglos/RESUMEN_CAMBIOS_PARA_NUEVA_VERSION.md`

---

**Versión anterior:** 1.1.0  
**Nueva versión:** 1.1.1  
**Tipo:** Patch (Bug Fixes)

