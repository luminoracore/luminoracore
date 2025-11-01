# ✅ Fix: Package Data para Personalidades

**Fecha:** 2025-01-27  
**Prioridad:** ⚠️ **CRÍTICO**  
**Estado:** ✅ **APLICADO**

---

## 📋 Problema Identificado

### Síntoma

El equipo de backend reportó que en la Lambda Layer v75 **solo 3 personalidades** están disponibles (fallback hardcodeado), en lugar de las **11 personalidades** que existen en el SDK.

### Diagnóstico

**Causa raíz:** Los archivos JSON de personalidades NO se incluyen en el paquete cuando se instala con `pip install`.

**Análisis técnico:**

1. **SDK tiene 11 personalidades:**
   - `grandma_hope.json`
   - `dr_luna.json`
   - `dr_luna_v1_1.json`
   - `captain_hook.json`
   - `professor_stern.json`
   - `lila_charm.json`
   - `victoria_sterling.json`
   - `zero_cool.json`
   - `alex_digital.json`
   - `marcus_sarcastic.json`
   - `rocky_inspiration.json`

2. **`setup.py` tiene package_data:**
   ```python
   package_data={
       'luminoracore_sdk': ['personalities/*.json'],
   },
   ```
   ✅ Correcto

3. **`pyproject.toml` NO tenía package_data:**
   ```toml
   [tool.setuptools.packages.find]
   where = ["."]
   include = ["luminoracore*"]
   # ❌ FALTA: [tool.setuptools.package-data]
   ```

4. **Build moderno usa `pyproject.toml`:**
   - Los builds modernos de Python (PEP 517/518) priorizan `pyproject.toml`
   - Si falta la declaración en `pyproject.toml`, los JSON NO se incluyen
   - `pip install` solo instala archivos `.py`, no archivos de datos

5. **Resultado en Lambda:**
   ```
   /opt/python/
     luminoracore_sdk/
       personalities/  ← Directorio NO existe o está vacío
   ```

---

## ✅ Solución Aplicada

### Cambio 1: Agregar package-data en pyproject.toml

**Archivo:** `luminoracore-sdk-python/pyproject.toml`  
**Después de línea 94:**

```toml
[tool.setuptools.package-data]
luminoracore_sdk = ["personalities/*.json"]
```

### Cambio 2: Actualizar versión

**Archivos modificados:**
- `pyproject.toml`: `version = "1.1.2"`
- `__version__.py`: `__version__ = "1.1.2"`

---

## 📊 Comparación: CORE vs SDK

### CORE (Correcto desde el inicio)

**`setup.py`:**
```python
package_data={
    'luminoracore': ['schema/*.json', 'personalities/*.json'],
},
```

**`pyproject.toml`:**
```toml
[tool.setuptools.package-data]
luminoracore = ["schema/*.json", "personalities/*.json"]
```

✅ **Resultado:** Las personalidades se incluyen correctamente.

---

### SDK (Corregido ahora)

**`setup.py`:** ✅ Ya tenía package_data
```python
package_data={
    'luminoracore_sdk': ['personalities/*.json'],
},
```

**`pyproject.toml` (ANTES):**
```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["luminoracore*"]
# ❌ FALTABA package-data
```

**`pyproject.toml` (AHORA):**
```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["luminoracore*"]

[tool.setuptools.package-data]
luminoracore_sdk = ["personalities/*.json"]  # ✅ AGREGADO
```

✅ **Resultado:** Las personalidades ahora se incluirán correctamente.

---

## 🔬 Verificación

### Test Local

Para verificar que el fix funciona:

```bash
# Instalar en entorno limpio
python -m venv test_env
source test_env/bin/activate  # Windows: test_env\Scripts\activate

# Instalar el paquete
cd luminoracore-sdk-python
pip install -e .

# Verificar que los JSON están accesibles
python -c "
from pathlib import Path
import luminoracore_sdk
sdk_path = Path(luminoracore_sdk.__file__).parent
personalities_dir = sdk_path / 'personalities'
json_files = list(personalities_dir.glob('*.json'))
print(f'Personalidades encontradas: {len(json_files)}')
for f in json_files:
    print(f'  - {f.name}')
"
```

**Resultado esperado:**
```
Personalidades encontradas: 11
  - grandma_hope.json
  - dr_luna.json
  - dr_luna_v1_1.json
  - captain_hook.json
  - professor_stern.json
  - lila_charm.json
  - victoria_sterling.json
  - zero_cool.json
  - alex_digital.json
  - marcus_sarcastic.json
  - rocky_inspiration.json
```

---

### Test en Lambda Layer

Después de construir nueva layer:

```bash
# En el Dockerfile, después de pip install
RUN python -c "
import os
from pathlib import Path
sdk_path = Path('/opt/python/luminoracore_sdk')
personalities = list((sdk_path / 'personalities').glob('*.json'))
print(f'Lambda Layer - Personalidades: {len(personalities)}')
assert len(personalities) >= 11, f'Solo {len(personalities)} personalidades encontradas'
"
```

---

## 📦 Impacto en Deployment

### Lambda Layer v76 (Nueva versión requerida)

**Cambios necesarios:**

1. ✅ SDK actualizado a v1.1.2 (con fix de package_data)
2. ⏳ Reconstruir Lambda Layer con nuevo SDK
3. ⏳ Subir a AWS como v76
4. ⏳ Actualizar `serverless.yml` con nuevo ARN
5. ⏳ Redesplegar API

**Estructura esperada en Lambda Layer v76:**

```
/opt/python/
  luminoracore/
    personalities/
      grandma_hope.json
      dr_luna.json
      ... (12 archivos)
  
  luminoracore_sdk/
    personalities/  ← AHORA EXISTIRÁ Y TENDRÁ CONTENIDO
      grandma_hope.json
      dr_luna.json
      dr_luna_v1_1.json
      captain_hook.json
      professor_stern.json
      lila_charm.json
      victoria_sterling.json
      zero_cool.json
      alex_digital.json
      marcus_sarcastic.json
      rocky_inspiration.json
```

---

## 🎯 Resultado Esperado

### API `/api/v1/personalities`

**Antes (Layer v75):**
```json
{
  "personalities": [
    "Dr. Luna",
    "Grandma Hope", 
    "Captain Hook"
  ],
  "total": 3,
  "source": "fallback"
}
```

**Después (Layer v76):**
```json
{
  "personalities": [
    "Grandma Hope",
    "Dr. Luna",
    "Dr. Luna (v1.1)",
    "Captain Hook",
    "Professor Stern",
    "Lila Charm",
    "Victoria Sterling",
    "Zero Cool",
    "Alex Digital",
    "Marcus Sarcastic",
    "Rocky Inspiration"
  ],
  "total": 11,
  "source": "framework"
}
```

---

## 📝 Changelog v1.1.2

### Fixed
- **[CRITICAL]** Package data configuration: Added missing `[tool.setuptools.package-data]` section in `pyproject.toml` to ensure personality JSON files are included when installing the package via pip
- Personality files now correctly included in distributions and Lambda Layers

### Technical Details
- Added `luminoracore_sdk = ["personalities/*.json"]` to `pyproject.toml`
- This fix is required for Python build tools that use PEP 517/518 (modern builds)
- The `setup.py` already had this configuration, but modern builds use `pyproject.toml`

---

## 🔗 Archivos Modificados

1. **`luminoracore-sdk-python/pyproject.toml`**
   - Línea 7: `version = "1.1.2"`
   - Líneas 96-97: Agregada sección `[tool.setuptools.package-data]`

2. **`luminoracore-sdk-python/luminoracore_sdk/__version__.py`**
   - Línea 3: `__version__ = "1.1.2"`
   - Línea 4: `__version_info__ = (1, 1, 2)`

---

## ⚠️ Importante

**Este fix es CRÍTICO porque:**

1. Sin él, el SDK solo tiene código Python pero NO los datos (personalidades)
2. Las personalidades son el contenido principal del framework
3. La API queda limitada a 3 personalidades hardcodeadas (fallback)
4. Los usuarios no pueden usar las 11 personalidades disponibles
5. Lambda Layer estaba "rota" en cuanto a contenido

**Por qué no se detectó antes:**

- En desarrollo local, cuando usas `-e .` (editable install), los archivos están disponibles porque apuntan al directorio fuente
- Solo se manifiesta cuando haces `pip install` real (como en Lambda Layer)
- El `setup.py` tenía la configuración, pero los builds modernos usan `pyproject.toml`

---

## ✅ Estado

- [x] **Fix aplicado** - package-data agregado en pyproject.toml
- [x] **Versión actualizada** - v1.1.2
- [x] **Documentado** - Este documento
- [ ] **Lambda Layer reconstruida** - Pendiente (equipo backend)
- [ ] **Desplegado** - Pendiente (equipo backend)
- [ ] **Verificado en producción** - Pendiente

---

**Fecha de Implementación:** 2025-01-27  
**Versión:** 1.1.2  
**Fix crítico:** Sí - Package data para personalidades

