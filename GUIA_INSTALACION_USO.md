# 📘 Guía Completa de Instalación y Uso de LuminoraCore

Esta guía te llevará paso a paso desde cero hasta poder usar LuminoraCore en tu proyecto local.

---

## 🏗️ Arquitectura del Proyecto

LuminoraCore está compuesto por **3 componentes principales**:

```
┌─────────────────────────────────────────────────┐
│  1. luminoracore (Motor Base)                   │
│     - Gestión de personalidades                 │
│     - Validación y compilación                  │
│     - PersonaBlend™ Technology                  │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌───────────────┐    ┌─────────────────────┐
│  2. luminora  │    │  3. luminoracore    │
│  core-cli     │    │  -sdk-python        │
│               │    │                     │
│  Herramienta  │    │  SDK Completo       │
│  CLI          │    │  para Apps          │
└───────────────┘    └─────────────────────┘
```

**Dependencias:**
- ✅ **luminoracore**: No depende de nada (motor base)
- ✅ **luminoracore-cli**: Depende de `luminoracore`
- ✅ **luminoracore-sdk**: Depende de `luminoracore`

---

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener:

- ✅ **Python 3.8 o superior** instalado
- ✅ **pip** (gestor de paquetes de Python)
- ✅ **git** (para clonar el repositorio)
- ✅ Un editor de código (VS Code, PyCharm, etc.)
- ✅ Terminal o consola de comandos

### Verificar versiones instaladas:

```bash
python --version
# Debería mostrar: Python 3.8.x o superior

pip --version
# Debería mostrar: pip x.x.x

git --version
# Debería mostrar: git version x.x.x
```

---

## 🚀 Opción 1: Instalación en Modo Desarrollo (Recomendado)

Esta opción te permite editar el código fuente y ver los cambios inmediatamente.

### Paso 1: Clonar o ubicar el repositorio

Si ya tienes el proyecto descargado, navega a su carpeta:

```bash
cd "D:\Proyectos Ereace\LuminoraCoreBase"
```

Si no lo tienes, clónalo:

```bash
git clone <url-del-repositorio>
cd LuminoraCoreBase
```

### Paso 2: Crear un entorno virtual (Recomendado)

Esto aísla las dependencias del proyecto:

```bash
# Crear entorno virtual
python -m venv venv

# Activar en Windows PowerShell
.\venv\Scripts\Activate.ps1

# Activar en Windows CMD
.\venv\Scripts\activate.bat

# Activar en Linux/Mac
source venv/bin/activate
```

Cuando esté activado, verás `(venv)` al inicio de tu línea de comandos.

### Paso 3: Instalar el Motor Base (luminoracore)

Este es el componente fundamental que todos los demás necesitan:

```bash
# Navegar a la carpeta del motor base
cd luminoracore

# Instalar en modo desarrollo
pip install -e .

# Opcional: Instalar dependencias de desarrollo
pip install -e ".[dev]"

# Volver a la raíz
cd ..
```

**¿Qué hace `-e`?** 
- Instala en modo "editable"
- Los cambios en el código se reflejan inmediatamente
- No necesitas reinstalar después de cada modificación

### Paso 4: Instalar el CLI (luminoracore-cli)

```bash
# Navegar a la carpeta del CLI
cd luminoracore-cli

# Instalar en modo desarrollo
pip install -e .

# Opcional: Dependencias extras para servidor
pip install -e ".[server]"

# Volver a la raíz
cd ..
```

### Paso 5: Instalar el SDK (luminoracore-sdk-python)

```bash
# Navegar a la carpeta del SDK
cd luminoracore-sdk-python

# Instalar en modo desarrollo
pip install -e .

# Opcional: Instalar con todos los proveedores
pip install -e ".[all]"

# O solo los proveedores que necesites:
pip install -e ".[openai]"      # Solo OpenAI
pip install -e ".[anthropic]"   # Solo Anthropic
pip install -e ".[cohere]"      # Solo Cohere

# Volver a la raíz
cd ..
```

### Paso 6: Verificar la instalación

```bash
# Verificar que luminoracore está instalado
python -c "import luminoracore; print(luminoracore.__version__)"

# Verificar que el CLI está disponible
luminoracore --help

# También puedes usar el alias corto
lc --help

# Verificar el SDK
python -c "from luminoracore import LuminoraCoreClient; print('SDK OK')"
```

---

## 🎯 Opción 2: Instalación desde PyPI (Cuando esté publicado)

Cuando los paquetes estén publicados en PyPI, la instalación será más simple:

```bash
# Motor base
pip install luminoracore

# CLI
pip install luminoracore-cli

# SDK con todos los proveedores
pip install luminoracore-sdk[all]
```

---

## 📝 Uso Práctico - Caso 1: Usar el Motor Base (luminoracore)

### Ejemplo 1: Cargar y Validar una Personalidad

Crea un archivo `mi_ejemplo_core.py`:

```python
from luminoracore import Personality, PersonalityValidator, PersonalityCompiler, LLMProvider

# 1. Cargar una personalidad
print("1. Cargando personalidad...")
personality = Personality("personalidades/Dr. Luna Científica Entusiasta.json")
print(f"✅ Personalidad cargada: {personality.persona.name}")

# 2. Validar la personalidad
print("\n2. Validando personalidad...")
validator = PersonalityValidator()
result = validator.validate(personality)

if result.is_valid:
    print("✅ Validación exitosa")
    print(f"   - Advertencias: {len(result.warnings)}")
    print(f"   - Sugerencias: {len(result.suggestions)}")
else:
    print("❌ Validación fallida:")
    for error in result.errors:
        print(f"   - {error}")

# 3. Compilar para OpenAI
print("\n3. Compilando para OpenAI...")
compiler = PersonalityCompiler()
compiled = compiler.compile(personality, LLMProvider.OPENAI)
print(f"✅ Compilado exitosamente")
print(f"   - Tokens estimados: {compiled.token_estimate}")
print(f"   - Prompt (primeros 200 chars):\n{compiled.prompt[:200]}...")

# 4. Compilar para otros proveedores
print("\n4. Compilando para otros proveedores...")
for provider in [LLMProvider.ANTHROPIC, LLMProvider.LLAMA, LLMProvider.MISTRAL]:
    result = compiler.compile(personality, provider)
    print(f"✅ {provider.value}: {result.token_estimate} tokens")
```

**Ejecutar:**

```bash
python mi_ejemplo_core.py
```

### Ejemplo 2: Mezclar Personalidades (PersonaBlend)

```python
from luminoracore import Personality, PersonalityBlender

# Cargar dos personalidades
print("Cargando personalidades...")
dr_luna = Personality("personalidades/Dr. Luna Científica Entusiasta.json")
rocky = Personality("personalidades/Rocky Inspiración.json")

# Mezclar personalidades
print("\nMezclando personalidades...")
blender = PersonalityBlender()
blended = blender.blend(
    personalities=[dr_luna, rocky],
    weights=[0.7, 0.3],
    strategy="weighted_average"
)

print(f"✅ Personalidad mezclada creada: {blended.persona.name}")
print(f"   Descripción: {blended.persona.description}")
print(f"   Arqueotipo: {blended.core_traits.archetype}")
```

---

## 🛠️ Uso Práctico - Caso 2: Usar el CLI (luminoracore-cli)

El CLI te permite gestionar personalidades desde la terminal.

### Comandos Básicos:

```bash
# 1. Ver todas las personalidades disponibles
luminoracore list

# Con detalles
luminoracore list --detailed

# 2. Validar una personalidad
luminoracore validate "personalidades/Dr. Luna Científica Entusiasta.json"

# Validar todas las personalidades en una carpeta
luminoracore validate personalidades/ --strict

# 3. Compilar una personalidad
luminoracore compile "personalidades/Dr. Luna Científica Entusiasta.json" --provider openai

# Guardar en archivo
luminoracore compile "personalidades/Rocky Inspiración.json" --provider anthropic --output rocky_prompt.txt

# 4. Crear una nueva personalidad (modo interactivo)
luminoracore create --interactive

# 5. Mezclar personalidades
luminoracore blend "personalidades/Dr. Luna Científica Entusiasta.json:0.6" "personalidades/Rocky Inspiración.json:0.4" --output mezcla.json

# 6. Iniciar servidor de desarrollo con interfaz web
luminoracore serve

# En puerto personalizado
luminoracore serve --port 3000

# 7. Obtener información de una personalidad
luminoracore info "personalidades/Victoria Sterling.json"
```

### Ejemplo Práctico: Workflow Completo

```bash
# Paso 1: Crear una nueva personalidad
luminoracore create --interactive

# Paso 2: Validar que esté correcta
luminoracore validate mi_nueva_personalidad.json

# Paso 3: Probar compilación para diferentes proveedores
luminoracore compile mi_nueva_personalidad.json --provider openai
luminoracore compile mi_nueva_personalidad.json --provider anthropic

# Paso 4: Iniciar servidor para pruebas visuales
luminoracore serve
# Abre http://localhost:8000 en tu navegador
```

---

## 🐍 Uso Práctico - Caso 3: Usar el SDK (luminoracore-sdk)

El SDK es para construir aplicaciones completas con IA.

### Ejemplo 1: Aplicación Básica con OpenAI

Crea un archivo `mi_app_sdk.py`:

```python
import asyncio
import os
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig
from luminoracore.types.session import StorageConfig

async def main():
    # 1. Crear configuración del cliente
    print("1. Inicializando cliente...")
    client = LuminoraCoreClient(
        storage_config=StorageConfig(
            storage_type="memory"  # Puede ser: memory, redis, postgres, mongodb
        )
    )
    
    await client.initialize()
    print("✅ Cliente inicializado")
    
    # 2. Configurar proveedor LLM (OpenAI)
    print("\n2. Configurando OpenAI...")
    provider_config = ProviderConfig(
        name="openai",
        api_key=os.getenv("OPENAI_API_KEY", "tu-api-key-aquí"),
        model="gpt-3.5-turbo",
        extra={
            "timeout": 30,
            "max_retries": 3
        }
    )
    print("✅ Proveedor configurado")
    
    # 3. Crear una personalidad personalizada
    print("\n3. Cargando personalidad...")
    personality_data = {
        "name": "asistente_programacion",
        "description": "Un asistente experto en programación Python",
        "system_prompt": "Eres un experto en programación Python. Explicas conceptos de forma clara y concisa. Siempre proporcionas ejemplos de código cuando es relevante.",
        "metadata": {
            "version": "1.0.0",
            "author": "Mi Empresa",
            "tags": ["programacion", "python", "educativo"]
        }
    }
    
    await client.load_personality("asistente_programacion", personality_data)
    print("✅ Personalidad cargada")
    
    # 4. Crear una sesión
    print("\n4. Creando sesión...")
    session_id = await client.create_session(
        personality_name="asistente_programacion",
        provider_config=provider_config
    )
    print(f"✅ Sesión creada: {session_id}")
    
    # 5. Enviar mensajes (ESTO HACE LLAMADAS REALES A LA API)
    print("\n5. Enviando mensaje a OpenAI...")
    
    # IMPORTANTE: Esto consumirá tokens de tu cuenta de OpenAI
    try:
        response = await client.send_message(
            session_id=session_id,
            message="¿Puedes explicarme qué son las list comprehensions en Python?"
        )
        
        print("✅ Respuesta recibida:")
        print(f"   Contenido: {response.content[:200]}...")
        print(f"   Tokens usados: {response.usage}")
        print(f"   Costo estimado: ${response.cost}")
        
    except Exception as e:
        print(f"⚠️  Error al llamar API: {e}")
        print("   (Asegúrate de tener una API key válida en OPENAI_API_KEY)")
    
    # 6. Ver el historial de conversación
    print("\n6. Obteniendo historial...")
    messages = await client.get_conversation(session_id)
    print(f"✅ La conversación tiene {len(messages)} mensajes")
    
    # 7. Guardar información en memoria de sesión
    print("\n7. Guardando preferencias del usuario...")
    await client.store_memory(
        session_id=session_id,
        key="nivel_experiencia",
        value="intermedio"
    )
    print("✅ Memoria guardada")
    
    # 8. Limpieza
    print("\n8. Limpiando...")
    await client.cleanup()
    print("✅ Limpieza completada")

# Ejecutar
if __name__ == "__main__":
    asyncio.run(main())
```

**Ejecutar:**

```bash
# Configurar tu API key
export OPENAI_API_KEY="sk-tu-api-key-aquí"  # Linux/Mac
set OPENAI_API_KEY=sk-tu-api-key-aquí       # Windows CMD
$env:OPENAI_API_KEY="sk-tu-api-key-aquí"    # Windows PowerShell

# Ejecutar
python mi_app_sdk.py
```

### Ejemplo 2: Mezclar Personalidades en Runtime

```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig

async def main():
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Cargar dos personalidades diferentes
    scientist_data = {
        "name": "científico",
        "system_prompt": "Eres un científico riguroso que explica todo con evidencia y datos.",
        "metadata": {"version": "1.0.0"}
    }
    
    creative_data = {
        "name": "creativo",
        "system_prompt": "Eres un pensador creativo que encuentra soluciones innovadoras.",
        "metadata": {"version": "1.0.0"}
    }
    
    await client.load_personality("científico", scientist_data)
    await client.load_personality("creativo", creative_data)
    
    # Mezclar personalidades (60% científico, 40% creativo)
    blended = await client.blend_personalities(
        personality_names=["científico", "creativo"],
        weights=[0.6, 0.4],
        blend_name="científico_creativo"
    )
    
    print(f"✅ Personalidad mezclada: {blended}")
    
    # Usar la personalidad mezclada
    provider_config = ProviderConfig(
        name="openai",
        api_key="tu-api-key",
        model="gpt-3.5-turbo"
    )
    
    session_id = await client.create_session(
        personality_name="científico_creativo",
        provider_config=provider_config
    )
    
    print(f"✅ Sesión con personalidad mezclada: {session_id}")
    
    await client.cleanup()

asyncio.run(main())
```

---

## 🔑 Configuración de API Keys

### OpenAI

```bash
# Obtener tu API key en: https://platform.openai.com/api-keys

# Linux/Mac
export OPENAI_API_KEY="sk-..."

# Windows PowerShell
$env:OPENAI_API_KEY="sk-..."

# Windows CMD
set OPENAI_API_KEY=sk-...
```

### Anthropic (Claude)

```bash
# Obtener tu API key en: https://console.anthropic.com/

# Linux/Mac
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

### Cohere

```bash
# Obtener tu API key en: https://dashboard.cohere.ai/

export COHERE_API_KEY="..."
```

---

## 📂 Estructura de un Proyecto Típico

```
mi-proyecto/
├── venv/                          # Entorno virtual
├── personalidades/                # Tus personalidades personalizadas
│   ├── asistente_ventas.json
│   ├── soporte_tecnico.json
│   └── creativo_marketing.json
├── config/
│   └── providers.yaml            # Configuración de proveedores
├── src/
│   ├── main.py                   # Tu aplicación principal
│   ├── handlers.py               # Lógica de negocio
│   └── utils.py                  # Utilidades
├── tests/
│   └── test_personalidades.py   # Tests
├── requirements.txt              # Dependencias
└── README.md                     # Documentación
```

**requirements.txt:**

```txt
# Para usar solo el motor base
luminoracore>=0.1.0

# Para usar el CLI
luminoracore-cli>=1.0.0

# Para usar el SDK completo con OpenAI
luminoracore-sdk[openai]>=1.0.0

# O con todos los proveedores
luminoracore-sdk[all]>=1.0.0
```

---

## 🐛 Solución de Problemas Comunes

### Problema 1: "ModuleNotFoundError: No module named 'luminoracore'"

**Solución:**

```bash
# Asegúrate de estar en el entorno virtual correcto
.\venv\Scripts\Activate.ps1

# Reinstala el paquete
cd luminoracore
pip install -e .
cd ..
```

### Problema 2: "Command 'luminoracore' not found"

**Solución:**

```bash
# Reinstala el CLI
cd luminoracore-cli
pip install -e .
cd ..

# Verifica que esté en el PATH
pip show luminoracore-cli
```

### Problema 3: Error al importar el SDK

**Solución:**

```bash
# Instala las dependencias del proveedor que estés usando
cd luminoracore-sdk-python
pip install -e ".[openai]"  # Para OpenAI
pip install -e ".[anthropic]"  # Para Anthropic
pip install -e ".[all]"  # Para todos
cd ..
```

### Problema 4: "Permission denied" al activar entorno virtual en Windows

**Solución:**

```powershell
# Ejecuta esto en PowerShell como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problema 5: Las personalidades no se encuentran

**Solución:**

```python
# Usa rutas absolutas o relativas correctas
from pathlib import Path

# Obtener la ruta del proyecto
PROJECT_ROOT = Path(__file__).parent
PERSONALITIES_DIR = PROJECT_ROOT / "personalidades"

# Cargar personalidad
personality_path = PERSONALITIES_DIR / "Dr. Luna Científica Entusiasta.json"
personality = Personality(str(personality_path))
```

---

## 📚 Recursos Adicionales

### Documentación Oficial

- **Motor Base:** `luminoracore/docs/`
- **CLI:** `luminoracore-cli/README.md`
- **SDK:** `luminoracore-sdk-python/docs/api_reference.md`

### Ejemplos Incluidos

```bash
# Ejemplos del motor base
python luminoracore/examples/basic_usage.py
python luminoracore/examples/blending_demo.py
python luminoracore/examples/multi_llm_demo.py

# Ejemplos del SDK
python luminoracore-sdk-python/examples/basic_usage.py
python luminoracore-sdk-python/examples/personality_blending.py
```

### Archivos de Referencia

- `ESTADO_ACTUAL_PROYECTO.md` - Estado del proyecto
- `CARACTERISTICAS_TECNICAS_LUMINORACORE.md` - Características técnicas
- `COMO_PROBAR_WIZARD.md` - Guía para probar el wizard

---

## ✅ Lista de Verificación para Nuevos Desarrolladores

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] `luminoracore` instalado
- [ ] `luminoracore-cli` instalado (si lo necesitas)
- [ ] `luminoracore-sdk` instalado (si lo necesitas)
- [ ] API keys configuradas (si vas a hacer llamadas reales)
- [ ] Primer ejemplo ejecutado exitosamente
- [ ] Documentación leída

---

## 🎓 Próximos Pasos

1. **Explora las personalidades incluidas** en la carpeta `personalidades/`
2. **Ejecuta los ejemplos** en `luminoracore/examples/`
3. **Crea tu primera personalidad personalizada**
4. **Integra LuminoraCore en tu aplicación**
5. **Comparte tus personalidades con la comunidad**

---

## 💡 Casos de Uso Recomendados

### Caso 1: Chatbot de Atención al Cliente

```python
# Usa el SDK con una personalidad de soporte amigable
# Almacenamiento en Redis para persistencia
# Métricas y analytics incluidos
```

### Caso 2: Asistente Educativo

```python
# Usa el motor base para cambiar entre personalidades
# Profesor riguroso para exámenes
# Tutor amigable para aprendizaje
```

### Caso 3: Generador de Contenido

```python
# Mezcla personalidades creativas con analíticas
# Genera contenido con voz de marca consistente
```

---

## 📞 Soporte

Si tienes problemas o preguntas:

1. Revisa esta guía completa
2. Consulta `ESTADO_ACTUAL_PROYECTO.md`
3. Revisa los ejemplos en `examples/`
4. Crea un issue en el repositorio

---

**¡Listo! Ahora tienes todo lo necesario para empezar a usar LuminoraCore en tus proyectos.** 🚀

