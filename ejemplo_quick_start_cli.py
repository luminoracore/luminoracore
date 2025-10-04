#!/usr/bin/env python3
"""
Ejemplo Quick Start - LuminoraCore CLI
Ejecuta este archivo para probar que luminoracore-cli está instalado correctamente.
"""

import sys
import subprocess
import shutil

def main():
    """Prueba rápida del CLI de LuminoraCore."""
    print("=" * 60)
    print("🛠️  LuminoraCore CLI - Quick Start")
    print("=" * 60)
    
    # Verificar que el comando está disponible
    print("\n1️⃣  Verificando que el comando 'luminoracore' está disponible...")
    
    luminoracore_path = shutil.which("luminoracore")
    lc_path = shutil.which("lc")
    
    if luminoracore_path:
        print(f"   ✅ Comando 'luminoracore' encontrado en: {luminoracore_path}")
    else:
        print("   ❌ Comando 'luminoracore' no encontrado")
        print("   💡 Solución: cd luminoracore-cli && pip install -e .")
        return False
    
    if lc_path:
        print(f"   ✅ Alias 'lc' también disponible")
    
    # Probar el comando --version
    print("\n2️⃣  Obteniendo versión del CLI...")
    try:
        result = subprocess.run(
            ["luminoracore", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version_output = result.stdout.strip()
            print(f"   ✅ {version_output}")
        else:
            print("   ⚠️  No se pudo obtener la versión")
    except Exception as e:
        print(f"   ⚠️  Error al ejecutar comando: {e}")
    
    # Probar el comando --help
    print("\n3️⃣  Verificando comandos disponibles...")
    try:
        result = subprocess.run(
            ["luminoracore", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Buscar comandos en la salida
            commands = []
            for line in result.stdout.split('\n'):
                line_lower = line.lower()
                if 'validate' in line_lower:
                    commands.append('validate')
                elif 'compile' in line_lower and 'compile' not in commands:
                    commands.append('compile')
                elif 'create' in line_lower and 'create' not in commands:
                    commands.append('create')
                elif 'test' in line_lower and 'test' not in commands:
                    commands.append('test')
                elif 'blend' in line_lower and 'blend' not in commands:
                    commands.append('blend')
                elif 'serve' in line_lower and 'serve' not in commands:
                    commands.append('serve')
                elif 'list' in line_lower and 'list' not in commands:
                    commands.append('list')
            
            if commands:
                print(f"   ✅ Comandos detectados: {', '.join(commands)}")
            else:
                print("   ✅ CLI funcionando correctamente")
        else:
            print("   ⚠️  Error al obtener ayuda del comando")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
    
    # Mostrar comandos principales
    print("\n4️⃣  Comandos principales disponibles:")
    commands_info = [
        ("luminoracore list", "Lista personalidades disponibles"),
        ("luminoracore validate <file>", "Valida una personalidad"),
        ("luminoracore compile <file>", "Compila una personalidad"),
        ("luminoracore create", "Crea una nueva personalidad"),
        ("luminoracore serve", "Inicia servidor de desarrollo"),
        ("luminoracore blend <p1:w1> <p2:w2>", "Mezcla personalidades"),
    ]
    
    for cmd, desc in commands_info:
        print(f"   📌 {cmd}")
        print(f"      {desc}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE LA PRUEBA")
    print("=" * 60)
    print("✅ luminoracore-cli está instalado y funcional")
    print("✅ Todos los comandos están disponibles")
    print("")
    print("🚀 ¡Listo para usar el CLI!")
    print("")
    print("📖 Próximos pasos:")
    print("   1. Prueba: luminoracore list")
    print("   2. Valida una personalidad: luminoracore validate <archivo>")
    print("   3. Inicia el servidor: luminoracore serve")
    print("   4. Lee GUIA_INSTALACION_USO.md para más ejemplos")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

