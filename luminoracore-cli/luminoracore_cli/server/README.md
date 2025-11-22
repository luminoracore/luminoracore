# LuminoraCore CLI Development Server

**Propósito:** Servidor de desarrollo local para probar y desarrollar personalidades de LuminoraCore.

---

## ¿Cuándo se usa el Server?

### Casos de Uso

1. **Desarrollo Local:**
   - Probar personalidades sin instalar el SDK
   - Interfaz web para testing interactivo
   - Desarrollo rápido de personalidades

2. **Testing Interactivo:**
   - Chat en tiempo real con personalidades
   - Validación y compilación desde el navegador
   - Blending de personalidades visual

3. **API Local:**
   - Proporcionar API REST para herramientas externas
   - Integración con otros servicios locales
   - Desarrollo frontend sin backend propio

4. **Documentación Interactiva:**
   - Swagger/OpenAPI docs automáticos (`/docs`)
   - Probar endpoints desde el navegador
   - Ejemplos de uso

---

## ¿Cómo se usa?

### 1. Iniciar el Server

```bash
# Básico (puerto 8000 por defecto)
luminoracore serve

# Puerto personalizado
luminoracore serve --port 8080

# Solo API (sin interfaz web)
luminoracore serve --api-only

# Con CORS habilitado (para desarrollo frontend)
luminoracore serve --cors

# Con auto-reload (desarrollo)
luminoracore serve --reload

# Modo verbose
luminoracore serve --verbose
```

### 2. Acceder a la Interfaz Web

Una vez iniciado, abre en el navegador:
- **Interfaz Web:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### 3. Usar la API REST

```bash
# Listar personalidades
curl http://localhost:8000/api/personalities

# Obtener personalidad específica
curl http://localhost:8000/api/personalities/my_personality

# Validar personalidad
curl -X POST http://localhost:8000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"personality_data": {...}, "strict": false}'

# Compilar personalidad
curl -X POST http://localhost:8000/api/compile \
  -H "Content-Type: application/json" \
  -d '{"personality_data": {...}, "provider": "openai"}'

# Blending de personalidades
curl -X POST http://localhost:8000/api/blend \
  -H "Content-Type: application/json" \
  -d '{"personality_weights": {"p1": 0.5, "p2": 0.5}}'
```

### 4. Usar WebSocket Chat

```javascript
// Ejemplo JavaScript
const ws = new WebSocket('ws://localhost:8000/ws/chat');

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: 'chat',
    personality_id: 'my_personality',
    message: 'Hello!',
    provider: 'openai',
    model: 'gpt-3.5-turbo'
  }));
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Response:', data.response);
};
```

---

## ¿El SDK puede usarlo?

### Respuesta Corta: **SÍ, pero indirectamente**

El SDK **NO** usa el server directamente, pero **SÍ puede hacer requests HTTP** a la API del server.

### Arquitectura

```
┌─────────────────────────────────────┐
│         SDK (luminoracore-sdk)      │
│         Usa Core directamente       │
└──────────────┬──────────────────────┘
               │
               │ HTTP Requests (opcional)
               │
┌──────────────▼──────────────────────┐
│    CLI Server (luminoracore serve)   │
│    FastAPI + WebSocket               │
│    Usa CLI Client internamente        │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Core (luminoracore)             │
│      Business Logic                  │
└─────────────────────────────────────┘
```

### Uso del SDK con el Server

**Opción 1: SDK usa Core directamente (Recomendado)**
```python
from luminoracore_sdk import LuminoraCoreClient

# SDK usa Core directamente - NO necesita server
client = LuminoraCoreClient()
await client.initialize()
```

**Opción 2: SDK hace requests HTTP al server (Opcional)**
```python
import httpx

# SDK puede hacer requests al server si está corriendo
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/validate",
        json={"personality_data": {...}}
    )
    result = response.json()
```

### ¿Cuándo usar cada opción?

| Escenario | Recomendación |
|-----------|---------------|
| **Producción** | SDK usa Core directamente |
| **Desarrollo con Frontend** | Usar Server + requests HTTP |
| **Testing Interactivo** | Usar Server (interfaz web) |
| **Integración con otras herramientas** | Usar Server (API REST) |
| **Aplicaciones Python** | SDK usa Core directamente |

---

## Endpoints Disponibles

### REST API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Interfaz web o mensaje API |
| `GET` | `/health` | Health check |
| `GET` | `/api/personalities` | Listar personalidades |
| `GET` | `/api/personalities/{id}` | Obtener personalidad |
| `POST` | `/api/compile` | Compilar personalidad |
| `POST` | `/api/validate` | Validar personalidad |
| `POST` | `/api/blend` | Blending de personalidades |
| `POST` | `/api/test` | Probar personalidad con LLM |

### WebSocket

| Endpoint | Descripción |
|----------|-------------|
| `/ws/chat` | Chat en tiempo real con personalidades |

---

## Ejemplo Completo: SDK usando Server

```python
import httpx
import asyncio

async def use_server_api():
    """Ejemplo: SDK haciendo requests al server"""
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # 1. Health check
        health = await client.get(f"{base_url}/health")
        print(f"Server status: {health.json()}")
        
        # 2. Listar personalidades
        personalities = await client.get(f"{base_url}/api/personalities")
        print(f"Personalities: {personalities.json()}")
        
        # 3. Validar personalidad
        validation = await client.post(
            f"{base_url}/api/validate",
            json={
                "personality_data": {
                    "persona": {"name": "Test", "description": "Test"}
                },
                "strict": False
            }
        )
        print(f"Validation: {validation.json()}")

# Ejecutar
asyncio.run(use_server_api())
```

**Nota:** Esto requiere que el server esté corriendo:
```bash
# Terminal 1: Iniciar server
luminoracore serve

# Terminal 2: Ejecutar script Python
python use_server.py
```

---

## Dependencias

El server requiere dependencias adicionales:

```bash
# Instalar con dependencias del server
pip install 'luminoracore-cli[server]'

# O instalar manualmente
pip install fastapi uvicorn websockets
```

---

## Limitaciones

1. **Solo Desarrollo:** El server está diseñado para desarrollo, no producción
2. **Sin Autenticación:** No tiene autenticación por defecto
3. **Local:** Por defecto solo accesible desde localhost
4. **Sin Persistencia:** No guarda datos entre reinicios (usa cache del CLI)

---

## Comparación: SDK vs Server

| Característica | SDK (Core directo) | Server (API REST) |
|----------------|-------------------|-------------------|
| **Uso Principal** | Producción | Desarrollo |
| **Rendimiento** | Más rápido | Más lento (HTTP overhead) |
| **Interfaz Web** | No | Sí |
| **WebSocket** | No | Sí |
| **Autenticación** | No necesaria | No incluida |
| **Escalabilidad** | Alta | Baja (single instance) |
| **Recomendado para** | Apps Python | Frontend, testing |

---

## Resumen

### ¿Cuándo usar el Server?
- ✅ Desarrollo local de personalidades
- ✅ Testing interactivo con interfaz web
- ✅ Integración con frontend (React, Vue, etc.)
- ✅ API REST para herramientas externas
- ✅ Documentación interactiva

### ¿Cuándo NO usar el Server?
- ❌ Producción (usar SDK directamente)
- ❌ Aplicaciones Python (usar SDK directamente)
- ❌ Alto rendimiento (usar SDK directamente)

### ¿El SDK puede usarlo?
- ✅ **Sí**, haciendo requests HTTP (opcional)
- ✅ **Pero** es mejor usar Core directamente en producción
- ✅ El server es útil para desarrollo y testing

---

**Última Actualización:** 2025-11-21  
**Versión:** 1.2.0

