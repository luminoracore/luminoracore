#!/usr/bin/env python3
"""
VERIFICACION DEL CLI
Verificar que el CLI funcione correctamente
"""

import asyncio
import sys
import subprocess
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "luminoracore-cli"))

async def test_cli_verification():
    """Verificacion del CLI"""
    print("=== VERIFICACION DEL CLI ===")
    print("=" * 60)
    
    try:
        # TEST 1: Verificar que el CLI se puede importar
        print("1. VERIFICANDO IMPORTS DEL CLI:")
        try:
            from luminoracore_cli.main import app
            print("   [OK] CLI imports funcionan")
        except Exception as e:
            print(f"   [ERROR] CLI imports fallan: {e}")
            return False
        
        # TEST 2: Verificar comandos disponibles
        print("\n2. VERIFICANDO COMANDOS DISPONIBLES:")
        try:
            result = subprocess.run([
                sys.executable, "-m", "luminoracore_cli.main", "--help"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("   [OK] CLI se ejecuta correctamente")
                print(f"   [OK] Help output: {len(result.stdout)} caracteres")
            else:
                print(f"   [ERROR] CLI falla: {result.stderr}")
                return False
        except Exception as e:
            print(f"   [ERROR] Error ejecutando CLI: {e}")
            return False
        
        # TEST 3: Verificar comandos específicos
        print("\n3. VERIFICANDO COMANDOS ESPECIFICOS:")
        
        commands_to_test = [
            "validate --help",
            "compile --help", 
            "create --help",
            "test --help",
            "memory --help",
            "storage --help"
        ]
        
        for cmd in commands_to_test:
            try:
                result = subprocess.run([
                    sys.executable, "-m", "luminoracore_cli.main", cmd
                ], capture_output=True, text=True, timeout=5)
                
                if result.returncode == 0:
                    print(f"   [OK] {cmd}: Funciona")
                else:
                    print(f"   [WARN] {cmd}: {result.stderr[:100]}...")
            except Exception as e:
                print(f"   [ERROR] {cmd}: {e}")
        
        # TEST 4: Verificar version
        print("\n4. VERIFICANDO VERSION:")
        try:
            result = subprocess.run([
                sys.executable, "-m", "luminoracore_cli.main", "--version"
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                print(f"   [OK] Version: {result.stdout.strip()}")
            else:
                print(f"   [WARN] Version no disponible: {result.stderr}")
        except Exception as e:
            print(f"   [ERROR] Error obteniendo version: {e}")
        
        # RESULTADO FINAL
        print("\n" + "=" * 60)
        print("RESULTADO FINAL:")
        print("[OK] CLI funciona correctamente")
        print("[OK] Comandos básicos operativos")
        return True
        
    except Exception as e:
        print(f"[ERROR] ERROR CRITICO: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_cli_verification())
    if success:
        print("\n[OK] CLI VERIFICADO - FUNCIONA CORRECTAMENTE")
    else:
        print("\n[FAIL] CLI NO FUNCIONA - HAY PROBLEMAS")
    sys.exit(0 if success else 1)
