# 🧪 Guía: Script de Verificación de Instalación

**Versión:** 1.0.0  
**Script:** `verificar_instalacion.py`  
**Actualizado:** Octubre 2025

---

## 📌 ¿Qué es este script?

`verificar_instalacion.py` es un **script de diagnóstico automático** que verifica que LuminoraCore esté instalado correctamente y funcionando.

---

## ✅ Cuándo Usarlo

### Siempre úsalo DESPUÉS de:
1. ✅ **Primera instalación** - Para confirmar que todo funciona
2. ✅ **Actualizar componentes** - Para verificar compatibilidad
3. ✅ **Reinstalar** - Para confirmar que todo se restableció
4. ✅ **Cambiar de entorno virtual** - Para validar el nuevo entorno
5. ✅ **Agregar providers** - Para confirmar que están disponibles
6. ✅ **Configurar API keys** - Para ver cuáles están activas
7. ✅ **Antes de reportar un error** - Para tener información de diagnóstico

### También úsalo SI:
- ❓ No estás seguro si algo está instalado
- ❓ Algo no funciona y no sabes por qué
- ❓ Quieres ver qué providers tienes disponibles
- ❓ Necesitas verificar tus API keys sin mostrarlas

---

## 📥 Cómo Obtener el Script

### Opción 1: Clonar desde GitHub

```bash
# Si clonaste el repositorio completo, ya lo tienes:
cd LuminoraCoreBase
ls verificar_instalacion.py   # Debe existir
```

### Opción 2: Descargar Directamente

```bash
# Descarga desde GitHub (actualiza la URL con tu repositorio real)
curl -O https://raw.githubusercontent.com/tu-usuario/luminoracore/main/verificar_instalacion.py

# O con wget:
wget https://raw.githubusercontent.com/tu-usuario/luminoracore/main/verificar_instalacion.py
```

### Opción 3: Copiar Manualmente

Si tienes acceso al código fuente, copia el archivo desde:
```
LuminoraCoreBase/verificar_instalacion.py
```

---

## 🚀 Cómo Usarlo

### Paso 1: Asegúrate de que tu entorno virtual está activo

```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### Paso 2: Ejecuta el script

```bash
python verificar_instalacion.py
```

### Paso 3: Revisa la salida

El script imprimirá un informe detallado de 6 secciones.

---

## 📊 Qué Verifica el Script

### 1. Entorno Virtual

```
✅ Entorno virtual activado
   Python: 3.11.0
   Path: /ruta/a/tu/venv/bin/python
```

O:

```
⚠️  WARNING: No estas en un entorno virtual
   Recomendacion: Activa tu venv antes de continuar
```

**¿Qué significa?**
- ✅ Verde = Estás trabajando en un entorno aislado (correcto)
- ⚠️ Amarillo = Estás usando Python del sistema (no recomendado)

---

### 2. Motor Base (luminoracore)

```
1. MOTOR BASE (luminoracore)
----------------------------------------------------------------------
✅ Instalado correctamente (v1.0.0)
   - Personality: OK
   - PersonalityValidator: OK
   - PersonalityCompiler: OK
   - LLMProvider: OK
```

O:

```
❌ ERROR: No module named 'luminoracore'
   Solucion: cd luminoracore && pip install -e .
```

**¿Qué significa?**
- ✅ Verde = El motor base está instalado y funcional
- ❌ Rojo = Falta instalar el motor base

---

### 3. CLI (luminoracore-cli)

```
2. CLI (luminoracore-cli)
----------------------------------------------------------------------
✅ Instalado correctamente (v1.0.0)
   - Comando 'luminoracore': OK
```

O:

```
❌ ERROR: No module named 'luminoracore_cli'
   Solucion: cd luminoracore-cli && pip install -e .
```

**¿Qué significa?**
- ✅ Verde = El CLI está instalado y el comando está disponible
- ❌ Rojo = Falta instalar el CLI
- ⚠️ Amarillo = Paquete instalado pero comando no encontrado (reinstalar)

---

### 4. SDK (luminoracore-sdk-python)

```
3. SDK (luminoracore-sdk-python)
----------------------------------------------------------------------
✅ Instalado correctamente
   - LuminoraCoreClient: OK
   - ProviderConfig: OK
   - StorageConfig: OK
```

O:

```
❌ ERROR: cannot import name 'LuminoraCoreClient'
   Solucion: cd luminoracore-sdk-python && pip install -e '.[openai]'
```

**¿Qué significa?**
- ✅ Verde = El SDK está instalado y funcional
- ❌ Rojo = Falta instalar el SDK

---

### 5. Providers Disponibles

```
4. PROVIDERS DISPONIBLES
----------------------------------------------------------------------
  ✅ Openai       - OpenAIProvider
  ✅ Anthropic    - AnthropicProvider
  ✅ Deepseek     - DeepSeekProvider
  ✅ Mistral      - MistralProvider
  ✅ Cohere       - CohereProvider
  ✅ Google       - GoogleProvider
  ✅ Llama        - LlamaProvider

✅ Todos los providers (7) disponibles
```

O:

```
  ✅ Openai       - OpenAIProvider
  ❌ Anthropic    - ERROR: No module named 'anthropic'
  ...
  
⚠️  2 provider(s) con problemas
```

**¿Qué significa?**
- ✅ Verde = Provider disponible y funcional
- ❌ Rojo = Falta instalar la dependencia del provider

**Cómo solucionarlo:**
```bash
# Instalar provider específico
pip install -e ".[anthropic]"

# O todos
pip install -e ".[all]"
```

---

### 6. Dependencias Opcionales

```
5. DEPENDENCIAS OPCIONALES
----------------------------------------------------------------------
  ✅ openai       - OpenAI API
  ⚪ anthropic    - Anthropic Claude API (no instalado)
  ⚪ redis        - Redis storage (no instalado)
  ⚪ asyncpg      - PostgreSQL storage (no instalado)
  ⚪ motor        - MongoDB storage (no instalado)
```

**¿Qué significa?**
- ✅ Verde = Dependencia instalada
- ⚪ Blanco = Dependencia opcional no instalada (no es error)

**Estas son opcionales**, solo instálalas si las necesitas:
```bash
# Solo si necesitas Redis
pip install redis

# Solo si necesitas PostgreSQL
pip install asyncpg

# Solo si necesitas MongoDB
pip install motor
```

---

### 7. API Keys Configuradas

```
6. CONFIGURACION
----------------------------------------------------------------------
  ✅ OPENAI_API_KEY
  ⚪ ANTHROPIC_API_KEY (no configurada)
  ⚪ DEEPSEEK_API_KEY (no configurada)
  ⚪ MISTRAL_API_KEY (no configurada)
  ⚪ COHERE_API_KEY (no configurada)
  ⚪ GOOGLE_API_KEY (no configurada)

✅ 1 API key(s) configurada(s)
```

**¿Qué significa?**
- ✅ Verde = API key configurada en variable de entorno
- ⚪ Blanco = API key no configurada (solo configura las que necesites)

**El script NO muestra el valor** de tus API keys (por seguridad), solo si existen.

---

## 📋 Resumen Final

### Si todo está bien:

```
==================================================================
RESUMEN
==================================================================
🎉 INSTALACION COMPLETA Y CORRECTA

Todos los componentes principales instalados:
  ✅ Motor Base (luminoracore)
  ✅ CLI (luminoracore-cli)
  ✅ SDK (luminoracore-sdk)

Siguientes pasos:
  1. Configura tus API keys (variables de entorno)
  2. Lee: INICIO_RAPIDO.md
  3. Prueba: luminoracore --help
  4. Ejecuta ejemplos: python ejemplo_quick_start_core.py
==================================================================
```

**Exit code:** `0` (éxito)

---

### Si hay problemas:

```
==================================================================
RESUMEN
==================================================================
⚠️  ALGUNOS COMPONENTES FALTAN

Problemas encontrados:
  ❌ Motor Base no instalado
  ❌ SDK no instalado

Consulta: GUIA_INSTALACION_USO.md seccion 'Solucion de Problemas'
==================================================================
```

**Exit code:** `1` (error)

---

## 🐛 Solución de Problemas Comunes

### Problema 1: "python: command not found"

**Solución:**
```bash
# Usa python3 en lugar de python
python3 verificar_instalacion.py
```

---

### Problema 2: "Permission denied"

**Solución:**
```bash
# Dale permisos de ejecución (Linux/Mac)
chmod +x verificar_instalacion.py
python verificar_instalacion.py
```

---

### Problema 3: "ModuleNotFoundError: No module named 'luminoracore'"

**Solución:**
1. Asegúrate de que el entorno virtual está activo
2. Instala los componentes:
```bash
cd luminoracore
pip install -e .
```

---

### Problema 4: "All providers failing"

**Solución:**
```bash
# Reinstala el SDK con todos los providers
cd luminoracore-sdk-python
pip install -e ".[all]"
```

---

### Problema 5: El script no imprime correctamente en Windows

El script incluye un fix para Windows, pero si ves caracteres extraños:

```bash
# Usa PowerShell con UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python verificar_instalacion.py
```

---

## 📖 Interpretando los Resultados

### Resultado: Todo Verde ✅

```
✅ Motor Base: OK
✅ CLI: OK
✅ SDK: OK
✅ 7 Providers disponibles
```

**Acción:** ¡Perfecto! Puedes empezar a usar LuminoraCore.

---

### Resultado: Algunos Componentes Faltan ⚠️

```
✅ Motor Base: OK
❌ CLI: NO INSTALADO
✅ SDK: OK
```

**Acción:** Instala los componentes faltantes según las instrucciones del script.

---

### Resultado: Providers con Problemas ❌

```
✅ OpenAI: OK
❌ Anthropic: ERROR
✅ DeepSeek: OK
```

**Acción:** 
```bash
# Instala el provider que falta
cd luminoracore-sdk-python
pip install -e ".[anthropic]"

# Verifica de nuevo
python verificar_instalacion.py
```

---

### Resultado: Sin API Keys ⚪

```
⚪ OPENAI_API_KEY (no configurada)
⚪ ANTHROPIC_API_KEY (no configurada)
```

**Acción:**
```bash
# Configura la API key que necesites (ejemplo: OpenAI)
# Windows
$env:OPENAI_API_KEY="sk-tu-api-key"

# Linux/Mac
export OPENAI_API_KEY="sk-tu-api-key"

# Verifica de nuevo
python verificar_instalacion.py
```

---

## 🔄 Cuándo Re-ejecutarlo

### Siempre que:
1. ✅ Instales o actualices componentes
2. ✅ Agregues un nuevo provider
3. ✅ Configures una nueva API key
4. ✅ Cambies de entorno virtual
5. ✅ Algo deje de funcionar

### Es tu "Doctor" para LuminoraCore:
- 🩺 **Diagnóstico completo** en segundos
- 🔍 **Detecta problemas** automáticamente
- 💡 **Sugiere soluciones** específicas
- ✅ **Confirma** que todo funciona

---

## 📝 Casos de Uso Reales

### Caso 1: Primera Instalación

```bash
# 1. Clonar e instalar
git clone https://github.com/tu-usuario/luminoracore.git
cd luminoracore
./instalar_todo.sh

# 2. Verificar
python verificar_instalacion.py

# ✅ Resultado: Todo instalado correctamente
```

---

### Caso 2: Agregar un Provider Nuevo

```bash
# Antes de instalar
python verificar_instalacion.py
# ❌ Anthropic Provider: ERROR

# Instalar
pip install -e ".[anthropic]"

# Después de instalar
python verificar_instalacion.py
# ✅ Anthropic Provider: OK
```

---

### Caso 3: Configurar API Keys

```bash
# Antes de configurar
python verificar_instalacion.py
# ⚪ OPENAI_API_KEY (no configurada)

# Configurar
export OPENAI_API_KEY="sk-..."

# Después de configurar
python verificar_instalacion.py
# ✅ OPENAI_API_KEY configurada
```

---

### Caso 4: Reportar un Error

Antes de reportar un error en GitHub o pedir ayuda:

```bash
# 1. Ejecuta el script
python verificar_instalacion.py > diagnostico.txt

# 2. Adjunta diagnostico.txt a tu reporte
```

Esto ayuda a los desarrolladores a entender tu configuración.

---

## 🎯 Resumen Rápido

| Cuándo | Comando | Propósito |
|--------|---------|-----------|
| **Después de instalar** | `python verificar_instalacion.py` | Confirmar instalación |
| **Algo no funciona** | `python verificar_instalacion.py` | Diagnosticar problema |
| **Agregar provider** | `python verificar_instalacion.py` | Verificar disponibilidad |
| **Configurar API key** | `python verificar_instalacion.py` | Confirmar configuración |
| **Reportar error** | `python verificar_instalacion.py > diag.txt` | Generar diagnóstico |

---

## ✅ Checklist de Verificación Manual

Si prefieres verificar manualmente:

```bash
# 1. Motor Base
python -c "import luminoracore; print(luminoracore.__version__)"

# 2. CLI
luminoracore --version

# 3. SDK
python -c "from luminoracore import LuminoraCoreClient; print('OK')"

# 4. Provider (ejemplo: OpenAI)
python -c "from luminoracore.providers import OpenAIProvider; print('OK')"

# 5. API Key
echo $OPENAI_API_KEY  # Linux/Mac
echo $env:OPENAI_API_KEY  # Windows
```

---

## 📚 Referencias

- **Documentación principal:** [GUIA_INSTALACION_USO.md](./GUIA_INSTALACION_USO.md)
- **Solución de problemas:** [GUIA_INSTALACION_USO.md#solución-de-problemas](./GUIA_INSTALACION_USO.md)
- **Inicio rápido:** [INICIO_RAPIDO.md](./INICIO_RAPIDO.md)
- **Script fuente:** `verificar_instalacion.py`

---

**🎓 TIP PROFESIONAL:**  
Ejecuta `python verificar_instalacion.py` después de cada cambio importante en tu entorno. ¡Es rápido, completo y te ahorra tiempo de debugging!

