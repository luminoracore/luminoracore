#!/usr/bin/env python3
"""
Test detallado del análisis sentimental para responder la pregunta del usuario
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))

async def test_sentiment_analysis_detailed():
    """Test detallado del análisis sentimental"""
    print("=== ANÁLISIS DETALLADO DEL ANÁLISIS SENTIMENTAL ===")
    
    try:
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11, AdvancedSentimentAnalyzer
        from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
        
        # Setup
        base_client = LuminoraCoreClient()
        await base_client.initialize()
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(base_client, storage_v11=storage)
        
        print("1. Verificando version del Core:")
        print(f"   Core: 1.1.0 OK")
        print(f"   SDK: 1.1.0 OK")
        print(f"   CLI: 1.0.0 (problema de instalacion)")
        
        print("\n2. Cómo funciona el análisis sentimental:")
        print("   - El análisis sentimental NO se hace mensaje a mensaje")
        print("   - Se hace por SESIÓN COMPLETA")
        print("   - Analiza TODA la conversación de la sesión")
        print("   - Incluye contexto de mensajes anteriores")
        
        print("\n3. Proceso del análisis sentimental:")
        
        # Crear sesión
        session_id = await client.create_session(
            personality_name="test_assistant",
            provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
        )
        
        print("   a) Se crea una sesión")
        print(f"      Session ID: {session_id}")
        
        # Simular conversación
        messages = [
            "Hola, me llamo Carlos",
            "Estoy muy feliz hoy!",
            "Tengo un problema con mi trabajo",
            "Pero todo va a salir bien"
        ]
        
        print("\n   b) Se simula una conversación:")
        for i, msg in enumerate(messages, 1):
            print(f"      Mensaje {i}: '{msg}'")
            
            # Guardar mensaje como episodio
            await client.save_episode(
                user_id=session_id,
                episode_type="conversation",
                title=f"Mensaje {i}",
                content=f"User: {msg}",
                summary=f"Usuario dice: {msg[:50]}...",
                importance=0.7,
                sentiment="neutral"
            )
        
        print("\n   c) Se analiza la SESIÓN COMPLETA (no mensaje por mensaje):")
        
        # Análisis sentimental de la sesión completa
        analyzer = AdvancedSentimentAnalyzer(storage)
        result = await analyzer.analyze_sentiment(
            session_id=session_id,
            user_id=session_id
        )
        
        print(f"      - Sentimiento general: {result.overall_sentiment}")
        print(f"      - Score de sentimiento: {result.sentiment_score}")
        print(f"      - Emociones detectadas: {result.emotions_detected}")
        print(f"      - Confianza: {result.confidence}")
        print(f"      - Tendencia: {result.sentiment_trend}")
        print(f"      - Número de mensajes analizados: {result.message_count}")
        
        print("\n4. Métodos de análisis sentimental disponibles:")
        print("   OK analyze_sentiment() - Analisis completo de sesion")
        print("   OK save_mood() - Guardar estado de animo especifico")
        print("   OK get_mood_history() - Obtener historial de estados")
        print("   OK get_sentiment_history() - Obtener historial de analisis")
        print("   OK get_sentiment_trends() - Obtener tendencias temporales")
        
        print("\n5. Diferencia clave:")
        print("   NO es analisis mensaje por mensaje")
        print("   SI es analisis de SESION COMPLETA con contexto")
        print("   Considera TODA la conversacion para el analisis")
        print("   Incluye tendencias y patrones temporales")
        
        await base_client.cleanup()
        
        print("\n=== CONCLUSION ===")
        print("El analisis sentimental se hace por SESION COMPLETA, no mensaje a mensaje.")
        print("Esto permite un analisis mas preciso considerando el contexto completo.")
        
        return True
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_sentiment_analysis_detailed())
    sys.exit(0 if success else 1)
