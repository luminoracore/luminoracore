# 📘 Guía Completa de Instalación y Uso de LuminoraCore

Esta guía te llevará paso a paso desde cero hasta poder usar LuminoraCore en tu proyecto local.

## ⚠️ Aclaración Importante sobre Almacenamiento

**Pregunta común:** "¿Necesito mi propia base de datos?"

**Respuesta:** NO necesariamente. LuminoraCore ofrece MÚLTIPLES opciones:

```
┌─────────────────────────────────────────────────┐
│  🎯 OPCIÓN 1: Sin Base de Datos (Por defecto)  │
├─────────────────────────────────────────────────┤
│  • Storage: En memoria RAM                      │
│  • Persistente: NO (se pierde al cerrar)        │
│  • Instalación: 0 pasos                         │
│  • Ideal para: Pruebas, demos                   │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  💾 OPCIÓN 2: Archivo JSON (Simple)  ✨ NUEVO  │
├─────────────────────────────────────────────────┤
│  • Storage: Archivo .json o .json.gz            │
│  • Persistente: SÍ (archivo en disco)           │
│  • Instalación: 0 pasos                         │
│  • Ideal para: Bots personales, backups         │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  📱 OPCIÓN 3: SQLite (Móviles)  ✨ NUEVO       │
├─────────────────────────────────────────────────┤
│  • Storage: Archivo .db (SQLite)                │
│  • Persistente: SÍ (perfecto para móviles)      │
│  • Instalación: 0 pasos                         │
│  • Ideal para: Apps iOS/Android, desktop        │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  🚀 OPCIÓN 4+: Con Base de Datos (Opcional)    │
├─────────────────────────────────────────────────┤
│  • Storage: Redis/PostgreSQL/MongoDB            │
│  • Persistente: SÍ                              │
│  • Instalación: Requiere servidor BBDD          │
│  • Ideal para: Producción web, alta escala      │
└─────────────────────────────────────────────────┘
```

**👉 Para empezar NO necesitas nada. Todo funciona en memoria.**

**👉 Para apps móviles usa SQLite (incluido, sin instalación adicional).**

**👉 Para persistencia simple usa JSON (sin servidor de BBDD).**

Detalles completos en: [Sección de Almacenamiento](#-almacenamiento-de-conversaciones-storage)

---

## 🏗️ Arquitectura del Proyecto

LuminoraCore está compuesto por **3 componentes principales**:

```
┌─────────────────────────────────────────────────────┐
│  1. luminoracore (Motor Base / Core Engine)         │
│     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│     • Gestión de personalidades                     │
│     • Validación y compilación                      │
│     • PersonaBlend™ Technology                      │
│     • NO tiene interfaz (es una librería)           │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ AMBOS USAN EL MOTOR BASE
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌───────────────┐    ┌─────────────────────────┐
│  2. CLI       │    │  3. SDK                 │
│  (Terminal)   │    │  (Python Apps)          │
│───────────────│    │─────────────────────────│
│ • Comandos    │    │ • Client API            │
│ • Wizard      │    │ • Sessions              │
│ • Testing     │    │ • Real LLM calls        │
│ • Servidor    │    │ • Multi-provider        │
│               │    │                         │
│ DEPENDE DE:   │    │ DEPENDE DE:             │
│ luminoracore  │    │ luminoracore            │
└───────────────┘    └─────────────────────────┘
```

**⚠️ IMPORTANTE - Orden de Instalación:**

```
1. PRIMERO: luminoracore (motor base)
           ↓
2. DESPUÉS: luminoracore-cli (usa el motor)
           ↓
3. DESPUÉS: luminoracore-sdk (usa el motor)
```

**¿Por qué este orden?**
- El **CLI** importa `from luminoracore import Personality, PersonalityCompiler`
- El **SDK** importa `from luminoracore import Personality, PersonalityBlender`
- Si instalas CLI o SDK **sin** el motor base, obtendrás `ModuleNotFoundError`

**Dependencias técnicas:**
```python
# luminoracore-cli/setup.py
install_requires=[
    'luminoracore>=0.1.0',  # ← Requiere el motor base
    'click>=8.0.0',
    ...
]

# luminoracore-sdk-python/setup.py
install_requires=[
    'luminoracore>=0.1.0',  # ← Requiere el motor base
    'aiohttp>=3.8.0',
    ...
]
```

---

## 🤔 ¿Qué es Cada Componente?

### 1️⃣ **luminoracore** (Motor Base)

**Es:** Una librería Python (sin interfaz)

**Hace:**
- Carga archivos JSON de personalidades
- Valida que el JSON sea correcto
- Compila personalidades para diferentes LLMs
- Mezcla personalidades (PersonaBlend)

**NO hace:**
- ❌ NO tiene comandos de terminal
- ❌ NO hace llamadas a APIs de LLM
- ❌ NO tiene interfaz gráfica
- ❌ NO gestiona sesiones

**Uso típico:**
```python
# En tu código Python
from luminoracore import Personality, PersonalityCompiler

personality = Personality("dr_luna.json")
compiler = PersonalityCompiler()
result = compiler.compile(personality, "openai")
```

**Analogía:** Es como el "motor" de un coche. Funciona, pero necesitas el resto del coche para conducir.

---

### 2️⃣ **luminoracore-cli** (Herramienta de Terminal)

**Es:** Una herramienta de línea de comandos que **USA** el motor base

**Hace:**
- ✅ Ejecutar comandos desde la terminal
- ✅ Validar archivos: `luminoracore validate archivo.json`
- ✅ Compilar: `luminoracore compile archivo.json`
- ✅ Crear personalidades: `luminoracore create --interactive`
- ✅ Listar: `luminoracore list`
- ✅ Testing básico

**Internamente:**
```python
# Dentro de luminoracore-cli
from luminoracore import Personality, PersonalityCompiler  # ← USA EL MOTOR

def validate_command(file_path):
    personality = Personality(file_path)  # ← Usa el motor base
    # ... resto del código
```

**Analogía:** Es como el "volante y los pedales" del coche. Te permite USAR el motor desde la terminal.

---

### 3️⃣ **luminoracore-sdk** (SDK para Apps)

**Es:** Un cliente completo para construir aplicaciones que **USA** el motor base

**Hace:**
- ✅ Gestionar sesiones de conversación
- ✅ Hacer llamadas REALES a APIs de LLM (OpenAI, DeepSeek, etc.)
- ✅ Almacenar historial de conversaciones
- ✅ Gestionar memoria de sesión
- ✅ Analytics y métricas

**Internamente:**
```python
# Dentro de luminoracore-sdk
from luminoracore import Personality, PersonalityCompiler  # ← USA EL MOTOR

class LuminoraCoreClient:
    async def create_session(self, personality_name, provider_config):
        personality = Personality(f"{personality_name}.json")  # ← Usa el motor base
        # ... resto del código para sesiones, LLM calls, etc.
```

**Analogía:** Es como un "coche completo con GPS y sonido". Tiene el motor + todo lo necesario para una app completa.

---

## 📊 Tabla Comparativa

| Característica | Motor Base | CLI | SDK |
|----------------|------------|-----|-----|
| **Carga personalidades** | ✅ | ✅ (usa motor) | ✅ (usa motor) |
| **Valida JSON** | ✅ | ✅ (usa motor) | ✅ (usa motor) |
| **Compila prompts** | ✅ | ✅ (usa motor) | ✅ (usa motor) |
| **Comandos terminal** | ❌ | ✅ | ❌ |
| **Llamadas a LLM** | ❌ | ❌ | ✅ |
| **Gestión sesiones** | ❌ | ❌ | ✅ |
| **Interfaz Python** | ✅ | ❌ | ✅ |
| **Wizard interactivo** | ❌ | ✅ | ❌ |

---

## 🎯 Respuesta a tu Pregunta

**Tu pregunta:** 
> "El CLI sirve para probar comandos de luminoracore, ¿tiene que tener compilado o compilar luminoracore al igual que el SDK?"

**Respuesta:**

**SÍ, exactamente.** El CLI:

1. ✅ **Necesita que instales primero `luminoracore`** (el motor base)
2. ✅ **Importa y usa el motor base internamente**
3. ✅ **No funciona si no tienes el motor base instalado**

**Lo mismo aplica para el SDK:**
- También necesita el motor base instalado
- También importa `from luminoracore import ...`

**Orden correcto de instalación:**
```bash
# 1. PRIMERO el motor (obligatorio)
cd luminoracore
pip install -e .

# 2. DESPUÉS el CLI (opcional - solo si quieres comandos de terminal)
cd ../luminoracore-cli
pip install -e .

# 3. DESPUÉS el SDK (opcional - solo si vas a construir apps)
cd ../luminoracore-sdk-python
pip install -e .
```

**Si intentas instalar el CLI sin el motor:**
```bash
cd luminoracore-cli
pip install -e .

# ❌ ERROR al ejecutar comandos:
luminoracore validate archivo.json
# ModuleNotFoundError: No module named 'luminoracore'
```

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
pip install -e ".[deepseek]"    # Solo DeepSeek (económico)
pip install -e ".[mistral]"     # Solo Mistral AI
pip install -e ".[llama]"       # Solo Llama (vía Replicate)
pip install -e ".[cohere]"      # Solo Cohere
pip install -e ".[google]"      # Solo Google Gemini

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
for provider in [LLMProvider.ANTHROPIC, LLMProvider.DEEPSEEK, LLMProvider.LLAMA, LLMProvider.MISTRAL]:
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
    
    # IMPORTANTE: storage_type define DÓNDE se guardan las conversaciones
    # - "memory": En RAM (se pierde al cerrar, perfecto para pruebas)
    # - "redis": En Redis (persistente, requiere servidor Redis)
    # - "postgres": En PostgreSQL (persistente, requiere BBDD)
    # - "mongodb": En MongoDB (persistente, requiere BBDD)
    
    client = LuminoraCoreClient(
        storage_config=StorageConfig(
            storage_type="memory"  # 👈 Por defecto: memoria RAM (NO persistente)
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
    
    # 7. Guardar información personalizada en la sesión
    print("\n7. Guardando preferencias del usuario...")
    # NOTA: Esto guarda datos ADICIONALES sobre el usuario
    # (nivel, preferencias, contexto personalizado)
    # Se guarda en el mismo storage que las conversaciones
    await client.store_memory(
        session_id=session_id,
        key="nivel_experiencia",
        value="intermedio"
    )
    print("✅ Memoria guardada (se perderá al cerrar si usas 'memory')")
    
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

## 💾 Almacenamiento de Conversaciones (Storage)

### ¿Dónde se guardan las conversaciones?

**Respuesta corta:** Depende de ti. LuminoraCore ofrece 4 opciones:

| Storage | Persistente | Requiere | Cuándo usar |
|---------|-------------|----------|-------------|
| **memory** | ❌ NO | Nada | Pruebas, demos |
| **json** | ✅ SÍ | Solo disco | Apps simples, backups |
| **sqlite** | ✅ SÍ | Solo disco | Apps móviles, desktop |
| **redis** | ✅ SÍ | Servidor Redis | Producción web, alta velocidad |
| **postgres** | ✅ SÍ | PostgreSQL | Producción, datos relacionales |
| **mongodb** | ✅ SÍ | MongoDB | Producción, datos flexibles |

### Opción 1: Memory (Por defecto - Sin BBDD)

```python
from luminoracore import LuminoraCoreClient
from luminoracore.types.session import StorageConfig

client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="memory"  # 👈 En RAM
    )
)
```

**✅ Ventajas:**
- No necesitas instalar nada
- Ideal para pruebas y desarrollo
- Muy rápido

**❌ Desventajas:**
- Se pierde todo al cerrar la app
- No sirve para producción
- No comparte datos entre procesos

**Cuándo usar:**
- Demos y prototipos
- Testing
- Scripts de una sola ejecución

---

### Opción 2: JSON File (Simple y Portátil) ✨ NUEVO

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="json",
        json_file_path="./sessions/conversations.json"  # O .json.gz comprimido
    )
)
```

**✅ Ventajas:**
- Persistente (archivo en disco)
- No necesitas servidor de BBDD
- Portátil (puedes mover el archivo)
- Fácil de hacer backup
- Legible (puedes ver el JSON)
- Ideal para desarrollo

**❌ Desventajas:**
- Lento con muchas sesiones (>1000)
- No apto para múltiples procesos concurrentes
- Sin queries complejas

**Cuándo usar:**
- Apps de escritorio
- Bots personales
- Scripts que se ejecutan periódicamente
- Prototipado sin complicaciones
- Backups y portabilidad

**Ejemplo con compresión:**
```python
# Guarda comprimido (ahorra espacio)
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="json",
        json_file_path="./sessions/conversations.json.gz",
        compress=True  # Comprime con gzip
    )
)
```

---

### Opción 3: SQLite (Perfecto para Móviles) 📱 NUEVO

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="sqlite",
        sqlite_path="./data/luminoracore.db"
    )
)
```

**✅ Ventajas:**
- Persistente (archivo .db)
- **PERFECTO para apps móviles** (iOS/Android)
- Queries SQL rápidas
- Ligero (solo un archivo)
- Sin servidor externo
- Transacciones ACID

**❌ Desventajas:**
- No apto para alta concurrencia
- Sin escalabilidad horizontal

**Cuándo usar:**
- **Apps móviles (iOS/Android)** ⭐
- Apps de escritorio
- Prototipos que necesitan SQL
- Apps con un solo usuario

**Ejemplo para móvil:**
```python
# En Android/iOS
import os
from pathlib import Path

# Ruta en el almacenamiento de la app
if platform.system() == "Android":
    db_path = Path("/data/data/com.tuapp/databases/luminoracore.db")
else:  # iOS
    db_path = Path.home() / "Documents" / "luminoracore.db"

client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="sqlite",
        sqlite_path=str(db_path)
    )
)
```

---

### Opción 4: Redis (Recomendado para producción web)

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="redis",
        redis_url="redis://localhost:6379",
        redis_db=0
    )
)
```

**✅ Ventajas:**
- Persistente
- Muy rápido (en memoria)
- Perfecto para sesiones
- TTL automático

**❌ Desventajas:**
- Requiere servidor Redis

**Instalación de Redis:**
```bash
# Linux/Mac (con Homebrew)
brew install redis
redis-server

# Windows (con Docker)
docker run -d -p 6379:6379 redis

# Instalar cliente Python
pip install redis
```

**Cuándo usar:**
- Chatbots en producción
- Apps con múltiples usuarios
- Necesitas velocidad + persistencia

---

### Opción 5: PostgreSQL

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="postgres",
        postgres_url="postgresql://user:password@localhost/luminoracore"
    )
)
```

**✅ Ventajas:**
- Persistente
- Queries SQL complejas
- Backups fáciles

**❌ Desventajas:**
- Más lento que Redis
- Requiere BBDD PostgreSQL

**Cuándo usar:**
- Ya tienes PostgreSQL
- Necesitas hacer análisis SQL
- Backups y auditoría importantes

---

### Opción 6: MongoDB

```python
client = LuminoraCoreClient(
    storage_config=StorageConfig(
        storage_type="mongodb",
        mongodb_url="mongodb://localhost:27017",
        mongodb_database="luminoracore"
    )
)
```

**✅ Ventajas:**
- Persistente
- Esquema flexible
- Buen rendimiento

**❌ Desventajas:**
- Requiere servidor MongoDB

**Cuándo usar:**
- Ya tienes MongoDB
- Datos no estructurados
- Escalabilidad horizontal

---

### ¿Qué se guarda exactamente?

**En el storage elegido se guardan:**

1. **Historial de mensajes**
   ```python
   [
     {"role": "user", "content": "Hola"},
     {"role": "assistant", "content": "¡Hola!"}
   ]
   ```

2. **Contexto de sesión**
   ```python
   {
     "session_id": "abc123",
     "personality_name": "dr_luna",
     "created_at": "2024-10-03T10:00:00Z"
   }
   ```

3. **Memoria personalizada**
   ```python
   {
     "nivel_experiencia": "intermedio",
     "preferencias": {"idioma": "es"},
     "contexto": {...}
   }
   ```

**NO se guarda:**
- ❌ El archivo JSON de la personalidad (es estático)
- ❌ Tu código Python (es tu aplicación)
- ❌ Las API keys (están en variables de entorno)

---

### Ejemplo Completo: Sin BBDD vs Con Redis

#### Sin BBDD (Memory):
```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.session import StorageConfig

async def main():
    # Opción 1: Memory (se pierde al cerrar)
    client = LuminoraCoreClient(
        storage_config=StorageConfig(storage_type="memory")
    )
    
    await client.initialize()
    session_id = await client.create_session(...)
    await client.send_message(session_id, "Hola")
    
    # ⚠️ Al cerrar la app, se pierde todo
    await client.cleanup()

asyncio.run(main())
```

#### Con Redis (Persistente):
```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.session import StorageConfig

async def main():
    # Opción 2: Redis (persistente)
    client = LuminoraCoreClient(
        storage_config=StorageConfig(
            storage_type="redis",
            redis_url="redis://localhost:6379"
        )
    )
    
    await client.initialize()
    
    # Puedes retomar sesiones anteriores
    existing_session_id = "session_from_yesterday"
    await client.send_message(existing_session_id, "Hola de nuevo")
    
    # ✅ Al cerrar, los datos quedan en Redis
    await client.cleanup()

asyncio.run(main())
```

---

### Decisión Rápida

**¿Estás probando?** → Usa `memory` (sin BBDD)

**¿App móvil (iOS/Android)?** → Usa `sqlite` ⭐ **RECOMENDADO**

**¿App de escritorio simple?** → Usa `json` o `sqlite`

**¿Bot personal o script?** → Usa `json` (fácil y portátil)

**¿Producción web con muchos usuarios?** → Usa `redis` (rápido + persistente)

**¿Ya tienes PostgreSQL?** → Usa `postgres`

**¿Ya tienes MongoDB?** → Usa `mongodb`

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

### DeepSeek (Muy Económico) 💰 ✨ NUEVO

```bash
# Obtener tu API key en: https://platform.deepseek.com/
# 🌟 Modelo ULTRA BARATO: ~$0.14 por 1M tokens
# Popular entre desarrolladores por su precio

# Linux/Mac
export DEEPSEEK_API_KEY="sk-..."

# Windows PowerShell
$env:DEEPSEEK_API_KEY="sk-..."

# Windows CMD
set DEEPSEEK_API_KEY=sk-...
```

**¿Por qué DeepSeek?**
- 💰 **Precio:** ~20x más barato que GPT-4
- ⚡ **Velocidad:** Respuestas rápidas
- 🎯 **Calidad:** Competitivo con GPT-3.5
- 🔥 **Popular:** Favorito de desarrolladores

**Uso en el SDK:**
```python
provider_config = ProviderConfig(
    name="deepseek",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    model="deepseek-chat"  # Modelo más económico
)
```

### Cohere

```bash
# Obtener tu API key en: https://dashboard.cohere.ai/

export COHERE_API_KEY="..."
```

### Mistral AI

```bash
# Obtener tu API key en: https://console.mistral.ai/

export MISTRAL_API_KEY="..."
```

### Google Gemini

```bash
# Obtener tu API key en: https://makersuite.google.com/app/apikey

export GOOGLE_API_KEY="..."
```

### Llama (vía Replicate)

```bash
# Obtener tu API key en: https://replicate.com/account/api-tokens

export REPLICATE_API_KEY="..."
```

---

## 🔧 Configuración Avanzada de Providers

### 📍 URLs Personalizadas de Proveedores

**IMPORTANTE:** Todas las URLs de los proveedores están configurables en un archivo JSON central:

📁 **Ubicación:** `luminoracore-sdk-python/luminoracore/config/provider_urls.json`

Este archivo contiene las URLs base para todos los proveedores:

```json
{
  "providers": {
    "openai": {
      "base_url": "https://api.openai.com/v1",
      "default_model": "gpt-3.5-turbo"
    },
    "anthropic": {
      "base_url": "https://api.anthropic.com/v1",
      "default_model": "claude-3-sonnet-20240229"
    },
    "deepseek": {
      "base_url": "https://api.deepseek.com/v1",
      "default_model": "deepseek-chat"
    },
    "mistral": {
      "base_url": "https://api.mistral.ai/v1",
      "default_model": "mistral-tiny"
    },
    ...
  }
}
```

### ✨ ¿Por qué es importante esto?

1. **URLs Cambian:** Si un proveedor cambia su endpoint, solo editas el archivo JSON
2. **Nuevos Providers:** Puedes añadir fácilmente nuevos LLMs sin modificar código
3. **Proxies/Mirrors:** Usa URLs alternativas o proxies para acceder a los LLMs
4. **Self-hosted:** Conecta a instancias locales de modelos (Ollama, LocalAI, etc.)

### 🛠️ Cómo Personalizar URLs

#### Opción 1: Editar el archivo de configuración

```json
// luminoracore-sdk-python/luminoracore/config/provider_urls.json
{
  "custom_providers": {
    "mi-llm-local": {
      "name": "Mi LLM Local",
      "base_url": "http://localhost:8000/v1",
      "default_model": "local-model",
      "chat_endpoint": "/chat/completions"
    }
  }
}
```

#### Opción 2: Override en tiempo de ejecución (Python)

```python
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig

# Crear provider con URL personalizada
provider_config = ProviderConfig(
    name="openai",
    api_key="sk-...",
    base_url="https://mi-proxy.com/openai/v1",  # URL personalizada
    model="gpt-4"
)

client = LuminoraCoreClient(provider_config=provider_config)
```

### 📋 Providers Disponibles

| Provider | URL Base | Modelo Default | Instalación |
|----------|----------|----------------|-------------|
| **OpenAI** | `https://api.openai.com/v1` | `gpt-3.5-turbo` | `pip install -e ".[openai]"` |
| **Anthropic** | `https://api.anthropic.com/v1` | `claude-3-sonnet-20240229` | `pip install -e ".[anthropic]"` |
| **DeepSeek** 💰 | `https://api.deepseek.com/v1` | `deepseek-chat` | `pip install -e ".[deepseek]"` |
| **Mistral** | `https://api.mistral.ai/v1` | `mistral-tiny` | `pip install -e ".[mistral]"` |
| **Cohere** | `https://api.cohere.ai/v1` | `command` | `pip install -e ".[cohere]"` |
| **Google** | `https://generativelanguage.googleapis.com/v1` | `gemini-pro` | `pip install -e ".[google]"` |
| **Llama** | `https://api.replicate.com/v1` | `llama-2-7b-chat` | `pip install -e ".[llama]"` |

### 🎯 Casos de Uso

**1. Usar Ollama localmente:**
```python
provider_config = ProviderConfig(
    name="openai",  # Compatible con OpenAI API
    api_key="ollama",  # Dummy key
    base_url="http://localhost:11434/v1",
    model="llama2"
)
```

**2. Usar Azure OpenAI:**
```python
provider_config = ProviderConfig(
    name="openai",
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    base_url="https://YOUR-RESOURCE.openai.azure.com",
    model="gpt-35-turbo"
)
```

**3. Usar proxy corporativo:**
```python
provider_config = ProviderConfig(
    name="openai",
    api_key="sk-...",
    base_url="https://proxy.company.com/openai/v1",
    model="gpt-4"
)
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

