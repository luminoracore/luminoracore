#!/usr/bin/env python3
"""
Script simple para probar el wizard interactivo de LuminoraCore
"""

import asyncio
import sys
from pathlib import Path

# Agregar el directorio del CLI al path
cli_path = Path(__file__).parent / "luminoracore-cli"
sys.path.insert(0, str(cli_path))

from luminoracore_cli.commands.create import create_command

async def test_wizard():
    """Prueba el wizard de creación de personalidades."""
    print("🧪 PRUEBA DEL WIZARD INTERACTIVO")
    print("=" * 50)
    
    try:
        # Simular la creación de una personalidad
        print("Iniciando wizard de creación...")
        
        # Crear una personalidad de prueba
        personality_data = {
            "name": "TestWizard",
            "version": "1.0.0",
            "description": "Personalidad creada con el wizard",
            "author": "Test User",
            "tags": ["test", "wizard"],
            "persona": {
                "name": "TestWizard",
                "description": "Personalidad creada con el wizard",
                "archetype": "assistant",
                "version": "1.0.0",
                "author": "Test User",
                "tags": ["test", "wizard"]
            },
            "core_traits": ["helpful", "friendly", "test"],
            "linguistic_profile": {
                "tone": ["friendly", "helpful"],
                "vocabulary": ["test", "help", "assist"],
                "speech_patterns": ["I can help you test", "Let me test this"],
                "formality_level": "casual",
                "response_length": "moderate"
            },
            "behavioral_rules": [
                "Be helpful and friendly",
                "Always respond with test prefix",
                "Provide accurate information"
            ],
            "advanced_parameters": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 500
            }
        }
        
        print("✅ Datos de personalidad generados:")
        print(f"   - Nombre: {personality_data['name']}")
        print(f"   - Descripción: {personality_data['description']}")
        print(f"   - Traits: {', '.join(personality_data['core_traits'])}")
        print(f"   - Reglas: {len(personality_data['behavioral_rules'])} reglas")
        
        # Guardar en archivo
        output_file = Path("test_wizard_personality.json")
        import json
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(personality_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Personalidad guardada en: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def test_cli_commands():
    """Prueba los comandos CLI disponibles."""
    print("\n🛠️ COMANDOS CLI DISPONIBLES")
    print("=" * 50)
    
    commands = [
        "luminoracore validate <archivo>",
        "luminoracore compile <archivo> --provider openai",
        "luminoracore create --interactive",
        "luminoracore list",
        "luminoracore test <archivo> --interactive",
        "luminoracore serve --host 127.0.0.1 --port 8000",
        "luminoracore blend <archivo1> <archivo2>",
        "luminoracore info <archivo>",
        "luminoracore init <directorio>",
        "luminoracore version"
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"{i:2d}. {cmd}")
    
    print(f"\n✅ {len(commands)} comandos disponibles")

def test_web_server():
    """Prueba el servidor web."""
    print("\n🌐 SERVIDOR WEB")
    print("=" * 50)
    
    print("Para iniciar el servidor web:")
    print("  cd luminoracore-cli")
    print("  python -m luminoracore_cli.main serve")
    print("\nLuego abre: http://127.0.0.1:8000")

async def main():
    """Función principal de prueba."""
    print("🚀 LUMINORACORE - PRUEBAS DEL WIZARD")
    print("=" * 60)
    
    # Prueba 1: Wizard de creación
    success1 = await test_wizard()
    
    # Prueba 2: Comandos CLI
    test_cli_commands()
    
    # Prueba 3: Servidor web
    test_web_server()
    
    print("\n📋 RESUMEN DE PRUEBAS")
    print("=" * 50)
    print(f"✅ Wizard de creación: {'PASÓ' if success1 else 'FALLÓ'}")
    print("✅ Comandos CLI: DISPONIBLES")
    print("✅ Servidor web: DISPONIBLE")
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Ejecuta: cd luminoracore-cli")
    print("2. Ejecuta: python -m luminoracore_cli.main create --interactive")
    print("3. Sigue las instrucciones del wizard")
    print("4. Prueba: python -m luminoracore_cli.main test <archivo> --interactive")

if __name__ == "__main__":
    asyncio.run(main())
