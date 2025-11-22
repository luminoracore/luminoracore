# LuminoraCore SDK - Personality Module

Módulo de gestión de personalidades AI para el SDK.

---

## 📋 Componentes

### 1. PersonalityBlender (`blender.py`)

**Propósito:** Mezcla de personalidades AI con integración Core.

**Características:**
- ✅ Mezcla de múltiples personalidades
- ✅ Pesos personalizados
- ✅ Integración con Core PersonaBlend (v1.2.0)
- ✅ Fallback a implementación propia
- ✅ Cache de blends
- ✅ 100% Backward Compatible

**Uso:**
```python
from luminoracore_sdk.personality import PersonalityBlender

blender = PersonalityBlender()
result = await blender.blend_personalities(
    personalities=[personality1, personality2],
    weights=[0.6, 0.4],
    blend_name="blended_personality"
)
```

**Integración Core (v1.2.0):**
- Usa `luminoracore.tools.blender.PersonaBlend` cuando disponible
- Fallback automático si Core no está disponible
- Transparente para el usuario

---

### 2. PersonaBlendAdapter (`adapter.py`)

**Propósito:** Adapter para usar Core PersonaBlend con API del SDK.

**Características:**
- ✅ Traduce entre SDK (PersonalityData) y Core (Personality)
- ✅ Maneja diferencias async/sync
- ✅ Conversión de estructuras de datos
- ✅ Validación de inputs

**Uso:**
```python
from luminoracore_sdk.personality import PersonaBlendAdapter

adapter = PersonaBlendAdapter()
result = await adapter.blend_personalities(
    personalities=[personality1, personality2],
    weights=[0.6, 0.4],
    blend_name="blended"
)
```

**Conversiones:**
- `PersonalityData` (SDK) → `Personality` (Core)
- `Personality` (Core) → `PersonalityData` (SDK)
- Maneja diferencias en estructura de datos

---

### 3. PersonalityManager (`manager.py`)

**Propósito:** Gestión de personalidades (carga, almacenamiento, búsqueda).

**Características:**
- ✅ Carga de personalidades desde archivos
- ✅ Carga desde directorios
- ✅ Validación de personalidades
- ✅ Almacenamiento en memoria
- ✅ Búsqueda y filtrado

**Uso:**
```python
from luminoracore_sdk.personality import PersonalityManager

manager = PersonalityManager(personalities_dir="./personalities")
await manager.load_personalities_from_directory()

personality = await manager.get_personality("dr_luna")
```

---

### 4. PersonalityValidator (`validator.py`)

**Propósito:** Validación de personalidades.

**Características:**
- ✅ Validación de estructura
- ✅ Validación de campos requeridos
- ✅ Validación de tipos
- ✅ Validación de valores

**Uso:**
```python
from luminoracore_sdk.personality import PersonalityValidator

validator = PersonalityValidator()
await validator.validate_personality_config(config)
```

---

## 🆕 v1.2.0 - Core Integration

### Adapter Pattern

**Nuevo:** `PersonaBlendAdapter` permite usar Core PersonaBlend manteniendo API del SDK.

**Beneficios:**
- ✅ Elimina duplicación de código
- ✅ Usa implementación Core (más robusta)
- ✅ 100% Backward Compatible
- ✅ Fallback automático si Core no disponible

**Flujo:**
```
PersonalityBlender.blend_personalities()
    ↓
PersonaBlendAdapter.blend_personalities()
    ↓
Core PersonaBlend.blend() (sync, ejecutado en executor)
    ↓
Conversión Core → SDK
    ↓
Retorna PersonalityData
```

---

## 📊 Arquitectura

```
PersonalityBlender
    ├── PersonaBlendAdapter (v1.2.0)
    │   ├── Core PersonaBlend
    │   └── Conversión SDK ↔ Core
    └── Fallback Implementation (si Core no disponible)
        └── Implementación propia del SDK

PersonalityManager
    ├── PersonalityValidator
    └── Storage (memoria)
```

---

## 🔄 Flujo de Blending

### Con Core (v1.2.0)

```
1. PersonalityBlender.blend_personalities()
2. Valida inputs
3. Genera cache key
4. PersonaBlendAdapter.blend_personalities()
5. Convierte SDK PersonalityData → Core Personality
6. Core PersonaBlend.blend() (en executor)
7. Convierte Core Personality → SDK PersonalityData
8. Cache resultado
9. Retorna PersonalityData
```

### Sin Core (Fallback)

```
1. PersonalityBlender.blend_personalities()
2. Valida inputs
3. Genera cache key
4. _perform_blend() (implementación propia)
5. Cache resultado
6. Retorna PersonalityData
```

---

## 🔧 Conversión de Datos

### SDK → Core

```python
PersonalityData {
    name: str
    description: str
    system_prompt: str
    metadata: dict
    core_traits: dict
}
    ↓
Personality {
    persona: {
        name: str
        description: str
        ...
    }
    core_traits: {...}
    linguistic_profile: {...}
    behavioral_rules: [...]
    metadata: {...}
}
```

### Core → SDK

```python
Personality {
    persona: {...}
    core_traits: {...}
    ...
}
    ↓
PersonalityData {
    name: str
    description: str
    system_prompt: str
    metadata: dict
    core_traits: dict
}
```

---

## 🐛 Troubleshooting

### Error: "luminoracore not available"

**Solución:** Es normal si Core no está instalado. PersonalityBlender usa fallback automáticamente.

### Error: "Personality not found"

**Solución:** Asegúrate de cargar la personalidad antes de usarla:
```python
await manager.load_personality("name", config)
```

### Error: "Weights must sum to 1.0"

**Solución:** Normaliza los pesos:
```python
total = sum(weights)
weights = [w / total for w in weights]
```

---

## 📚 Más Información

- **Client Documentation:** `../client.py`
- **Types:** `../types/personality.py`
- **Core Integration:** `../../luminoracore/tools/blender.py`
- **Architecture:** `../../../ARCHITECTURE.md`

---

**Última Actualización:** 2025-11-21  
**Versión SDK:** 1.2.0  
**Estado:** ✅ Módulo completo y funcionando

