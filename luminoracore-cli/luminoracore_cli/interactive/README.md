# LuminoraCore CLI Interactive Module

Módulo para interfaces interactivas del CLI.

---

## ¿Qué es?

El módulo `interactive` proporciona interfaces interactivas para trabajar con personalidades de LuminoraCore desde la terminal.

---

## Componentes

### `chat.py` - Chat Interactivo

**Propósito:** Chat interactivo en terminal para probar personalidades con LLM providers.

**Clase Principal:** `InteractiveChat`

**Funcionalidades:**
- ✅ Chat en tiempo real con personalidades
- ✅ Soporte para múltiples providers (OpenAI, Anthropic, Google, etc.)
- ✅ Historial de conversación
- ✅ Comandos interactivos (help, clear, history, etc.)
- ✅ Renderizado con Rich (markdown, colores)

**Uso:**
```python
from luminoracore_cli.interactive import start_interactive_chat

# Iniciar chat interactivo
start_interactive_chat(
    personality_path="personalities/my_personality.json",
    provider="openai"
)
```

**Comandos Disponibles:**
- `help` - Mostrar ayuda
- `clear` - Limpiar historial
- `history` - Mostrar historial reciente
- `personality` - Mostrar información de personalidad
- `settings` - Mostrar configuración actual
- `provider <name>` - Cambiar provider
- `exit/quit/bye` - Salir del chat

---

## ¿Cuándo se usa?

### Casos de Uso

1. **Testing Interactivo:**
   - Probar personalidades antes de usar en producción
   - Ver cómo responde la personalidad en tiempo real
   - Ajustar personalidad basado en respuestas

2. **Desarrollo:**
   - Desarrollar nuevas personalidades
   - Iterar rápidamente sobre cambios
   - Validar comportamiento

3. **Demostraciones:**
   - Mostrar capacidades de personalidades
   - Pruebas rápidas con usuarios
   - Prototipado

---

## Integración con Comandos CLI

El módulo `interactive` se usa desde comandos CLI:

```bash
# Comando test con modo interactivo
luminoracore test my_personality --interactive

# Esto internamente usa:
# from luminoracore_cli.interactive import start_interactive_chat
```

---

## Dependencias

- `questionary` - Input interactivo en terminal
- `rich` - Renderizado con colores y markdown
- `PersonalityCompiler` - Compilar personalidades
- `PersonalityTester` - Probar con LLM providers

---

## Correcciones Realizadas (v1.2.0)

### 1. `__init__.py` - Imports Corregidos

**Problema:** Importaba módulos que no existen (`wizard`, `prompts`, `tui`)

**Solución:** Solo exporta lo que existe:
```python
from .chat import InteractiveChat, start_interactive_chat

__all__ = [
    "InteractiveChat",
    "start_interactive_chat"
]
```

### 2. `chat.py` - Métodos Corregidos

**Problema:** Usaba métodos que no existen:
- `compiler.compile_to_openai()` → No existe
- `tester.test_openai()` → No existe

**Solución:** Usa métodos correctos:
- `compiler.compile()` → Método correcto
- `tester.test()` → Método correcto (async)

**Cambios:**
- `_get_system_message()` ahora usa `compiler.compile()`
- `_get_assistant_response()` ahora usa `tester.test()` con manejo async
- Agregado `_get_mock_response()` como fallback

---

## Estado Actual

| Componente | Estado | Notas |
|------------|--------|-------|
| `chat.py` | ✅ Corregido | Métodos actualizados |
| `__init__.py` | ✅ Corregido | Imports limpiados |
| Imports | ✅ Correctos | Sin errores |
| Sintaxis | ✅ Correcta | Compila sin errores |

---

## Ejemplo de Uso Completo

```python
from luminoracore_cli.interactive import InteractiveChat
from rich.console import Console

# Crear instancia
console = Console()
chat = InteractiveChat(
    personality_path="personalities/assistant.json",
    provider="openai",
    console=console
)

# Iniciar chat
chat.start_chat()
```

**Flujo:**
1. Carga personalidad desde archivo
2. Compila personalidad a system prompt
3. Inicia loop interactivo
4. Usuario escribe mensajes
5. Sistema obtiene respuesta del LLM
6. Muestra respuesta formateada
7. Repite hasta que usuario salga

---

## Notas Importantes

1. **Async/Sync:** `PersonalityTester.test()` es async, pero `InteractiveChat.start_chat()` es sync. Se maneja con `asyncio.run_until_complete()` o fallback a mock.

2. **API Keys:** Requiere API keys configuradas para providers reales. Sin keys, usa respuestas mock.

3. **Providers Soportados:**
   - OpenAI
   - Anthropic
   - Google
   - Cohere
   - HuggingFace

4. **Historial:** Mantiene último historial (configurable, default 50 mensajes).

---

## Mejoras Futuras (Opcional)

1. **Async Nativo:** Convertir `start_chat()` a async para mejor manejo
2. **Múltiples Personalidades:** Cambiar entre personalidades en runtime
3. **Exportar Conversación:** Guardar historial a archivo
4. **Streaming:** Respuestas en tiempo real (streaming)

---

**Última Actualización:** 2025-11-21  
**Versión:** 1.2.0  
**Estado:** ✅ Corregido y funcionando

