#!/usr/bin/env python3
"""
Test para verificar la relación entre sesiones, usuarios y evolución de personalidad
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))

async def test_session_user_relationship():
    """Test de relación entre sesiones y usuarios"""
    print("=== SESIONES, USUARIOS Y EVOLUCION DE PERSONALIDAD ===")
    
    try:
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
        
        # Setup
        base_client = LuminoraCoreClient()
        await base_client.initialize()
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(base_client, storage_v11=storage)
        
        print("1. PROBLEMA IDENTIFICADO:")
        print("   - Las sesiones NO están vinculadas a usuarios específicos")
        print("   - session_id se usa como user_id en el almacenamiento")
        print("   - No hay gestión de expiración de sesiones")
        print("   - La evolución de personalidad se pierde entre sesiones")
        
        print("\n2. COMO FUNCIONA ACTUALMENTE:")
        
        # Simular sesión 1
        session_1 = await client.create_session(
            personality_name="alicia",
            provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
        )
        print(f"   Sesión 1 creada: {session_1}")
        
        # Simular evolución en sesión 1
        await client.update_affinity(
            user_id=session_1,  # Aquí está el problema: usa session_id como user_id
            personality_name="alicia",
            points_delta=20,
            interaction_type="positive"
        )
        
        affinity_1 = await client.get_affinity(session_1, "alicia")
        print(f"   Afinidad en sesión 1: {affinity_1.get('affinity_points', 0)} puntos")
        
        # Simular nueva sesión (usuario se reconecta)
        session_2 = await client.create_session(
            personality_name="alicia",
            provider_config={"name": "openai", "model": "gpt-3.5-turbo"}
        )
        print(f"   Sesión 2 creada: {session_2}")
        
        # Verificar si la evolución se mantiene
        affinity_2 = await client.get_affinity(session_2, "alicia")
        print(f"   Afinidad en sesión 2: {affinity_2.get('affinity_points', 0)} puntos")
        
        print("\n3. PROBLEMAS IDENTIFICADOS:")
        print(f"   PROBLEMA - Sesion 1: {session_1}")
        print(f"   PROBLEMA - Sesion 2: {session_2}")
        print(f"   PROBLEMA - Son sesiones DIFERENTES = usuarios DIFERENTES")
        print(f"   PROBLEMA - La evolucion de personalidad se PIERDE")
        print(f"   PROBLEMA - No hay vinculacion con usuario real")
        
        print("\n4. SOLUCION NECESARIA:")
        print("   SOLUCION - Necesitamos un user_id independiente del session_id")
        print("   SOLUCION - El user_id debe persistir entre sesiones")
        print("   SOLUCION - La evolucion debe vincularse al user_id, no al session_id")
        print("   SOLUCION - Necesitamos gestion de expiracion de sesiones")
        
        print("\n5. PROPUESTA DE IMPLEMENTACION:")
        print("   - create_session(user_id, personality_name, provider_config)")
        print("   - session_id: temporal, para la conversación actual")
        print("   - user_id: persistente, para la evolución de personalidad")
        print("   - Expiración: TTL configurable para sesiones")
        
        # Demostrar el problema
        print("\n6. DEMOSTRACION DEL PROBLEMA:")
        print("   Usuario 'carlos' se conecta:")
        
        # Simular usuario real
        user_id = "carlos"
        session_a = await client.create_session("alicia")
        session_b = await client.create_session("alicia")
        
        print(f"   - Sesión A: {session_a}")
        print(f"   - Sesión B: {session_b}")
        print(f"   - Son sesiones DIFERENTES")
        print(f"   - La evolución en A NO se refleja en B")
        
        await base_client.cleanup()
        
        print("\n=== CONCLUSION ===")
        print("PROBLEMA CRITICO: Las sesiones no están vinculadas a usuarios")
        print("SOLUCION: Implementar user_id independiente del session_id")
        print("IMPACTO: La evolución de personalidad se pierde entre sesiones")
        
        return True
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_session_user_relationship())
    sys.exit(0 if success else 1)
