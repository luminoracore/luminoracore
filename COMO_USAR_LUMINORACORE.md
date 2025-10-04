# 🎯 Cómo Usar LuminoraCore - Guía Visual Rápida

## 🚀 En 3 Pasos

```
┌─────────────────────────────────────────────┐
│  PASO 1: Instalar                           │
│  .\instalar_todo.ps1                        │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│  PASO 2: Verificar                          │
│  python ejemplo_quick_start_core.py         │
└─────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│  PASO 3: Usar                               │
│  from luminoracore import Personality       │
└─────────────────────────────────────────────┘
```

---

## 📚 3 Componentes = 3 Formas de Usar

### 1️⃣ LuminoraCore (Motor Base) - Para Desarrollo Python

**¿Qué hace?**
- Carga y valida personalidades
- Compila para diferentes LLMs
- Mezcla personalidades

**Instalación:**
```bash
cd luminoracore
pip install -e .
```

**Uso básico:**
```python
from luminoracore import Personality, PersonalityValidator

# Cargar personalidad
personality = Personality("mi_personalidad.json")

# Validar
validator = PersonalityValidator()
result = validator.validate(personality)

# Compilar
from luminoracore import PersonalityCompiler, LLMProvider
compiler = PersonalityCompiler()
compiled = compiler.compile(personality, LLMProvider.OPENAI)
print(compiled.prompt)
```

**Cuándo usarlo:**
- Estás construyendo una librería Python
- Solo necesitas validación/compilación
- No necesitas llamadas a APIs

---

### 2️⃣ LuminoraCore CLI - Para Línea de Comandos

**¿Qué hace?**
- Gestiona personalidades desde la terminal
- Crea personalidades con wizard
- Servidor web de desarrollo

**Instalación:**
```bash
cd luminoracore-cli
pip install -e .
```

**Uso básico:**
```bash
# Listar personalidades
luminoracore list

# Validar
luminoracore validate personalidad.json

# Crear nueva
luminoracore create --interactive

# Compilar
luminoracore compile personalidad.json --provider openai

# Servidor web
luminoracore serve
```

**Cuándo usarlo:**
- Prefieres trabajar en terminal
- Quieres un wizard interactivo
- Necesitas interfaz web rápida
- Scripts de automatización

---

### 3️⃣ LuminoraCore SDK - Para Aplicaciones Completas

**¿Qué hace?**
- Conexiones REALES a OpenAI, Anthropic, etc.
- Gestión de sesiones y conversaciones
- Memoria persistente
- Monitoreo y métricas

**Instalación:**
```bash
cd luminoracore-sdk-python
pip install -e ".[openai]"  # O [all] para todos los providers
```

**Uso básico:**
```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig

async def main():
    # Crear cliente
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Configurar proveedor
    provider_config = ProviderConfig(
        name="openai",
        api_key="tu-api-key",
        model="gpt-3.5-turbo"
    )
    
    # Crear sesión
    session_id = await client.create_session(
        personality_name="asistente",
        provider_config=provider_config
    )
    
    # ¡Enviar mensaje real!
    response = await client.send_message(
        session_id=session_id,
        message="Hola, explícame Python"
    )
    
    print(response.content)
    await client.cleanup()

asyncio.run(main())
```

**Cuándo usarlo:**
- Construyes un chatbot/asistente
- Necesitas llamadas reales a LLMs
- Quieres gestión de sesiones
- Aplicación de producción

---

## 🎯 Tabla de Decisión Rápida

| Necesito... | Usa | Instalación | Ejemplo |
|-------------|-----|-------------|---------|
| Solo validar archivos | CLI | `cd luminoracore-cli && pip install -e .` | `luminoracore validate file.json` |
| Compilar prompts | Core | `cd luminoracore && pip install -e .` | Ver código arriba |
| Crear personalidades | CLI | `cd luminoracore-cli && pip install -e .` | `luminoracore create --interactive` |
| Chatbot con OpenAI | SDK | `cd luminoracore-sdk-python && pip install -e ".[openai]"` | Ver código arriba |
| Interfaz web | CLI | `cd luminoracore-cli && pip install -e .` | `luminoracore serve` |
| Mezclar personalidades | Core o CLI | Ambos | Ver ejemplos |
| App de producción | SDK | `cd luminoracore-sdk-python && pip install -e ".[all]"` | Ver integrations/ |

---

## 💡 Ejemplos Prácticos Completos

### Ejemplo 1: Validar todas mis personalidades

**Opción A: Con CLI**
```bash
luminoracore validate personalidades/*.json
```

**Opción B: Con Python**
```python
from luminoracore import Personality, PersonalityValidator
from pathlib import Path

validator = PersonalityValidator()

for file in Path("personalidades").glob("*.json"):
    personality = Personality(str(file))
    result = validator.validate(personality)
    
    if result.is_valid:
        print(f"✅ {file.name}: Válido")
    else:
        print(f"❌ {file.name}: {result.errors}")
```

---

### Ejemplo 2: Crear un chatbot simple

```python
import asyncio
import os
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig

async def chatbot():
    # Setup
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Cargar personalidad
    personality = {
        "name": "asistente_amigable",
        "system_prompt": "Eres un asistente amigable y servicial.",
        "metadata": {"version": "1.0.0"}
    }
    await client.load_personality("asistente_amigable", personality)
    
    # Configurar OpenAI
    provider_config = ProviderConfig(
        name="openai",
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-3.5-turbo"
    )
    
    # Crear sesión
    session_id = await client.create_session(
        personality_name="asistente_amigable",
        provider_config=provider_config
    )
    
    # Chat loop
    print("Chatbot iniciado. Escribe 'salir' para terminar.")
    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ['salir', 'exit', 'quit']:
            break
            
        response = await client.send_message(
            session_id=session_id,
            message=user_input
        )
        print(f"Bot: {response.content}")
    
    await client.cleanup()

# Ejecutar
asyncio.run(chatbot())
```

---

### Ejemplo 3: Mezclar dos personalidades

**Opción A: Con CLI**
```bash
luminoracore blend \
  "personalidades/Dr. Luna Científica Entusiasta.json:0.7" \
  "personalidades/Rocky Inspiración.json:0.3" \
  --output cientifico_motivador.json
```

**Opción B: Con Python**
```python
from luminoracore import Personality, PersonalityBlender

# Cargar personalidades
dr_luna = Personality("personalidades/Dr. Luna Científica Entusiasta.json")
rocky = Personality("personalidades/Rocky Inspiración.json")

# Mezclar (70% científico, 30% motivador)
blender = PersonalityBlender()
blended = blender.blend(
    personalities=[dr_luna, rocky],
    weights=[0.7, 0.3],
    strategy="weighted_average"
)

print(f"Nueva personalidad: {blended.persona.name}")
print(f"Descripción: {blended.persona.description}")
```

---

### Ejemplo 4: Servidor web de pruebas

```bash
# Iniciar servidor
luminoracore serve --port 8000

# Abre en tu navegador: http://localhost:8000
```

Esto te da:
- ✅ Interfaz web para probar personalidades
- ✅ API REST para usar programáticamente
- ✅ WebSocket para chat en tiempo real
- ✅ Documentación automática en /docs

---

## 🔗 Dependencias entre Componentes

```
luminoracore (Motor Base)
    ↓
    ├── luminoracore-cli depende de → luminoracore
    └── luminoracore-sdk depende de → luminoracore
```

**Importante:** Siempre instala `luminoracore` primero si instalas manualmente.

---

## ⚙️ Instalación Según tu Caso de Uso

### Caso 1: Solo quiero probar y experimentar
```bash
.\instalar_todo.ps1  # Instala todo
```

### Caso 2: Solo necesito validación y compilación
```bash
cd luminoracore
pip install -e .
```

### Caso 3: Solo necesito el CLI
```bash
cd luminoracore && pip install -e . && cd ..
cd luminoracore-cli && pip install -e . && cd ..
```

### Caso 4: Voy a construir una app de producción
```bash
cd luminoracore && pip install -e . && cd ..
cd luminoracore-sdk-python && pip install -e ".[all]" && cd ..
```

---

## 🎨 Flujo de Trabajo Típico

```
┌─────────────────────────┐
│ 1. Crear Personalidad   │
│    luminoracore create  │
│    --interactive        │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ 2. Validar              │
│    luminoracore         │
│    validate file.json   │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ 3. Probar Localmente    │
│    luminoracore serve   │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ 4. Integrar en App      │
│    Usar SDK             │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│ 5. Desplegar            │
│    Tu aplicación        │
└─────────────────────────┘
```

---

## 📝 Comandos Más Usados

### CLI

```bash
# Ayuda
luminoracore --help

# Listar personalidades
luminoracore list
luminoracore list --detailed

# Validar
luminoracore validate archivo.json
luminoracore validate carpeta/ --strict

# Compilar
luminoracore compile archivo.json --provider openai
luminoracore compile archivo.json --provider anthropic --output prompt.txt

# Crear
luminoracore create --interactive
luminoracore create --name "Mi Asistente" --archetype helper

# Mezclar
luminoracore blend p1.json:0.6 p2.json:0.4
luminoracore blend p1.json:0.5 p2.json:0.3 p3.json:0.2

# Servidor
luminoracore serve
luminoracore serve --port 3000
```

### Python (Motor Base)

```python
from luminoracore import (
    Personality,
    PersonalityValidator,
    PersonalityCompiler,
    PersonalityBlender,
    LLMProvider
)

# Cargar
p = Personality("file.json")

# Validar
validator = PersonalityValidator()
result = validator.validate(p)

# Compilar
compiler = PersonalityCompiler()
compiled = compiler.compile(p, LLMProvider.OPENAI)

# Mezclar
blender = PersonalityBlender()
blended = blender.blend([p1, p2], [0.6, 0.4])
```

### Python (SDK)

```python
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig

# Crear cliente
client = LuminoraCoreClient()
await client.initialize()

# Crear sesión
session_id = await client.create_session(
    personality_name="nombre",
    provider_config=config
)

# Enviar mensaje
response = await client.send_message(
    session_id=session_id,
    message="Hola"
)

# Limpiar
await client.cleanup()
```

---

## 📚 Documentación Completa

Para más detalles, consulta:

- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Guía de 5 minutos
- **[GUIA_INSTALACION_USO.md](GUIA_INSTALACION_USO.md)** - Guía completa con todos los detalles
- **[INDICE_DOCUMENTACION.md](INDICE_DOCUMENTACION.md)** - Índice de toda la documentación
- **[README_EMPEZAR.md](README_EMPEZAR.md)** - Punto de entrada principal

---

## ✅ Resumen

| Componente | Propósito | Primer Comando |
|------------|-----------|----------------|
| **luminoracore** | Motor base en Python | `from luminoracore import Personality` |
| **luminoracore-cli** | Herramienta CLI | `luminoracore --help` |
| **luminoracore-sdk** | Apps con IA | `from luminoracore import LuminoraCoreClient` |

**¿Primera vez? → [INICIO_RAPIDO.md](INICIO_RAPIDO.md)**

**¿Quieres detalles? → [GUIA_INSTALACION_USO.md](GUIA_INSTALACION_USO.md)**

**¡Listo para empezar! 🚀**

