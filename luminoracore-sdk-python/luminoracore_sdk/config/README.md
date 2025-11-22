# LuminoraCore SDK - Config Module

Módulo de configuración para URLs y modelos por defecto de los providers LLM.

---

## 📋 Propósito

Este módulo proporciona configuración centralizada para:
- **URLs base** de los providers LLM
- **Modelos por defecto** para cada provider
- **Endpoints de chat** específicos de cada provider
- **Custom providers** configurables

---

## 📁 Archivos

### `provider_urls.json`
Archivo JSON con la configuración de todos los providers soportados.

**Estructura:**
```json
{
  "providers": {
    "openai": {
      "name": "OpenAI",
      "base_url": "https://api.openai.com/v1",
      "default_model": "gpt-3.5-turbo",
      "chat_endpoint": "/chat/completions",
      "description": "OpenAI GPT models"
    },
    ...
  },
  "custom_providers": {
    "_example": {
      "name": "My Custom LLM",
      "base_url": "https://api.mycustom.com/v1",
      "default_model": "custom-model",
      "chat_endpoint": "/chat/completions",
      "description": "My custom LLM provider"
    }
  }
}
```

**Providers Incluidos:**
- ✅ OpenAI
- ✅ Anthropic
- ✅ DeepSeek
- ✅ Mistral
- ✅ Cohere
- ✅ Google (Gemini)
- ✅ Llama (via Replicate)

---

## 🔧 Funciones

### `get_provider_urls() -> Dict[str, Dict[str, str]]`

Carga todas las configuraciones de providers desde `provider_urls.json`.

**Returns:**
- Diccionario con configuraciones de todos los providers
- Incluye providers estándar y custom providers
- Usa cache para evitar múltiples lecturas del archivo

**Ejemplo:**
```python
from luminoracore_sdk.config import get_provider_urls

urls = get_provider_urls()
print(urls["openai"]["base_url"])  # https://api.openai.com/v1
print(urls["openai"]["default_model"])  # gpt-3.5-turbo
```

---

### `get_provider_base_url(provider_name: str) -> Optional[str]`

Obtiene la URL base para un provider específico.

**Args:**
- `provider_name`: Nombre del provider (ej: "openai", "anthropic")

**Returns:**
- URL base como string o `None` si no se encuentra

**Ejemplo:**
```python
from luminoracore_sdk.config import get_provider_base_url

openai_url = get_provider_base_url("openai")
# Returns: "https://api.openai.com/v1"

anthropic_url = get_provider_base_url("anthropic")
# Returns: "https://api.anthropic.com/v1"
```

---

### `get_provider_default_model(provider_name: str) -> Optional[str]`

Obtiene el modelo por defecto para un provider específico.

**Args:**
- `provider_name`: Nombre del provider (ej: "openai", "anthropic")

**Returns:**
- Modelo por defecto como string o `None` si no se encuentra

**Ejemplo:**
```python
from luminoracore_sdk.config import get_provider_default_model

openai_model = get_provider_default_model("openai")
# Returns: "gpt-3.5-turbo"

anthropic_model = get_provider_default_model("anthropic")
# Returns: "claude-3-sonnet-20240229"
```

---

## 💡 Uso en Providers

Este módulo se usa internamente por los providers para obtener URLs y modelos por defecto:

```python
from luminoracore_sdk.config import get_provider_base_url, get_provider_default_model
from luminoracore_sdk.types.provider import ProviderConfig

# Crear provider config usando valores por defecto del config
provider_name = "openai"
config = ProviderConfig(
    name=provider_name,
    api_key="your-key",
    base_url=get_provider_base_url(provider_name) or "https://api.openai.com/v1",
    model=get_provider_default_model(provider_name) or "gpt-3.5-turbo"
)
```

---

## ➕ Agregar Custom Providers

Para agregar un nuevo provider:

1. **Editar `provider_urls.json`:**
```json
{
  "custom_providers": {
    "my_provider": {
      "name": "My Provider",
      "base_url": "https://api.myprovider.com/v1",
      "default_model": "my-model",
      "chat_endpoint": "/chat/completions",
      "description": "My custom LLM provider"
    }
  }
}
```

2. **Registrar el provider en el SDK:**
```python
from luminoracore_sdk.providers import ProviderFactory
from luminoracore_sdk.providers.base import BaseProvider

class MyProvider(BaseProvider):
    def get_default_model(self) -> str:
        return "my-model"
    
    async def chat(self, messages, **kwargs):
        # Implementación...
        pass
    
    async def stream_chat(self, messages, **kwargs):
        # Implementación...
        pass

# Registrar
ProviderFactory.register_provider("my_provider", MyProvider)
```

3. **Usar el provider:**
```python
from luminoracore_sdk.config import get_provider_base_url, get_provider_default_model
from luminoracore_sdk.types.provider import ProviderConfig

config = ProviderConfig(
    name="my_provider",
    api_key="your-key",
    base_url=get_provider_base_url("my_provider"),
    model=get_provider_default_model("my_provider")
)

provider = ProviderFactory.create_provider(config)
```

---

## 🔍 Cache

El módulo usa cache global (`_config_cache`) para evitar múltiples lecturas del archivo JSON:

```python
# Primera llamada: lee el archivo
urls1 = get_provider_urls()

# Segunda llamada: usa cache
urls2 = get_provider_urls()  # No lee el archivo de nuevo

# Cache persiste durante la ejecución del programa
```

**Nota:** Si necesitas recargar la configuración, no hay función para limpiar el cache. Reinicia el programa o edita el código directamente.

---

## 🐛 Troubleshooting

### Error: "Could not load provider_urls.json"

**Causa:** El archivo `provider_urls.json` no se encuentra o está corrupto.

**Solución:**
1. Verifica que `provider_urls.json` esté en `luminoracore_sdk/config/`
2. Verifica que el JSON sea válido:
   ```bash
   python -c "import json; json.load(open('luminoracore_sdk/config/provider_urls.json'))"
   ```
3. El módulo retornará un diccionario vacío `{}` como fallback

---

### Provider no encontrado

**Causa:** El provider no está en `provider_urls.json`.

**Solución:**
- Agregar el provider a `provider_urls.json` en la sección `custom_providers`
- O usar valores hardcoded al crear el `ProviderConfig`

---

### Custom provider no se carga

**Causa:** La clave del custom provider empieza con `_` (comentario).

**Solución:**
- Las claves que empiezan con `_` se ignoran automáticamente
- Usa una clave sin `_`:
  ```json
  {
    "custom_providers": {
      "my_provider": { ... },  // ✅ Se carga
      "_example": { ... }       // ❌ Se ignora (comentario)
    }
  }
  ```

---

## 📚 Más Información

- **Providers:** `../providers/README.md`
- **ProviderFactory:** `../providers/factory.py`
- **ProviderConfig:** `../types/provider.py`

---

**Última Actualización:** 2025-11-21  
**Versión SDK:** 1.2.0  
**Estado:** ✅ Módulo completo y funcionando

