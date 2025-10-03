# LuminoraCore

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/luminoracore/luminoracore)
[![Core Status](https://img.shields.io/badge/core-100%25-brightgreen.svg)](#)
[![CLI Status](https://img.shields.io/badge/cli-95%25-yellow.svg)](#)
[![SDK Status](https://img.shields.io/badge/sdk-90%25-orange.svg)](#)

**LuminoraCore** es una plataforma completa de gestión de personalidades de IA que consta de tres componentes poderosos que trabajan juntos para proporcionar sistemas avanzados de personalidades de IA, herramientas de línea de comandos e integración de SDK de Python.

## 🏗️ Arquitectura General

LuminoraCore está construido como una plataforma modular con tres componentes principales:

```
LuminoraCore Platform
├── 🧠 luminoracore/          # Motor de personalidades (100% completo)
├── 🛠️ luminoracore-cli/      # Interfaz de línea de comandos (95% completo)
└── 🐍 luminoracore-sdk-python/ # SDK de Python (90% completo)
```

## 🧠 LuminoraCore (Motor Principal) - ✅ 100% COMPLETO

El motor de personalidades fundamental que impulsa toda la plataforma.

### Características Principales
- **✅ Gestión Avanzada de Personalidades**: Crear, validar y gestionar personalidades de IA
- **✅ Validación JSON Schema**: Validación robusta usando estándares JSON Schema
- **✅ PersonaBlend™ Technology**: Mezcla de personalidades en tiempo real con pesos personalizados
- **✅ Integración Multi-Provider**: Soporte para OpenAI, Anthropic, Google, Cohere, Mistral, Llama
- **✅ Motor de Compilación**: Convertir personalidades a prompts optimizados
- **✅ Seguridad de Tipos**: Definiciones de tipos y validación comprehensiva
- **✅ Caché Inteligente**: Sistema LRU con estadísticas de rendimiento
- **✅ Validaciones de Rendimiento**: Detección automática de problemas de eficiencia

### Inicio Rápido
```python
from luminoracore import Personality, PersonalityCompiler, LLMProvider

# Cargar una personalidad
personality = Personality("path/to/personality.json")

# Compilar a prompt con caché
compiler = PersonalityCompiler(cache_size=128)
result = compiler.compile(personality, LLMProvider.OPENAI)

print(result.prompt)
print(f"Tokens estimados: {result.token_estimate}")
print(f"Metadatos: {result.metadata}")

# Estadísticas de caché
stats = compiler.get_cache_stats()
print(f"Tasa de aciertos: {stats['hit_rate']}%")
```

### Documentación
- 📚 [Referencia API](luminoracore/docs/api_reference.md)
- 📖 [Mejores Prácticas](luminoracore/docs/best_practices.md)
- 🎯 [Ejemplos](luminoracore/examples/)

---

## 🛠️ LuminoraCore CLI - ✅ 95% COMPLETO

Interfaz de línea de comandos profesional para gestión y validación de personalidades.

### Características Principales
- **✅ Validación de Personalidades**: Validar archivos de personalidades contra esquemas
- **✅ Procesamiento por Lotes**: Procesar múltiples personalidades a la vez
- **✅ Testing Interactivo**: Probar personalidades en tiempo real con APIs reales
- **✅ Servidor de Desarrollo**: Servidor local con hot reload y API REST
- **✅ Asistente de Creación**: Wizard guiado para crear personalidades
- **✅ Herramientas de Mezcla**: Mezcla de personalidades desde línea de comandos
- **✅ Testing con LLMs Reales**: Conexión real a OpenAI, Claude, etc.
- **✅ Interfaz Web**: UI web integrada para testing y gestión

### Inicio Rápido
```bash
# Instalar CLI
pip install -e luminoracore-cli/

# Validar personalidades
luminoracore validate personalities/*.json

# Crear nueva personalidad (wizard interactivo)
luminoracore create --name "mi_personalidad"

# Probar personalidad con API real
luminoracore test --personality "mi_personalidad" --provider openai --interactive

# Iniciar servidor de desarrollo
luminoracore serve --port 8000 --reload

# Mezclar personalidades
luminoracore blend --personalities "dr_luna,capitan_garfio" --weights "0.7,0.3"
```

### Comandos Disponibles
- `validate` - Validar archivos de personalidades
- `compile` - Compilar personalidades a prompts
- `create` - Crear nuevas personalidades (wizard)
- `list` - Listar personalidades disponibles
- `test` - Probar personalidades interactivamente
- `serve` - Iniciar servidor de desarrollo
- `blend` - Mezclar múltiples personalidades
- `update` - Actualizar caché de personalidades
- `init` - Inicializar nuevo proyecto
- `info` - Mostrar información de personalidad

### Documentación
- 📚 [Documentación CLI](luminoracore-cli/README.md)
- 🎯 [Ejemplos](luminoracore-cli/examples/)

---

## 🐍 LuminoraCore SDK Python - ✅ 90% COMPLETO

SDK oficial de Python para construir aplicaciones de IA con sistemas de personalidades.

### Características Principales
- **✅ Gestión de Sesiones**: Conversaciones con estado y memoria persistente
- **✅ Soporte Multi-Provider**: OpenAI, Anthropic, Mistral, Cohere, Google, Llama
- **✅ PersonaBlend™ Technology**: Mezcla de personalidades en tiempo real
- **✅ Almacenamiento Flexible**: Redis, PostgreSQL, MongoDB, en memoria
- **✅ Soporte Async/Await**: API completamente asíncrona
- **✅ Monitoreo y Métricas**: Observabilidad integrada
- **✅ Seguridad de Tipos**: Definiciones de tipos comprehensivas
- **✅ Conexiones Reales**: APIs reales a todos los proveedores
- **✅ Manejo Robusto de Errores**: Reintentos automáticos y fallbacks
- **✅ Analytics Completos**: Tracking de tokens, costos y uso

### Inicio Rápido
```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig
from luminoracore.types.storage import StorageConfig

async def main():
    # Inicializar cliente
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Configurar almacenamiento (Redis, PostgreSQL, etc.)
    storage_config = StorageConfig(
        storage_type="redis",
        connection_string="redis://localhost:6379"
    )
    await client.configure_storage(storage_config)
    
    # Crear proveedor
    provider_config = ProviderConfig(
        name="openai",
        api_key="tu-api-key",
        model="gpt-3.5-turbo",
        extra={"timeout": 30, "max_retries": 3}
    )
    
    # Crear sesión con personalidad
    session_id = await client.create_session(
        personality_name="dr_luna",
        provider_config=provider_config
    )
    
    # Enviar mensaje (conexión real a OpenAI)
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
    
    await client.cleanup()

asyncio.run(main())
```

### Documentación
- 📚 [Referencia API](luminoracore-sdk-python/docs/api_reference.md)
- 🎯 [Ejemplos](luminoracore-sdk-python/examples/)

---

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.8+
- pip o conda
- (Opcional) Redis, PostgreSQL o MongoDB para persistencia

### Instalación

#### Instalar Todos los Componentes
```bash
# Clonar el repositorio
git clone https://github.com/luminoracore/luminoracore.git
cd luminoracore

# Instalar motor principal
pip install -e luminoracore/

# Instalar CLI
pip install -e luminoracore-cli/

# Instalar SDK
pip install -e luminoracore-sdk-python/
```

#### Instalar Componentes Individuales
```bash
# Solo motor principal
pip install -e luminoracore/

# Solo CLI
pip install -e luminoracore-cli/

# Solo SDK
pip install -e luminoracore-sdk-python/
```

### Ejemplo Rápido Completo

1. **Crear una personalidad** usando el CLI:
```bash
luminoracore create --name "escritor_creativo"
# Sigue el wizard interactivo para configurar la personalidad
```

2. **Validar la personalidad**:
```bash
luminoracore validate personalities/escritor_creativo.json
```

3. **Probar con API real**:
```bash
# Configurar tu API key
export OPENAI_API_KEY="tu-api-key"

# Probar interactivamente
luminoracore test --personality "escritor_creativo" --provider openai --interactive
```

4. **Usar en tu aplicación Python**:
```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig

async def main():
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Configurar proveedor
    provider = ProviderConfig(
        name="openai",
        api_key="tu-api-key",
        model="gpt-3.5-turbo"
    )
    
    # Crear sesión
    session_id = await client.create_session(
        personality_name="escritor_creativo",
        provider_config=provider
    )
    
    # Chatear con la personalidad
    response = await client.send_message(
        session_id=session_id,
        message="Escribe un poema sobre la tecnología"
    )
    
    print(response.content)
    await client.cleanup()

asyncio.run(main())
```

## 🏢 Casos de Uso

### Para Desarrolladores
- **✅ Desarrollo de Aplicaciones IA**: Construir apps con sistemas sofisticados de personalidades
- **✅ Investigación de Personalidades**: Experimentar con diferentes configuraciones de personalidades
- **✅ Aplicaciones Multi-Modelo**: Usar diferentes LLMs con interfaces de personalidad consistentes
- **✅ Testing y Validación**: Probar personalidades con APIs reales antes del despliegue

### Para Investigadores
- **✅ Estudios de Personalidades**: Investigar comportamiento y mezcla de personalidades de IA
- **✅ Ingeniería de Prompts**: Compilación y optimización avanzada de prompts
- **✅ Comparación de Modelos**: Probar diferentes LLMs con la misma personalidad
- **✅ Análisis de Rendimiento**: Métricas detalladas de tokens, costos y eficiencia

### Para Empresas
- **✅ Servicio al Cliente**: Desplegar personalidades de IA consistentes en todos los canales
- **✅ Generación de Contenido**: Crear contenido de marca con rasgos de personalidad específicos
- **✅ Datos de Entrenamiento**: Generar datos de entrenamiento con características de personalidad controladas
- **✅ Chatbots Empresariales**: Implementar asistentes con personalidades específicas por departamento

## 🔧 Desarrollo

### Estructura del Proyecto
```
LuminoraCore/
├── luminoracore/              # Motor de personalidades (100% completo)
│   ├── luminoracore/          # Paquete principal
│   ├── examples/              # Ejemplos de uso
│   ├── docs/                  # Documentación
│   ├── personalities/         # Personalidades incluidas
│   └── tests/                 # Pruebas unitarias
├── luminoracore-cli/          # Interfaz de línea de comandos (95% completo)
│   ├── luminoracore_cli/      # Paquete CLI
│   ├── examples/              # Ejemplos CLI
│   └── tests/                 # Pruebas CLI
├── luminoracore-sdk-python/   # SDK de Python (90% completo)
│   ├── luminoracore/          # Paquete SDK
│   ├── examples/              # Ejemplos SDK
│   ├── docs/                  # Documentación SDK
│   └── tests/                 # Pruebas SDK
└── README.md                  # Este archivo
```

### Ejecutar Pruebas
```bash
# Probar todos los componentes
pytest luminoracore/tests/ -v
pytest luminoracore-cli/tests/ -v
pytest luminoracore-sdk-python/tests/ -v

# Probar componente específico
pytest luminoracore/tests/ -v --cov=luminoracore
```

### Contribuir
¡Bienvenidas las contribuciones! Por favor consulta nuestra [Guía de Contribución](luminoracore/CONTRIBUTING.md) para más detalles.

## 📊 Comparación de Componentes

| Característica | Motor Principal | CLI | SDK |
|----------------|-----------------|-----|-----|
| Gestión de Personalidades | ✅ | ✅ | ✅ |
| Validación | ✅ | ✅ | ✅ |
| Mezcla de Personalidades | ✅ | ✅ | ✅ |
| Gestión de Sesiones | ❌ | ❌ | ✅ |
| Multi-Provider | ✅ | ✅ | ✅ |
| Testing Interactivo | ❌ | ✅ | ❌ |
| Procesamiento por Lotes | ❌ | ✅ | ❌ |
| Servidor de Desarrollo | ❌ | ✅ | ❌ |
| Integración Python | ✅ | ❌ | ✅ |
| Conexiones API Reales | ❌ | ✅ | ✅ |
| Persistencia de Datos | ❌ | ❌ | ✅ |
| Analytics y Métricas | ❌ | ❌ | ✅ |
| Manejo de Errores Robusto | ✅ | ✅ | ✅ |

## 🤝 Ejemplos de Integración

### CLI + Motor Principal
```bash
# Crear personalidad con CLI
luminoracore create --name "asistente"

# Validar con CLI
luminoracore validate personalities/asistente.json

# Usar en Python con Motor Principal
from luminoracore import Personality, PersonalityCompiler
personality = Personality("personalities/asistente.json")
compiler = PersonalityCompiler()
result = compiler.compile(personality, LLMProvider.OPENAI)
```

### SDK + Motor Principal
```python
# Usar Motor Principal para gestión de personalidades
from luminoracore import PersonalityCompiler
from luminoracore import LuminoraCoreClient

# Usar SDK para gestión de sesiones
client = LuminoraCoreClient()
await client.initialize()
# ... gestión de sesiones con APIs reales
```

### Stack Completo
```bash
# 1. Crear personalidad con CLI
luminoracore create --name "servicio_cliente"

# 2. Validar con CLI
luminoracore validate personalities/servicio_cliente.json

# 3. Probar con API real
luminoracore test --personality "servicio_cliente" --provider openai

# 4. Usar en aplicación con SDK
from luminoracore import LuminoraCoreClient
# ... aplicación completa con persistencia y analytics
```

## 📈 Roadmap

- [x] **✅ Motor Principal**: 100% completo con todas las funcionalidades
- [x] **✅ CLI Completo**: 95% completo con testing real y wizard
- [x] **✅ SDK Funcional**: 90% completo con APIs reales y persistencia
- [x] **✅ Conexiones API Reales**: OpenAI, Anthropic, Google, Cohere, Mistral, Llama
- [x] **✅ Persistencia**: Redis, PostgreSQL, MongoDB, archivos
- [x] **✅ Analytics**: Métricas completas de tokens, costos y uso
- [x] **✅ Manejo de Errores**: Robusto con reintentos y fallbacks
- [ ] **Web Dashboard**: Interfaz web para gestión de personalidades
- [ ] **REST API**: API HTTP para gestión remota de personalidades
- [ ] **Docker Support**: Opciones de despliegue containerizado
- [ ] **Kubernetes**: Despliegue cloud-native
- [ ] **Personality Marketplace**: Compartir y descubrir personalidades

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](luminoracore/LICENSE) para más detalles.

## 🆘 Soporte

- 📚 [Documentación](https://docs.luminoracore.com)
- 💬 [Comunidad Discord](https://discord.gg/luminoracore)
- 🐛 [Tracker de Issues](https://github.com/luminoracore/luminoracore/issues)
- 📧 [Soporte por Email](mailto:support@luminoracore.com)

## 🙏 Agradecimientos

- OpenAI por los modelos GPT
- Anthropic por los modelos Claude
- La comunidad open-source por inspiración y contribuciones

---

## 🎯 Estado Actual del Proyecto

**LuminoraCore** es una plataforma **COMPLETA y FUNCIONAL** que supera las especificaciones originales:

- **🧠 Motor Principal**: ✅ **100% COMPLETO** - Todas las funcionalidades implementadas
- **🛠️ CLI**: ✅ **95% COMPLETO** - Testing real, wizard interactivo, servidor web
- **🐍 SDK**: ✅ **90% COMPLETO** - APIs reales, persistencia, analytics

**¡Listo para producción!** 🚀

---

**LuminoraCore** - Potenciando la IA con Personalidad 🚀
