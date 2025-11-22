# LuminoraCore SDK - Monitoring Module

Módulo de monitoreo, logging, métricas y tracing distribuido para el SDK.

---

## 📋 Componentes

### 1. LuminoraLogger (`logger.py`)

**Propósito:** Sistema de logging avanzado con formato JSON y texto.

**Características:**
- ✅ Formato JSON o texto
- ✅ Sanitización automática de datos sensibles
- ✅ Logging a consola y archivo
- ✅ Métodos especializados para eventos del SDK
- ✅ Timestamps y metadata incluidos

**Uso:**
```python
from luminoracore_sdk.monitoring import LuminoraLogger

# Crear logger
logger = LuminoraLogger(
    name="my_app",
    level="INFO",
    log_file="app.log",
    format="json",
    sanitize_sensitive=True
)

# Logging básico
logger.info("Application started")
logger.error("Something went wrong", error_code=500)

# Logging especializado
logger.log_api_call(
    provider="openai",
    model="gpt-3.5-turbo",
    endpoint="/chat/completions",
    method="POST",
    status_code=200,
    response_time=1.23,
    tokens_used=150
)

logger.log_session_event(
    session_id="session_123",
    event_type="created",
    message="New session created"
)
```

**Formatos:**
- **JSON:** `{"timestamp": "...", "level": "INFO", "message": "...", ...}`
- **Text:** `[2025-11-21T10:00:00] [INFO] [module] message (key=value)`

**Sanitización:**
- Detecta automáticamente claves sensibles (api_key, password, secret, etc.)
- Sanitiza valores usando `sanitize_api_key()` helper
- Funciona recursivamente en dicts y lists

---

### 2. MetricsCollector (`metrics.py`)

**Propósito:** Recolección y gestión de métricas para el SDK.

**Características:**
- ✅ Contadores (counters)
- ✅ Gauges (valores instantáneos)
- ✅ Histogramas (distribuciones)
- ✅ Timing (duraciones)
- ✅ Historial de métricas
- ✅ Exportación a JSON y Prometheus

**Uso:**
```python
from luminoracore_sdk.monitoring import MetricsCollector

# Crear collector
metrics = MetricsCollector(max_history=1000)

# Contadores
await metrics.increment_counter("api_calls", value=1, tags={"provider": "openai"})
await metrics.increment_counter("errors", value=1, tags={"type": "timeout"})

# Gauges
await metrics.set_gauge("active_sessions", value=42)
await metrics.set_gauge("memory_usage_mb", value=128.5)

# Histogramas
await metrics.record_histogram("response_time", value=1.23)
await metrics.record_histogram("tokens_per_request", value=150)

# Timing
await metrics.record_timing("api_request", duration=1.23)

# Obtener métricas
counter_value = await metrics.get_counter("api_calls")
gauge_value = await metrics.get_gauge("active_sessions")
histogram_stats = await metrics.get_histogram_stats("response_time")
# Returns: {"count": 100, "min": 0.1, "max": 5.0, "mean": 1.2, "median": 1.0, "p95": 2.5, "p99": 4.0}

# Exportar
all_metrics = await metrics.get_all_metrics()
prometheus_export = await metrics.export_metrics(format="prometheus")
```

**Tipos de Métricas:**
- **Counter:** Incrementa valores (ej: número de requests)
- **Gauge:** Valor instantáneo (ej: sesiones activas)
- **Histogram:** Distribución de valores (ej: tiempos de respuesta)
- **Timing:** Duración de operaciones (wrapper de histogram)

**Exportación Prometheus:**
```prometheus
# TYPE api_calls counter
api_calls 1000
# TYPE active_sessions gauge
active_sessions 42
# TYPE response_time histogram
response_time_count 100
response_time_sum 120.5
response_time_mean 1.205
response_time_p95 2.5
```

---

### 3. DistributedTracer (`tracer.py`)

**Propósito:** Tracing distribuido para debugging y observabilidad.

**Características:**
- ✅ Traces y spans
- ✅ Spans anidados (parent-child)
- ✅ Tags y logs en spans
- ✅ Exportación a JSON y Jaeger
- ✅ Context managers para spans

**Uso:**
```python
from luminoracore_sdk.monitoring import DistributedTracer

# Crear tracer
tracer = DistributedTracer(service_name="luminoracore")

# Iniciar trace
trace_id = tracer.start_trace("api_request")

# Crear span
span_id = tracer.start_span(
    operation_name="call_provider",
    trace_id=trace_id,
    tags={"provider": "openai", "model": "gpt-3.5-turbo"}
)

# Agregar tags y logs
tracer.add_span_tag(span_id, "status", "success")
tracer.add_span_log(span_id, "Request sent", {"message_count": 3})

# Finalizar span
tracer.finish_span(span_id)

# Finalizar trace
tracer.finish_trace(trace_id)

# Obtener trace
trace = tracer.get_trace(trace_id)
print(trace.to_dict())

# Exportar
jaeger_export = tracer.export_trace(trace_id, format="jaeger")
```

**Context Manager:**
```python
from luminoracore_sdk.monitoring import trace_span

# Usar context manager
async with trace_span(tracer, "operation_name", trace_id, tags={"key": "value"}):
    # Tu código aquí
    await do_something()
    # Span se finaliza automáticamente
```

**Estructura de Trace:**
```json
{
  "trace_id": "trace_123",
  "service_name": "luminoracore",
  "start_time": "2025-11-21T10:00:00",
  "end_time": "2025-11-21T10:00:05",
  "duration": 5.0,
  "span_count": 3,
  "spans": [
    {
      "trace_id": "trace_123",
      "span_id": "span_1",
      "operation_name": "api_request",
      "start_time": "2025-11-21T10:00:00",
      "end_time": "2025-11-21T10:00:05",
      "duration": 5.0,
      "tags": {"provider": "openai"},
      "logs": [...],
      "child_spans": [...]
    }
  ]
}
```

---

## 🔧 Integración con SDK

### Logger en Client

```python
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.monitoring import LuminoraLogger

# Crear logger personalizado
logger = LuminoraLogger(
    name="luminoracore_client",
    format="json",
    log_file="client.log"
)

# El client usa logging estándar de Python
# Los logs se capturan automáticamente
```

### Metrics en Client

```python
from luminoracore_sdk.monitoring import MetricsCollector

metrics = MetricsCollector()

# Registrar métricas durante operaciones
await metrics.increment_counter("sessions_created")
await metrics.record_timing("session_creation", duration=0.5)
```

### Tracing en Client

```python
from luminoracore_sdk.monitoring import DistributedTracer, trace_span

tracer = DistributedTracer()

# Envolver operaciones con tracing
trace_id = tracer.start_trace("create_session")
async with trace_span(tracer, "load_personality", trace_id):
    await client.load_personality("assistant", personality_data)
tracer.finish_trace(trace_id)
```

---

## 📊 Ejemplo Completo

```python
import asyncio
from luminoracore_sdk import LuminoraCoreClient
from luminoracore_sdk.monitoring import (
    LuminoraLogger,
    MetricsCollector,
    DistributedTracer,
    trace_span
)

async def main():
    # Inicializar monitoring
    logger = LuminoraLogger(format="json", log_file="app.log")
    metrics = MetricsCollector()
    tracer = DistributedTracer()
    
    # Iniciar trace
    trace_id = tracer.start_trace("main_operation")
    
    try:
        # Crear client
        client = LuminoraCoreClient()
        await client.initialize()
        
        logger.info("Client initialized", trace_id=trace_id)
        await metrics.increment_counter("client_initializations")
        
        # Operación con tracing
        async with trace_span(tracer, "create_session", trace_id):
            session_id = await client.create_session(...)
            await metrics.increment_counter("sessions_created")
            logger.log_session_event(session_id, "created", "Session created")
        
        # Obtener métricas
        all_metrics = await metrics.get_all_metrics()
        logger.log_metrics("sessions_created", all_metrics["counters"]["sessions_created"], "counter")
        
    except Exception as e:
        logger.error("Operation failed", exception=e, trace_id=trace_id)
        await metrics.increment_counter("errors", tags={"type": type(e).__name__})
    finally:
        tracer.finish_trace(trace_id)
        await client.cleanup()

asyncio.run(main())
```

---

## 🎯 Casos de Uso

### 1. Debugging de Sesiones

```python
logger.log_session_event(
    session_id="session_123",
    event_type="message_sent",
    message="User message processed",
    message_length=50,
    provider="openai"
)
```

### 2. Monitoreo de Performance

```python
# Medir tiempo de respuesta
start_time = time.time()
response = await client.send_message(session_id, "Hello")
duration = time.time() - start_time

await metrics.record_timing("message_response_time", duration)
```

### 3. Análisis de Errores

```python
try:
    await client.send_message(session_id, "Hello")
except Exception as e:
    logger.log_error(
        error_type=type(e).__name__,
        message=str(e),
        exception=e,
        session_id=session_id
    )
    await metrics.increment_counter("errors", tags={"type": type(e).__name__})
```

### 4. Tracing de Operaciones Complejas

```python
trace_id = tracer.start_trace("blend_personalities")
async with trace_span(tracer, "load_personalities", trace_id):
    p1 = await client.load_personality("personality1")
    p2 = await client.load_personality("personality2")

async with trace_span(tracer, "blend", trace_id):
    blended = await client.blend_personalities([p1, p2], [0.5, 0.5])

tracer.finish_trace(trace_id)
```

---

## 🔍 Exportación y Análisis

### Exportar Métricas a Prometheus

```python
prometheus_data = await metrics.export_metrics(format="prometheus")
# Guardar en archivo o enviar a Prometheus server
```

### Exportar Traces a Jaeger

```python
jaeger_data = tracer.export_trace(trace_id, format="jaeger")
# Enviar a Jaeger collector
```

### Análisis de Histogramas

```python
stats = await metrics.get_histogram_stats("response_time")
print(f"Mean: {stats['mean']:.2f}s")
print(f"P95: {stats['p95']:.2f}s")
print(f"P99: {stats['p99']:.2f}s")
```

---

## 🐛 Troubleshooting

### Logs no aparecen

**Solución:** Verifica el nivel de logging:
```python
logger = LuminoraLogger(level="DEBUG")  # Cambiar a DEBUG
```

### Métricas no se actualizan

**Solución:** Asegúrate de usar `await`:
```python
# ✅ Correcto
await metrics.increment_counter("counter")

# ❌ Incorrecto
metrics.increment_counter("counter")
```

### Traces no se exportan

**Solución:** Verifica que el trace esté finalizado:
```python
tracer.finish_trace(trace_id)  # Finalizar antes de exportar
export = tracer.export_trace(trace_id)
```

---

## 📚 Más Información

- **Helpers:** `../utils/helpers.py` (sanitize_api_key, generate_session_id)
- **Client Integration:** `../client.py`
- **API Reference:** `../../docs/api_reference.md`

---

**Última Actualización:** 2025-11-21  
**Versión SDK:** 1.2.0  
**Estado:** ✅ Módulo completo y funcionando

