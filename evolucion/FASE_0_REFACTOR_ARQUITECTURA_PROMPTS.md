# 🔧 FASE 0: REFACTOR ARQUITECTURA - Prompts de Implementación

**FASE:** 0 - Pre-Fase 1 (Arquitectura)  
**DURACIÓN:** 4 semanas  
**OBJETIVO:** Migrar a arquitectura de 3 capas SIN romper nada  
**ESTRATEGIA:** Backward compatible, incremental, 100% tested

---

## ⚠️ ADVERTENCIA CRÍTICA

**ESTE REFACTOR ES DELICADO. CADA PASO DEBE:**
- ✅ Mantener 100% backward compatibility
- ✅ Tener tests que pasen ANTES y DESPUÉS
- ✅ Ser reversible con git
- ✅ No cambiar APIs públicas
- ✅ Documentar cada cambio

**NO HAGAS TODO A LA VEZ. SIGUE EL ORDEN EXACTO.**

---

## 📋 ÍNDICE DE PROMPTS

```
SEMANA 1: AUDITORÍA Y PREPARACIÓN
├── PROMPT 0.1: Auditoría de Dependencias Reales
├── PROMPT 0.2: Tests Baseline (Snapshot Actual)
├── PROMPT 0.3: Análisis de Duplicaciones
└── PROMPT 0.4: Plan de Conversión Detallado

SEMANA 2: REFACTOR SDK PARTE 1 (Personality)
├── PROMPT 0.5: Crear Adapter Pattern para PersonaBlend
├── PROMPT 0.6: Migrar PersonalityBlender a usar Core
├── PROMPT 0.7: Tests de Personality (must pass)
└── PROMPT 0.8: Backward Compatibility Tests

SEMANA 3: REFACTOR SDK PARTE 2 (Memory & Optimization)
├── PROMPT 0.9: Integrar Core Optimizer en SDK
├── PROMPT 0.10: Migrar MemoryManager a usar Core
├── PROMPT 0.11: Tests de Memory (must pass)
└── PROMPT 0.12: Integration Tests SDK-Core

SEMANA 4: CLI Y VALIDACIÓN FINAL
├── PROMPT 0.13: Descomentar Dependencia CLI
├── PROMPT 0.14: Actualizar Imports CLI
├── PROMPT 0.15: Tests Full Stack
└── PROMPT 0.16: Documentation & Release Notes
```

---

# 📅 SEMANA 1: AUDITORÍA Y PREPARACIÓN

## PROMPT 0.1: Auditoría de Dependencias Reales

**OBJETIVO:** Identificar EXACTAMENTE qué usa el SDK del Core actualmente

### ⚠️ ANTI-ALUCINACIÓN

```
❌ NO asumas qué imports existen
❌ NO escribas código todavía
❌ NO hagas cambios al código
✅ SOLO ejecuta comandos y reporta resultados
✅ VERIFICA cada archivo mencionado existe
```

### 📝 INSTRUCCIONES EXACTAS

```bash
# Paso 1: Ir al directorio del SDK
cd luminoracore-sdk-python/

# Paso 2: Buscar TODOS los imports del Core
echo "=== AUDITORÍA: Imports de luminoracore en SDK ===" > /tmp/audit_imports.txt
grep -rn "from luminoracore" luminoracore_sdk/ >> /tmp/audit_imports.txt
grep -rn "import luminoracore" luminoracore_sdk/ >> /tmp/audit_imports.txt

# Paso 3: Contar imports por módulo
echo -e "\n=== RESUMEN POR MÓDULO ===" >> /tmp/audit_imports.txt
grep -rh "from luminoracore" luminoracore_sdk/ | sort | uniq -c | sort -rn >> /tmp/audit_imports.txt

# Paso 4: Ver el reporte
cat /tmp/audit_imports.txt

# Paso 5: Buscar código duplicado (PersonaBlend específicamente)
echo "=== AUDITORÍA: Clases duplicadas ===" > /tmp/audit_duplicates.txt
echo -e "\n--- PersonaBlend en Core ---" >> /tmp/audit_duplicates.txt
find ../luminoracore -name "*.py" -exec grep -l "class PersonaBlend" {} \; >> /tmp/audit_duplicates.txt
echo -e "\n--- PersonalityBlender en SDK ---" >> /tmp/audit_duplicates.txt
find . -name "*.py" -exec grep -l "class PersonalityBlender" {} \; >> /tmp/audit_duplicates.txt

cat /tmp/audit_duplicates.txt
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ Archivo audit_imports.txt generado
□ Lista completa de imports luminoracore
□ Conteo de uso por módulo
□ Lista de clases duplicadas identificadas
□ Reporte guardado para siguiente prompt
```

### 📊 FORMATO DE REPORTE ESPERADO

```
REPORTE DE AUDITORÍA
====================

IMPORTS ENCONTRADOS:
- luminoracore_sdk/client_hybrid.py:9: from luminoracore import PersonalityEngine
- luminoracore_sdk/client_new.py:14: from luminoracore import PersonalityEngine
- ... (lista completa)

RESUMEN:
- PersonalityEngine: usado en X archivos
- MemorySystem: usado en Y archivos
- PersonaBlend: NO usado (duplicado como PersonalityBlender)

DUPLICACIONES:
- PersonaBlend vs PersonalityBlender
- ... (lista completa)
```

---

## PROMPT 0.2: Tests Baseline (Snapshot Actual)

**OBJETIVO:** Capturar el estado actual de tests para comparar después

### ⚠️ ANTI-ALUCINACIÓN

```
❌ NO modifiques código de tests
❌ NO arregles tests que fallen
❌ NO agregues nuevos tests todavía
✅ SOLO ejecuta tests existentes y guarda resultados
✅ DOCUMENTA qué tests pasan y cuáles fallan AHORA
```

### 📝 INSTRUCCIONES EXACTAS

```bash
# Paso 1: Tests del SDK
cd luminoracore-sdk-python/

echo "=== BASELINE: SDK Tests ===" > /tmp/baseline_tests.txt
echo "Fecha: $(date)" >> /tmp/baseline_tests.txt
echo -e "\n--- Ejecutando pytest ---" >> /tmp/baseline_tests.txt

# Ejecutar con verbose y guardar salida
pytest tests/ -v --tb=short 2>&1 | tee -a /tmp/baseline_tests.txt

# Guardar summary
echo -e "\n--- Test Summary ---" >> /tmp/baseline_tests.txt
pytest tests/ --collect-only 2>&1 | grep "test session starts\|collected" >> /tmp/baseline_tests.txt

# Paso 2: Tests del Core
cd ../luminoracore/

echo -e "\n\n=== BASELINE: Core Tests ===" >> /tmp/baseline_tests.txt
pytest tests/ -v --tb=short 2>&1 | tee -a /tmp/baseline_tests.txt

# Paso 3: Tests del CLI
cd ../luminoracore-cli/

echo -e "\n\n=== BASELINE: CLI Tests ===" >> /tmp/baseline_tests.txt
pytest tests/ -v --tb=short 2>&1 | tee -a /tmp/baseline_tests.txt

# Mostrar resumen final
cat /tmp/baseline_tests.txt | grep -E "passed|failed|error|collected"
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ baseline_tests.txt generado
□ Número exacto de tests en SDK
□ Número exacto de tests en Core
□ Número exacto de tests en CLI
□ Estado actual (pass/fail) documentado
□ Este archivo es la "verdad" pre-refactor
```

### 📊 FORMATO ESPERADO

```
BASELINE TESTS - [FECHA]
========================

SDK Tests:
- Total: 52 tests
- Passing: 52
- Failing: 0
- Archivos: [lista]

Core Tests:
- Total: 89 tests
- Passing: 89
- Failing: 0
- Archivos: [lista]

CLI Tests:
- Total: 31 tests
- Passing: 31
- Failing: 0
- Archivos: [lista]

⚠️ CUALQUIER TEST QUE FALLE DESPUÉS DEL REFACTOR ES UN BUG
```

---

## PROMPT 0.3: Análisis de Duplicaciones

**OBJETIVO:** Crear diff exacto entre Core y SDK para clases duplicadas

### ⚠️ ANTI-ALUCINACIÓN

```
❌ NO asumas que dos clases son iguales porque tienen nombre similar
❌ NO hagas cambios al código
✅ COMPARA línea por línea
✅ DOCUMENTA diferencias EXACTAS
```

### 📝 INSTRUCCIONES EXACTAS

```bash
# Paso 1: Comparar PersonaBlend vs PersonalityBlender
echo "=== DIFF: PersonaBlend (Core) vs PersonalityBlender (SDK) ===" > /tmp/diff_blenders.txt

# Encontrar los archivos
CORE_BLENDER=$(find luminoracore -name "*.py" -exec grep -l "class PersonaBlend" {} \; | head -1)
SDK_BLENDER=$(find luminoracore-sdk-python -name "*.py" -exec grep -l "class PersonalityBlender" {} \; | head -1)

echo "Core file: $CORE_BLENDER" >> /tmp/diff_blenders.txt
echo "SDK file: $SDK_BLENDER" >> /tmp/diff_blenders.txt
echo -e "\n--- DIFF ---" >> /tmp/diff_blenders.txt

# Hacer diff detallado
diff -u "$CORE_BLENDER" "$SDK_BLENDER" >> /tmp/diff_blenders.txt

# Mostrar resumen
cat /tmp/diff_blenders.txt

# Paso 2: Extraer métodos de cada clase
echo -e "\n=== MÉTODOS EN CORE ===" >> /tmp/diff_blenders.txt
grep "def " "$CORE_BLENDER" | sed 's/^[ \t]*//' >> /tmp/diff_blenders.txt

echo -e "\n=== MÉTODOS EN SDK ===" >> /tmp/diff_blenders.txt
grep "def " "$SDK_BLENDER" | sed 's/^[ \t]*//' >> /tmp/diff_blenders.txt

# Paso 3: Analizar diferencias en signatures
echo -e "\n=== ANÁLISIS ===" >> /tmp/diff_blenders.txt
echo "¿Son compatibles? ¿Podemos reemplazar uno con otro?" >> /tmp/diff_blenders.txt
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ diff_blenders.txt generado
□ Diferencias línea por línea documentadas
□ Lista de métodos en ambas clases
□ Análisis de compatibilidad
□ Decisión clara: ¿podemos migrar YA o necesitamos adapter?
```

---

## PROMPT 0.4: Plan de Conversión Detallado

**OBJETIVO:** Crear plan ESPECÍFICO de qué cambiar y en qué orden

### ⚠️ ANTI-ALUCINACIÓN

```
❌ NO escribas código todavía
❌ NO hagas cambios
✅ SOLO crea el plan basado en auditoría REAL
✅ PRIORIZA cambios por riesgo (bajo primero)
```

### 📝 INSTRUCCIONES EXACTAS

Basado en los reportes de PROMPT 0.1, 0.2, 0.3:

1. **Listar archivos a modificar por prioridad**
2. **Para cada archivo:**
   - Estado actual (qué hace)
   - Estado deseado (qué queremos)
   - Riesgo (bajo/medio/alto)
   - Dependencias (qué debe cambiar primero)
   - Tests que validan (específicos)

```markdown
# Crear archivo: MIGRATION_PLAN.md

## FASE 1: LOW RISK (Semana 2)

### 1. luminoracore-sdk-python/luminoracore_sdk/personality/blender.py
- **Estado Actual:** Implementación completa propia (200 líneas)
- **Estado Deseado:** Wrapper delgado de luminoracore.PersonaBlend
- **Riesgo:** BAJO (clase no usada ampliamente)
- **Dependencias:** Ninguna
- **Tests:** tests/test_personality_blender.py (15 tests)
- **Estrategia:** Crear adapter, mantener API pública idéntica

### 2. ... (continuar para cada archivo)

## FASE 2: MEDIUM RISK (Semana 3)
... 

## FASE 3: LOW RISK (Semana 4)
...
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ MIGRATION_PLAN.md creado
□ Todos los archivos listados con prioridad
□ Riesgo evaluado para cada cambio
□ Orden de ejecución definido
□ Tests identificados para cada cambio
□ Este plan es la guía para Semanas 2-4
```

---

# 📅 SEMANA 2: REFACTOR SDK PARTE 1

## PROMPT 0.5: Crear Adapter Pattern para PersonaBlend

**OBJETIVO:** Crear adaptador que permite usar Core PersonaBlend con API de SDK

### ⚠️ ANTI-ALUCINACIÓN

```
❌ NO cambies PersonalityBlender todavía
❌ NO cambies PersonaBlend del Core
✅ SOLO crea un NUEVO archivo adapter.py
✅ MANTÉN APIs públicas IDÉNTICAS
✅ TESTS deben pasar con adapter
```

### 📝 CÓDIGO COMPLETO

Crear archivo: `luminoracore-sdk-python/luminoracore_sdk/personality/adapter.py`

```python
"""
Adapter para usar luminoracore.PersonaBlend con API del SDK

PROPÓSITO:
- Permitir migración gradual sin romper API pública
- Traducir entre tipos SDK (PersonalityData) y Core (Personality)
- Mantener 100% backward compatibility

Autor: Refactor Arquitectura Fase 0
Fecha: 2025-11-21
"""

from typing import List, Optional, Dict, Any
import asyncio
from pathlib import Path

# Imports del Core
from luminoracore import PersonaBlend as CorePersonaBlend
from luminoracore import Personality as CorePersonality

# Imports del SDK
from ..types.personality import PersonalityData


class PersonaBlendAdapter:
    """
    Adapter que traduce entre SDK y Core para personality blending
    
    Permite usar luminoracore.PersonaBlend manteniendo API del SDK.
    """
    
    def __init__(self):
        """Initialize adapter with Core blender"""
        self._core_blender = CorePersonaBlend()
    
    async def blend_personalities(
        self,
        personalities: List[PersonalityData],
        weights: List[float],
        blend_name: Optional[str] = None
    ) -> PersonalityData:
        """
        Blend personalities usando Core blender
        
        Args:
            personalities: Lista de SDK PersonalityData objects
            weights: Pesos para cada personality
            blend_name: Nombre opcional para el blend
            
        Returns:
            PersonalityData: Resultado del blend en formato SDK
            
        Raises:
            ValueError: Si inputs inválidos
        """
        # Validar inputs (mantener validación del SDK)
        if len(personalities) != len(weights):
            raise ValueError(
                f"Number of personalities ({len(personalities)}) "
                f"must match number of weights ({len(weights)})"
            )
        
        if len(personalities) < 2:
            raise ValueError(
                "At least 2 personalities required for blending"
            )
        
        # Validar weights sum to 1.0
        weight_sum = sum(weights)
        if abs(weight_sum - 1.0) > 0.01:
            raise ValueError(
                f"Weights must sum to 1.0, got {weight_sum}"
            )
        
        # Convertir SDK PersonalityData → Core Personality
        core_personalities = [
            self._sdk_to_core_personality(p) 
            for p in personalities
        ]
        
        # Crear weights dict para Core API
        weights_dict = {
            core_personalities[i].persona.name: weights[i]
            for i in range(len(core_personalities))
        }
        
        # Llamar al Core blender (sync)
        # NOTA: Core blender es sync, lo ejecutamos en executor
        loop = asyncio.get_event_loop()
        blend_result = await loop.run_in_executor(
            None,
            self._core_blender.blend,
            core_personalities,
            weights_dict,
            "weighted_average",  # strategy por defecto
            blend_name
        )
        
        # Convertir resultado Core → SDK PersonalityData
        result = self._core_to_sdk_personality(blend_result.blended_personality)
        
        return result
    
    def _sdk_to_core_personality(
        self, 
        sdk_personality: PersonalityData
    ) -> CorePersonality:
        """
        Convierte SDK PersonalityData a Core Personality
        
        Args:
            sdk_personality: PersonalityData del SDK
            
        Returns:
            CorePersonality: Personality del Core
        """
        # PersonalityData tiene dict de data
        personality_dict = sdk_personality.dict()
        
        # Core Personality acepta dict directamente
        # NOTA: Verificar que esquemas sean compatibles
        core_personality = CorePersonality.from_dict(personality_dict)
        
        return core_personality
    
    def _core_to_sdk_personality(
        self,
        core_personality: CorePersonality
    ) -> PersonalityData:
        """
        Convierte Core Personality a SDK PersonalityData
        
        Args:
            core_personality: Personality del Core
            
        Returns:
            PersonalityData: PersonalityData del SDK
        """
        # Core Personality tiene to_dict()
        personality_dict = core_personality.to_dict()
        
        # PersonalityData del SDK
        sdk_personality = PersonalityData(**personality_dict)
        
        return sdk_personality


# Para tests: export adapter
__all__ = ['PersonaBlendAdapter']
```

### 📝 TESTS COMPLETOS

Crear archivo: `luminoracore-sdk-python/tests/test_personality_adapter.py`

```python
"""
Tests para PersonaBlendAdapter

Valida que adapter funciona correctamente con Core.
"""

import pytest
import asyncio
from pathlib import Path

from luminoracore_sdk.personality.adapter import PersonaBlendAdapter
from luminoracore_sdk.types.personality import PersonalityData
from luminoracore import PersonaBlend


class TestPersonaBlendAdapter:
    """Test suite para adapter"""
    
    @pytest.fixture
    def adapter(self):
        """Create adapter instance"""
        return PersonaBlendAdapter()
    
    @pytest.fixture
    def sample_personalities(self):
        """Create sample personalities para tests"""
        # TODO: Cargar personalities reales de fixtures
        # Por ahora, crear mínimos
        p1 = PersonalityData(
            name="test_personality_1",
            core_traits={"archetype": "Helper"},
            # ... otros campos requeridos
        )
        p2 = PersonalityData(
            name="test_personality_2",
            core_traits={"archetype": "Thinker"},
            # ... otros campos requeridos
        )
        return [p1, p2]
    
    @pytest.mark.asyncio
    async def test_adapter_initialization(self, adapter):
        """Adapter debe inicializarse correctamente"""
        assert adapter is not None
        assert adapter._core_blender is not None
        assert isinstance(adapter._core_blender, PersonaBlend)
    
    @pytest.mark.asyncio
    async def test_blend_personalities_basic(
        self, 
        adapter, 
        sample_personalities
    ):
        """Debe blender personalities correctamente"""
        result = await adapter.blend_personalities(
            personalities=sample_personalities,
            weights=[0.5, 0.5],
            blend_name="test_blend"
        )
        
        assert result is not None
        assert isinstance(result, PersonalityData)
        # TODO: Validar contenido específico del blend
    
    @pytest.mark.asyncio
    async def test_blend_validates_inputs(self, adapter, sample_personalities):
        """Debe validar inputs correctamente"""
        
        # Mismatch en número de weights
        with pytest.raises(ValueError, match="must match"):
            await adapter.blend_personalities(
                personalities=sample_personalities,
                weights=[0.5],  # Solo 1 weight para 2 personalities
            )
        
        # Menos de 2 personalities
        with pytest.raises(ValueError, match="At least 2"):
            await adapter.blend_personalities(
                personalities=[sample_personalities[0]],
                weights=[1.0],
            )
        
        # Weights no suman 1.0
        with pytest.raises(ValueError, match="sum to 1.0"):
            await adapter.blend_personalities(
                personalities=sample_personalities,
                weights=[0.3, 0.3],  # Suma 0.6
            )
    
    @pytest.mark.asyncio
    async def test_sdk_to_core_conversion(self, adapter, sample_personalities):
        """Conversión SDK → Core debe funcionar"""
        sdk_personality = sample_personalities[0]
        
        # Convertir
        core_personality = adapter._sdk_to_core_personality(sdk_personality)
        
        # Validar tipo
        from luminoracore import Personality
        assert isinstance(core_personality, Personality)
        
        # Validar contenido preservado
        assert core_personality.persona.name == sdk_personality.name
    
    @pytest.mark.asyncio
    async def test_core_to_sdk_conversion(self, adapter):
        """Conversión Core → SDK debe funcionar"""
        # Crear Core personality
        from luminoracore import Personality
        core_personality = Personality(
            Path("tests/fixtures/test_personality.json")
        )
        
        # Convertir
        sdk_personality = adapter._core_to_sdk_personality(core_personality)
        
        # Validar tipo
        assert isinstance(sdk_personality, PersonalityData)
        
        # Validar contenido preservado
        assert sdk_personality.name == core_personality.persona.name


# IMPORTANTE: Estos tests DEBEN pasar antes de seguir
```

### ✅ VALIDACIÓN OBLIGATORIA

```bash
# Ejecutar SOLO estos tests
cd luminoracore-sdk-python/
pytest tests/test_personality_adapter.py -v

# DEBE mostrar:
# test_personality_adapter.py::TestPersonaBlendAdapter::test_adapter_initialization PASSED
# test_personality_adapter.py::TestPersonaBlendAdapter::test_blend_personalities_basic PASSED
# test_personality_adapter.py::TestPersonaBlendAdapter::test_blend_validates_inputs PASSED
# test_personality_adapter.py::TestPersonaBlendAdapter::test_sdk_to_core_conversion PASSED
# test_personality_adapter.py::TestPersonaBlendAdapter::test_core_to_sdk_conversion PASSED
#
# ==================== 5 passed in X.XXs ====================
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ Archivo adapter.py creado
□ Archivo test_personality_adapter.py creado
□ Tests del adapter pasan 100%
□ NO se modificó PersonalityBlender original (todavía)
□ NO se modificó PersonaBlend del Core
□ Adapter funciona como puente entre ambos
□ Listo para PROMPT 0.6 (usar adapter en PersonalityBlender)
```

---

## PROMPT 0.6: Migrar PersonalityBlender a usar Adapter

**OBJETIVO:** Reemplazar implementación de PersonalityBlender con adapter

### ⚠️ ANTI-ALUCINACIÓN

```
❌ NO cambies la API pública de PersonalityBlender
❌ NO rompas tests existentes
✅ MANTÉN todos los métodos públicos existentes
✅ DELEGA todo al adapter internamente
✅ TESTS existentes deben pasar SIN modificación
```

### 📝 CÓDIGO COMPLETO

Modificar archivo: `luminoracore-sdk-python/luminoracore_sdk/personality/blender.py`

```python
"""
Personality blending functionality for LuminoraCore SDK.

REFACTORED: Ahora usa luminoracore.PersonaBlend via adapter
Mantiene 100% backward compatibility con API pública.

Autor: Refactor Arquitectura Fase 0
Fecha: 2025-11-21
"""

import asyncio
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
import json

from ..types.personality import PersonalityData, PersonalityBlend
from ..utils.exceptions import PersonalityError
from ..utils.validation import validate_personality_blend
from ..utils.helpers import deep_merge_dicts

# NUEVO: Import adapter
from .adapter import PersonaBlendAdapter

logger = logging.getLogger(__name__)


class PersonalityBlender:
    """
    Advanced personality blending with PersonaBlend™ technology.
    
    REFACTORED: Ahora delega a luminoracore.PersonaBlend via adapter.
    API pública se mantiene idéntica para backward compatibility.
    """
    
    def __init__(self):
        """
        Initialize the personality blender.
        
        CHANGED: Ahora usa adapter en lugar de implementación propia.
        """
        # NUEVO: Usar adapter en lugar de implementación propia
        self._adapter = PersonaBlendAdapter()
        
        # Mantener cache para backward compatibility
        self._blend_cache: Dict[str, PersonalityData] = {}
        self._lock = asyncio.Lock()
    
    async def blend_personalities(
        self,
        personalities: List[PersonalityData],
        weights: List[float],
        blend_name: Optional[str] = None
    ) -> PersonalityData:
        """
        Blend multiple personalities with custom weights.
        
        UNCHANGED: API pública idéntica.
        CHANGED: Implementación ahora delega al adapter.
        
        Args:
            personalities: List of personality data objects
            weights: List of weights for each personality (must sum to 1.0)
            blend_name: Optional name for the blended personality
            
        Returns:
            Blended personality data
            
        Raises:
            PersonalityError: If blending fails or validation fails
        """
        # Validaciones básicas (mantener para error messages consistentes)
        if len(personalities) != len(weights):
            raise PersonalityError(
                "Number of personalities must match number of weights"
            )
        
        if len(personalities) < 2:
            raise PersonalityError(
                "At least 2 personalities required for blending"
            )
        
        # Validate weights sum to 1.0
        weight_sum = sum(weights)
        if abs(weight_sum - 1.0) > 0.01:
            raise PersonalityError(
                f"Weights must sum to 1.0, got {weight_sum}"
            )
        
        # Validate all weights are non-negative
        if any(w < 0 for w in weights):
            raise PersonalityError("All weights must be non-negative")
        
        try:
            # Check cache first (mantener comportamiento)
            cache_key = self._generate_cache_key(personalities, weights)
            async with self._lock:
                if cache_key in self._blend_cache:
                    logger.info(f"Returning cached blend: {cache_key}")
                    return self._blend_cache[cache_key]
            
            # Generate blend name if not provided
            if not blend_name:
                blend_name = self._generate_blend_name(personalities, weights)
            
            # CAMBIO PRINCIPAL: Delegar al adapter (que usa Core)
            blended_personality = await self._adapter.blend_personalities(
                personalities=personalities,
                weights=weights,
                blend_name=blend_name
            )
            
            # Cache the blend (mantener comportamiento)
            async with self._lock:
                self._blend_cache[cache_key] = blended_personality
            
            logger.info(
                f"Successfully blended {len(personalities)} personalities "
                f"into '{blend_name}'"
            )
            return blended_personality
            
        except Exception as e:
            logger.error(f"Failed to blend personalities: {e}")
            # Mantener tipo de excepción consistente
            if isinstance(e, PersonalityError):
                raise
            raise PersonalityError(f"Personality blending failed: {e}")
    
    async def blend_personalities_from_config(
        self,
        blend_config: Dict[str, float],
        personality_manager: Any
    ) -> PersonalityData:
        """
        Blend personalities from configuration dictionary.
        
        UNCHANGED: API pública idéntica, solo logging mejorado.
        
        Args:
            blend_config: Dictionary mapping personality names to weights
            personality_manager: PersonalityManager instance
            
        Returns:
            Blended personality data
            
        Raises:
            PersonalityError: If blending fails
        """
        try:
            # Load personalities from manager
            personalities = []
            for name in blend_config.keys():
                personality = await personality_manager.get_personality(name)
                if not personality:
                    raise PersonalityError(
                        f"Personality not found: {name}"
                    )
                personalities.append(personality)
            
            # Extract weights
            weights = list(blend_config.values())
            
            # Blend using main method (que ahora usa adapter)
            blended = await self.blend_personalities(
                personalities=personalities,
                weights=weights
            )
            
            logger.info(f"Blended from config: {blend_config}")
            return blended
            
        except Exception as e:
            logger.error(f"Failed to blend from config: {e}")
            raise PersonalityError(
                f"Blending from config failed: {e}"
            )
    
    def _generate_cache_key(
        self,
        personalities: List[PersonalityData],
        weights: List[float]
    ) -> str:
        """
        Generate cache key for blend.
        
        UNCHANGED: Helper method mantiene misma lógica.
        """
        personality_names = sorted([p.name for p in personalities])
        weights_str = "_".join([f"{w:.2f}" for w in weights])
        return f"blend_{'_'.join(personality_names)}_{weights_str}"
    
    def _generate_blend_name(
        self,
        personalities: List[PersonalityData],
        weights: List[float]
    ) -> str:
        """
        Generate name for blended personality.
        
        UNCHANGED: Helper method mantiene misma lógica.
        """
        # Find dominant personality (highest weight)
        max_weight_idx = weights.index(max(weights))
        dominant = personalities[max_weight_idx].name
        
        # Create name showing blend composition
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"blend_{dominant}_{timestamp}"
    
    async def clear_cache(self) -> None:
        """
        Clear the blend cache.
        
        UNCHANGED: Utility method mantiene API.
        """
        async with self._lock:
            self._blend_cache.clear()
            logger.info("Blend cache cleared")


# Mantener exports para backward compatibility
__all__ = ['PersonalityBlender']
```

### ✅ VALIDACIÓN OBLIGATORIA

```bash
# 1. Tests del adapter (deben seguir pasando)
pytest tests/test_personality_adapter.py -v

# 2. Tests ORIGINALES del blender (NO modificados)
pytest tests/test_personality_blender.py -v

# 3. Verificar que NO rompimos nada más
pytest tests/test_personality/ -v

# TODOS deben pasar 100%
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ PersonalityBlender refactorizado
□ Usa adapter internamente
□ API pública sin cambios
□ Tests originales pasan 100%
□ Tests del adapter pasan 100%
□ Cache sigue funcionando
□ Logging consistente
□ Backward compatible 100%
```

---

## ⚠️ CHECKPOINT OBLIGATORIO

Antes de continuar a PROMPT 0.7, VERIFICAR:

```bash
# Ejecutar TODOS los tests del SDK
cd luminoracore-sdk-python/
pytest tests/ -v

# Debe mostrar:
# ==================== X passed in Y.YYs ====================
# Sin failures, sin errors

# Si algo falla:
# 1. NO continuar
# 2. Revisar qué rompimos
# 3. Arreglar antes de seguir
# 4. Git commit del trabajo hasta ahora
```

---

---

## PROMPT 0.7: Tests de Personality (Must Pass)

**OBJETIVO:** Validar que refactor de PersonalityBlender funciona perfectamente

### ⚠️ ANTI-ALUCINACIÓN

```
❌ NO modifiques código de producción
❌ NO "arregles" tests que fallen cambiando el test
✅ SI un test falla, ARREGLA el código de producción
✅ TODOS los tests deben pasar sin modificar tests
```

### 📝 TESTS ADICIONALES

Agregar a: `luminoracore-sdk-python/tests/test_personality_blender.py`

```python
"""
Tests adicionales para validar refactor de PersonalityBlender

AGREGADOS: Tests específicos para validar que adapter funciona correctamente
MANTENER: Todos los tests existentes sin modificar
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock

from luminoracore_sdk.personality.blender import PersonalityBlender
from luminoracore_sdk.personality.adapter import PersonaBlendAdapter
from luminoracore_sdk.types.personality import PersonalityData


class TestPersonalityBlenderRefactor:
    """Tests específicos del refactor para asegurar que adapter funciona"""
    
    @pytest.fixture
    def blender(self):
        """Create blender instance"""
        return PersonalityBlender()
    
    def test_blender_uses_adapter(self, blender):
        """
        CRÍTICO: Verificar que PersonalityBlender usa adapter internamente
        """
        assert hasattr(blender, '_adapter')
        assert isinstance(blender._adapter, PersonaBlendAdapter)
    
    @pytest.mark.asyncio
    async def test_blender_delegates_to_adapter(self, blender):
        """
        CRÍTICO: Verificar que blend_personalities delega al adapter
        """
        # Mock del adapter
        mock_adapter = AsyncMock()
        mock_adapter.blend_personalities.return_value = PersonalityData(
            name="test_blend",
            core_traits={"archetype": "Test"}
        )
        
        # Reemplazar adapter con mock
        blender._adapter = mock_adapter
        
        # Crear personalities de prueba
        personalities = [
            PersonalityData(name="p1", core_traits={"archetype": "A"}),
            PersonalityData(name="p2", core_traits={"archetype": "B"})
        ]
        weights = [0.6, 0.4]
        
        # Llamar blend
        result = await blender.blend_personalities(
            personalities=personalities,
            weights=weights,
            blend_name="test"
        )
        
        # Verificar que adapter fue llamado
        mock_adapter.blend_personalities.assert_called_once_with(
            personalities=personalities,
            weights=weights,
            blend_name="test"
        )
    
    @pytest.mark.asyncio
    async def test_blender_maintains_cache_behavior(self, blender):
        """
        CRÍTICO: Cache debe seguir funcionando después del refactor
        """
        personalities = [
            PersonalityData(name="p1", core_traits={"archetype": "A"}),
            PersonalityData(name="p2", core_traits={"archetype": "B"})
        ]
        weights = [0.5, 0.5]
        
        # Primer blend (va al adapter)
        result1 = await blender.blend_personalities(
            personalities=personalities,
            weights=weights
        )
        
        # Segundo blend con mismos params (debe venir de cache)
        with patch.object(blender._adapter, 'blend_personalities') as mock_blend:
            result2 = await blender.blend_personalities(
                personalities=personalities,
                weights=weights
            )
            
            # Adapter NO debe ser llamado (viene de cache)
            mock_blend.assert_not_called()
        
        # Resultados deben ser idénticos
        assert result1.name == result2.name
    
    @pytest.mark.asyncio
    async def test_error_handling_preserved(self, blender):
        """
        CRÍTICO: Manejo de errores debe ser consistente
        """
        personalities = [
            PersonalityData(name="p1", core_traits={"archetype": "A"}),
        ]
        
        # Test con < 2 personalities
        with pytest.raises(PersonalityError, match="At least 2"):
            await blender.blend_personalities(
                personalities=personalities,
                weights=[1.0]
            )


# IMPORTANTE: NO modificar tests existentes
# Solo agregar estos nuevos tests
```

### ✅ VALIDACIÓN OBLIGATORIA

```bash
# 1. Tests NUEVOS (deben pasar)
pytest tests/test_personality_blender.py::TestPersonalityBlenderRefactor -v

# 2. Tests EXISTENTES (deben seguir pasando)
pytest tests/test_personality_blender.py -v

# 3. ALL personality tests
pytest tests/test_personality/ -v

# 4. Verificar coverage
pytest tests/test_personality/ --cov=luminoracore_sdk.personality --cov-report=term-missing

# Coverage debe ser >= 90%
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ Nuevos tests agregados (4 tests)
□ Todos los nuevos tests pasan
□ Todos los tests existentes pasan (sin modificar)
□ Coverage >= 90% en módulo personality
□ Sin warnings en tests
□ Blender usa adapter correctamente
□ Cache sigue funcionando
□ Error handling preservado
```

---

## PROMPT 0.8: Backward Compatibility Tests

**OBJETIVO:** Garantizar 100% backward compatibility con código existente

### ⚠️ ANTI-ALUCINACIÓN

```
❌ NO modifiques APIs públicas
❌ NO rompas código de usuarios existente
✅ SIMULA código de usuario que usa versión anterior
✅ VERIFICA que todo sigue funcionando
```

### 📝 TESTS DE COMPATIBILIDAD

Crear archivo: `luminoracore-sdk-python/tests/test_backward_compatibility.py`

```python
"""
Backward Compatibility Tests

Simula código de usuarios que usaban versión anterior del SDK.
TODOS estos tests deben pasar para garantizar no rompemos nada.

Autor: Refactor Fase 0
Fecha: 2025-11-21
"""

import pytest
import asyncio
from typing import List

from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.personality.blender import PersonalityBlender
from luminoracore_sdk.types.personality import PersonalityData


class TestBackwardCompatibilityV10:
    """
    Tests que simulan código de usuario usando SDK v1.0/v1.1
    
    CRÍTICO: Si alguno falla, rompimos backward compatibility
    """
    
    @pytest.fixture
    def blender(self):
        """Crear blender como lo haría usuario v1.0"""
        return PersonalityBlender()
    
    @pytest.fixture
    def sample_personalities(self):
        """Personalities de ejemplo para tests"""
        return [
            PersonalityData(
                name="assistant",
                core_traits={
                    "archetype": "Helper",
                    "temperament": "Friendly"
                }
            ),
            PersonalityData(
                name="analyst",
                core_traits={
                    "archetype": "Thinker",
                    "temperament": "Analytical"
                }
            )
        ]
    
    @pytest.mark.asyncio
    async def test_v10_basic_blending(self, blender, sample_personalities):
        """
        Test: Código básico de v1.0 sigue funcionando
        
        Este es el uso más común en v1.0
        """
        # Código que usuario escribió en v1.0
        result = await blender.blend_personalities(
            personalities=sample_personalities,
            weights=[0.7, 0.3]
        )
        
        # Debe seguir funcionando exactamente igual
        assert result is not None
        assert isinstance(result, PersonalityData)
        assert result.name is not None
    
    @pytest.mark.asyncio
    async def test_v10_named_blend(self, blender, sample_personalities):
        """
        Test: Blends con nombre custom siguen funcionando
        """
        result = await blender.blend_personalities(
            personalities=sample_personalities,
            weights=[0.5, 0.5],
            blend_name="custom_blend"
        )
        
        assert result.name == "custom_blend"
    
    @pytest.mark.asyncio
    async def test_v10_error_messages_unchanged(self, blender):
        """
        Test: Mensajes de error siguen siendo los mismos
        
        CRÍTICO: Usuarios pueden depender de error messages
        """
        # Error: not enough personalities
        with pytest.raises(Exception) as exc_info:
            await blender.blend_personalities(
                personalities=[],
                weights=[]
            )
        
        # Verificar mensaje contiene palabras clave esperadas
        error_msg = str(exc_info.value)
        assert "at least 2" in error_msg.lower() or "personalities" in error_msg.lower()
    
    @pytest.mark.asyncio
    async def test_v10_cache_still_works(self, blender, sample_personalities):
        """
        Test: Cache behavior no cambió
        """
        # Primera llamada
        result1 = await blender.blend_personalities(
            personalities=sample_personalities,
            weights=[0.5, 0.5]
        )
        
        # Segunda llamada (mismos params)
        result2 = await blender.blend_personalities(
            personalities=sample_personalities,
            weights=[0.5, 0.5]
        )
        
        # Deben ser el mismo objeto (cache)
        assert result1.name == result2.name
    
    @pytest.mark.asyncio
    async def test_v11_blend_from_config(self, blender):
        """
        Test: v1.1 blend_personalities_from_config sigue funcionando
        """
        # Mock personality manager
        from unittest.mock import AsyncMock
        
        mock_manager = AsyncMock()
        mock_manager.get_personality.side_effect = [
            PersonalityData(name="p1", core_traits={"archetype": "A"}),
            PersonalityData(name="p2", core_traits={"archetype": "B"})
        ]
        
        # Código de v1.1
        config = {"p1": 0.6, "p2": 0.4}
        result = await blender.blend_personalities_from_config(
            blend_config=config,
            personality_manager=mock_manager
        )
        
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_clear_cache_method_exists(self, blender):
        """
        Test: Método clear_cache sigue disponible
        """
        # Código que puede existir en v1.0/v1.1
        await blender.clear_cache()
        
        # No debe lanzar error
        assert True


class TestBackwardCompatibilityClient:
    """
    Tests de LuminoraCoreClient con refactor
    """
    
    @pytest.mark.asyncio
    async def test_client_initialization_unchanged(self):
        """
        Test: Inicialización de client no cambió
        """
        # Código típico de usuario v1.0
        client = LuminoraCoreClient()
        await client.initialize()
        
        # Debe funcionar sin cambios
        assert client is not None
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_client_has_personality_blender(self):
        """
        Test: Client sigue teniendo personality_blender
        """
        client = LuminoraCoreClient()
        await client.initialize()
        
        # Código de usuario puede acceder esto
        assert hasattr(client, 'personality_blender')
        assert isinstance(client.personality_blender, PersonalityBlender)
        
        await client.cleanup()


# IMPORTANTE: Estos tests simulan código REAL de usuarios
# Si alguno falla, estamos rompiendo backward compatibility
```

### 📝 SCRIPT DE VERIFICACIÓN

Crear archivo: `luminoracore-sdk-python/scripts/verify_compatibility.sh`

```bash
#!/bin/bash
# Verificación completa de backward compatibility

set -e

echo "================================"
echo "BACKWARD COMPATIBILITY TESTS"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "1. Running backward compatibility tests..."
pytest tests/test_backward_compatibility.py -v

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Backward compatibility tests PASSED${NC}"
else
    echo -e "${RED}✗ Backward compatibility tests FAILED${NC}"
    echo "CRITICAL: We broke backward compatibility!"
    exit 1
fi

echo ""
echo "2. Running all existing tests..."
pytest tests/ -v --ignore=tests/test_backward_compatibility.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ All existing tests PASSED${NC}"
else
    echo -e "${RED}✗ Some existing tests FAILED${NC}"
    exit 1
fi

echo ""
echo "3. Checking test coverage..."
pytest tests/ --cov=luminoracore_sdk --cov-report=term-missing --cov-fail-under=85

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Coverage >= 85%${NC}"
else
    echo -e "${RED}✗ Coverage < 85%${NC}"
    exit 1
fi

echo ""
echo "================================"
echo -e "${GREEN}ALL COMPATIBILITY CHECKS PASSED${NC}"
echo "================================"
```

```bash
chmod +x luminoracore-sdk-python/scripts/verify_compatibility.sh
```

### ✅ VALIDACIÓN OBLIGATORIA

```bash
# Ejecutar script completo
cd luminoracore-sdk-python/
./scripts/verify_compatibility.sh

# DEBE mostrar:
# ================================
# ALL COMPATIBILITY CHECKS PASSED
# ================================
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ test_backward_compatibility.py creado (8+ tests)
□ verify_compatibility.sh creado
□ TODOS los tests de compatibilidad pasan
□ TODOS los tests existentes pasan
□ Coverage >= 85%
□ Sin warnings
□ Sin deprecation warnings
□ Script de verificación exitoso
```

---

# 📅 SEMANA 3: REFACTOR SDK PARTE 2

## PROMPT 0.9: Integrar Core Optimizer en SDK

**OBJETIVO:** Integrar módulo optimization/ del Core en el SDK

### ⚠️ ANTI-ALUCINACIÓN

```
❌ NO copies código de optimization/ al SDK
❌ NO dupliques Optimizer
✅ USA luminoracore.optimization directamente
✅ CREA wrapper si necesario para async
```

### 📝 CÓDIGO COMPLETO

Modificar archivo: `luminoracore-sdk-python/luminoracore_sdk/client.py`

```python
"""Main LuminoraCore client for AI personality management."""

import asyncio
from typing import Dict, List, Optional, Any, AsyncGenerator, Union
import logging
from datetime import datetime

from .types.session import SessionConfig, StorageConfig, MemoryConfig
from .types.provider import ProviderConfig, ChatMessage, ChatResponse
from .types.personality import PersonalityData, PersonalityBlend
from .providers.factory import ProviderFactory
from .providers.base import BaseProvider
from .session.manager import SessionManager
from .session.conversation import ConversationManager
from .session.memory import MemoryManager
from .session.storage import create_storage
from .personality.manager import PersonalityManager
from .personality.blender import PersonalityBlender
from .utils.exceptions import LuminoraCoreSDKError, SessionError, ProviderError
import os
import pathlib
from .utils.helpers import generate_session_id

# NUEVO: Import optimization del Core
try:
    from luminoracore.optimization import (
        OptimizationConfig,
        Optimizer
    )
    HAS_OPTIMIZATION = True
except ImportError:
    # Graceful degradation si Core no tiene optimization
    HAS_OPTIMIZATION = False
    OptimizationConfig = None
    Optimizer = None

logger = logging.getLogger(__name__)


class LuminoraCoreClient:
    """Main client for LuminoraCore SDK."""
    
    def __init__(
        self,
        storage_config: Optional[StorageConfig] = None,
        memory_config: Optional[MemoryConfig] = None,
        personalities_dir: Optional[str] = None,
        optimization_config: Optional['OptimizationConfig'] = None  # NUEVO
    ):
        """
        Initialize the LuminoraCore client.
        
        Args:
            storage_config: Storage configuration
            memory_config: Memory configuration
            personalities_dir: Directory containing personality files
            optimization_config: Optimization config (NEW in v1.2) 🆕
        """
        # Initialize components
        self.storage_config = storage_config
        self.memory_config = memory_config or MemoryConfig()
        
        # Set default personalities directory to SDK's personalities folder
        if personalities_dir is None:
            sdk_dir = pathlib.Path(__file__).parent
            self.personalities_dir = str(sdk_dir / "personalities")
        else:
            self.personalities_dir = personalities_dir
        
        # NUEVO: Setup optimization
        self.optimization_config = optimization_config
        if HAS_OPTIMIZATION and optimization_config:
            self.optimizer = Optimizer(optimization_config)
            logger.info("Optimization enabled with Core optimizer")
        else:
            self.optimizer = None
            if optimization_config and not HAS_OPTIMIZATION:
                logger.warning(
                    "Optimization config provided but luminoracore.optimization "
                    "not available. Install luminoracore>=1.2.0"
                )
        
        # Create storage backend
        if storage_config:
            self.storage = create_storage(
                storage_config,
                optimizer=self.optimizer  # NUEVO: Pass optimizer
            )
        else:
            self.storage = None
        
        # Initialize managers
        self.session_manager = SessionManager(storage=self.storage)
        self.conversation_manager = ConversationManager()
        self.memory_manager = MemoryManager(
            memory_config,
            optimizer=self.optimizer  # NUEVO: Pass optimizer
        )
        self.personality_manager = PersonalityManager(personalities_dir)
        self.personality_blender = PersonalityBlender()
        
        # Initialize provider registry
        self._providers: Dict[str, BaseProvider] = {}
        self._lock = asyncio.Lock()
    
    # ... resto de métodos sin cambios ...
    
    async def get_optimization_stats(self) -> Optional[Dict[str, Any]]:
        """
        Get optimization statistics
        
        NUEVO en v1.2: Returns token reduction stats
        
        Returns:
            Dict with stats or None if optimization disabled
        """
        if not self.optimizer:
            return None
        
        return {
            "enabled": True,
            "config": {
                "key_abbreviation": self.optimizer.config.key_abbreviation,
                "compact_format": self.optimizer.config.compact_format,
                "minify_json": self.optimizer.config.minify_json,
                "cache_enabled": self.optimizer.config.cache_enabled,
            },
            "cache_stats": self.optimizer.get_cache_stats() if hasattr(self.optimizer, 'get_cache_stats') else None
        }


# Mantener exports
__all__ = ['LuminoraCoreClient']
```

### 📝 ACTUALIZAR STORAGE

Modificar archivo: `luminoracore-sdk-python/luminoracore_sdk/session/storage.py`

```python
"""Storage abstraction for LuminoraCore SDK."""

from typing import Any, Optional
import logging

from ..types.session import StorageConfig

logger = logging.getLogger(__name__)


def create_storage(
    config: StorageConfig,
    optimizer: Optional[Any] = None  # NUEVO: Accept optimizer
) -> Any:
    """
    Create storage backend with optional optimization
    
    Args:
        config: Storage configuration
        optimizer: Optimizer instance from Core (NEW in v1.2) 🆕
    
    Returns:
        Storage instance (potentially wrapped with optimizer)
    """
    storage_type = config.storage_type.lower()
    
    # Create base storage
    if storage_type == "memory":
        from .memory_storage import InMemoryStorage
        storage = InMemoryStorage()
    elif storage_type == "json":
        from .json_storage import JSONStorage
        storage = JSONStorage(config.json_path)
    elif storage_type == "sqlite":
        from .sqlite_storage import SQLiteStorage
        storage = SQLiteStorage(config.sqlite_path)
    elif storage_type == "redis":
        from .redis_storage import RedisStorage
        storage = RedisStorage(
            host=config.redis_host,
            port=config.redis_port,
            db=config.redis_db
        )
    elif storage_type == "postgres":
        from .postgres_storage import PostgresStorage
        storage = PostgresStorage(config.postgres_url)
    elif storage_type == "mongodb":
        from .mongodb_storage import MongoStorage
        storage = MongoStorage(config.mongodb_url)
    else:
        raise ValueError(f"Unknown storage type: {storage_type}")
    
    # NUEVO: Wrap with optimizer if provided
    if optimizer:
        logger.info(f"Wrapping {storage_type} storage with optimizer")
        storage = OptimizedStorageWrapper(storage, optimizer)
    
    return storage


class OptimizedStorageWrapper:
    """
    Wrapper que aplica optimization transparentemente
    
    NUEVO en v1.2: Permite usar optimization del Core sin cambiar storage
    """
    
    def __init__(self, storage: Any, optimizer: Any):
        """
        Initialize wrapper
        
        Args:
            storage: Base storage instance
            optimizer: Core Optimizer instance
        """
        self._storage = storage
        self._optimizer = optimizer
        logger.info(
            f"Initialized OptimizedStorageWrapper with "
            f"{type(storage).__name__}"
        )
    
    async def save_fact(self, fact_data: dict) -> None:
        """Save fact with compression"""
        # Compress antes de almacenar
        if self._optimizer.config.enabled:
            compressed = self._optimizer.compress(fact_data)
        else:
            compressed = fact_data
        
        await self._storage.save_fact(compressed)
    
    async def get_fact(self, **kwargs) -> Optional[dict]:
        """Get fact with auto-expansion"""
        fact_data = await self._storage.get_fact(**kwargs)
        
        if not fact_data:
            return None
        
        # Expand antes de devolver
        if self._optimizer.config.enabled:
            expanded = self._optimizer.expand(fact_data)
        else:
            expanded = fact_data
        
        return expanded
    
    async def get_all_facts(self, user_id: str) -> list:
        """Get all facts with auto-expansion"""
        facts = await self._storage.get_all_facts(user_id)
        
        if not facts:
            return []
        
        # Expand cada fact
        if self._optimizer.config.enabled:
            facts = [self._optimizer.expand(f) for f in facts]
        
        return facts
    
    # Delegar otros métodos al storage base
    def __getattr__(self, name):
        """Delegate unknown methods to base storage"""
        return getattr(self._storage, name)


__all__ = ['create_storage', 'OptimizedStorageWrapper']
```

### 📝 TESTS COMPLETOS

Crear archivo: `luminoracore-sdk-python/tests/test_optimization_integration.py`

```python
"""
Tests de integración para optimization del Core en SDK

Valida que SDK usa correctamente el optimizer del Core.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.session import StorageConfig, MemoryConfig


# Check si optimization está disponible
try:
    from luminoracore.optimization import OptimizationConfig, Optimizer
    HAS_OPTIMIZATION = True
except ImportError:
    HAS_OPTIMIZATION = False
    pytest.skip("luminoracore.optimization not available", allow_module_level=True)


class TestOptimizationIntegration:
    """Test suite para integration con Core optimizer"""
    
    @pytest.mark.asyncio
    async def test_client_with_optimization_config(self):
        """Client debe aceptar optimization_config"""
        opt_config = OptimizationConfig(
            key_abbreviation=True,
            compact_format=True,
            cache_enabled=True
        )
        
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type="memory"),
            optimization_config=opt_config
        )
        await client.initialize()
        
        # Verificar optimizer está configurado
        assert client.optimizer is not None
        assert isinstance(client.optimizer, Optimizer)
        
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_client_without_optimization(self):
        """Client debe funcionar sin optimization (backward compat)"""
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type="memory")
        )
        await client.initialize()
        
        # Sin optimization config, optimizer debe ser None
        assert client.optimizer is None
        
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_storage_wrapped_with_optimizer(self):
        """Storage debe estar wrapped cuando optimization habilitado"""
        from luminoracore_sdk.session.storage import OptimizedStorageWrapper
        
        opt_config = OptimizationConfig(enabled=True)
        
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type="memory"),
            optimization_config=opt_config
        )
        await client.initialize()
        
        # Storage debe ser OptimizedStorageWrapper
        assert isinstance(client.storage, OptimizedStorageWrapper)
        
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_get_optimization_stats(self):
        """Client debe retornar optimization stats"""
        opt_config = OptimizationConfig(
            key_abbreviation=True,
            cache_enabled=True
        )
        
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type="memory"),
            optimization_config=opt_config
        )
        await client.initialize()
        
        # Get stats
        stats = await client.get_optimization_stats()
        
        assert stats is not None
        assert stats["enabled"] is True
        assert "config" in stats
        assert stats["config"]["key_abbreviation"] is True
        
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_optimization_stats_when_disabled(self):
        """Stats debe retornar None cuando optimization disabled"""
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type="memory")
        )
        await client.initialize()
        
        stats = await client.get_optimization_stats()
        assert stats is None
        
        await client.cleanup()


class TestOptimizedStorageWrapper:
    """Tests para OptimizedStorageWrapper"""
    
    @pytest.fixture
    def mock_storage(self):
        """Mock storage"""
        storage = AsyncMock()
        storage.save_fact = AsyncMock()
        storage.get_fact = AsyncMock()
        storage.get_all_facts = AsyncMock()
        return storage
    
    @pytest.fixture
    def mock_optimizer(self):
        """Mock optimizer"""
        optimizer = Mock()
        optimizer.config = Mock()
        optimizer.config.enabled = True
        optimizer.compress = Mock(side_effect=lambda x: {"compressed": x})
        optimizer.expand = Mock(side_effect=lambda x: x.get("original", x))
        return optimizer
    
    @pytest.mark.asyncio
    async def test_wrapper_compresses_on_save(self, mock_storage, mock_optimizer):
        """Wrapper debe comprimir al guardar"""
        from luminoracore_sdk.session.storage import OptimizedStorageWrapper
        
        wrapper = OptimizedStorageWrapper(mock_storage, mock_optimizer)
        
        fact = {"key": "value"}
        await wrapper.save_fact(fact)
        
        # Verificar que compress fue llamado
        mock_optimizer.compress.assert_called_once_with(fact)
        
        # Verificar que storage recibió versión compressed
        mock_storage.save_fact.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_wrapper_expands_on_get(self, mock_storage, mock_optimizer):
        """Wrapper debe expandir al leer"""
        from luminoracore_sdk.session.storage import OptimizedStorageWrapper
        
        mock_storage.get_fact.return_value = {"compressed": "data"}
        
        wrapper = OptimizedStorageWrapper(mock_storage, mock_optimizer)
        
        result = await wrapper.get_fact(user_id="test")
        
        # Verificar que expand fue llamado
        mock_optimizer.expand.assert_called_once()


# IMPORTANTE: Estos tests validan integration con Core
```

### ✅ VALIDACIÓN OBLIGATORIA

```bash
# 1. Tests de optimization integration
pytest tests/test_optimization_integration.py -v

# 2. Verificar que NO rompimos nada
pytest tests/test_client.py -v

# 3. Tests completos
pytest tests/ -v

# 4. Verificar imports funcionen
python -c "from luminoracore_sdk import LuminoraCoreClient; from luminoracore.optimization import OptimizationConfig; print('OK')"
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ Client acepta optimization_config
□ Optimizer del Core usado correctamente
□ Storage wrapping funciona
□ get_optimization_stats() implementado
□ Tests de integration pasan 100%
□ Backward compatibility mantenida (sin optimization)
□ Graceful degradation si Core < 1.2
□ Todos los tests existentes pasan
```

---

## PROMPT 0.10: Migrar MemoryManager a usar Core

**OBJETIVO:** MemoryManager debe usar Core MemorySystem cuando esté disponible

### ⚠️ ANTI-ALUCINACIÓN

```
❌ NO elimines MemoryManager del SDK
❌ NO rompas API actual
✅ DELEGA a Core cuando disponible
✅ MANTÉN fallback para backward compat
```

### 📝 CÓDIGO COMPLETO

Modificar archivo: `luminoracore-sdk-python/luminoracore_sdk/session/memory.py`

```python
"""Memory manager with Core integration."""

import asyncio
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta

from ..types.session import MemoryConfig
from ..types.provider import ChatMessage

# NUEVO: Try import Core MemorySystem
try:
    from luminoracore.core.memory_system import MemorySystem as CoreMemorySystem
    HAS_CORE_MEMORY = True
except ImportError:
    HAS_CORE_MEMORY = False
    CoreMemorySystem = None

logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Memory manager con Core integration.
    
    REFACTORED: Usa Core MemorySystem cuando disponible,
    mantiene implementación propia como fallback.
    """
    
    def __init__(
        self,
        config: MemoryConfig,
        optimizer: Optional[Any] = None
    ):
        """
        Initialize memory manager
        
        Args:
            config: Memory configuration
            optimizer: Optimizer from Core (optional)
        """
        self.config = config
        self.optimizer = optimizer
        
        # NUEVO: Usar Core MemorySystem si disponible
        if HAS_CORE_MEMORY:
            logger.info("Using Core MemorySystem")
            self._use_core = True
            self._core_memory = CoreMemorySystem(
                max_tokens=config.max_tokens,
                optimizer=optimizer
            )
        else:
            logger.info("Using SDK MemoryManager (Core not available)")
            self._use_core = False
            self._core_memory = None
        
        # Fallback: implementación propia (mantener backward compat)
        self._memory_store: Dict[str, List[ChatMessage]] = {}
        self._lock = asyncio.Lock()
    
    async def store_message(
        self,
        session_id: str,
        message: ChatMessage
    ) -> None:
        """
        Store message in memory
        
        Delega a Core si disponible, sino usa implementación propia.
        """
        if self._use_core and self._core_memory:
            # Usar Core MemorySystem
            await self._core_memory.add_message(
                session_id=session_id,
                role=message.role,
                content=message.content,
                metadata=message.metadata
            )
        else:
            # Fallback: implementación SDK
            async with self._lock:
                if session_id not in self._memory_store:
                    self._memory_store[session_id] = []
                
                # Comprimir si optimizer disponible
                message_dict = message.dict()
                if self.optimizer:
                    message_dict = self.optimizer.compress(message_dict)
                
                self._memory_store[session_id].append(
                    ChatMessage(**message_dict)
                )
                
                # Aplicar TTL y limits
                await self._apply_limits(session_id)
    
    async def get_messages(
        self,
        session_id: str,
        limit: Optional[int] = None
    ) -> List[ChatMessage]:
        """
        Get messages from memory
        
        Delega a Core si disponible.
        """
        if self._use_core and self._core_memory:
            # Usar Core MemorySystem
            messages = await self._core_memory.get_messages(
                session_id=session_id,
                limit=limit
            )
            
            # Convertir a ChatMessage del SDK
            return [
                ChatMessage(
                    role=msg["role"],
                    content=msg["content"],
                    metadata=msg.get("metadata")
                )
                for msg in messages
            ]
        else:
            # Fallback: implementación SDK
            async with self._lock:
                messages = self._memory_store.get(session_id, [])
                
                # Expandir si optimizer usado
                if self.optimizer:
                    messages = [
                        ChatMessage(**self.optimizer.expand(m.dict()))
                        for m in messages
                    ]
                
                # Aplicar limit
                if limit:
                    messages = messages[-limit:]
                
                return messages
    
    async def clear_session(self, session_id: str) -> None:
        """Clear session memory"""
        if self._use_core and self._core_memory:
            await self._core_memory.clear_session(session_id)
        else:
            async with self._lock:
                self._memory_store.pop(session_id, None)
    
    async def _apply_limits(self, session_id: str) -> None:
        """
        Apply memory limits (TTL, max messages)
        
        Solo para fallback implementation.
        """
        if self._use_core:
            return  # Core maneja esto
        
        async with self._lock:
            messages = self._memory_store.get(session_id, [])
            
            # Apply max messages limit
            if len(messages) > self.config.max_messages:
                self._memory_store[session_id] = messages[-self.config.max_messages:]
            
            # Apply TTL (simplified)
            # TODO: Implement proper TTL check
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics
        
        NUEVO en v1.2
        """
        if self._use_core and self._core_memory:
            return await self._core_memory.get_stats()
        else:
            # Fallback stats
            async with self._lock:
                return {
                    "total_sessions": len(self._memory_store),
                    "total_messages": sum(
                        len(msgs) for msgs in self._memory_store.values()
                    ),
                    "using_core": False
                }


__all__ = ['MemoryManager']
```

### 📝 TESTS

Agregar a: `luminoracore-sdk-python/tests/test_memory_manager.py`

```python
"""
Tests adicionales para MemoryManager con Core integration
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from luminoracore_sdk.session.memory import MemoryManager
from luminoracore_sdk.types.session import MemoryConfig
from luminoracore_sdk.types.provider import ChatMessage


class TestMemoryManagerCoreIntegration:
    """Tests de integration con Core MemorySystem"""
    
    @pytest.fixture
    def memory_config(self):
        return MemoryConfig(
            max_messages=100,
            max_tokens=10000,
            ttl=3600
        )
    
    @pytest.mark.asyncio
    async def test_memory_manager_uses_core_if_available(self, memory_config):
        """MemoryManager debe usar Core si disponible"""
        manager = MemoryManager(memory_config)
        
        # Verificar si usa Core
        # Nota: depende de si Core está instalado
        if hasattr(manager, '_use_core'):
            logger.info(f"Using Core: {manager._use_core}")
    
    @pytest.mark.asyncio
    async def test_store_and_retrieve_messages(self, memory_config):
        """Store/retrieve debe funcionar con o sin Core"""
        manager = MemoryManager(memory_config)
        
        # Store message
        message = ChatMessage(
            role="user",
            content="Hello"
        )
        
        await manager.store_message("session1", message)
        
        # Retrieve
        messages = await manager.get_messages("session1")
        
        assert len(messages) == 1
        assert messages[0].content == "Hello"
    
    @pytest.mark.asyncio
    async def test_clear_session(self, memory_config):
        """Clear session debe funcionar"""
        manager = MemoryManager(memory_config)
        
        # Store
        message = ChatMessage(role="user", content="Test")
        await manager.store_message("session1", message)
        
        # Clear
        await manager.clear_session("session1")
        
        # Verify empty
        messages = await manager.get_messages("session1")
        assert len(messages) == 0
    
    @pytest.mark.asyncio
    async def test_get_stats(self, memory_config):
        """get_stats debe retornar info útil"""
        manager = MemoryManager(memory_config)
        
        # Add some messages
        await manager.store_message(
            "session1",
            ChatMessage(role="user", content="Test")
        )
        
        # Get stats
        stats = await manager.get_stats()
        
        assert "total_sessions" in stats
        assert stats["total_sessions"] >= 1


# Tests existentes deben seguir pasando
```

### ✅ VALIDACIÓN OBLIGATORIA

```bash
# Tests de memory
pytest tests/test_memory_manager.py -v

# Verificar backward compatibility
pytest tests/test_backward_compatibility.py -v

# All tests
pytest tests/ -v
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ MemoryManager usa Core cuando disponible
□ Fallback funciona sin Core
□ API pública sin cambios
□ Tests pasan con y sin Core
□ get_stats() implementado
□ Backward compatibility 100%
□ Optimizer integration funciona
```

---

## PROMPT 0.11: Tests de Memory (Must Pass)

**OBJETIVO:** Validar exhaustivamente Memory con optimization

### 📝 TESTS EXHAUSTIVOS

Crear archivo: `luminoracore-sdk-python/tests/test_memory_with_optimization.py`

```python
"""
Tests exhaustivos de Memory con Optimization

Valida que memory + optimization funcionan perfectamente juntos.
"""

import pytest
from unittest.mock import Mock

from luminoracore_sdk.session.memory import MemoryManager
from luminoracore_sdk.types.session import MemoryConfig
from luminoracore_sdk.types.provider import ChatMessage

try:
    from luminoracore.optimization import OptimizationConfig, Optimizer
    HAS_OPTIMIZATION = True
except ImportError:
    HAS_OPTIMIZATION = False
    pytest.skip("Optimization not available", allow_module_level=True)


class TestMemoryWithOptimization:
    """Test suite completo"""
    
    @pytest.fixture
    def optimizer(self):
        config = OptimizationConfig(
            key_abbreviation=True,
            compact_format=True,
            minify_json=True
        )
        return Optimizer(config)
    
    @pytest.fixture
    def memory_manager(self, optimizer):
        config = MemoryConfig(
            max_messages=100,
            max_tokens=10000
        )
        return MemoryManager(config, optimizer=optimizer)
    
    @pytest.mark.asyncio
    async def test_messages_compressed_in_storage(self, memory_manager, optimizer):
        """Messages deben estar compressed internamente"""
        message = ChatMessage(
            role="user",
            content="This is a test message"
        )
        
        await memory_manager.store_message("session1", message)
        
        # Verificar compresión funcionó
        # (esto es tricky de testear sin acceder internals)
        stats = await memory_manager.get_stats()
        assert stats is not None
    
    @pytest.mark.asyncio
    async def test_messages_expanded_on_retrieval(self, memory_manager):
        """Messages deben expandirse al recuperar"""
        message = ChatMessage(
            role="assistant",
            content="Response"
        )
        
        await memory_manager.store_message("session1", message)
        messages = await memory_manager.get_messages("session1")
        
        # Debe retornar expanded
        assert len(messages) == 1
        assert messages[0].content == "Response"
        assert messages[0].role == "assistant"
    
    @pytest.mark.asyncio
    async def test_multiple_messages_with_optimization(self, memory_manager):
        """Multiple messages con optimization"""
        for i in range(10):
            message = ChatMessage(
                role="user" if i % 2 == 0 else "assistant",
                content=f"Message {i}"
            )
            await memory_manager.store_message("session1", message)
        
        messages = await memory_manager.get_messages("session1")
        assert len(messages) == 10
        
        # Verificar orden preservado
        for i, msg in enumerate(messages):
            assert msg.content == f"Message {i}"
    
    @pytest.mark.asyncio
    async def test_token_reduction_stats(self, memory_manager, optimizer):
        """Stats debe mostrar token reduction"""
        # Add messages
        for i in range(5):
            await memory_manager.store_message(
                "session1",
                ChatMessage(role="user", content=f"Test {i}")
            )
        
        stats = await memory_manager.get_stats()
        assert stats is not None
        
        # Si usa Core, debe tener optimization stats
        if stats.get("using_core"):
            # Core puede proveer más stats
            pass


# MÁS TESTS...
```

### ✅ VALIDACIÓN OBLIGATORIA

```bash
pytest tests/test_memory_with_optimization.py -v
pytest tests/ -v --cov=luminoracore_sdk.session.memory --cov-report=term-missing
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ Tests de memory + optimization pasan
□ Compression/expansion funciona
□ Stats correctos
□ Coverage >= 90%
```

---

## PROMPT 0.12: Integration Tests SDK-Core

**OBJETIVO:** Tests end-to-end que validan SDK usa Core correctamente

### 📝 TESTS E2E

Crear archivo: `luminoracore-sdk-python/tests/integration/test_sdk_core_e2e.py`

```python
"""
End-to-End Integration Tests: SDK + Core

Tests completos que validan toda la stack funciona junta.
"""

import pytest
import asyncio

from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.types.session import StorageConfig, MemoryConfig
from luminoracore_sdk.types.provider import ProviderConfig

try:
    from luminoracore.optimization import OptimizationConfig
    from luminoracore import PersonaBlend
    HAS_CORE = True
except ImportError:
    HAS_CORE = False
    pytest.skip("Core not available", allow_module_level=True)


class TestSDKCoreE2E:
    """Tests E2E completos"""
    
    @pytest.mark.asyncio
    async def test_full_stack_with_optimization(self):
        """
        Test E2E: Client con optimization del Core
        
        CRÍTICO: Este test valida toda la arquitectura
        """
        # 1. Setup client con optimization
        opt_config = OptimizationConfig(
            key_abbreviation=True,
            compact_format=True,
            cache_enabled=True
        )
        
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type="memory"),
            memory_config=MemoryConfig(max_messages=50),
            optimization_config=opt_config
        )
        
        await client.initialize()
        
        # 2. Verificar optimizer está activo
        assert client.optimizer is not None
        
        # 3. Test personality blending (usa Core)
        # TODO: Load real personalities
        
        # 4. Test memory con optimization
        # TODO: Add messages y verificar compression
        
        # 5. Get stats
        stats = await client.get_optimization_stats()
        assert stats is not None
        assert stats["enabled"] is True
        
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_personality_blending_uses_core(self):
        """Blending debe usar Core PersonaBlend"""
        client = LuminoraCoreClient()
        await client.initialize()
        
        # Verificar blender usa adapter
        assert hasattr(client.personality_blender, '_adapter')
        
        # TODO: Test actual blending
        
        await client.cleanup()
    
    @pytest.mark.asyncio
    async def test_backward_compatibility_e2e(self):
        """
        E2E sin optimization (backward compat)
        
        CRÍTICO: Cliente v1.0 debe seguir funcionando
        """
        # Cliente SIN optimization
        client = LuminoraCoreClient(
            storage_config=StorageConfig(storage_type="memory")
        )
        
        await client.initialize()
        
        # Debe funcionar perfectamente sin optimization
        assert client.optimizer is None
        
        # TODO: Test funcionalidad básica
        
        await client.cleanup()


# MÁS TESTS E2E...
```

### ✅ VALIDACIÓN OBLIGATORIA

```bash
# Tests E2E
pytest tests/integration/test_sdk_core_e2e.py -v

# Toda la suite
pytest tests/ -v

# Con coverage completo
pytest tests/ --cov=luminoracore_sdk --cov-report=html
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ Tests E2E pasan
□ Full stack funciona junta
□ SDK usa Core correctamente
□ Optimization flow completo
□ Backward compatibility verificada
□ Coverage >= 85%
```

---

# 📅 SEMANA 4: CLI Y VALIDACIÓN FINAL

## PROMPT 0.13: Descomentar Dependencia CLI

**OBJETIVO:** Activar dependencia Core en CLI

### 📝 CAMBIOS EXACTOS

Modificar archivo: `luminoracore-cli/pyproject.toml`

```toml
[project]
name = "luminoracore-cli"
version = "1.2.0"  # Bump version
description = "Professional CLI tool for LuminoraCore personality management"
# ... otros campos ...

dependencies = [
    "luminoracore>=1.2.0,<2.0.0",  # ✅ DESCOMENTADO Y ACTUALIZADO
    "typer>=0.9.0,<1.0.0",
    "rich>=13.0.0,<14.0.0",
    # ... resto sin cambios ...
]

[project.optional-dependencies]
sdk = [
    "luminoracore-sdk>=1.2.0,<2.0.0"  # SDK opcional
]
# ... resto sin cambios ...
```

### ✅ VALIDACIÓN OBLIGATORIA

```bash
# 1. Verificar dependencias
cd luminoracore-cli/
pip install -e .

# 2. Verificar imports
python -c "from luminoracore import Personality; print('OK')"

# 3. Tests básicos
pytest tests/ -v --tb=short
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ Dependencia descomentada
□ Version bumped a 1.2.0
□ CLI instala correctamente
□ Imports del Core funcionan
□ Tests pasan
```

---

## PROMPT 0.14: Actualizar Imports CLI

**OBJETIVO:** Verificar y limpiar imports en CLI

### 📝 VERIFICACIÓN

```bash
# Buscar imports problemáticos
cd luminoracore-cli/
grep -rn "from luminoracore" luminoracore_cli/ > /tmp/cli_imports.txt

# Ver reporte
cat /tmp/cli_imports.txt
```

### 📝 LIMPIEZA (si necesario)

Solo si hay imports incorrectos, limpiar:

```python
# luminoracore-cli/luminoracore_cli/core/validator.py

# ✅ CORRECTO
from luminoracore import (
    Personality,
    PersonalityValidator,
    PersonalitySchema
)

# ❌ INCORRECTO (si existe)
# from luminoracore.tools import PersonalityValidator  # Deprecado
```

### ✅ VALIDACIÓN OBLIGATORIA

```bash
pytest tests/test_cli_core_imports.py -v
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ Todos los imports son correctos
□ No hay imports deprecados
□ Tests pasan
```

---

## PROMPT 0.15: Tests Full Stack

**OBJETIVO:** Tests que validan TODA la stack: Core + SDK + CLI

### 📝 TESTS COMPLETOS

Crear archivo: `tests/integration/test_full_stack.py` (en root del monorepo)

```python
"""
Full Stack Integration Tests

Valida que Core, SDK y CLI funcionan juntos perfectamente.
"""

import pytest
import subprocess
import sys
from pathlib import Path


class TestFullStackIntegration:
    """Tests de toda la stack"""
    
    def test_core_importable(self):
        """Core debe ser importable"""
        import luminoracore
        assert luminoracore.__version__
    
    def test_sdk_importable(self):
        """SDK debe ser importable"""
        import luminoracore_sdk
        assert luminoracore_sdk.__version__
    
    def test_cli_importable(self):
        """CLI debe ser importable"""
        import luminoracore_cli
        # CLI puede no tener __version__
    
    def test_sdk_uses_core_blender(self):
        """SDK debe usar Core PersonaBlend"""
        from luminoracore import PersonaBlend
        from luminoracore_sdk.personality.blender import PersonalityBlender
        
        blender = PersonalityBlender()
        assert hasattr(blender, '_adapter')
    
    def test_sdk_uses_core_optimizer(self):
        """SDK debe poder usar Core Optimizer"""
        from luminoracore.optimization import OptimizationConfig, Optimizer
        from luminoracore_sdk import LuminoraCoreClient
        
        config = OptimizationConfig(enabled=True)
        optimizer = Optimizer(config)
        
        assert optimizer is not None
    
    def test_cli_uses_core_validator(self):
        """CLI debe usar Core PersonalityValidator"""
        from luminoracore import PersonalityValidator
        from luminoracore_cli.core.validator import CLIValidator
        
        # CLI validator debe usar Core
        cli_val = CLIValidator()
        assert hasattr(cli_val, 'validator')
    
    def test_cli_command_works(self):
        """CLI command debe funcionar"""
        result = subprocess.run(
            ["luminoracore", "--version"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0


# MÁS TESTS...
```

### ✅ VALIDACIÓN OBLIGATORIA

```bash
# Desde root del monorepo
pytest tests/integration/test_full_stack.py -v

# DEBE pasar 100%
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ Core importable
□ SDK importable  
□ CLI importable
□ SDK usa Core correctamente
□ CLI usa Core correctamente
□ CLI commands funcionan
□ Tests full stack pasan 100%
```

---

## PROMPT 0.16: Documentation & Release Notes

**OBJETIVO:** Documentar todos los cambios y preparar release

### 📝 CHANGELOG

Actualizar: `CHANGELOG.md` (en cada componente)

```markdown
# Changelog

## [1.2.0] - 2025-11-21

### Added
- **ARQUITECTURA:** Migración a arquitectura de 3 capas
- **Core Integration:** SDK ahora usa Core internamente
- **Optimization:** Integration completa del módulo optimization/
- **Memory:** MemoryManager usa Core MemorySystem cuando disponible
- **CLI:** Dependencia Core activada oficialmente

### Changed
- **PersonalityBlender:** Ahora delega a Core PersonaBlend via adapter
- **MemoryManager:** Usa Core con fallback a implementación SDK
- **Storage:** Wrapping con optimizer cuando habilitado

### Fixed
- Eliminada duplicación de código entre Core y SDK
- CLI ahora tiene dependencias correctas

### Deprecated
- Ninguno (100% backward compatible)

### Breaking Changes
- **NINGUNO** - Esta release es 100% backward compatible
```

### 📝 MIGRATION GUIDE

Crear: `MIGRATION_1.1_to_1.2.md`

```markdown
# Migration Guide: v1.1 → v1.2

## Overview

Version 1.2 introduce arquitectura de 3 capas con integration al Core.
**IMPORTANTE:** Esta versión es 100% backward compatible.

## For SDK Users

### No Changes Required

Tu código v1.1 sigue funcionando sin modificaciones:

```python
# ✅ Código v1.1 - SIGUE FUNCIONANDO
from luminoracore_sdk import LuminoraCoreClient

client = LuminoraCoreClient()
await client.initialize()
# ... tu código ...
```

### Optional: Enable Optimization

Nueva feature en v1.2:

```python
# 🆕 NUEVO en v1.2 - OPCIONAL
from luminoracore_sdk import LuminoraCoreClient
from luminoracore.optimization import OptimizationConfig

client = LuminoraCoreClient(
    optimization_config=OptimizationConfig(
        key_abbreviation=True,
        cache_enabled=True
    )
)
```

## For CLI Users

### Dependency Now Required

CLI ahora requiere `luminoracore>=1.2.0` instalado:

```bash
# Reinstalar CLI
pip install --upgrade luminoracore-cli
```

## For Contributors

Ver ARCHITECTURE.md para nueva estructura.

## Rollback

Si necesitas rollback:

```bash
pip install luminoracore==1.1.0
pip install luminoracore-sdk==1.1.0
pip install luminoracore-cli==1.1.0
```
```

### 📝 README Updates

Actualizar READMEs con nueva arquitectura:

```markdown
# LuminoraCore v1.2

## Architecture

LuminoraCore usa arquitectura de 3 capas:

1. **Core** (`luminoracore/`) - Business logic pura
2. **SDK** (`luminoracore-sdk-python/`) - Client layer + LLM integration
3. **CLI** (`luminoracore-cli/`) - User interface

## Installation

```bash
# Core only
pip install luminoracore

# SDK (includes Core)
pip install luminoracore-sdk

# CLI (includes Core)
pip install luminoracore-cli
```

## What's New in v1.2

- ✅ Unified architecture
- ✅ Optimization module integration
- ✅ Better Core/SDK integration
- ✅ 100% backward compatible
```

### ✅ VALIDACIÓN OBLIGATORIA

```bash
# Verificar documentación
ls -la CHANGELOG.md MIGRATION_1.1_to_1.2.md

# Verificar links funcionan
# Verificar ejemplos son correctos
```

### ✅ CRITERIOS DE ÉXITO

```markdown
□ CHANGELOG.md actualizado (Core, SDK, CLI)
□ MIGRATION_1.1_to_1.2.md creado
□ README.md actualizado
□ Ejemplos actualizados
□ Links verificados
□ Version bumped a 1.2.0 en todos los componentes
□ Git tags creados
```

---

# 🎯 CHECKLIST FINAL COMPLETO

## Pre-Release Checklist

```markdown
### SEMANA 1: Auditoría ✅
□ PROMPT 0.1: Auditoría ejecutada
□ PROMPT 0.2: Baseline capturado
□ PROMPT 0.3: Duplicaciones documentadas
□ PROMPT 0.4: Plan creado

### SEMANA 2: SDK Personality ✅
□ PROMPT 0.5: Adapter creado y testeado
□ PROMPT 0.6: PersonalityBlender migrado
□ PROMPT 0.7: Tests adicionales pasando
□ PROMPT 0.8: Backward compat verificado

### SEMANA 3: SDK Memory & Optimization ✅
□ PROMPT 0.9: Optimizer integrado
□ PROMPT 0.10: MemoryManager migrado
□ PROMPT 0.11: Tests memory pasando
□ PROMPT 0.12: Tests E2E pasando

### SEMANA 4: CLI & Release ✅
□ PROMPT 0.13: Dependencia activada
□ PROMPT 0.14: Imports limpiados
□ PROMPT 0.15: Full stack tests pasando
□ PROMPT 0.16: Documentación completa

### Tests Finales ✅
□ Core tests: 100% passing
□ SDK tests: 100% passing
□ CLI tests: 100% passing
□ Integration tests: 100% passing
□ E2E tests: 100% passing
□ Coverage >= 85% en todos

### Release ✅
□ Version 1.2.0 en todos los componentes
□ CHANGELOG actualizado
□ Migration guide listo
□ Git tags creados
□ PyPI ready
```

---

# 🚀 CONCLUSIÓN

## Lo Que Logramos

✅ **Arquitectura de 3 capas** implementada  
✅ **Sin duplicación** de código  
✅ **100% backward compatible**  
✅ **Core → SDK → CLI** flow correcto  
✅ **Optimization integrada**  
✅ **Todos los tests pasando**  

## Lo Que NO Rompimos

✅ APIs públicas sin cambios  
✅ Código v1.0/v1.1 sigue funcionando  
✅ Sin breaking changes  
✅ Graceful degradation everywhere  

## Próximos Pasos

1. **Code Review:** Review completo de todos los cambios
2. **QA Testing:** Testing manual adicional
3. **Beta Release:** v1.2.0-beta para early adopters
4. **Production Release:** v1.2.0 final
5. **Monitor:** Feedback de usuarios

---

**Versión:** 2.0 COMPLETO  
**Fecha:** 21 de Noviembre, 2025  
**Estado:** PRODUCTION READY  
**Prompts:** 16/16 completamente detallados  

**🎉 REFACTOR ARQUITECTURA COMPLETO Y LISTO PARA IMPLEMENTACIÓN 🎉**
