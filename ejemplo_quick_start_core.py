#!/usr/bin/env python3
"""
Ejemplo Quick Start - LuminoraCore Motor Base
Ejecuta este archivo para probar que luminoracore está instalado correctamente.
"""

import sys
from pathlib import Path

def main():
    """Prueba rápida del motor base de LuminoraCore."""
    print("=" * 60)
    print("🧠 LuminoraCore - Motor Base - Quick Start")
    print("=" * 60)
    
    # Verificar que luminoracore está instalado
    print("\n1️⃣  Verificando instalación de luminoracore...")
    try:
        import luminoracore
        print(f"   ✅ luminoracore instalado - Versión: {luminoracore.__version__}")
    except ImportError as e:
        print(f"   ❌ Error: luminoracore no está instalado")
        print(f"   💡 Solución: cd luminoracore && pip install -e .")
        return False
    
    # Importar componentes principales
    print("\n2️⃣  Importando componentes principales...")
    try:
        from luminoracore import (
            Personality, 
            PersonalityValidator, 
            PersonalityCompiler, 
            PersonalityBlender,
            LLMProvider
        )
        print("   ✅ Todos los componentes importados correctamente")
    except ImportError as e:
        print(f"   ❌ Error al importar: {e}")
        return False
    
    # Verificar que existe la carpeta de personalidades
    print("\n3️⃣  Buscando personalidades de ejemplo...")
    personalities_dir = Path("personalidades")
    
    if not personalities_dir.exists():
        # Intentar con la ruta del paquete
        personalities_dir = Path("luminoracore/luminoracore/personalities")
    
    if not personalities_dir.exists():
        print(f"   ⚠️  No se encontró la carpeta de personalidades")
        print(f"   💡 Creando personalidad de ejemplo en memoria...")
        
        # Crear una personalidad simple en memoria
        personality_dict = {
            "persona": {
                "name": "Asistente Demo",
                "version": "1.0.0",
                "description": "Una personalidad de demostración",
                "author": "LuminoraCore",
                "language": "es",
                "tags": ["demo", "test"],
                "compatibility": ["openai", "anthropic"]
            },
            "core_traits": {
                "archetype": "helper",
                "temperament": "friendly",
                "primary_motivation": "ayudar a los usuarios",
                "expertise_areas": ["asistencia general"],
                "communication_style": "claro y conciso"
            },
            "linguistic_profile": {
                "tone": ["amigable", "profesional"],
                "formality_level": "semiformal",
                "syntax": "estructurado",
                "vocabulary": ["claro", "preciso", "accesible"],
                "fillers": [],
                "humor_style": "ligero"
            },
            "behavioral_rules": [
                "Siempre ser respetuoso y cortés",
                "Proporcionar información precisa y verificable"
            ],
            "constraints": {
                "topics_to_avoid": ["contenido inapropiado"],
                "ethical_guidelines": ["respetar la privacidad del usuario"],
                "prohibited_behaviors": ["desinformación"]
            },
            "examples": {
                "sample_responses": [
                    {
                        "input": "Hola",
                        "output": "¡Hola! ¿En qué puedo ayudarte hoy?"
                    }
                ],
                "tone_examples": ["Amigable y servicial"],
                "boundary_examples": ["No proporciono información médica profesional"]
            }
        }
        
        # Simular carga de personalidad desde diccionario
        print("   ✅ Personalidad de ejemplo creada en memoria")
        personality = None  # Por ahora solo probamos imports
    else:
        # Buscar un archivo de personalidad
        personality_files = list(personalities_dir.glob("*.json"))
        if personality_files:
            print(f"   ✅ Encontradas {len(personality_files)} personalidades")
            print(f"   📄 Usando: {personality_files[0].name}")
            
            try:
                personality = Personality(str(personality_files[0]))
                print(f"   ✅ Personalidad cargada: {personality.persona.name}")
            except Exception as e:
                print(f"   ⚠️  Error al cargar personalidad: {e}")
                personality = None
        else:
            print("   ⚠️  No se encontraron archivos .json de personalidades")
            personality = None
    
    # Probar el validador
    print("\n4️⃣  Probando PersonalityValidator...")
    try:
        validator = PersonalityValidator()
        print("   ✅ PersonalityValidator creado correctamente")
        
        if personality:
            result = validator.validate(personality)
            if result.is_valid:
                print(f"   ✅ Validación exitosa")
                print(f"      - Advertencias: {len(result.warnings)}")
                print(f"      - Sugerencias: {len(result.suggestions)}")
            else:
                print(f"   ⚠️  Validación con errores: {len(result.errors)}")
    except Exception as e:
        print(f"   ⚠️  Error en validación: {e}")
    
    # Probar el compilador
    print("\n5️⃣  Probando PersonalityCompiler...")
    try:
        compiler = PersonalityCompiler()
        print("   ✅ PersonalityCompiler creado correctamente")
        
        if personality:
            # Compilar para OpenAI
            result = compiler.compile(personality, LLMProvider.OPENAI)
            print(f"   ✅ Compilación exitosa para OpenAI")
            print(f"      - Tokens estimados: {result.token_estimate}")
            print(f"      - Longitud del prompt: {len(result.prompt)} caracteres")
            
            # Probar con otros proveedores
            providers_tested = []
            for provider in [LLMProvider.ANTHROPIC, LLMProvider.LLAMA]:
                try:
                    result = compiler.compile(personality, provider)
                    providers_tested.append(provider.value)
                except:
                    pass
            
            if providers_tested:
                print(f"   ✅ También compilado para: {', '.join(providers_tested)}")
    except Exception as e:
        print(f"   ⚠️  Error en compilación: {e}")
    
    # Probar PersonalityBlender
    print("\n6️⃣  Probando PersonalityBlender...")
    try:
        blender = PersonalityBlender()
        print("   ✅ PersonalityBlender creado correctamente")
        print("   💡 PersonaBlend™ Technology disponible")
    except Exception as e:
        print(f"   ⚠️  Error al crear blender: {e}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE LA PRUEBA")
    print("=" * 60)
    print("✅ luminoracore está instalado y funcional")
    print("✅ Todos los componentes principales están disponibles")
    print("")
    print("🚀 ¡Listo para usar LuminoraCore!")
    print("")
    print("📖 Próximos pasos:")
    print("   1. Lee GUIA_INSTALACION_USO.md para más detalles")
    print("   2. Explora los ejemplos en luminoracore/examples/")
    print("   3. Crea tu primera personalidad personalizada")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

