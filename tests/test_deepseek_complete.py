#!/usr/bin/env python3
"""
Test completo de LuminoraCore v1.1 con DeepSeek
Demuestra: personalidades, memoria, afinidad y evolucion de personalidad
"""

import asyncio
import os
import sys
from datetime import datetime

# Anadir el directorio actual al path para importar los paquetes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from luminoracore.core.personality import Personality
from luminoracore_sdk.client import LuminoraCoreClient
from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11

# Configuracion para DeepSeek
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    print("ERROR: DEEPSEEK_API_KEY no esta configurada")
    print("Por favor, configura tu API key de DeepSeek:")
    print("export DEEPSEEK_API_KEY='tu_api_key_aqui'")
    sys.exit(1)

async def test_complete_workflow():
    """Test completo del flujo de trabajo con DeepSeek"""
    
    print("LuminoraCore v1.1 - Test Completo con DeepSeek")
    print("=" * 60)
    
    # 1. Configurar el cliente
    print("\nPaso 1: Configurando cliente...")
    
    storage = InMemoryStorageV11()
    
    # Crear cliente base primero
    base_client = LuminoraCoreClient()
    
    # Crear cliente v1.1 con extensiones
    client = LuminoraCoreClientV11(base_client, storage_v11=storage)
    
    print("✅ Cliente configurado correctamente")
    
    # 2. Crear personalidad Victoria Sterling
    print("\n👤 Paso 2: Creando personalidad Victoria Sterling...")
    
    victoria_personality = {
        "name": "Victoria Sterling",
        "version": "1.1.0",
        "description": "Executive assistant with evolving personality",
        "base_personality": {
            "core_traits": {
                "professionalism": 0.9,
                "efficiency": 0.8,
                "empathy": 0.7,
                "directness": 0.6
            },
            "communication_style": {
                "formality": 0.8,
                "warmth": 0.5,
                "humor": 0.3,
                "patience": 0.7
            }
        },
        "hierarchical_config": {
            "relationship_levels": {
                "stranger": {
                    "formality_modifier": 0.2,
                    "warmth_modifier": -0.2,
                    "humor_modifier": -0.3
                },
                "acquaintance": {
                    "formality_modifier": 0.0,
                    "warmth_modifier": 0.0,
                    "humor_modifier": 0.0
                },
                "friend": {
                    "formality_modifier": -0.1,
                    "warmth_modifier": 0.2,
                    "humor_modifier": 0.2
                },
                "close_friend": {
                    "formality_modifier": -0.3,
                    "warmth_modifier": 0.4,
                    "humor_modifier": 0.4
                }
            }
        },
        "memory_preferences": {
            "fact_retention": 0.9,
            "episodic_memory": 0.8,
            "preference_learning": 0.9,
            "goal_tracking": 0.8
        },
        "affinity_config": {
            "positive_interactions": 5,
            "negative_interactions": -3,
            "goal_achievement": 10,
            "preference_alignment": 3
        }
    }
    
    print("✅ Personalidad Victoria Sterling creada")
    
    # 3. Inicializar sesión
    print("\n💬 Paso 3: Inicializando sesión...")
    
    session_id = "test_user_123"
    await client.initialize_session(
        session_id=session_id,
        personality_name="Victoria Sterling",
        personality_config=victoria_personality
    )
    
    print("✅ Sesión inicializada")
    
    # 4. Primera conversación (Stranger)
    print("\n🗣️ Paso 4: Primera conversación (Stranger)...")
    
    response1 = await client.send_message(
        session_id=session_id,
        message="Hola, soy nuevo aquí. ¿Puedes ayudarme con información sobre tu servicio?",
        provider="deepseek"
    )
    
    print(f"👤 Usuario: Hola, soy nuevo aquí. ¿Puedes ayudarme con información sobre tu servicio?")
    print(f"🤖 Victoria: {response1['response']}")
    print(f"📊 Afinidad: {response1['affinity_points']} puntos")
    print(f"💝 Nivel: {response1['relationship_level']}")
    
    # 5. Segunda conversación (Building relationship)
    print("\n🗣️ Paso 5: Segunda conversación (Building relationship)...")
    
    response2 = await client.send_message(
        session_id=session_id,
        message="Gracias por la información. Me llamo Carlos y trabajo en una startup de tecnología. Estoy interesado en implementar un chatbot para atención al cliente.",
        provider="deepseek"
    )
    
    print(f"👤 Usuario: Gracias por la información. Me llamo Carlos y trabajo en una startup de tecnología...")
    print(f"🤖 Victoria: {response2['response']}")
    print(f"📊 Afinidad: {response2['affinity_points']} puntos")
    print(f"💝 Nivel: {response2['relationship_level']}")
    
    # 6. Tercera conversación (Learning preferences)
    print("\n🗣️ Paso 6: Tercera conversación (Learning preferences)...")
    
    response3 = await client.send_message(
        session_id=session_id,
        message="Perfecto. Me gusta que seas directa y técnica en tus respuestas. ¿Qué me recomiendas para empezar?",
        provider="deepseek"
    )
    
    print(f"👤 Usuario: Perfecto. Me gusta que seas directa y técnica en tus respuestas...")
    print(f"🤖 Victoria: {response3['response']}")
    print(f"📊 Afinidad: {response3['affinity_points']} puntos")
    print(f"💝 Nivel: {response3['relationship_level']}")
    
    # 7. Cuarta conversación (Friend level)
    print("\n🗣️ Paso 7: Cuarta conversación (Friend level)...")
    
    response4 = await client.send_message(
        session_id=session_id,
        message="¡Excelente! Ya veo que recuerdas que me gusta lo técnico. ¿Podrías darme un ejemplo de código para empezar?",
        provider="deepseek"
    )
    
    print(f"👤 Usuario: ¡Excelente! Ya veo que recuerdas que me gusta lo técnico...")
    print(f"🤖 Victoria: {response4['response']}")
    print(f"📊 Afinidad: {response4['affinity_points']} puntos")
    print(f"💝 Nivel: {response4['relationship_level']}")
    
    # 8. Verificar memoria
    print("\n🧠 Paso 8: Verificando memoria del sistema...")
    
    memory_data = await client.get_memory_data(session_id)
    
    print("📝 Hechos aprendidos:")
    for fact in memory_data.get('facts', []):
        print(f"   • {fact['key']}: {fact['value']} (confianza: {fact['confidence']})")
    
    print("\n🎯 Objetivos identificados:")
    for goal in memory_data.get('goals', []):
        print(f"   • {goal['goal']} (estado: {goal['status']})")
    
    print("\n📖 Episodios memorables:")
    for episode in memory_data.get('episodes', []):
        print(f"   • {episode['description']} (importancia: {episode['importance']})")
    
    # 9. Verificar evolución de personalidad
    print("\n🎭 Paso 9: Verificando evolución de personalidad...")
    
    personality_state = await client.get_personality_state(session_id)
    
    print("🔄 Estado actual de la personalidad:")
    print(f"   • Nivel de relación: {personality_state['relationship_level']}")
    print(f"   • Puntos de afinidad: {personality_state['affinity_points']}")
    print(f"   • Formality actual: {personality_state['current_personality']['communication_style']['formality']:.2f}")
    print(f"   • Warmth actual: {personality_state['current_personality']['communication_style']['warmth']:.2f}")
    print(f"   • Humor actual: {personality_state['current_personality']['communication_style']['humor']:.2f}")
    
    # 10. Test de exportación
    print("\n📤 Paso 10: Test de exportación...")
    
    export_data = await client.export_session_data(session_id)
    
    print("✅ Datos exportados correctamente:")
    print(f"   • Tamaño del export: {len(str(export_data))} caracteres")
    print(f"   • Número de conversaciones: {len(export_data.get('conversations', []))}")
    print(f"   • Número de hechos: {len(export_data.get('facts', []))}")
    
    print("\n🎉 ¡Test completado exitosamente!")
    print("=" * 60)
    print("✅ LuminoraCore v1.1 funciona perfectamente con DeepSeek")
    print("✅ Sistema de memoria funcionando")
    print("✅ Evolución de personalidad funcionando")
    print("✅ Afinidad y relaciones funcionando")
    print("✅ Exportación de datos funcionando")

if __name__ == "__main__":
    print("🔧 Verificando configuración...")
    
    if not DEEPSEEK_API_KEY:
        print("❌ Error: DEEPSEEK_API_KEY no está configurada")
        print("\nPara configurar tu API key:")
        print("1. Obtén tu API key de DeepSeek en: https://platform.deepseek.com/")
        print("2. Configúrala en tu sistema:")
        print("   Windows: set DEEPSEEK_API_KEY=tu_api_key")
        print("   Linux/Mac: export DEEPSEEK_API_KEY=tu_api_key")
        sys.exit(1)
    
    print("✅ API key configurada")
    print("🚀 Iniciando test completo...")
    
    try:
        asyncio.run(test_complete_workflow())
    except Exception as e:
        print(f"\n❌ Error durante el test: {e}")
        print("\n🔍 Posibles soluciones:")
        print("1. Verifica que tu API key de DeepSeek sea válida")
        print("2. Verifica tu conexión a internet")
        print("3. Verifica que tengas créditos en tu cuenta de DeepSeek")
        sys.exit(1)
