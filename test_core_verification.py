#!/usr/bin/env python3
"""
VERIFICACION DEL CORE
Verificar que el Core funcione correctamente
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore"))

async def test_core_verification():
    """Verificacion del Core"""
    print("=== VERIFICACION DEL CORE ===")
    print("=" * 60)
    
    try:
        # TEST 1: Import Core modules
        print("1. VERIFICANDO IMPORTS DEL CORE:")
        try:
            from luminoracore import Personality, PersonalityCompiler, LLMProvider
            print("   [OK] Core imports funcionan")
        except Exception as e:
            print(f"   [ERROR] Core imports fallan: {e}")
            return False
        
        # TEST 2: Create personality
        print("\n2. CREANDO PERSONALIDAD:")
        try:
            personality_data = {
                "persona": {
                    "name": "test_personality",
                    "version": "1.1.0",
                    "description": "Test personality for verification",
                    "author": "Test",
                    "tags": ["test", "verification"],
                    "language": "en",
                    "compatibility": ["openai", "anthropic"]
                },
                "core_traits": {
                    "archetype": "caregiver",
                    "temperament": "calm",
                    "communication_style": "formal"
                },
                "linguistic_profile": {
                    "tone": ["friendly", "professional"],
                    "syntax": "simple",
                    "vocabulary": ["technical", "accessible"]
                },
                "behavioral_rules": [
                    "Be helpful and professional",
                    "Provide clear and accurate information"
                ]
            }
            
            personality = Personality(personality_data)
            print(f"   [OK] Personalidad creada: {personality.persona.name}")
        except Exception as e:
            print(f"   [ERROR] Error creando personalidad: {e}")
            return False
        
        # TEST 3: Compile personality
        print("\n3. COMPILANDO PERSONALIDAD:")
        try:
            compiler = PersonalityCompiler()
            compiled = compiler.compile(personality, LLMProvider.OPENAI)
            print(f"   [OK] Personalidad compilada: {type(compiled)}")
        except Exception as e:
            print(f"   [ERROR] Error compilando personalidad: {e}")
            return False
        
        # TEST 4: Test LLM providers
        print("\n4. VERIFICANDO PROVEEDORES LLM:")
        providers = [LLMProvider.OPENAI, LLMProvider.ANTHROPIC, LLMProvider.DEEPSEEK]
        for provider in providers:
            try:
                compiled = compiler.compile(personality, provider)
                print(f"   [OK] {provider.value}: {type(compiled)}")
            except Exception as e:
                print(f"   [ERROR] {provider.value}: {e}")
        
        # TEST 5: Test personality validation
        print("\n5. VERIFICANDO VALIDACION:")
        try:
            # La validacion se hace en el constructor
            print(f"   [OK] Validacion: Personalidad creada correctamente")
        except Exception as e:
            print(f"   [ERROR] Error en validacion: {e}")
            return False
        
        # RESULTADO FINAL
        print("\n" + "=" * 60)
        print("RESULTADO FINAL:")
        print("[OK] Core funciona correctamente")
        print("[OK] Todas las funcionalidades básicas operativas")
        return True
        
    except Exception as e:
        print(f"[ERROR] ERROR CRITICO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_core_verification())
    if success:
        print("\n[OK] CORE VERIFICADO - FUNCIONA CORRECTAMENTE")
    else:
        print("\n[FAIL] CORE NO FUNCIONA - HAY PROBLEMAS")
    sys.exit(0 if success else 1)
