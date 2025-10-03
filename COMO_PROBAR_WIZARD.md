# 🧪 CÓMO PROBAR EL WIZARD INTERACTIVO DE LUMINORACORE

## 📋 RESUMEN

El wizard interactivo de LuminoraCore está **100% implementado y funcional**. Te explico todas las formas de probarlo:

## 🚀 MÉTODOS DE PRUEBA

### 1. **PRUEBA DIRECTA CON CLI** ⭐ **RECOMENDADO**

```bash
# Navegar al directorio CLI
cd luminoracore-cli

# Instalar dependencias (si no está hecho)
pip install -e .

# Ejecutar wizard interactivo
python -m luminoracore_cli.main create --interactive
```

**¿Qué hace?**
- Te guía paso a paso para crear una personalidad
- Pregunta por nombre, descripción, traits, reglas, etc.
- Valida los datos en tiempo real
- Guarda la personalidad en formato JSON

### 2. **PRUEBA CON COMANDOS ESPECÍFICOS**

```bash
# Crear personalidad con wizard
luminoracore create --interactive

# Validar personalidad creada
luminoracore validate mi_personalidad.json

# Compilar para OpenAI
luminoracore compile mi_personalidad.json --provider openai

# Probar personalidad interactivamente
luminoracore test mi_personalidad.json --interactive

# Ver información de la personalidad
luminoracore info mi_personalidad.json
```

### 3. **PRUEBA CON SERVIDOR WEB** 🌐

```bash
# Iniciar servidor de desarrollo
cd luminoracore-cli
python -m luminoracore_cli.main serve

# Abrir en navegador
# http://127.0.0.1:8000
```

**Características del servidor:**
- Interfaz web completa
- API REST para todas las operaciones
- WebSocket para chat en tiempo real
- Creación de personalidades desde la web

### 4. **PRUEBA CON SDK PYTHON** 🐍

```python
from luminoracore import LuminoraCoreClient

# Crear cliente
client = LuminoraCoreClient()

# Crear personalidad programáticamente
personality_data = {
    "name": "MiPersonalidad",
    "description": "Una personalidad de prueba",
    "system_prompt": "Eres un asistente útil y amigable",
    "metadata": {"version": "1.0.0"}
}

await client.load_personality("mi_personalidad", personality_data)

# Crear sesión y chatear
session = await client.create_session(
    personality=personality_data,
    provider_config=provider_config
)

response = await session.send_message("Hola, ¿cómo estás?")
print(response.content)
```

## 🎯 FLUJO COMPLETO DE PRUEBA

### **Paso 1: Crear Personalidad**
```bash
cd luminoracore-cli
python -m luminoracore_cli.main create --interactive
```

**Respuestas sugeridas:**
- Nombre: `TestWizard`
- Descripción: `Personalidad creada con el wizard`
- Traits: `helpful, friendly, test`
- Reglas: `Be helpful and friendly`, `Always respond with test prefix`

### **Paso 2: Validar Personalidad**
```bash
python -m luminoracore_cli.main validate TestWizard.json
```

### **Paso 3: Compilar para OpenAI**
```bash
python -m luminoracore_cli.main compile TestWizard.json --provider openai
```

### **Paso 4: Probar Interactivamente**
```bash
python -m luminoracore_cli.main test TestWizard.json --interactive
```

## 🔧 CONFIGURACIÓN PARA PRUEBAS REALES

### **Variables de Entorno (Opcional)**
```bash
# Para pruebas con APIs reales
export OPENAI_API_KEY="tu_api_key_aqui"
export ANTHROPIC_API_KEY="tu_api_key_aqui"
export GOOGLE_API_KEY="tu_api_key_aqui"
```

### **Sin API Keys (Modo Mock)**
- El sistema funciona perfectamente sin API keys
- Usa respuestas simuladas para las pruebas
- Ideal para desarrollo y testing

## 📊 FUNCIONALIDADES DEL WIZARD

### ✅ **IMPLEMENTADO Y FUNCIONANDO**

1. **Creación Interactiva**
   - Preguntas guiadas paso a paso
   - Validación en tiempo real
   - Sugerencias automáticas

2. **Validación Completa**
   - Esquema JSON Schema
   - Validaciones de negocio
   - Sugerencias de mejora

3. **Compilación Multi-Provider**
   - OpenAI, Anthropic, Google, Cohere, Mistral
   - Caché inteligente
   - Optimizaciones de rendimiento

4. **Testing Interactivo**
   - Chat en tiempo real
   - Múltiples proveedores
   - Modo mock y real

5. **Servidor Web**
   - Interfaz gráfica completa
   - API REST
   - WebSocket para chat

## 🐛 SOLUCIÓN DE PROBLEMAS

### **Error: "Module not found"**
```bash
# Instalar en modo desarrollo
cd luminoracore-cli
pip install -e .
```

### **Error: "Permission denied"**
```bash
# En Windows, ejecutar como administrador
# En Linux/Mac, usar sudo si es necesario
```

### **Error: "Port already in use"**
```bash
# Usar puerto diferente
python -m luminoracore_cli.main serve --port 8001
```

## 📈 MÉTRICAS DE ÉXITO

### **Indicadores de Funcionamiento Correcto:**

1. **Wizard de Creación**
   - ✅ Preguntas aparecen correctamente
   - ✅ Validación funciona en tiempo real
   - ✅ Archivo JSON se genera correctamente

2. **Validación**
   - ✅ Errores se muestran claramente
   - ✅ Sugerencias aparecen
   - ✅ Formato de salida es correcto

3. **Compilación**
   - ✅ Prompts se generan correctamente
   - ✅ Caché funciona
   - ✅ Múltiples proveedores funcionan

4. **Testing**
   - ✅ Chat interactivo funciona
   - ✅ Respuestas se muestran correctamente
   - ✅ Múltiples sesiones funcionan

## 🎉 CONCLUSIÓN

**El wizard interactivo está 100% funcional** y listo para usar. Puedes:

1. **Crear personalidades** con el wizard interactivo
2. **Validar** las personalidades creadas
3. **Compilar** para diferentes proveedores
4. **Probar** con chat interactivo
5. **Usar** el servidor web para interfaz gráfica

**¡Todo funciona perfectamente!** 🚀
