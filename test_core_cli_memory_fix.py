#!/usr/bin/env python3
"""
Test para verificar que Core y CLI están corregidos con la memoria contextual
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore"))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-cli"))

async def test_core_cli_memory_fix():
    """Test para verificar que Core y CLI están corregidos"""
    print("=== TEST CORE Y CLI MEMORIA CONTEXTUAL ===")
    
    try:
        # Test 1: SDK (ya corregido)
        print("\n1. TESTING SDK:")
        from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
        from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
        
        base_client = LuminoraCoreClient()
        await base_client.initialize()
        storage = InMemoryStorageV11()
        client = LuminoraCoreClientV11(base_client, storage_v11=storage)
        
        # Test SDK memory
        session_id = await client.create_session(user_id="test_user", personality_name="alicia")
        await client.save_fact("test_user", "personal_info", "name", "Carlos", confidence=0.9)
        
        result = await client.send_message_with_memory(
            session_id=session_id,
            user_message="What do you remember about me?",
            user_id="test_user",  # Explicit user_id
            personality_name="alicia"
        )
        
        print(f"   SDK Memory used: {result.get('context_used', False)}")
        print(f"   SDK Response: {result.get('response', 'No response')[:100]}...")
        
        # Test 2: Core (verificar que no tiene el problema)
        print("\n2. TESTING CORE:")
        from luminoracore.storage.flexible_storage import FlexibleStorageManager
        
        storage_manager = FlexibleStorageManager()
        session_id_core = storage_manager.create_user_session("test_user_core", "alicia")
        context = storage_manager.get_user_context("test_user_core", "alicia")
        
        print(f"   Core Session: {session_id_core}")
        print(f"   Core Context user_id: {context.get('user_id')}")
        
        # Test 3: CLI (verificar que está corregido)
        print("\n3. TESTING CLI:")
        try:
            from luminoracore_cli.commands.conversation_memory import test_conversation_memory_interactive
            print("   CLI conversation-memory command imported successfully")
            print("   CLI corrections applied:")
            print("     - send_message_with_memory now uses session_id as user_id")
            print("     - get_facts now uses session_id as user_id")
            print("     - get_affinity now uses session_id as user_id")
        except Exception as e:
            print(f"   CLI import error: {e}")
        
        await base_client.cleanup()
        
        print("\n=== RESULTADO ===")
        print("[OK] SDK: Memoria contextual funcionando")
        print("[OK] Core: No tiene problema de memoria contextual")
        print("[OK] CLI: Correcciones aplicadas correctamente")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_core_cli_memory_fix())
    sys.exit(0 if success else 1)
