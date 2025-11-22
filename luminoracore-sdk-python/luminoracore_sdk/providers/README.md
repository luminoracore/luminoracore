# LuminoraCore SDK - Providers Module

Módulo de proveedores LLM para el SDK.

---

## 📋 Componentes

### 1. BaseProvider (`base.py`)

**Propósito:** Clase base abstracta para todos los proveedores LLM.

**Características:**
- ✅ Interfaz común para todos los providers
- ✅ Retry automático con backoff
- ✅ Manejo de errores unificado
- ✅ Soporte para streaming
- ✅ Integración con Core Personality (v1.2.0)

**Métodos Abstractos:**
- `get_default_model() -> str` - Modelo por defecto
- `chat()` - Enviar mensaje
- `stream_chat()` - Stream de mensajes

**Métodos Opcionales:**
- `chat_with_personality()` - Chat con personalidad (usa Core)
- `stream_chat_with_personality()` - Stream con personalidad (usa Core)

---

### 2. ProviderFactory (`factory.py`)

**Propósito:** Factory para crear instancias de providers.

**Características:**
- ✅ Registro de providers
- ✅ Creación desde config
- ✅ Creación desde dict
- ✅ Creación desde env vars
- ✅ Múltiples providers

**Uso:**
```python
from luminoracore_sdk.providers import ProviderFactory
from luminoracore_sdk.types.provider import ProviderConfig

# Crear desde config
config = ProviderConfig(
    name="openai",
    api_key="your-key",
    model="gpt-3.5-turbo"
)
provider = ProviderFactory.create_provider(config)

# Crear desde dict
provider = ProviderFactory.create_provider_from_dict({
    "name": "openai",
    "api_key": "your-key",
    "model": "gpt-3.5-turbo"
})

# Crear desde env vars
provider = ProviderFactory.create_provider_from_env("openai")
```

---

### 3. Providers Implementados

#### OpenAIProvider (`openai.py`)
- ✅ Modelos: gpt-3.5-turbo, gpt-4, gpt-4-turbo
- ✅ Streaming support
- ✅ Function calling support

#### AnthropicProvider (`anthropic.py`)
- ✅ Modelos: claude-3-sonnet, claude-3-opus, claude-3-haiku
- ✅ Streaming support
- ✅ System messages support

#### DeepSeekProvider (`deepseek.py`)
- ✅ Modelos: deepseek-chat, deepseek-coder
- ✅ OpenAI-compatible API

#### GoogleProvider (`google.py`)
- ✅ Modelos: gemini-pro, gemini-pro-vision
- ✅ Streaming support

#### CohereProvider (`cohere.py`)
- ✅ Modelos: command, command-light
- ✅ Streaming support

#### MistralProvider (`mistral.py`)
- ✅ Modelos: mistral-tiny, mistral-small, mistral-medium
- ✅ Streaming support

#### LlamaProvider (`llama.py`)
- ✅ Modelos locales: llama-2, llama-3
- ✅ OpenAI-compatible API

---

## 🔧 Uso Básico

### Crear Provider

```python
from luminoracore_sdk.providers import OpenAIProvider
from luminoracore_sdk.types.provider import ProviderConfig

config = ProviderConfig(
    name="openai",
    api_key="your-api-key",
    model="gpt-3.5-turbo"
)

provider = OpenAIProvider(config)
```

### Enviar Mensaje

```python
from luminoracore_sdk.types.provider import ChatMessage

messages = [
    ChatMessage(role="system", content="You are a helpful assistant."),
    ChatMessage(role="user", content="Hello!")
]

response = await provider.chat(messages)
print(response.content)
```

### Streaming

```python
async for chunk in provider.stream_chat(messages):
    print(chunk.content, end="", flush=True)
```

---

## 🆕 v1.2.0 - Core Integration

### Chat con Personalidad

Los providers ahora pueden usar Core Personality para compilar system prompts:

```python
# Esto usa Core PersonalityCompiler internamente
response = await provider.chat_with_personality(
    personality_data={
        "persona": {
            "name": "Dr. Luna",
            "description": "A scientific assistant"
        },
        "core_traits": {...},
        ...
    },
    user_message="Explain quantum computing",
    conversation_history=[]
)
```

**Requisitos:**
- `luminoracore>=1.2.0` (Core package)
- Se lanza error si Core no está disponible

**Internamente:**
1. Crea `Personality` desde Core
2. Usa `PersonalityCompiler` para compilar system prompt
3. Aplica personalidad a la conversación

---

## 📊 Providers Disponibles

| Provider | Clase | Modelos Default | Streaming |
|----------|-------|-----------------|-----------|
| **OpenAI** | `OpenAIProvider` | gpt-3.5-turbo | ✅ |
| **Anthropic** | `AnthropicProvider` | claude-3-sonnet | ✅ |
| **DeepSeek** | `DeepSeekProvider` | deepseek-chat | ✅ |
| **Google** | `GoogleProvider` | gemini-pro | ✅ |
| **Cohere** | `CohereProvider` | command | ✅ |
| **Mistral** | `MistralProvider` | mistral-tiny | ✅ |
| **Llama** | `LlamaProvider` | llama-2 | ✅ |

---

## 🔄 Retry y Error Handling

Todos los providers incluyen retry automático:

```python
# Configurar retry en ProviderConfig
config = ProviderConfig(
    name="openai",
    api_key="your-key",
    model="gpt-3.5-turbo",
    extra={
        "timeout": 30,
        "max_retries": 3  # Retry automático
    }
)
```

**Comportamiento:**
- ✅ Retry con exponential backoff
- ✅ Manejo de rate limits
- ✅ Timeout handling
- ✅ Error logging

---

## 🎯 Ejemplo Completo

```python
import asyncio
from luminoracore_sdk.providers import ProviderFactory
from luminoracore_sdk.types.provider import ProviderConfig, ChatMessage

async def main():
    # Crear provider
    config = ProviderConfig(
        name="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo"
    )
    
    provider = ProviderFactory.create_provider(config)
    
    # Enviar mensaje
    messages = [
        ChatMessage(role="user", content="Hello!")
    ]
    
    response = await provider.chat(messages)
    print(f"Response: {response.content}")
    
    # Streaming
    print("Streaming response:")
    async for chunk in provider.stream_chat(messages):
        print(chunk.content, end="", flush=True)

asyncio.run(main())
```

---

## 🐛 Troubleshooting

### Error: "API key is required"

**Solución:** Asegúrate de proporcionar la API key:
```python
config = ProviderConfig(
    name="openai",
    api_key="your-key-here"  # ✅ Requerido
)
```

### Error: "Unsupported provider type"

**Solución:** Verifica que el provider esté registrado:
```python
available = ProviderFactory.get_available_providers()
print(f"Available: {available}")
```

### Error: "Core components not available"

**Solución:** Solo ocurre si usas `chat_with_personality()`. Instala Core:
```bash
pip install -e ../luminoracore/
```

---

## 📚 Más Información

- **Client Documentation:** `../client.py`
- **Types:** `../types/provider.py`
- **Core Integration:** `../../luminoracore/tools/compiler.py`

---

**Última Actualización:** 2025-11-21  
**Versión SDK:** 1.2.0  
**Estado:** ✅ Módulo completo y funcionando

