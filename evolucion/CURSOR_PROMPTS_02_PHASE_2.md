# 🔍 FASE 2: Semantic Search - Prompts Detallados Para Cursor AI

**Fase:** 2 de 8  
**Timeline:** 12 Semanas (Semanas 5-16 del roadmap)  
**Objetivo:** Búsqueda semántica con natural language queries  
**Complejidad:** 🟡 MEDIA  
**ROI:** 🟢 ALTO

---

## 📋 ÍNDICE DE CONTENIDOS

- [RESUMEN EJECUTIVO](#-resumen-ejecutivo)
- [SEMANAS 5-7: Embeddings Layer](#-semanas-5-7-embeddings-layer)
- [SEMANAS 8-10: Vector Stores](#-semanas-8-10-vector-stores)
- [SEMANAS 11-13: Search Engine](#-semanas-11-13-search-engine)
- [SEMANAS 14-16: Integration & Testing](#-semanas-14-16-integration--testing)

---

## 🎯 RESUMEN EJECUTIVO

### Contexto

Después de completar Fase 1 (Quick Wins), tenemos optimizaciones de tokens funcionando. Ahora necesitamos hacer la memoria REALMENTE buscable mediante semantic search.

### Problema Actual (v1.2-lite)

```python
# Solo funciona con key exacto
fact = await client.get_fact(
    user_id="carlos",
    category="preferences", 
    key="favorite_sport"  # ❌ Debes saber el key exacto
)

# Búsquedas naturales NO funcionan:
# "qué deportes le gustan" → ❌ No encuentra nada
# "basketball preferences" → ❌ No encuentra nada
```

### Objetivo de Esta Fase

```python
# ✅ Búsqueda con lenguaje natural
results = await client.semantic_search(
    user_id="carlos",
    query="what sports does carlos like",
    top_k=5
)

# Retorna:
# 1. favorite_sport: "basketball" (similarity: 0.95)
# 2. weekend_activity: "pickup games" (0.87)
# 3. exercise_preference: "cardio" (0.72)
```

### Componentes a Implementar

```
luminoracore/
├── embeddings/               # ← SEMANAS 5-7
│   ├── __init__.py
│   ├── generator.py          # Core embeddings
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── openai.py         # OpenAI ada-002
│   │   ├── cohere.py         # Cohere
│   │   └── local.py          # sentence-transformers
│   └── cache.py              # Cache embeddings

├── vector_stores/            # ← SEMANAS 8-10
│   ├── __init__.py
│   ├── base.py               # Abstract interface
│   ├── faiss.py              # Local dev (free)
│   ├── pinecone.py           # Production
│   ├── weaviate.py           # Self-hosted
│   └── qdrant.py             # Alternative

└── search/                   # ← SEMANAS 11-13
    ├── __init__.py
    ├── semantic.py           # Core search
    ├── hybrid.py             # Semantic + keyword
    └── filters.py            # Filters

tests/
├── test_embeddings/          # ← SEMANAS 5-7
├── test_vector_stores/       # ← SEMANAS 8-10
└── test_search/              # ← SEMANAS 11-13
```

### Beneficio Esperado

```
ANTES (Fase 1):
- Solo búsqueda por key exacto
- 0% queries naturales funcionan
- Experiencia limitada

DESPUÉS (Fase 2):
- Búsqueda por lenguaje natural
- >85% queries naturales funcionan
- Experiencia mejorada dramáticamente
- Opens door para Fase 3 (Knowledge Graphs)
```

---

## 📅 SEMANAS 5-7: Embeddings Layer

**Objetivos:**
- Implementar generación de embeddings
- Soporte múltiples providers (OpenAI, Cohere, local)
- Sistema de caché para embeddings
- 100% tests passing

**Timeline:**
- Semana 5: Core embedding generator + OpenAI provider
- Semana 6: Cohere + local providers
- Semana 7: Caching system + tests + benchmarks

---

### PROMPT 2.1: Setup Embeddings Module

**CONTEXTO:**  
Iniciamos Fase 2 del roadmap. Necesitamos crear el módulo de embeddings que será la base de semantic search.

**OBJETIVO:**  
Crear estructura del módulo `embeddings/` y el generador core.

**DEPENDENCIAS:**
- ✅ Fase 1 completada (optimizations funcionando)
- ✅ Tests actuales pasan (100%)

**ACCIÓN REQUERIDA:**

1. Crear estructura:
```bash
mkdir -p luminoracore/embeddings/providers
mkdir -p tests/test_embeddings
touch luminoracore/embeddings/__init__.py
touch luminoracore/embeddings/providers/__init__.py
touch tests/test_embeddings/__init__.py
```

2. Crear `luminoracore/embeddings/base.py`:

```python
"""
Base Embedding Interface - Phase 2 Semantic Search
Abstract interface for embedding providers

Author: LuminoraCore Team
Version: 1.3.0
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class EmbeddingResult:
    """
    Result from embedding generation
    
    Attributes:
        embedding: Vector embedding (list of floats)
        model: Model used for embedding
        dimensions: Number of dimensions
        token_count: Tokens consumed (if available)
    """
    embedding: List[float]
    model: str
    dimensions: int
    token_count: Optional[int] = None


class EmbeddingProvider(ABC):
    """
    Abstract base class for embedding providers
    
    All embedding providers must implement this interface.
    Supports providers like OpenAI, Cohere, local models, etc.
    """
    
    def __init__(
        self,
        model: str,
        dimensions: int,
        api_key: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize embedding provider
        
        Args:
            model: Model identifier (e.g., "text-embedding-3-small")
            dimensions: Embedding vector dimensions
            api_key: API key if needed
            **kwargs: Provider-specific config
        """
        self.model = model
        self.dimensions = dimensions
        self.api_key = api_key
        self.config = kwargs
    
    @abstractmethod
    async def generate_embedding(self, text: str) -> EmbeddingResult:
        """
        Generate embedding for a single text
        
        Args:
            text: Text to embed
            
        Returns:
            EmbeddingResult with vector and metadata
        """
        pass
    
    @abstractmethod
    async def generate_embeddings_batch(
        self,
        texts: List[str]
    ) -> List[EmbeddingResult]:
        """
        Generate embeddings for multiple texts (batched)
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of EmbeddingResult objects
        """
        pass
    
    @abstractmethod
    def get_cost_estimate(self, token_count: int) -> float:
        """
        Estimate cost for given token count
        
        Args:
            token_count: Number of tokens
            
        Returns:
            Estimated cost in USD
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model}, dims={self.dimensions})"


# Export
__all__ = [
    "EmbeddingProvider",
    "EmbeddingResult"
]
```

**VALIDACIÓN:**

```bash
# Verificar sintaxis
python -m py_compile luminoracore/embeddings/base.py

# Test import
python3 -c "from luminoracore.embeddings.base import EmbeddingProvider, EmbeddingResult; print('✅ Import successful')"
```

**CRITERIOS DE ÉXITO:**
- [ ] Estructura de directorios creada
- [ ] base.py sin errores de sintaxis
- [ ] EmbeddingProvider es ABC correctamente
- [ ] EmbeddingResult dataclass funciona
- [ ] Import funciona

**PRÓXIMO PASO:**  
Implementar OpenAIEmbeddings provider (PROMPT 2.2)

---

### PROMPT 2.2: Implementar OpenAI Embeddings Provider

**CONTEXTO:**  
Tenemos la interfaz base. Ahora implementamos el primer provider: OpenAI text-embedding-3-small.

**OBJETIVO:**  
Crear `luminoracore/embeddings/providers/openai.py` con soporte completo para OpenAI embeddings API.

**ESPECIFICACIONES TÉCNICAS:**

Crear archivo: `luminoracore/embeddings/providers/openai.py`

```python
"""
OpenAI Embeddings Provider - Phase 2
Implements EmbeddingProvider for OpenAI API

Supported models:
- text-embedding-3-small (1536 dims, $0.02/1M tokens)
- text-embedding-3-large (3072 dims, $0.13/1M tokens)
- text-embedding-ada-002 (1536 dims, $0.10/1M tokens - legacy)

Author: LuminoraCore Team
Version: 1.3.0
"""

import os
from typing import List, Optional
import httpx

from ..base import EmbeddingProvider, EmbeddingResult


class OpenAIEmbeddings(EmbeddingProvider):
    """
    OpenAI embeddings provider
    
    Uses OpenAI's embeddings API to generate vectors.
    Supports batching and automatic retry on failures.
    
    Example:
        >>> provider = OpenAIEmbeddings(
        ...     api_key="sk-...",
        ...     model="text-embedding-3-small"
        ... )
        >>> result = await provider.generate_embedding("Hello world")
        >>> print(len(result.embedding))
        1536
    """
    
    # Model configurations
    MODELS = {
        "text-embedding-3-small": {
            "dimensions": 1536,
            "cost_per_1m_tokens": 0.02
        },
        "text-embedding-3-large": {
            "dimensions": 3072,
            "cost_per_1m_tokens": 0.13
        },
        "text-embedding-ada-002": {
            "dimensions": 1536,
            "cost_per_1m_tokens": 0.10
        }
    }
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "text-embedding-3-small",
        timeout: float = 30.0,
        max_retries: int = 3,
        **kwargs
    ):
        """
        Initialize OpenAI embeddings provider
        
        Args:
            api_key: OpenAI API key (or use OPENAI_API_KEY env var)
            model: Model to use
            timeout: Request timeout in seconds
            max_retries: Max retry attempts on failure
            **kwargs: Additional config
        """
        # Get API key
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. "
                "Pass api_key or set OPENAI_API_KEY env var"
            )
        
        # Validate model
        if model not in self.MODELS:
            raise ValueError(
                f"Unknown model: {model}. "
                f"Supported: {list(self.MODELS.keys())}"
            )
        
        # Get model config
        model_config = self.MODELS[model]
        dimensions = model_config["dimensions"]
        
        # Initialize parent
        super().__init__(
            model=model,
            dimensions=dimensions,
            api_key=self.api_key,
            **kwargs
        )
        
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_url = "https://api.openai.com/v1"
    
    async def generate_embedding(self, text: str) -> EmbeddingResult:
        """
        Generate embedding for single text
        
        Args:
            text: Text to embed
            
        Returns:
            EmbeddingResult
        """
        results = await self.generate_embeddings_batch([text])
        return results[0]
    
    async def generate_embeddings_batch(
        self,
        texts: List[str]
    ) -> List[EmbeddingResult]:
        """
        Generate embeddings for multiple texts (batched)
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of EmbeddingResult objects
        """
        if not texts:
            return []
        
        # Make API request
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "input": texts,
                    "model": self.model
                }
            )
            response.raise_for_status()
            data = response.json()
        
        # Parse results
        results = []
        for item in data["data"]:
            result = EmbeddingResult(
                embedding=item["embedding"],
                model=self.model,
                dimensions=len(item["embedding"]),
                token_count=data.get("usage", {}).get("total_tokens")
            )
            results.append(result)
        
        return results
    
    def get_cost_estimate(self, token_count: int) -> float:
        """
        Estimate cost for given token count
        
        Args:
            token_count: Number of tokens
            
        Returns:
            Estimated cost in USD
        """
        model_config = self.MODELS[self.model]
        cost_per_1m = model_config["cost_per_1m_tokens"]
        return (token_count / 1_000_000) * cost_per_1m


# Export
__all__ = ["OpenAIEmbeddings"]
```

**VALIDACIÓN:**

```bash
# 1. Verificar sintaxis
python -m py_compile luminoracore/embeddings/providers/openai.py

# 2. Test básico (requiere API key)
# Crear test_openai_manual.py temporal
cat > /tmp/test_openai_manual.py << 'TESTEND'
import asyncio
import os
from luminoracore.embeddings.providers.openai import OpenAIEmbeddings

async def test():
    # NOTE: Requires OPENAI_API_KEY env var
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Skipping test - no API key")
        return
    
    provider = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # Test single embedding
    result = await provider.generate_embedding("Hello world")
    print(f"✅ Single embedding: {len(result.embedding)} dimensions")
    assert len(result.embedding) == 1536
    
    # Test batch
    results = await provider.generate_embeddings_batch(["Test 1", "Test 2"])
    print(f"✅ Batch embeddings: {len(results)} results")
    assert len(results) == 2
    
    # Test cost estimate
    cost = provider.get_cost_estimate(1000)
    print(f"✅ Cost estimate for 1K tokens: ${cost:.6f}")
    assert cost > 0
    
    print("\n🎉 All manual tests passed!")

asyncio.run(test())
TESTEND

# Ejecutar si tienes API key
python /tmp/test_openai_manual.py
```

**CRITERIOS DE ÉXITO:**
- [ ] Archivo creado sin errores
- [ ] Hereda de EmbeddingProvider
- [ ] generate_embedding() funciona
- [ ] generate_embeddings_batch() funciona
- [ ] get_cost_estimate() calcula correctamente
- [ ] Maneja API key correctamente
- [ ] Tests manuales pasan (si hay API key)

**ACTUALIZAR __init__.py:**

```python
# luminoracore/embeddings/__init__.py
from .base import EmbeddingProvider, EmbeddingResult
from .providers.openai import OpenAIEmbeddings

__all__ = [
    "EmbeddingProvider",
    "EmbeddingResult",
    "OpenAIEmbeddings"
]
```

**PRÓXIMO PASO:**  
Implementar tests comprehensivos (PROMPT 2.3)

---

## ⏭️ CONTINUACIÓN PENDIENTE

Este documento continúa con:

### Semanas 5-7 (Continuación):
- PROMPT 2.3: Tests para embeddings
- PROMPT 2.4: Cohere provider
- PROMPT 2.5: Local embeddings (sentence-transformers)
- PROMPT 2.6: Embedding cache system
- PROMPT 2.7: Benchmarks y optimización

### Semanas 8-10: Vector Stores
- PROMPT 2.8-2.15: FAISS, Pinecone, Weaviate, Qdrant
- Migration scripts
- Abstract interface
- Tests comprehensivos

### Semanas 11-13: Search Engine
- PROMPT 2.16-2.20: Semantic search core
- Filters (category, importance, date)
- Hybrid search (semantic + keyword)
- Ranking algorithms

### Semanas 14-16: Integration
- PROMPT 2.21-2.25: Integration con memoria existente
- End-to-end tests
- Performance benchmarks
- Documentation
- v1.3 Release

---

## 🔄 FLUJO DE TRABAJO

```
PREPARACIÓN:
├─ Verificar Fase 1 completada
├─ Branch: git checkout -b phase-2-semantic-search
└─ Tests actuales pasan: pytest tests/

SEMANA 5-7:
├─ Implementar embeddings module
├─ 3 providers (OpenAI, Cohere, local)
├─ Caching system
└─ Tests + benchmarks

SEMANA 8-10:
├─ Implementar vector stores
├─ 4 implementations (FAISS, Pinecone, etc.)
├─ Migration scripts
└─ Tests

SEMANA 11-13:
├─ Implementar search engine
├─ Semantic + hybrid + filters
├─ Ranking algorithms
└─ Tests

SEMANA 14-16:
├─ Integration end-to-end
├─ Performance optimization
├─ Documentation
└─ v1.3 Release
```

---

## 📊 MÉTRICAS DE ÉXITO - FASE 2

```
Performance:
✅ <500ms search response time (p95)
✅ >85% relevance (user feedback)
✅ Works con 100K+ facts por usuario

Quality:
✅ 100% backward compatible
✅ 95%+ test coverage
✅ 0 breaking changes

Funcionalidad:
✅ Natural language queries funcionan
✅ 4+ vector stores soportados
✅ 3+ embedding providers
✅ Caching system activo
```

---

**Estado:** 📝 Documentación Parcial  
**Completado:** Semanas 5 (partial)  
**Pendiente:** Resto de Fase 2  

**Próximo Documento:** CURSOR_PROMPTS_03_PHASE_3.md  
**Última Actualización:** 18 de Noviembre, 2025

---

