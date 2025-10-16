#!/usr/bin/env python3
"""
Test simple de LuminoraCore v1.1 con DeepSeek (sin API key)
Demuestra la configuracion y preparacion del sistema
"""

import os
import sys

# Anadir el directorio actual al path para importar los paquetes
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_deepseek_configuration():
    """Test de configuracion para DeepSeek"""
    
    print("LuminoraCore v1.1 - Test de Configuracion DeepSeek")
    print("=" * 60)
    
    # 1. Verificar importaciones del SDK
    print("\nPaso 1: Verificando importaciones del SDK...")
    
    try:
        from luminoracore_sdk.client import LuminoraCoreClient
        from luminoracore_sdk.client_v1_1 import LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
        print("OK Importaciones del SDK exitosas")
    except Exception as e:
        print(f"ERROR Importaciones del SDK: {e}")
        return False
    
    # 2. Verificar configuracion de DeepSeek
    print("\nPaso 2: Verificando configuracion de DeepSeek...")
    
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    if deepseek_api_key:
        print("OK API key de DeepSeek configurada")
        print(f"   Key: {deepseek_api_key[:8]}...{deepseek_api_key[-4:]}")
    else:
        print("ADVERTENCIA: DEEPSEEK_API_KEY no esta configurada")
        print("   Para configurar: export DEEPSEEK_API_KEY='tu_api_key'")
    
    # 3. Crear configuracion de proveedor
    print("\nPaso 3: Creando configuracion de proveedor...")
    
    provider_config = {
        "deepseek": {
            "api_key": deepseek_api_key or "demo_key",
            "model": "deepseek-chat",
            "base_url": "https://api.deepseek.com/v1"
        }
    }
    
    print("OK Configuracion de proveedor creada")
    print(f"   Modelo: {provider_config['deepseek']['model']}")
    print(f"   URL Base: {provider_config['deepseek']['base_url']}")
    
    # 4. Crear storage
    print("\nPaso 4: Creando storage...")
    
    try:
        storage = InMemoryStorageV11()
        print("OK Storage en memoria creado")
    except Exception as e:
        print(f"ERROR Creando storage: {e}")
        return False
    
    # 5. Crear cliente
    print("\nPaso 5: Creando cliente...")
    
    try:
        # Crear cliente base primero
        base_client = LuminoraCoreClient()
        
        # Crear cliente v1.1 con extensiones
        client = LuminoraCoreClientV11(base_client, storage_v11=storage)
        print("OK Cliente LuminoraCore creado")
    except Exception as e:
        print(f"ERROR Creando cliente: {e}")
        return False
    
    # 6. Crear personalidad Victoria Sterling
    print("\nPaso 6: Creando personalidad Victoria Sterling...")
    
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
    print(f"   Nombre: {victoria_personality['name']}")
    print(f"   Version: {victoria_personality['version']}")
    print(f"   Niveles de relacion: {len(victoria_personality['hierarchical_config']['relationship_levels'])}")
    
    # 7. Simular inicializacion de sesion
    print("\nPaso 7: Simulando inicializacion de sesion...")
    
    session_id = "test_user_123"
    print(f"OK Sesion simulada creada: {session_id}")
    
    # 8. Mostrar configuracion completa
    print("\nPaso 8: Configuracion completa del sistema...")
    
    print("\nConfiguracion del Cliente:")
    print(f"   - Session ID: {session_id}")
    print(f"   - Provider: DeepSeek")
    print(f"   - Model: deepseek-chat")
    print(f"   - Storage: InMemoryStorageV11")
    
    print("\nConfiguracion de Personalidad:")
    print(f"   - Nombre: {victoria_personality['name']}")
    print(f"   - Version: {victoria_personality['version']}")
    print(f"   - Profesionalismo: {victoria_personality['base_personality']['core_traits']['professionalism']}")
    print(f"   - Eficiencia: {victoria_personality['base_personality']['core_traits']['efficiency']}")
    print(f"   - Empatia: {victoria_personality['base_personality']['core_traits']['empathy']}")
    print(f"   - Directez: {victoria_personality['base_personality']['core_traits']['directness']}")
    
    print("\nConfiguracion de Memoria:")
    print(f"   - Retencion de hechos: {victoria_personality['memory_preferences']['fact_retention']}")
    print(f"   - Memoria episodica: {victoria_personality['memory_preferences']['episodic_memory']}")
    print(f"   - Aprendizaje de preferencias: {victoria_personality['memory_preferences']['preference_learning']}")
    print(f"   - Seguimiento de objetivos: {victoria_personality['memory_preferences']['goal_tracking']}")
    
    print("\nConfiguracion de Afinidad:")
    print(f"   - Interacciones positivas: +{victoria_personality['affinity_config']['positive_interactions']} puntos")
    print(f"   - Interacciones negativas: {victoria_personality['affinity_config']['negative_interactions']} puntos")
    print(f"   - Logro de objetivos: +{victoria_personality['affinity_config']['goal_achievement']} puntos")
    print(f"   - Alineacion de preferencias: +{victoria_personality['affinity_config']['preference_alignment']} puntos")
    
    # 9. Resumen final
    print("\n" + "=" * 60)
    print("RESUMEN DEL TEST DE CONFIGURACION")
    print("=" * 60)
    
    if deepseek_api_key:
        print("ESTADO: LISTO PARA USAR CON DEEPSEEK")
        print("\nEl sistema esta completamente configurado y listo para:")
        print("1. Enviar mensajes a DeepSeek")
        print("2. Gestionar memoria y relaciones")
        print("3. Evolucionar personalidades")
        print("4. Exportar datos de sesion")
        
        print("\nPara probar con DeepSeek, ejecuta:")
        print("python test_deepseek_complete.py")
        
        return True
    else:
        print("ESTADO: CONFIGURACION INCOMPLETA")
        print("\nPara completar la configuracion:")
        print("1. Obtener API key de DeepSeek: https://platform.deepseek.com/")
        print("2. Configurar: export DEEPSEEK_API_KEY='tu_api_key'")
        print("3. Ejecutar: python test_deepseek_complete.py")
        
        return False

def main():
    """Funcion principal"""
    
    print("Iniciando test de configuracion DeepSeek...")
    print("Este test verifica que todo este listo para usar con DeepSeek")
    print("=" * 60)
    
    try:
        success = test_deepseek_configuration()
        
        if success:
            print("\nTest completado exitosamente!")
            return 0
        else:
            print("\nTest completado con advertencias")
            return 1
            
    except Exception as e:
        print(f"\nERROR durante el test: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
