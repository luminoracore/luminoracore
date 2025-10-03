# 🐍 LuminoraCore SDK Python

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/luminoracore/sdk-python)
[![Status](https://img.shields.io/badge/status-90%25_complete-orange.svg)](#)

**✅ SDK OFICIAL DE PYTHON - 90% COMPLETO**

**LuminoraCore SDK Python** es el cliente oficial de Python para gestión avanzada de personalidades de IA. Proporciona un conjunto completo de herramientas para construir aplicaciones de IA con sistemas sofisticados de personalidades, gestión de sesiones y soporte multi-proveedor LLM.

## Características Principales

- **✅ Gestión Avanzada de Personalidades**: Crear, mezclar y gestionar personalidades de IA con facilidad
- **✅ Gestión de Sesiones**: Conversaciones con estado y memoria persistente
- **✅ Soporte Multi-Provider**: Integración con OpenAI, Anthropic, Mistral, Cohere, Google y más
- **✅ PersonaBlend™ Technology**: Mezcla de personalidades en tiempo real con pesos personalizados
- **✅ Almacenamiento Flexible**: Soporte para Redis, PostgreSQL, MongoDB y almacenamiento en memoria
- **✅ Monitoreo y Métricas**: Observabilidad integrada con trazado distribuido
- **✅ Soporte Async/Await**: API completamente asíncrona para aplicaciones de alto rendimiento
- **✅ Seguridad de Tipos**: Definiciones de tipos comprehensivas y validación
- **✅ Conexiones API Reales**: APIs reales a todos los proveedores de LLM
- **✅ Manejo Robusto de Errores**: Reintentos automáticos y fallbacks
- **✅ Analytics Completos**: Tracking de tokens, costos y uso

## Instalación

```bash
pip install -e luminoracore-sdk-python/
```

## Inicio Rápido

```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig
from luminoracore.types.storage import StorageConfig

async def main():
    # Inicializar el cliente
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Configurar almacenamiento (Redis, PostgreSQL, etc.)
    storage_config = StorageConfig(
        storage_type="redis",
        connection_string="redis://localhost:6379"
    )
    await client.configure_storage(storage_config)
    
    # Crear configuración del proveedor
    provider_config = ProviderConfig(
        name="openai",
        api_key="tu-api-key",
        model="gpt-3.5-turbo",
        extra={"timeout": 30, "max_retries": 3}
    )
    
    # Crear una sesión
    session_id = await client.create_session(
        personality_name="dr_luna",
        provider_config=provider_config
    )
    
    # Enviar un mensaje (conexión real a OpenAI)
    response = await client.send_message(
        session_id=session_id,
        message="¡Hola! ¿Puedes ayudarme con física cuántica?"
    )
    
    print(f"Respuesta: {response.content}")
    print(f"Tokens usados: {response.usage}")
    print(f"Costo: ${response.cost}")
    
    # Obtener métricas
    metrics = await client.get_session_metrics(session_id)
    print(f"Mensajes totales: {metrics.total_messages}")
    
    # Limpiar
    await client.cleanup()

# Ejecutar el ejemplo
asyncio.run(main())
```

## Advanced Usage

### Personality Blending

```python
# Blend multiple personalities
blended_personality = await client.blend_personalities(
    personality_names=["creative_writer", "technical_expert"],
    weights=[0.3, 0.7],
    blend_name="creative_technical_expert"
)

# Create a session with the blended personality
session_id = await client.create_session(
    personality_name="creative_technical_expert",
    provider_config=provider_config
)
```

### Memory Management

```python
# Store session memory
await client.store_memory(
    session_id=session_id,
    key="user_preference",
    value="interested in AI personality blending",
    ttl=3600
)

# Retrieve memory
memory = await client.get_memory(session_id, "user_preference")
```

### Streaming Responses

```python
# Stream a response
async for chunk in client.stream_message(
    session_id=session_id,
    message="Tell me a story"
):
    print(chunk.content, end="", flush=True)
```

## Configuration

### Storage Configuration

```python
from luminoracore.types.session import StorageConfig

# Redis storage
storage_config = StorageConfig(
    storage_type="redis",
    connection_string="redis://localhost:6379"
)

# PostgreSQL storage
storage_config = StorageConfig(
    storage_type="postgres",
    connection_string="postgresql://user:password@localhost/db"
)

# MongoDB storage
storage_config = StorageConfig(
    storage_type="mongodb",
    connection_string="mongodb://localhost:27017/db"
)

# In-memory storage (default)
storage_config = StorageConfig(
    storage_type="memory"
)
```

### Memory Configuration

```python
from luminoracore.types.session import MemoryConfig

memory_config = MemoryConfig(
    enabled=True,
    max_entries=1000,
    decay_factor=0.1,
    importance_threshold=0.5,
    track_topics=True,
    track_preferences=True,
    track_context=True,
    track_emotions=False
)
```

## Supported Providers

- **OpenAI**: GPT-3.5, GPT-4, and other OpenAI models
- **Anthropic**: Claude-3 Sonnet, Claude-3 Haiku, and other Claude models
- **Mistral**: Mistral Tiny, Mistral Small, and other Mistral models
- **Cohere**: Command, Command Light, and other Cohere models
- **Google**: Gemini Pro, Gemini Ultra, and other Google models
- **Llama**: Llama-2, Llama-3, and other Llama models

## Examples

Check out the `examples/` directory for comprehensive examples:

- `basic_usage.py` - Basic usage examples
- `simple_usage.py` - Simple usage examples
- `personality_blending.py` - Personality blending examples
- `integrations/fastapi_integration.py` - FastAPI integration
- `integrations/streamlit_app.py` - Streamlit web app

## Testing

```bash
# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run all tests with coverage
pytest --cov=luminoracore tests/
```

## Development

```bash
# Clone the repository
git clone https://github.com/luminoracore/sdk-python.git
cd sdk-python

# Install development dependencies
pip install -e ".[dev]"

# Run linting
black luminoracore/
isort luminoracore/
mypy luminoracore/

# Run tests
pytest
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## API Documentation

- 📚 [API Reference](docs/api_reference.md) - Complete API documentation
- 📖 [Examples](examples/) - Code examples and tutorials

## Support

- 📚 [Documentation](https://docs.luminoracore.com)
- 💬 [Discord Community](https://discord.gg/luminoracore)
- 🐛 [Issue Tracker](https://github.com/luminoracore/sdk-python/issues)
- 📧 [Email Support](mailto:support@luminoracore.com)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.
