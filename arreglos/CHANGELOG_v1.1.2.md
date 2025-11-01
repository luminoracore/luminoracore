# Changelog - LuminoraCore SDK v1.1.2

**Fecha de release:** 2025-01-27  
**Tipo:** Patch (Fix crítico)

---

## 🔴 [1.1.2] - 2025-01-27

### 🐛 Fixed (CRÍTICO)

#### Package Data Configuration
**Problema:** Los archivos JSON de personalidades NO se incluían cuando se instalaba el paquete con `pip install`.

**Causa:** Faltaba la configuración de `package-data` en `pyproject.toml`. Los builds modernos de Python (PEP 517/518) usan `pyproject.toml` en lugar de `setup.py`.

**Solución:** Agregada sección `[tool.setuptools.package-data]` en `pyproject.toml`:

```toml
[tool.setuptools.package-data]
luminoracore_sdk = ["personalities/*.json"]
```

**Impacto:**
- ✅ Las 11 personalidades ahora se incluyen correctamente en el paquete
- ✅ Lambda Layers ahora contendrán todos los archivos JSON
- ✅ La API podrá exponer todas las personalidades (no solo el fallback de 3)

**Archivos afectados:**
- `luminoracore-sdk-python/pyproject.toml`
- `luminoracore-sdk-python/luminoracore_sdk/__version__.py`

---

## 📊 Comparación de Versiones

### v1.1.1 (Anterior)
- ❌ Personalidades NO incluidas en pip install
- ❌ Lambda Layer sin archivos JSON
- ❌ API limitada a 3 personalidades (fallback)

### v1.1.2 (Actual)
- ✅ Personalidades incluidas correctamente
- ✅ Lambda Layer con todos los JSON
- ✅ API expone 11 personalidades

---

## 🔧 Fixes Acumulados desde v1.1.0

### v1.1.2 (Este release)
- [CRÍTICO] Package data: Personalidades incluidas en distribución

### v1.1.1 (Release anterior)
- [CRÍTICO] Import relativo corregido (`from .types.provider`)
- [CRÍTICO] Path de personalidades corregido (`.parent`)
- Carga de personalidades desde JSON implementada
- Construcción de prompts completos desde JSON
- Normalización de fact values a string
- Filtro de conversation_history en user_facts
- Cálculo dinámico de context_used
- Integración con luminoracore.find_personality_file()

---

## 📦 Instalación

### PyPI (Cuando se publique)
```bash
pip install luminoracore-sdk==1.1.2
```

### Desde Source
```bash
cd luminoracore-sdk-python
pip install -e .
```

### Lambda Layer
```bash
# Construir nueva layer v76 con este fix
docker build -f Dockerfile-layer-v76 -t luminoracore-layer:v76 .
```

---

## 🧪 Verificación

### Test rápido
```python
from pathlib import Path
import luminoracore_sdk

sdk_path = Path(luminoracore_sdk.__file__).parent
personalities_dir = sdk_path / 'personalities'
json_files = list(personalities_dir.glob('*.json'))

print(f"Personalidades disponibles: {len(json_files)}")
assert len(json_files) >= 11, "Faltan personalidades!"
```

**Output esperado:**
```
Personalidades disponibles: 11
```

---

## 🚀 Migration Guide

### Si estás usando v1.1.0 o v1.1.1

**No hay cambios breaking.** Solo actualiza:

```bash
pip install --upgrade luminoracore-sdk==1.1.2
```

### Si estás usando Lambda Layer

**IMPORTANTE:** Debes reconstruir la layer con v1.1.2:

1. Actualizar SDK a v1.1.2 en tu Dockerfile
2. Reconstruir la layer (será v76)
3. Subir a AWS Lambda
4. Actualizar `serverless.yml` con el nuevo ARN
5. Redesplegar tu API

---

## 📝 Notas Técnicas

### Por qué este fix es necesario

**Builds modernos de Python:**
- PEP 517: Especifica el sistema de build (`pyproject.toml`)
- PEP 518: Define dependencias de build
- Tools como `pip`, `build`, y `poetry` ahora usan `pyproject.toml` primero

**Antes del fix:**
- `setup.py` tenía `package_data` ✅
- `pyproject.toml` NO tenía `package_data` ❌
- Builds modernos (Lambda Layer) usaban `pyproject.toml`
- Resultado: Sin archivos JSON

**Después del fix:**
- Ambos archivos tienen la configuración ✅
- Funciona con builds antiguos y modernos ✅

### Archivos incluidos ahora

```
luminoracore_sdk/
  personalities/
    __init__.py
    _template.json
    alex_digital.json
    captain_hook.json
    dr_luna_v1_1.json
    dr_luna.json
    grandma_hope.json
    lila_charm.json
    marcus_sarcastic.json
    professor_stern.json
    rocky_inspiration.json
    victoria_sterling.json
    zero_cool.json
```

**Total:** 12 archivos (11 personalidades + 1 template)

---

## ⚠️ Breaking Changes

**Ninguno.** Este es un patch release que solo corrige un bug de packaging.

---

## 🔗 Referencias

- **Issue:** Framework no exponía personalidades en pip install
- **PR:** Fix package-data configuration in pyproject.toml
- **Docs:** [Packaging Python Projects](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/)

---

## 👥 Contributors

- LuminoraCore Team - Fix de package data

---

## 📅 Próximos Releases

### v1.1.3 (Planeado)
- Mejoras de performance en carga de personalidades
- Caché de personalidades compiladas
- Soporte para personalidades custom vía path

---

**Para más información, ver:**
- [Guía de instalación](../INSTALLATION_GUIDE.md)
- [Documentación completa](https://docs.luminoracore.com/sdk/python)
- [Ejemplos](../examples/)

---

**¿Questions o issues?** [Abre un issue en GitHub](https://github.com/luminoracore/sdk-python/issues)

