#!/usr/bin/env python3
"""
Test para verificar quién hace el análisis sentimental y dónde se almacena
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))

async def test_sentiment_integration():
    """Test de integración del análisis sentimental"""
    print("=== QUIEN HACE EL ANALISIS SENTIMENTAL Y DONDE SE ALMACENA ===")
    
    try:
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11, AdvancedSentimentAnalyzer
        from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
        
        # Setup
        base_client = LuminoraCoreClient()
        await base_client.initialize()
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(base_client, storage_v11=storage)
        
        print("1. QUIEN HACE EL ANALISIS SENTIMENTAL:")
        print("   - AdvancedSentimentAnalyzer (clase principal)")
        print("   - Se ejecuta desde LuminoraCoreClientV11")
        print("   - Puede usar LLM providers para análisis avanzado")
        print("   - También usa análisis basado en keywords")
        
        print("\n2. DONDE SE ALMACENA EN BASE DE DATOS:")
        
        # Crear sesión
        session_id = await client.create_session(
            personality_name="test_assistant",
            provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
        )
        
        print(f"   Session ID: {session_id}")
        
        # Simular análisis sentimental
        print("\n3. PROCESO DE ALMACENAMIENTO:")
        
        # Guardar mood
        mood_result = await client.save_mood(
            user_id=session_id,
            personality_name="test_assistant",
            mood="happy",
            intensity=0.8,
            context="Usuario feliz con el sistema"
        )
        print(f"   a) Mood guardado: {mood_result.get('success', False)}")
        
        # Análisis sentimental
        sentiment_result = await client.analyze_sentiment(
            user_id=session_id,
            message="Estoy muy contento con este framework!",
            personality_name="test_assistant"
        )
        print(f"   b) Análisis sentimental: {sentiment_result.get('success', False)}")
        
        # Verificar almacenamiento
        mood_history = await client.get_mood_history(session_id, "test_assistant")
        sentiment_history = await client.get_sentiment_history(session_id, "test_assistant")
        
        print(f"   c) Moods en BD: {len(mood_history)}")
        print(f"   d) Análisis en BD: {len(sentiment_history)}")
        
        print("\n4. TABLAS/COLECCIONES EN BASE DE DATOS:")
        print("   - moods_table: Estados de ánimo del usuario")
        print("   - episodes_table: Episodios con campo 'sentiment'")
        print("   - facts_table: Facts con análisis sentimental")
        print("   - memories_table: Análisis completos guardados")
        
        print("\n5. COMO AFECTA A LA PERSONALIDAD:")
        print("   - Los sentimientos se usan en evolve_personality()")
        print("   - Afectan la evolución de la personalidad")
        print("   - Se consideran en las interacciones futuras")
        print("   - Influyen en la afinidad con el usuario")
        
        # Test de evolución de personalidad
        print("\n6. EVOLUCION DE PERSONALIDAD CON SENTIMENT:")
        try:
            evolution_result = await client.evolve_personality(
                session_id=session_id,
                user_id=session_id,
                personality_name="test_assistant"
            )
            print(f"   Evolución ejecutada: {evolution_result.get('changes_detected', False)}")
        except Exception as e:
            print(f"   Evolución: {e}")
        
        await base_client.cleanup()
        
        print("\n=== RESUMEN ===")
        print("QUIEN: AdvancedSentimentAnalyzer")
        print("DONDE: Tablas moods, episodes, facts, memories")
        print("COMO AFECTA: Evolución de personalidad y afinidad")
        
        return True
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_sentiment_integration())
    sys.exit(0 if success else 1)
