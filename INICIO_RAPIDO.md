# 🚀 Inicio Rápido - LuminoraCore

**¿Primera vez usando LuminoraCore? ¡Comienza aquí!**

---

## ⚡ Instalación Express (1 comando)

### Windows (PowerShell)

```powershell
.\instalar_todo.ps1
```

### Linux/Mac

```bash
chmod +x instalar_todo.sh
./instalar_todo.sh
```

**Esto instalará:**
- ✅ luminoracore (motor base)
- ✅ luminoracore-cli (herramienta CLI)
- ✅ luminoracore-sdk (SDK completo)

---

## ✅ Verificar Instalación

### Opción 1: Script Automático (Recomendado)

```bash
# Descarga el script (si no lo tienes)
curl -O https://raw.githubusercontent.com/tu-usuario/luminoracore/main/verificar_instalacion.py

# Ejecuta la verificación completa
python verificar_instalacion.py
```

**Salida esperada:** `🎉 INSTALACION COMPLETA Y CORRECTA`

### Opción 2: Scripts de Ejemplo (Paso a Paso)

```bash
# 1. Probar el motor base
python ejemplo_quick_start_core.py

# 2. Probar el CLI
python ejemplo_quick_start_cli.py

# 3. Probar el SDK
python ejemplo_quick_start_sdk.py
```

Si todos muestran ✅, ¡estás listo!

---

## 📚 ¿Qué componente necesito?

### 🧠 **luminoracore** (Motor Base)

**Úsalo si necesitas:**
- Cargar y validar personalidades de IA
- Compilar personalidades para diferentes LLMs
- Mezclar personalidades (PersonaBlend™)
- Sin conexiones a APIs externas

**Ejemplo:**
```python
from luminoracore import Personality, PersonalityValidator

personality = Personality("mi_personalidad.json")
validator = PersonalityValidator()
result = validator.validate(personality)
```

---

### 🛠️ **luminoracore-cli** (Herramienta CLI)

**Úsalo si necesitas:**
- Trabajar con personalidades desde la terminal
- Crear personalidades con wizard interactivo
- Servidor de desarrollo con interfaz web
- Validar y compilar sin escribir código

**Ejemplo:**
```bash
# Listar personalidades
luminoracore list

# Validar una personalidad
luminoracore validate mi_personalidad.json

# Iniciar servidor web
luminoracore serve
```

---

### 🐍 **luminoracore-sdk** (SDK Completo)

**Úsalo si necesitas:**
- Construir aplicaciones completas con IA
- Conexiones REALES a OpenAI, Anthropic, etc.
- Gestión de sesiones y conversaciones
- Memoria persistente (Redis, PostgreSQL, MongoDB)
- Monitoreo y métricas

**Ejemplo:**
```python
import asyncio
from luminoracore import LuminoraCoreClient
from luminoracore.types.provider import ProviderConfig

async def main():
    client = LuminoraCoreClient()
    await client.initialize()
    
    # Configurar OpenAI
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
    
    # Enviar mensaje (¡CONEXIÓN REAL!)
    response = await client.send_message(
        session_id=session_id,
        message="Hola, ¿cómo estás?"
    )
    
    print(response.content)
    await client.cleanup()

asyncio.run(main())
```

---

## 🎯 Casos de Uso Comunes

### 1. Solo quiero validar archivos de personalidades
👉 Usa **luminoracore-cli**
```bash
luminoracore validate personalidades/*.json
```

### 2. Quiero crear un chatbot con personalidad
👉 Usa **luminoracore-sdk**
```python
# Ver ejemplo_quick_start_sdk.py
```

### 3. Quiero mezclar dos personalidades
👉 Usa **luminoracore** (código) o **luminoracore-cli** (terminal)
```bash
# CLI
luminoracore blend persona1.json:0.6 persona2.json:0.4

# Código
from luminoracore import PersonalityBlender
blender = PersonalityBlender()
blended = blender.blend(personalities=[p1, p2], weights=[0.6, 0.4])
```

### 4. Necesito una interfaz gráfica para probar
👉 Usa **luminoracore-cli serve**
```bash
luminoracore serve
# Abre http://localhost:8000
```

---

## 🔑 Configurar API Keys (Solo para SDK)

Si vas a hacer llamadas REALES a APIs de LLM:

### OpenAI

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-tu-api-key-aquí"

# Linux/Mac
export OPENAI_API_KEY="sk-tu-api-key-aquí"
```

### Anthropic

```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-tu-api-key-aquí"

# Linux/Mac
export ANTHROPIC_API_KEY="sk-ant-tu-api-key-aquí"
```

**Obtener API keys:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Cohere: https://dashboard.cohere.ai/

---

## 📖 Documentación Completa

- **Guía Completa**: [GUIA_INSTALACION_USO.md](GUIA_INSTALACION_USO.md)
- **Estado del Proyecto**: [ESTADO_ACTUAL_PROYECTO.md](ESTADO_ACTUAL_PROYECTO.md)
- **Características Técnicas**: [CARACTERISTICAS_TECNICAS_LUMINORACORE.md](CARACTERISTICAS_TECNICAS_LUMINORACORE.md)

---

## 🆘 Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'luminoracore'"

```bash
# Activa el entorno virtual
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate

# Reinstala
cd luminoracore && pip install -e . && cd ..
```

### Error: "Command 'luminoracore' not found"

```bash
cd luminoracore-cli
pip install -e .
cd ..
```

### Error: "Permission denied" en Windows

```powershell
# Ejecuta en PowerShell como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 🎓 Aprender Más

### Ejemplos Incluidos

```bash
# Motor base
python luminoracore/examples/basic_usage.py
python luminoracore/examples/blending_demo.py

# SDK
python luminoracore-sdk-python/examples/simple_usage.py
python luminoracore-sdk-python/examples/personality_blending.py
```

### CLI Interactivo

```bash
# Modo interactivo para crear personalidades
luminoracore create --interactive

# Explorar personalidades disponibles
luminoracore list --detailed

# Servidor de desarrollo
luminoracore serve
```

---

## 📊 Resumen de Comandos

```bash
# Instalación
.\instalar_todo.ps1          # Windows
./instalar_todo.sh           # Linux/Mac

# Verificación
python ejemplo_quick_start_core.py
python ejemplo_quick_start_cli.py
python ejemplo_quick_start_sdk.py

# CLI
luminoracore --help          # Ver ayuda
luminoracore list            # Listar personalidades
luminoracore validate <file> # Validar
luminoracore compile <file>  # Compilar
luminoracore serve           # Servidor web

# Python
from luminoracore import Personality, PersonalityValidator
from luminoracore import LuminoraCoreClient  # SDK
```

---

## ✨ Próximos Pasos

1. ✅ **Instalar**: `.\instalar_todo.ps1` o `./instalar_todo.sh`
2. ✅ **Verificar**: Ejecutar los 3 scripts de quick start
3. ✅ **Explorar**: Lee [GUIA_INSTALACION_USO.md](GUIA_INSTALACION_USO.md)
4. ✅ **Practicar**: Ejecuta los ejemplos en `luminoracore/examples/`
5. ✅ **Crear**: Haz tu primera personalidad con `luminoracore create --interactive`

---

**¿Necesitas ayuda?** Lee la [Guía Completa](GUIA_INSTALACION_USO.md) o revisa [ESTADO_ACTUAL_PROYECTO.md](ESTADO_ACTUAL_PROYECTO.md)

**¡Listo para empezar! 🚀**

