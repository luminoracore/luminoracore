# 🧠 LuminoraCore - ¡Empieza Aquí!

<div align="center">

**Sistema Universal de Gestión de Personalidades de IA**

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│   ¿Primera vez aquí?                                    │
│   ¡Todo lo que necesitas en UN SOLO LUGAR! 👇          │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

</div>

---

## ⚡ Instalación Ultra-Rápida

### 1️⃣ Clona o ubica el proyecto

```bash
cd "D:\Proyectos Ereace\LuminoraCoreBase"
```

### 2️⃣ Ejecuta UN comando

**Windows:**
```powershell
.\instalar_todo.ps1
```

**Linux/Mac:**
```bash
./instalar_todo.sh
```

### 3️⃣ Verifica que funciona

```bash
python ejemplo_quick_start_core.py
python ejemplo_quick_start_cli.py
python ejemplo_quick_start_sdk.py
```

**✅ Si ves checkmarks verdes, ¡ya estás listo!**

---

## 📚 Documentación por Nivel

### 🟢 Nivel Principiante

| Documento | Tiempo | Descripción |
|-----------|--------|-------------|
| **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** | 5 min | Instalación express y primeros pasos |
| **[GUIA_INSTALACION_USO.md](GUIA_INSTALACION_USO.md)** | 30 min | Guía completa paso a paso con ejemplos |

### 🟡 Nivel Intermedio

| Documento | Descripción |
|-----------|-------------|
| `luminoracore/README.md` | Documentación del motor base |
| `luminoracore-cli/README.md` | Documentación del CLI |
| `luminoracore-sdk-python/README.md` | Documentación del SDK |
| [COMO_PROBAR_WIZARD.md](COMO_PROBAR_WIZARD.md) | Crear personalidades con wizard |

### 🔴 Nivel Avanzado

| Documento | Descripción |
|-----------|-------------|
| [CARACTERISTICAS_TECNICAS_LUMINORACORE.md](CARACTERISTICAS_TECNICAS_LUMINORACORE.md) | Detalles técnicos completos |
| [ESTADO_ACTUAL_PROYECTO.md](ESTADO_ACTUAL_PROYECTO.md) | Estado del desarrollo |
| `luminoracore/docs/api_reference.md` | API del motor base |
| `luminoracore-sdk-python/docs/api_reference.md` | API del SDK |

---

## 🎯 ¿Qué quieres hacer?

### 💬 "Quiero crear un chatbot con personalidad"

```
1. Lee: INICIO_RAPIDO.md (Sección SDK)
2. Instala: .\instalar_todo.ps1
3. Ejecuta: python ejemplo_quick_start_sdk.py
4. Configura tu API key de OpenAI/Anthropic
5. Sigue: GUIA_INSTALACION_USO.md (Caso 3: SDK)
```

### ✅ "Quiero validar archivos de personalidades"

```
1. Lee: INICIO_RAPIDO.md (Sección CLI)
2. Instala: .\instalar_todo.ps1
3. Ejecuta: luminoracore validate mi_archivo.json
4. Sigue: GUIA_INSTALACION_USO.md (Caso 2: CLI)
```

### 🎨 "Quiero crear una personalidad nueva"

```
1. Lee: COMO_PROBAR_WIZARD.md
2. Instala el CLI: cd luminoracore-cli && pip install -e .
3. Ejecuta: luminoracore create --interactive
4. Revisa: Docs/personality_format.md
```

### 🔀 "Quiero mezclar personalidades"

```
1. Lee: GUIA_INSTALACION_USO.md (Ejemplo 2 del Core)
2. Ejecuta: python luminoracore/examples/blending_demo.py
3. O usa CLI: luminoracore blend p1.json:0.6 p2.json:0.4
```

### 🌐 "Quiero una interfaz web"

```
1. Instala el CLI: cd luminoracore-cli && pip install -e .
2. Ejecuta: luminoracore serve
3. Abre: http://localhost:8000
4. Lee: GUIA_SETUP_WEB_DEMO.md
```

### 🔧 "Quiero integrar LuminoraCore en mi app"

```
1. Lee: GUIA_INSTALACION_USO.md (Sección SDK)
2. Revisa: luminoracore-sdk-python/examples/
3. Integra: Usa LuminoraCoreClient en tu código
4. Avanzado: luminoracore-sdk-python/examples/integrations/
```

---

## 🗂️ Estructura del Proyecto (Simplificada)

```
LuminoraCoreBase/
│
├── 📘 INICIO_RAPIDO.md              ⭐ EMPIEZA AQUÍ (5 min)
├── 📗 GUIA_INSTALACION_USO.md      ⭐ GUÍA COMPLETA (30 min)
├── 📚 INDICE_DOCUMENTACION.md      📑 Índice de toda la documentación
│
├── 🔧 instalar_todo.ps1/sh         ⚡ Instalación automática
├── ✅ ejemplo_quick_start_*.py     ✅ Scripts de verificación
│
├── 🧠 luminoracore/                Motor Base
│   ├── README.md                   Documentación
│   ├── examples/                   Ejemplos prácticos
│   └── docs/                       Docs técnicas
│
├── 🛠️ luminoracore-cli/            Herramienta CLI
│   ├── README.md                   Documentación
│   └── luminoracore_cli/           Código fuente
│
├── 🐍 luminoracore-sdk-python/     SDK Completo
│   ├── README.md                   Documentación
│   ├── examples/                   Ejemplos con APIs reales
│   └── docs/                       API reference
│
├── 🎭 personalidades/              10 personalidades ejemplo
│   ├── Dr. Luna Científica.json
│   ├── Rocky Inspiración.json
│   └── ...
│
└── 📄 Docs/                        Documentación adicional
    ├── personality_format.md       Formato de personalidades
    ├── LuminoraCore.txt            Especificación
    └── ...
```

---

## 🚦 Pasos Recomendados (Orden)

### Para Principiantes

```
┌─────────────────────────────────────────┐
│ 1. Lee INICIO_RAPIDO.md (5 min)        │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 2. Ejecuta .\instalar_todo.ps1         │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 3. Verifica con los 3 quick_start      │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 4. Lee GUIA_INSTALACION_USO.md         │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 5. Ejecuta ejemplos en examples/       │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│ 6. Crea tu primera personalidad        │
└─────────────────────────────────────────┘
```

### Para Desarrolladores Experimentados

```
1. .\instalar_todo.ps1
2. Revisa ESTADO_ACTUAL_PROYECTO.md
3. Lee luminoracore-sdk-python/docs/api_reference.md
4. Explora examples/integrations/
5. Integra en tu proyecto
```

---

## 📦 ¿Qué Componente Necesito?

| Si necesitas... | Usa | Comando de instalación |
|----------------|-----|------------------------|
| Solo validar/compilar personalidades | **luminoracore** | `cd luminoracore && pip install -e .` |
| Herramienta de línea de comandos | **luminoracore-cli** | `cd luminoracore-cli && pip install -e .` |
| Construir apps con IA | **luminoracore-sdk** | `cd luminoracore-sdk-python && pip install -e ".[openai]"` |
| Todo lo anterior | **Instalador completo** | `.\instalar_todo.ps1` |

---

## 🔑 Configuración Rápida de API Keys

Solo necesario si usas el **SDK** con conexiones reales:

### Windows PowerShell

```powershell
# OpenAI
$env:OPENAI_API_KEY="sk-tu-api-key"

# Anthropic
$env:ANTHROPIC_API_KEY="sk-ant-tu-api-key"
```

### Linux/Mac

```bash
# OpenAI
export OPENAI_API_KEY="sk-tu-api-key"

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-tu-api-key"
```

**Obtener keys:**
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/

---

## ✅ Checklist de Inicio

- [ ] Leí [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
- [ ] Ejecuté `.\instalar_todo.ps1` (o `.sh`)
- [ ] Verifiqué con los 3 scripts `ejemplo_quick_start_*.py`
- [ ] Todos mostraron ✅ checkmarks verdes
- [ ] Leí [GUIA_INSTALACION_USO.md](GUIA_INSTALACION_USO.md)
- [ ] Ejecuté al menos un ejemplo de `examples/`
- [ ] (Opcional) Configuré mis API keys
- [ ] (Opcional) Probé el CLI: `luminoracore --help`

---

## 🆘 ¿Problemas?

### Error en instalación

1. Verifica Python 3.8+: `python --version`
2. Verifica pip: `pip --version`
3. Lee: [GUIA_INSTALACION_USO.md](GUIA_INSTALACION_USO.md) - Sección "Solución de Problemas"

### Comandos no encontrados

```bash
# Asegúrate de activar el entorno virtual
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/Mac

# Reinstala el componente
cd luminoracore && pip install -e . && cd ..
```

### Más ayuda

- [GUIA_INSTALACION_USO.md](GUIA_INSTALACION_USO.md) - Sección completa de troubleshooting
- [ESTADO_ACTUAL_PROYECTO.md](ESTADO_ACTUAL_PROYECTO.md) - Estado del proyecto
- [INDICE_DOCUMENTACION.md](INDICE_DOCUMENTACION.md) - Toda la documentación

---

## 📊 Resumen de Archivos Clave

| Archivo | Propósito | Cuándo usarlo |
|---------|-----------|---------------|
| **INICIO_RAPIDO.md** | Inicio rápido | Primera vez |
| **GUIA_INSTALACION_USO.md** | Guía completa | Aprender en detalle |
| **INDICE_DOCUMENTACION.md** | Índice de docs | Buscar documentación específica |
| **instalar_todo.ps1/sh** | Instalador | Instalar todo |
| **ejemplo_quick_start_*.py** | Verificación | Comprobar instalación |
| **luminoracore/examples/** | Ejemplos | Aprender con código |
| **personalidades/*.json** | Ejemplos reales | Ver formato y ejemplos |

---

## 🎓 Recursos de Aprendizaje

### Video-tutoriales (Imaginarios - Para cuando existan)

- [ ] Instalación en 5 minutos
- [ ] Tu primera personalidad
- [ ] Construir un chatbot con LuminoraCore
- [ ] PersonaBlend: Mezclar personalidades

### Ejemplos Interactivos

```bash
# Ejemplos del motor base
python luminoracore/examples/basic_usage.py
python luminoracore/examples/blending_demo.py
python luminoracore/examples/multi_llm_demo.py

# Ejemplos del SDK
python luminoracore-sdk-python/examples/simple_usage.py
python luminoracore-sdk-python/examples/personality_blending.py

# CLI interactivo
luminoracore create --interactive
luminoracore serve
```

---

## 🌟 Siguiente Nivel

Una vez que domines lo básico:

1. **Explora PersonaBlend™**
   - `luminoracore/examples/blending_demo.py`
   
2. **Integra en Apps Reales**
   - `luminoracore-sdk-python/examples/integrations/`
   
3. **Crea Personalidades Personalizadas**
   - `luminoracore create --interactive`
   
4. **Contribuye al Proyecto**
   - `luminoracore/CONTRIBUTING.md`

---

<div align="center">

## 🚀 ¡Listo para Empezar!

**Empieza con:** [INICIO_RAPIDO.md](INICIO_RAPIDO.md)

**Guía completa:** [GUIA_INSTALACION_USO.md](GUIA_INSTALACION_USO.md)

**Toda la documentación:** [INDICE_DOCUMENTACION.md](INDICE_DOCUMENTACION.md)

---

**¿Preguntas? Consulta la documentación o crea un issue en el repositorio.**

**Made with ❤️ by the LuminoraCore Team**

</div>

