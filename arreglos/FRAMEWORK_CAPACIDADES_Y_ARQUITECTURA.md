# LuminoraCore v1.1 – Capacidades y Arquitectura (Explicado en lenguaje claro)

Este documento explica, de forma sencilla y sin código, qué hace el framework LuminoraCore v1.1, qué capacidades ofrece y cómo está construido por dentro (su arquitectura). Está pensado para que cualquier persona—técnica o de negocio—pueda entenderlo.


## 1) ¿Qué es LuminoraCore?
LuminoraCore es un framework para crear experiencias conversacionales con IA que recuerdan, aprenden y se adaptan a las personas a lo largo del tiempo. No es solo “un chat”: integra memoria, evolución de la personalidad de la IA, análisis de sentimientos, y persistencia de la información, de modo que las interacciones se hacen más útiles, personalizadas y coherentes con el tiempo.


## 2) ¿Qué puede hacer? (Capacidades principales)

### 2.1 Memoria Conversacional (recuerda y usa el contexto)
- LuminoraCore guarda los turnos de conversación (lo que dice la persona y lo que responde la IA) para que, al continuar la sesión, tenga presente lo hablado.
- Extrae “hechos” relevantes del usuario (por ejemplo, su nombre, preferencias, ciudad) y los guarda para futuras conversaciones.
- Utiliza esos recuerdos para responder de forma más personalizada y consistente, evitando repetir preguntas o ignorar información ya conocida.

### 2.2 Afinidad y Relación (cómo evoluciona el vínculo)
- El sistema calcula y actualiza un nivel de “afinidad” con el usuario, según cómo va la interacción.
- A mayor afinidad, el estilo de respuesta puede volverse más cercano o eficiente, manteniendo siempre el tono y límites adecuados.
- Esto permite ajustar la experiencia a la historia compartida y a la calidad del diálogo.

### 2.3 Personalidades (y Evolución de la Personalidad)
- Se definen “personalidades” de IA (por ejemplo, una psicóloga empática, un asesor técnico, un tutor) con rasgos, tono y reglas de comportamiento.
- La personalidad puede evolucionar con el tiempo según el tipo de interacción que se tenga: más directa, más empática, más formal, etc.
- Es posible combinar varias personalidades para crear estilos híbridos (por ejemplo, 60% técnica, 40% empática).

### 2.4 Análisis de Sentimientos y Emociones
- El sistema analiza el sentimiento y las emociones presentes en la conversación (positivo, negativo, neutral y emociones como alegría, preocupación, frustración…).
- Esto ayuda a adaptar la respuesta (por ejemplo, usar un tono más empático si detecta frustración) y a medir la experiencia del usuario en el tiempo.

### 2.5 Persistencia y Exportación
- Toda la información importante (conversaciones, hechos recordados, análisis, evolución) se guarda de forma segura, habitualmente en una base de datos (por ejemplo, DynamoDB en la nube).
- Se pueden exportar sesiones completas para auditorías, resúmenes, soporte o análisis externo.
- Se pueden crear “instantáneas” (snapshots) de una sesión en momentos clave para conservar su estado.

### 2.6 Proveedores de IA (DeepSeek, OpenAI, etc.)
- LuminoraCore puede conectarse con distintos proveedores de modelos de lenguaje (DeepSeek, OpenAI, Anthropic, Mistral, entre otros).
- Permite cambiar de proveedor o modelo con una configuración, sin reescribir toda la aplicación.


## 3) ¿Cómo se usa? (Experiencia típica)
1) El usuario inicia una sesión y envía un mensaje.
2) LuminoraCore recupera el historial y los hechos relevantes del usuario.
3) Construye un “contexto” para la IA (quién es el usuario, qué se dijo antes, qué personalidad responde, cuál es la relación actual, etc.).
4) Llama al modelo de IA elegido para generar la respuesta.
5) Extrae y guarda nuevos hechos del diálogo, si los hay.
6) Ajusta la afinidad según cómo fue la interacción.
7) Devuelve al cliente una respuesta rica en contexto y datos de utilidad (p. ej., si usó memoria, cuántos hechos tiene, cambios de afinidad).

En siguientes turnos, la IA responde teniendo en cuenta todo lo anterior, creando continuidad y coherencia.


## 4) ¿Cómo está construido por dentro? (Arquitectura)
LuminoraCore está organizado en componentes especializados. A grandes rasgos:

### 4.1 Capa de Sesiones y Conversaciones
- Gestiona las sesiones activas y el historial de mensajes.
- Se encarga de preparar los mensajes que se enviarán al proveedor de IA, según la personalidad y el contexto.

### 4.2 Capa de Memoria
- Guarda “hechos” sobre el usuario y la conversación (nombre, preferencias, datos relevantes).
- Proporciona métodos para guardar, buscar y recuperar información de forma estructurada.

### 4.3 Capa de Personalidades
- Define cómo “actúa” la IA: tono, estilo, reglas, ejemplos.
- Permite mezclar personalidades y hacerlas evolucionar según las interacciones.

### 4.4 Capa de Análisis (Sentimientos y Emociones)
- Analiza lo que se dice para detectar sentimientos y emociones.
- Puede usar tanto reglas simples como el poder del modelo de IA para un análisis más fino.

### 4.5 Capa de Proveedores de IA
- Abstrae las llamadas a los distintos servicios (DeepSeek, OpenAI…), de modo que la lógica del producto no depende de un proveedor específico.
- Gestiona parámetros como el modelo, temperaturas, límites, etc.

### 4.6 Capa de Almacenamiento
- Guarda de forma persistente sesiones, hechos, análisis, evoluciones y snapshots.
- Soporta distintos backends (por ejemplo, DynamoDB para producción y SQLite/JSON para desarrollo).

### 4.7 API Backend (opcional)
- Expone endpoints HTTP para que un frontend o sistema externo use las capacidades del framework (chat con memoria, análisis de sentimientos, evolución, exportación…).
- Se despliega en la nube (por ejemplo, AWS Lambda), y se conecta con la capa de almacenamiento.


## 5) ¿Qué beneficios aporta?
- Respuestas que “recuerdan” y se adaptan: mejor experiencia para el usuario.
- Personalización real: la IA no trata todas las conversaciones igual, respeta preferencias e historial.
- Escalabilidad: se pueden cambiar proveedores de IA y almacenamiento sin rehacer el sistema.
- Auditoría y cumplimiento: exportar, revisar y explicar interacciones es sencillo.


## 6) Casos de uso típicos
- Asistentes que acompañan a un usuario a lo largo de semanas o meses (salud, educación, soporte técnico).
- Atención al cliente que aprende preferencias y resuelve más rápido con el tiempo.
- Plataformas de formación que recuerdan el progreso y estilo de aprendizaje.


## 7) Recomendaciones prácticas para sacarle partido
- Mantener identificadores de sesión estables: así la IA puede recuperar el historial y los hechos.
- Definir bien la personalidad: cuanto más clara, más consistente será la respuesta.
- Activar y revisar análisis de sentimientos: ayuda a detectar puntos de fricción.
- Exportar y estudiar conversaciones reales: permite mejorar prompts, personalidades y flujos.
- Monitorizar latencias y uso de tokens: optimiza costes y tiempos de respuesta.


## 8) Limitaciones razonables
- Latencia y costes dependen del proveedor y del tamaño del contexto.
- No es una base de conocimiento global: guarda lo relevante de cada usuario/sesión, no “todo sobre todo”.
- La evolución de personalidad debe ser gradual y gobernada para no perder consistencia.


## 9) Conclusión
LuminoraCore v1.1 permite construir experiencias conversacionales inteligentes que no se quedan en respuestas aisladas. Recuerda, aprende y se adapta, combinando memoria, análisis, evolución de personalidad y persistencia. Su arquitectura modular y sus integraciones con distintos proveedores facilitan operar en producción con control, transparencia y capacidad de mejora continua.
