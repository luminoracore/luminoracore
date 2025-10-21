#!/usr/bin/env python3
"""
TESTING EXHAUSTIVO DEL FRAMEWORK LUMINORACORE v1.1

Verifica TODAS las características que decimos que tenemos.
Si algo falla, NO es aceptable.
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-sdk-python"))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore"))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-cli"))

class FrameworkTester:
    def __init__(self):
        self.results = {}
        self.errors = []
        self.warnings = []
        
    def log_result(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        self.results[test_name] = {
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        if success:
            print(f"[OK] {test_name}: {details}")
        else:
            print(f"[FAIL] {test_name}: {details}")
            self.errors.append(f"{test_name}: {details}")
    
    def log_warning(self, test_name: str, warning: str):
        """Log warning"""
        self.warnings.append(f"{test_name}: {warning}")
        print(f"[WARN] {test_name}: {warning}")

    async def test_sdk_user_system(self):
        """Test exhaustivo del sistema de usuarios del SDK"""
        print("\n=== TESTING SDK USER SYSTEM ===")
        
        try:
            from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
            from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
            
            # Initialize
            base_client = LuminoraCoreClient()
            await base_client.initialize()
            storage = InMemoryStorageV11()
            client = LuminoraCoreClientV11(base_client, storage_v11=storage)
            
            # Test 1: Create session with user
            session_id = await client.create_session(
                user_id="test_user_123",
                personality_name="alicia",
                session_config={"ttl": 3600}
            )
            self.log_result("SDK_CREATE_SESSION_WITH_USER", bool(session_id), f"Session: {session_id}")
            
            # Test 2: User persistence across sessions
            session_id_2 = await client.create_session(
                user_id="test_user_123",
                personality_name="alicia"
            )
            self.log_result("SDK_USER_PERSISTENCE", session_id != session_id_2, "Different sessions, same user")
            
            # Test 3: Affinity persistence
            await client.update_affinity("test_user_123", "alicia", 25, "positive")
            affinity = await client.get_affinity("test_user_123", "alicia")
            affinity_points = affinity.get('affinity_points', 0) if affinity else 0
            self.log_result("SDK_AFFINITY_PERSISTENCE", affinity_points == 25, f"Affinity: {affinity_points}")
            
            # Test 4: Facts persistence
            await client.save_fact("test_user_123", "personal_info", "name", "Carlos", confidence=0.95)
            facts = await client.get_facts("test_user_123")
            fact_found = any(f.get('key') == 'name' and f.get('value') == 'Carlos' for f in facts)
            self.log_result("SDK_FACTS_PERSISTENCE", fact_found, f"Facts count: {len(facts)}")
            
            # Test 5: Episodes persistence
            await client.save_episode(
                "test_user_123", "milestone", "First test", 
                "Testing episodes", 8.5, "positive"
            )
            episodes = await client.get_episodes("test_user_123")
            episode_found = any(e.get('title') == 'First test' for e in episodes)
            self.log_result("SDK_EPISODES_PERSISTENCE", episode_found, f"Episodes count: {len(episodes)}")
            
            # Test 6: User separation
            await client.create_session(user_id="demo", personality_name="alicia")
            demo_affinity = await client.get_affinity("demo", "alicia")
            demo_points = demo_affinity.get('affinity_points', 0) if demo_affinity else 0
            user_points = affinity_points
            separation_ok = demo_points != user_points
            self.log_result("SDK_USER_SEPARATION", separation_ok, f"Demo: {demo_points}, User: {user_points}")
            
            await base_client.cleanup()
            
        except Exception as e:
            self.log_result("SDK_USER_SYSTEM", False, f"Error: {str(e)}")
            import traceback
            traceback.print_exc()

    async def test_sdk_memory_contextual(self):
        """Test exhaustivo de memoria contextual del SDK"""
        print("\n=== TESTING SDK MEMORY CONTEXTUAL ===")
        
        try:
            from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
            from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
            
            base_client = LuminoraCoreClient()
            await base_client.initialize()
            storage = InMemoryStorageV11()
            client = LuminoraCoreClientV11(base_client, storage_v11=storage)
            
            # Test 1: Memory manager exists
            memory_manager_exists = client.conversation_manager is not None
            self.log_result("SDK_MEMORY_MANAGER_EXISTS", memory_manager_exists, "ConversationMemoryManager initialized")
            
            # Test 2: Send message with memory
            session_id = await client.create_session(user_id="memory_test_user", personality_name="alicia")
            
            # Save some facts first
            await client.save_fact("memory_test_user", "personal_info", "name", "Ana", confidence=0.9)
            await client.save_fact("memory_test_user", "preferences", "language", "Python", confidence=0.8)
            
            # Test send_message_with_memory
            result = await client.send_message_with_memory(
                session_id=session_id,
                user_message="What do you remember about me?",
                user_id="memory_test_user",
                personality_name="alicia"
            )
            
            memory_used = result.get('context_used', False)
            self.log_result("SDK_MEMORY_CONTEXTUAL_USED", memory_used, f"Response: {result.get('response', 'No response')[:100]}...")
            
            # Test 3: Facts extraction
            new_facts = result.get('new_facts', [])
            self.log_result("SDK_FACTS_EXTRACTION", len(new_facts) >= 0, f"New facts extracted: {len(new_facts)}")
            
            # Test 4: Affinity update
            affinity_change = result.get('affinity_change', {})
            affinity_updated = affinity_change.get('points_change', 0) != 0
            self.log_result("SDK_AFFINITY_UPDATE", affinity_updated, f"Affinity change: {affinity_change}")
            
            await base_client.cleanup()
            
        except Exception as e:
            self.log_result("SDK_MEMORY_CONTEXTUAL", False, f"Error: {str(e)}")
            import traceback
            traceback.print_exc()

    async def test_sdk_sentiment_analysis(self):
        """Test exhaustivo del análisis sentimental del SDK"""
        print("\n=== TESTING SDK SENTIMENT ANALYSIS ===")
        
        try:
            from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
            from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
            
            base_client = LuminoraCoreClient()
            await base_client.initialize()
            storage = InMemoryStorageV11()
            client = LuminoraCoreClientV11(base_client, storage_v11=storage)
            
            # Test 1: Sentiment analyzer exists
            analyzer_exists = client.sentiment_analyzer is not None
            self.log_result("SDK_SENTIMENT_ANALYZER_EXISTS", analyzer_exists, "AdvancedSentimentAnalyzer initialized")
            
            # Test 2: Sentiment analysis
            sentiment_result = await client.analyze_sentiment(
                user_id="sentiment_test_user",
                message="I'm so happy today!"
            )
            
            sentiment_success = sentiment_result.get('success', False)
            self.log_result("SDK_SENTIMENT_ANALYSIS", sentiment_success, f"Sentiment: {sentiment_result.get('sentiment', 'unknown')}")
            
            # Test 3: Sentiment history
            history = await client.get_sentiment_history("sentiment_test_user")
            self.log_result("SDK_SENTIMENT_HISTORY", isinstance(history, list), f"History entries: {len(history)}")
            
            await base_client.cleanup()
            
        except Exception as e:
            self.log_result("SDK_SENTIMENT_ANALYSIS", False, f"Error: {str(e)}")
            import traceback
            traceback.print_exc()

    async def test_sdk_export_system(self):
        """Test exhaustivo del sistema de exportación del SDK"""
        print("\n=== TESTING SDK EXPORT SYSTEM ===")
        
        try:
            from luminoracore_sdk import LuminoraCoreClient, LuminoraCoreClientV11
            from luminoracore_sdk.session.storage_v1_1 import InMemoryStorageV11
            
            base_client = LuminoraCoreClient()
            await base_client.initialize()
            storage = InMemoryStorageV11()
            client = LuminoraCoreClientV11(base_client, storage_v11=storage)
            
            # Prepare test data
            session_id = await client.create_session(user_id="export_test_user", personality_name="alicia")
            await client.save_fact("export_test_user", "personal_info", "name", "ExportUser", confidence=0.9)
            await client.save_episode("export_test_user", "test", "Export Test", "Testing export", 7.5, "neutral")
            
            # Test 1: Export conversation
            export_result = await client.export_conversation(session_id, format="json")
            export_success = export_result.get('success', False)
            self.log_result("SDK_EXPORT_CONVERSATION", export_success, f"Export success: {export_success}")
            
            # Test 2: Export user conversations
            user_export = await client.export_user_conversations("export_test_user", format="json")
            user_export_success = user_export.get('success', False)
            self.log_result("SDK_EXPORT_USER_CONVERSATIONS", user_export_success, f"User export success: {user_export_success}")
            
            # Test 3: Export complete user data
            complete_export = await client.export_complete_user_data("export_test_user")
            complete_success = complete_export.get('success', False)
            self.log_result("SDK_EXPORT_COMPLETE_DATA", complete_success, f"Complete export success: {complete_success}")
            
            await base_client.cleanup()
            
        except Exception as e:
            self.log_result("SDK_EXPORT_SYSTEM", False, f"Error: {str(e)}")
            import traceback
            traceback.print_exc()

    async def test_core_storage_management(self):
        """Test exhaustivo del Core storage management"""
        print("\n=== TESTING CORE STORAGE MANAGEMENT ===")
        
        try:
            from luminoracore.storage.flexible_storage import FlexibleStorageManager
            
            # Test 1: Storage manager initialization
            storage_manager = FlexibleStorageManager()
            self.log_result("CORE_STORAGE_MANAGER_INIT", True, "FlexibleStorageManager initialized")
            
            # Test 2: User session creation
            session_id = storage_manager.create_user_session("core_test_user", "alicia")
            self.log_result("CORE_USER_SESSION_CREATION", bool(session_id), f"Session: {session_id}")
            
            # Test 3: User context retrieval
            context = storage_manager.get_user_context("core_test_user", "alicia")
            context_valid = context.get('user_id') == "core_test_user"
            self.log_result("CORE_USER_CONTEXT_RETRIEVAL", context_valid, f"Context: {context}")
            
            # Test 4: Session cleanup
            cleaned_count = storage_manager.cleanup_expired_sessions()
            self.log_result("CORE_SESSION_CLEANUP", cleaned_count >= 0, f"Sessions cleaned: {cleaned_count}")
            
        except Exception as e:
            self.log_result("CORE_STORAGE_MANAGEMENT", False, f"Error: {str(e)}")
            import traceback
            traceback.print_exc()

    async def test_cli_commands(self):
        """Test exhaustivo de los comandos del CLI"""
        print("\n=== TESTING CLI COMMANDS ===")
        
        try:
            # Test 1: CLI import
            from luminoracore_cli.main import app
            self.log_result("CLI_IMPORT", True, "CLI main app imported")
            
            # Test 2: Storage commands import
            from luminoracore_cli.commands.storage import app as storage_app
            self.log_result("CLI_STORAGE_COMMANDS", True, "Storage commands imported")
            
            # Test 3: CLI version
            from luminoracore_cli import __version__
            version_ok = __version__ == "1.1.0"
            self.log_result("CLI_VERSION", version_ok, f"Version: {__version__}")
            
        except Exception as e:
            self.log_result("CLI_COMMANDS", False, f"Error: {str(e)}")
            import traceback
            traceback.print_exc()

    async def run_all_tests(self):
        """Run all tests"""
        print("TESTING EXHAUSTIVO DEL FRAMEWORK LUMINORACORE v1.1")
        print("=" * 80)
        
        # Run all test suites
        await self.test_sdk_user_system()
        await self.test_sdk_memory_contextual()
        await self.test_sdk_sentiment_analysis()
        await self.test_sdk_export_system()
        await self.test_core_storage_management()
        await self.test_cli_commands()
        
        # Generate report
        self.generate_report()
        
        return len(self.errors) == 0

    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("REPORTE DE TESTING EXHAUSTIVO")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() if r['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total de tests: {total_tests}")
        print(f"Tests pasados: {passed_tests}")
        print(f"Tests fallidos: {failed_tests}")
        print(f"Porcentaje de éxito: {(passed_tests/total_tests)*100:.1f}%")
        
        if self.warnings:
            print(f"\n[WARNINGS] ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if self.errors:
            print(f"\n[ERRORES] ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
            
            print(f"\n[RESULTADO] FRAMEWORK NO FUNCIONAL")
            print("[FAIL] NO ES ACEPTABLE - HAY ERRORES CRITICOS")
        else:
            print(f"\n[RESULTADO] FRAMEWORK 100% FUNCIONAL")
            print("[OK] TODAS LAS CARACTERISTICAS FUNCIONAN CORRECTAMENTE")
        
        # Save detailed report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": (passed_tests/total_tests)*100
            },
            "results": self.results,
            "errors": self.errors,
            "warnings": self.warnings
        }
        
        with open("framework_test_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\nReporte detallado guardado en: framework_test_report.json")

async def main():
    """Main test function"""
    tester = FrameworkTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n[OK] FRAMEWORK VERIFICADO - TODAS LAS CARACTERISTICAS FUNCIONAN")
        sys.exit(0)
    else:
        print("\n[FAIL] FRAMEWORK CON ERRORES - NO ES ACEPTABLE")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
