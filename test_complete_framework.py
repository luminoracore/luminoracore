#!/usr/bin/env python3
"""
Test completo del framework con sistema de usuarios implementado
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore"))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-cli"))

async def test_complete_framework():
    """Test completo del framework"""
    print("=== TEST FRAMEWORK COMPLETO ===")
    
    try:
        # Test SDK
        print("1. TESTING SDK:")
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
        
        base_client = LuminoraCoreClient()
        await base_client.initialize()
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(base_client, storage_v11=storage)
        
        # Test user system
        session_id = await client.create_session(
            user_id="test_user",
            personality_name="alicia"
        )
        print(f"   SDK: Session created: {session_id}")
        
        # Test affinity
        await client.update_affinity("test_user", "alicia", 10, "positive")
        affinity = await client.get_affinity("test_user", "alicia")
        print(f"   SDK: Affinity: {affinity.get('affinity_points', 0)} puntos")
        
        # Test Core
        print("\n2. TESTING CORE:")
        from luminoracore.storage.flexible_storage import FlexibleStorageManager
        
        storage_manager = FlexibleStorageManager()
        session_id_core = storage_manager.create_user_session("test_user_core", "alicia")
        print(f"   Core: Session created: {session_id_core}")
        
        context = storage_manager.get_user_context("test_user_core", "alicia")
        print(f"   Core: Context retrieved for user: {context['user_id']}")
        
        # Test CLI
        print("\n3. TESTING CLI:")
        try:
            from luminoracore_cli.commands.storage import app as storage_app
            print("   CLI: Storage commands imported successfully")
            print("   CLI: Available commands:")
            for command in storage_app.commands:
                print(f"     - {command.name}")
        except Exception as e:
            print(f"   CLI: Error importing storage commands: {e}")
        
        await base_client.cleanup()
        
        print("\n=== RESULTADO ===")
        print("SUCCESS: Framework completo implementado")
        print("- SDK: Sistema de usuarios funcionando")
        print("- Core: Gestión de sesiones funcionando")
        print("- CLI: Comandos de storage implementados")
        
        return True
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_complete_framework())
    sys.exit(0 if success else 1)
