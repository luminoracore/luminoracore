# LuminoraCore SDK - Integration Examples

Ejemplos de integración del SDK de LuminoraCore con frameworks populares.

---

## 📋 Ejemplos Disponibles

### 1. FastAPI Integration

**Archivo:** `fastapi_integration.py`

**Descripción:** API REST completa usando FastAPI para interactuar con LuminoraCore.

**Características:**
- ✅ Endpoints REST para gestión de sesiones
- ✅ Chat con personalidades
- ✅ Gestión de memoria
- ✅ Mezcla de personalidades
- ✅ Health check

**Endpoints:**
- `POST /sessions` - Crear sesión
- `POST /sessions/{session_id}/messages` - Enviar mensaje
- `GET /sessions/{session_id}/messages` - Obtener historial
- `DELETE /sessions/{session_id}/messages` - Limpiar conversación
- `DELETE /sessions/{session_id}` - Eliminar sesión
- `GET /sessions` - Listar sesiones
- `GET /sessions/{session_id}/info` - Información de sesión
- `GET /personalities` - Listar personalidades
- `POST /personalities/blend` - Mezclar personalidades
- `GET /health` - Health check

**Uso:**
```bash
# Instalar dependencias
pip install fastapi uvicorn

# Ejecutar servidor
python examples/integrations/fastapi_integration.py

# O con uvicorn directamente
uvicorn examples.integrations.fastapi_integration:app --host 0.0.0.0 --port 8000
```

**Ejemplo de uso:**
```bash
# Crear sesión
curl -X POST "http://localhost:8000/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "personality_name": "helpful_assistant",
    "provider_name": "openai",
    "model": "gpt-3.5-turbo",
    "api_key": "your-api-key"
  }'

# Enviar mensaje
curl -X POST "http://localhost:8000/sessions/{session_id}/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello!",
    "temperature": 0.7
  }'
```

---

### 2. Streamlit Integration

**Archivo:** `streamlit_app.py`

**Descripción:** Aplicación web interactiva usando Streamlit para interactuar con personalidades.

**Características:**
- ✅ Interfaz web interactiva
- ✅ Selección de personalidad
- ✅ Chat en tiempo real
- ✅ Visualización de memoria
- ✅ Mezcla de personalidades
- ✅ Gestión de sesiones

**Uso:**
```bash
# Instalar dependencias
pip install streamlit

# Ejecutar aplicación
streamlit run examples/integrations/streamlit_app.py
```

**Características de la UI:**
- **Sidebar:** Configuración de provider, modelo, API key, personalidad
- **Main Area:** Chat interface, historial de conversación
- **Session Info:** Métricas de sesión
- **Personality Blending:** Demo de mezcla de personalidades

---

## 🔧 Configuración

### Requisitos

```bash
# Instalar SDK
cd luminoracore-sdk-python
pip install -e .

# Para FastAPI
pip install fastapi uvicorn

# Para Streamlit
pip install streamlit
```

### Variables de Entorno

```bash
# Para usar providers reales
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
# etc.
```

---

## 🆕 v1.2.0 - Optimization Support

Ambos ejemplos pueden mejorarse para usar `OptimizationConfig`:

### FastAPI con Optimization

```python
from luminoracore.optimization import OptimizationConfig

# En startup
opt_config = OptimizationConfig(
    key_abbreviation=True,
    compact_format=True,
    deduplication=True,
    cache_enabled=True
)

client = LuminoraCoreClient(
    storage_config=StorageConfig(storage_type="memory"),
    optimization_config=opt_config  # 🆕
)
```

### Streamlit con Optimization

```python
@st.cache_resource
def get_client():
    opt_config = OptimizationConfig(
        key_abbreviation=True,
        compact_format=True,
        cache_enabled=True
    )
    
    client = LuminoraCoreClient(
        storage_config=StorageConfig(storage_type="memory"),
        optimization_config=opt_config  # 🆕
    )
    return client
```

**Beneficios:**
- ✅ Token reduction: 25-45%
- ✅ Storage size: Reduced by ~30-40%
- ✅ Cache hits: Faster reads
- ✅ Transparent: No code changes needed

---

## 📊 Comparación de Integraciones

| Característica | FastAPI | Streamlit |
|----------------|---------|-----------|
| **Tipo** | API REST | Web App |
| **Uso** | Backend/API | Frontend/Demo |
| **Complejidad** | Media | Baja |
| **Customización** | Alta | Media |
| **Deployment** | Producción | Desarrollo/Demo |
| **Optimization** | ✅ Soporta | ✅ Soporta |

---

## 🐛 Troubleshooting

### Error: "Module not found: luminoracore_sdk"

**Solución:**
```bash
cd luminoracore-sdk-python
pip install -e .
```

### Error: "FastAPI/Streamlit not found"

**Solución:**
```bash
pip install fastapi uvicorn  # Para FastAPI
pip install streamlit         # Para Streamlit
```

### Error: "Session not found"

**Solución:** Asegúrate de crear una sesión antes de enviar mensajes.

### Error: "Provider error"

**Solución:** Verifica que la API key esté configurada correctamente.

---

## 📚 Más Información

- **SDK Documentation:** `../README.md`
- **Examples:** `../README.md`
- **Architecture:** `../../../ARCHITECTURE.md`
- **Migration Guide:** `../../../MIGRATION_1.1_to_1.2.md`

---

## 🔄 Mejoras Futuras (Opcional)

1. **WebSocket Support:** Streaming de mensajes en tiempo real
2. **Authentication:** JWT o API keys para FastAPI
3. **Database Integration:** Persistencia de sesiones
4. **Monitoring:** Métricas y logging avanzado
5. **Optimization UI:** Visualización de stats de optimización en Streamlit

---

**Última Actualización:** 2025-11-21  
**Versión SDK:** 1.2.0  
**Estado:** ✅ Ejemplos funcionando correctamente

