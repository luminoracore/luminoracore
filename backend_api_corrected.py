# Backend API - LuminoraCore Integration (CORRECTED VERSION)

import json
import logging
import os
from datetime import datetime
from src.common.async_wrapper import lambda_async_handler
from src.common.logger import get_logger
from src.auth.jwt_authorizer import get_user_from_event

# LuminoraCore v1.1 imports
from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
from luminoracore_sdk.session import FlexibleDynamoDBStorageV11
from luminoracore_sdk.types.provider import ProviderConfig

logger = get_logger(__name__)

# Cache del cliente para reutilizar entre invocaciones (mejora de rendimiento)
_client_cache = None
_cache_provider_config = None

async def get_client_v11(provider_config=None):
    """
    Inicializa y retorna el cliente LuminoraCoreClientV11
    
    VERSIÓN CORREGIDA - Maneja correctamente la configuración del provider
    """
    global _client_cache, _cache_provider_config
    
    # Reutilizar cliente si ya existe Y tiene el mismo provider config
    if _client_cache is not None and _cache_provider_config == provider_config:
        return _client_cache
    
    try:
        # 1. Crear storage con configuración desde variables de entorno del serverless.yml
        dynamodb_storage = FlexibleDynamoDBStorageV11(
            table_name=os.getenv("DYNAMODB_TABLE"),
            region_name=os.getenv("DYNAMODB_REGION")
        )
        
        # 2. Crear e inicializar base client
        base_client = LuminoraCoreClient()
        await base_client.initialize()
        
        # 3. ✅ CONFIGURAR PROVIDER EN BASE_CLIENT (CORRECCIÓN CRÍTICA)
        if provider_config:
            from luminoracore_sdk.providers.factory import ProviderFactory
            provider = ProviderFactory.create_provider(provider_config)
            base_client._providers[provider_config.name] = provider
            logger.info(f"✅ Provider {provider_config.name} configurado en base_client")
        
        # 4. Crear client v11
        client_v11 = LuminoraCoreClientV11(
            base_client=base_client,
            storage_v11=dynamodb_storage
        )
        
        logger.info("✅ LuminoraCoreClientV11 initialized successfully")
        
        # Cachear para futuras invocaciones
        _client_cache = client_v11
        _cache_provider_config = provider_config
        return client_v11
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize client: {e}", exc_info=True)
        raise

@lambda_async_handler
async def handler(event, context):
    """
    Handler principal para chat con memoria contextual
    
    Request body:
    {
        "session_id": "unique-session-id",
        "message": "User message",
        "personality_name": "personality-name" (opcional, default: "Dr. Luna")
    }
    
    Response:
    {
        "response": "AI response",
        "session_id": "session-id",
        "user_id": "user-id",
        "personality_name": "personality-name",
        "memory_facts_count": 5,
        "new_facts_count": 2,
        "new_facts": [...],
        "context_used": true,
        "timestamp": "2024-01-01T00:00:00Z"
    }
    """
    try:
        logger.info("📨 Chat handler started")
        
        # 1. Parse request body
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event.get('body', {})
        
        # Extraer parámetros
        session_id = body.get('session_id')
        user_message = body.get('message')
        personality_name = body.get('personality_name', 'Dr. Luna')
        
        # 2. Validar parámetros requeridos
        if not session_id:
            logger.warning("❌ Missing session_id parameter")
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'session_id is required',
                    'field': 'session_id'
                })
            }
        
        if not user_message:
            logger.warning("❌ Missing message parameter")
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'message is required',
                    'field': 'message'
                })
            }
        
        logger.info(f"📝 Request parameters: session_id={session_id}, personality={personality_name}")
        
        # 3. Extraer user_id
        # Opción A: Si tienes JWT, extraer user_id del token
        # Opción B: Si no tienes JWT, usar session_id como user_id
        try:
            user = get_user_from_event(event)
            if user:
                # Usuario autenticado - usar ID real del JWT
                user_id = user.get('user_id') or user.get('sub') or session_id
                logger.info(f"👤 Authenticated user: {user_id}")
            else:
                # Usuario anónimo - usar session_id como user_id
                user_id = session_id
                logger.info(f"👤 Anonymous user: {user_id}")
        except Exception as e:
            # Si falla JWT, usar session_id como fallback
            logger.warning(f"⚠️ JWT extraction failed: {e}, using session_id as user_id")
            user_id = session_id
        
        # 4. Configurar provider
        deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        if not deepseek_api_key:
            logger.error("❌ DEEPSEEK_API_KEY not configured")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'AI provider not configured',
                    'details': 'DEEPSEEK_API_KEY environment variable is missing'
                })
            }
        
        provider_config = ProviderConfig(
            name="deepseek",
            api_key=deepseek_api_key,
            model="deepseek-chat"
        )
        
        logger.info("✅ Provider configured successfully")
        
        # 5. Obtener cliente v1.1 CON provider configurado
        try:
            client_v11 = await get_client_v11(provider_config=provider_config)
        except Exception as e:
            logger.error(f"❌ Failed to get client: {e}")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'Failed to initialize AI client',
                    'details': str(e)
                })
            }
        
        # 6. ✅ CORRECCIÓN CRÍTICA: Usar send_message_with_memory con parámetros correctos
        # El método espera: session_id, user_message, user_id, personality_name, provider_config
        logger.info(f"🤖 Sending message to AI: '{user_message[:50]}...'")
        
        try:
            result = await client_v11.send_message_with_memory(
                session_id=session_id,
                user_message=user_message,
                user_id=user_id,  # ✅ CORRECTO: pasar user_id explícitamente
                personality_name=personality_name,
                provider_config=provider_config
            )
        except Exception as e:
            logger.error(f"❌ Framework error: {e}", exc_info=True)
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'AI processing error',
                    'details': str(e)
                })
            }
        
        # 7. Verificar si hay errores en el resultado
        if not result.get("success", True):  # ✅ CORRECCIÓN: verificar success field
            error_msg = result.get("error", "Unknown error")
            logger.error(f"❌ Framework returned error: {error_msg}")
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'AI returned error',
                    'details': error_msg
                })
            }
        
        # 8. Construir respuesta exitosa
        response_data = {
            'response': result.get('response', ''),
            'session_id': session_id,
            'user_id': user_id,
            'personality_name': personality_name,
            'memory_facts_count': result.get('memory_facts_count', 0),
            'new_facts_count': len(result.get('new_facts', [])),
            'new_facts': result.get('new_facts', []),
            'context_used': result.get('context_used', False),
            'timestamp': datetime.utcnow().isoformat()
        }
        
        logger.info(f"✅ Response generated successfully")
        logger.info(f"📊 Stats: {response_data['memory_facts_count']} facts, {response_data['new_facts_count']} new facts")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Ajustar según necesidades CORS
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization'
            },
            'body': json.dumps(response_data)
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON in request: {e}")
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Invalid JSON in request body',
                'details': str(e)
            })
        }
    
    except Exception as e:
        logger.error(f"❌ Unexpected error in handler: {e}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Internal server error',
                'details': str(e)
            })
        }
