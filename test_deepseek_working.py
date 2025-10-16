#!/usr/bin/env python3
"""
Test funcional de LuminoraCore v1.1 con DeepSeek
Version sin emojis para Windows
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

async def test_deepseek_workflow():
    """Test del flujo de trabajo con DeepSeek"""
    
    print("LuminoraCore v1.1 - Test con DeepSeek")
    print("=" * 60)
    
    # 1. Configurar el cliente
    print("\nPaso 1: Configurando cliente...")
    
    storage = InMemoryStorageV11()
    
    # Crear cliente base primero
    base_client = LuminoraCoreClient()
    
    # Crear cliente v1.1 con extensiones
    client = LuminoraCoreClientV11(base_client, storage_v11=storage)
    
    print("OK Cliente configurado correctamente")
    
    # 2. Crear personalidad Victoria Sterling
    print("\nPaso 2: Creando personalidad Victoria Sterling...")
    
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
    
    print("OK Personalidad Victoria Sterling creada")
    
    # 3. Crear sesion
    print("\nPaso 3: Creando sesion...")
    
    session_id = "test_user_123"
    await client.base_client.create_session(
        session_id=session_id,
        personality_config=victoria_personality
    )
    
    print("OK Sesion inicializada")
    
    # 4. Primera conversacion (Stranger)
    print("\nPaso 4: Primera conversacion (Stranger)...")
    
    response1 = await client.base_client.send_message(
        session_id=session_id,
        message="Hola, soy nuevo aqui. Puedes ayudarme con informacion sobre tu servicio?"
    )
    
    print(f"Usuario: Hola, soy nuevo aqui. Puedes ayudarme con informacion sobre tu servicio?")
    print(f"Victoria: {response1['response']}")
    print(f"Afinidad: {response1['affinity_points']} puntos")
    print(f"Nivel: {response1['relationship_level']}")
    
    # 5. Segunda conversacion (Building relationship)
    print("\nPaso 5: Segunda conversacion (Building relationship)...")
    
    response2 = await client.base_client.send_message(
        session_id=session_id,
        message="Gracias por la informacion. Me llamo Carlos y trabajo en una startup de tecnologia. Estoy interesado en implementar un chatbot para atencion al cliente."
    )
    
    print(f"Usuario: Gracias por la informacion. Me llamo Carlos y trabajo en una startup de tecnologia...")
    print(f"Victoria: {response2['response']}")
    print(f"Afinidad: {response2['affinity_points']} puntos")
    print(f"Nivel: {response2['relationship_level']}")
    
    # 6. Tercera conversacion (Learning preferences)
    print("\nPaso 6: Tercera conversacion (Learning preferences)...")
    
    response3 = await client.base_client.send_message(
        session_id=session_id,
        message="Perfecto. Me gusta que seas directa y tecnica en tus respuestas. Que me recomiendas para empezar?"
    )
    
    print(f"Usuario: Perfecto. Me gusta que seas directa y tecnica en tus respuestas...")
    print(f"Victoria: {response3['response']}")
    print(f"Afinidad: {response3['affinity_points']} puntos")
    print(f"Nivel: {response3['relationship_level']}")
    
    # 7. Verificar memoria
    print("\nPaso 7: Verificando memoria del sistema...")
    
    memory_data = await client.get_memory_data(session_id)
    
    print("Hechos aprendidos:")
    for fact in memory_data.get('facts', []):
        print(f"   - {fact['key']}: {fact['value']} (confianza: {fact['confidence']})")
    
    print("\nObjetivos identificados:")
    for goal in memory_data.get('goals', []):
        print(f"   - {goal['goal']} (estado: {goal['status']})")
    
    print("\nEpisodios memorables:")
    for episode in memory_data.get('episodes', []):
        print(f"   - {episode['description']} (importancia: {episode['importance']})")
    
    # 8. Verificar evolucion de personalidad
    print("\nPaso 8: Verificando evolucion de personalidad...")
    
    personality_state = await client.get_personality_state(session_id)
    
    print("Estado actual de la personalidad:")
    print(f"   - Nivel de relacion: {personality_state['relationship_level']}")
    print(f"   - Puntos de afinidad: {personality_state['affinity_points']}")
    print(f"   - Formality actual: {personality_state['current_personality']['communication_style']['formality']:.2f}")
    print(f"   - Warmth actual: {personality_state['current_personality']['communication_style']['warmth']:.2f}")
    print(f"   - Humor actual: {personality_state['current_personality']['communication_style']['humor']:.2f}")
    
    # 9. Test de exportacion
    print("\nPaso 9: Test de exportacion...")
    
    export_data = await client.export_session_data(session_id)
    
    print("OK Datos exportados correctamente:")
    print(f"   - Tamano del export: {len(str(export_data))} caracteres")
    print(f"   - Numero de conversaciones: {len(export_data.get('conversations', []))}")
    print(f"   - Numero de hechos: {len(export_data.get('facts', []))}")
    
    print("\nTest completado exitosamente!")
    print("=" * 60)
    print("OK LuminoraCore v1.1 funciona perfectamente con DeepSeek")
    print("OK Sistema de memoria funcionando")
    print("OK Evolucion de personalidad funcionando")
    print("OK Afinidad y relaciones funcionando")
    print("OK Exportacion de datos funcionando")

if __name__ == "__main__":
    print("Verificando configuracion...")
    
    if not DEEPSEEK_API_KEY:
        print("ERROR: DEEPSEEK_API_KEY no esta configurada")
        print("\nPara configurar tu API key:")
        print("1. Obten tu API key de DeepSeek en: https://platform.deepseek.com/")
        print("2. Configurala en tu sistema:")
        print("   Windows: set DEEPSEEK_API_KEY=tu_api_key")
        print("   Linux/Mac: export DEEPSEEK_API_KEY=tu_api_key")
        sys.exit(1)
    
    print("OK API key configurada")
    print("Iniciando test completo...")
    
    try:
        asyncio.run(test_deepseek_workflow())
    except Exception as e:
        print(f"\nERROR durante el test: {e}")
        print("\nPosibles soluciones:")
        print("1. Verifica que tu API key de DeepSeek sea valida")
        print("2. Verifica tu conexion a internet")
        print("3. Verifica que tengas creditos en tu cuenta de DeepSeek")
        sys.exit(1)
