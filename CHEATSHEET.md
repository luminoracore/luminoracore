# ⚡ LuminoraCore CheatSheet

## 🚀 Instalación Rápida

```bash
# Todo en uno
.\instalar_todo.ps1        # Windows
./instalar_todo.sh         # Linux/Mac

# Manual - Solo Core
cd luminoracore && pip install -e . && cd ..

# Manual - Core + CLI
cd luminoracore && pip install -e . && cd ..
cd luminoracore-cli && pip install -e . && cd ..

# Manual - Core + SDK
cd luminoracore && pip install -e . && cd ..
cd luminoracore-sdk-python && pip install -e ".[openai]" && cd ..
```

---

## ✅ Verificación

```bash
python ejemplo_quick_start_core.py
python ejemplo_quick_start_cli.py
python ejemplo_quick_start_sdk.py
```

---

## 🧠 Motor Base (Python)

```python
# Imports básicos
from luminoracore import (
    Personality,
    PersonalityValidator,
    PersonalityCompiler,
    PersonalityBlender,
    LLMProvider
)

# Cargar personalidad
p = Personality("archivo.json")

# Validar
validator = PersonalityValidator()
result = validator.validate(p)
print(result.is_valid)

# Compilar
compiler = PersonalityCompiler()
compiled = compiler.compile(p, LLMProvider.OPENAI)
print(compiled.prompt)

# Mezclar
blender = PersonalityBlender()
blended = blender.blend([p1, p2], [0.6, 0.4])
```

---

## 🛠️ CLI

```bash
# Ayuda
luminoracore --help

# Listar
luminoracore list
luminoracore list --detailed

# Validar
luminoracore validate archivo.json
luminoracore validate carpeta/ --strict

# Compilar
luminoracore compile archivo.json --provider openai
luminoracore compile archivo.json --provider anthropic -o out.txt

# Crear
luminoracore create --interactive
luminoracore create --name "Mi Bot" --archetype helper

# Mezclar
luminoracore blend archivo1.json:0.7 archivo2.json:0.3
luminoracore blend p1.json:0.5 p2.json:0.3 p3.json:0.2 -o mix.json

# Servidor
luminoracore serve
luminoracore serve --port 3000
```

---

## 🐍 SDK (Aplicaciones)

```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig
from luminoracore.types.session import StorageConfig

async def main():
    # Cliente
    client = LuminoraCoreClient(
        storage_config=StorageConfig(storage_type="memory")
    )
    await client.initialize()
    
    # Cargar personalidad
    await client.load_personality("nombre", {
        "name": "nombre",
        "system_prompt": "Tu prompt aquí",
        "metadata": {"version": "1.0.0"}
    })
    
    # Proveedor
    config = ProviderConfig(
        name="openai",
        api_key="tu-key",
        model="gpt-3.5-turbo"
    )
    
    # Sesión
    session_id = await client.create_session(
        personality_name="nombre",
        provider_config=config
    )
    
    # Mensaje
    response = await client.send_message(
        session_id=session_id,
        message="Hola"
    )
    print(response.content)
    
    # Memoria
    await client.store_memory(session_id, "key", "value")
    memory = await client.get_memory(session_id, "key")
    
    # Limpieza
    await client.cleanup()

asyncio.run(main())
```

---

## 🔑 API Keys

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-..."
$env:ANTHROPIC_API_KEY="sk-ant-..."
$env:COHERE_API_KEY="..."

# Linux/Mac
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export COHERE_API_KEY="..."
```

---

## 📦 Providers Soportados

| Provider | Modelo Ejemplo | Instalación SDK |
|----------|---------------|-----------------|
| OpenAI | gpt-3.5-turbo, gpt-4 | `pip install -e ".[openai]"` |
| Anthropic | claude-3-sonnet | `pip install -e ".[anthropic]"` |
| Cohere | command | `pip install -e ".[cohere]"` |
| Google | gemini-pro | `pip install -e ".[google]"` |
| Mistral | mistral-large | Incluido |
| Llama | llama-2 | Incluido |

---

## 🎯 Tabla de Decisión

| Necesito | Usa |
|----------|-----|
| Solo validar archivos | **CLI** |
| Crear personalidades interactivamente | **CLI** |
| Mezclar personalidades | **Core** o **CLI** |
| Compilar prompts en Python | **Core** |
| Chatbot con API real | **SDK** |
| Interfaz web de prueba | **CLI** `serve` |
| App de producción | **SDK** |

---

## 🔧 Solución Rápida de Problemas

```bash
# ModuleNotFoundError
.\venv\Scripts\Activate.ps1  # Activar venv
cd luminoracore && pip install -e . && cd ..

# Command not found (CLI)
cd luminoracore-cli && pip install -e . && cd ..

# Permission denied (Windows)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📂 Estructura de Personalidad JSON

```json
{
  "persona": {
    "name": "Nombre",
    "version": "1.0.0",
    "description": "Descripción",
    "author": "Autor",
    "language": "es",
    "tags": ["tag1", "tag2"],
    "compatibility": ["openai", "anthropic"]
  },
  "core_traits": {
    "archetype": "helper",
    "temperament": "friendly",
    "primary_motivation": "ayudar",
    "expertise_areas": ["área1"],
    "communication_style": "claro"
  },
  "linguistic_profile": {
    "tone": ["amigable"],
    "formality_level": "semiformal",
    "syntax": "estructurado",
    "vocabulary": ["claro"],
    "fillers": [],
    "humor_style": "ligero"
  },
  "behavioral_rules": [
    "Regla 1",
    "Regla 2"
  ],
  "constraints": {
    "topics_to_avoid": ["tema"],
    "ethical_guidelines": ["guía"],
    "prohibited_behaviors": ["comportamiento"]
  },
  "examples": {
    "sample_responses": [
      {
        "input": "Pregunta",
        "output": "Respuesta"
      }
    ],
    "tone_examples": ["Ejemplo"],
    "boundary_examples": ["Límite"]
  }
}
```

---

## 🔗 Links Rápidos

- **Inicio:** [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
- **Guía Completa:** [GUIA_INSTALACION_USO.md](GUIA_INSTALACION_USO.md)
- **Referencia:** [COMO_USAR_LUMINORACORE.md](COMO_USAR_LUMINORACORE.md)
- **Índice:** [INDICE_DOCUMENTACION.md](INDICE_DOCUMENTACION.md)

---

## 🎨 Ejemplos Rápidos

### Validar archivo
```bash
luminoracore validate mi_archivo.json
```

### Crear chatbot
```python
# Ver ejemplo_quick_start_sdk.py
```

### Servidor web
```bash
luminoracore serve
```

### Mezclar personalidades
```bash
luminoracore blend p1.json:0.6 p2.json:0.4 -o mix.json
```

---

**Imprime o guarda este archivo para referencia rápida! 📄**

