#!/usr/bin/env python
"""
Runner principal para la Test Suite de LuminoraCore
Ejecuta todos los tests o suites específicas con reportes detallados
"""
import sys
import os
import subprocess
import argparse
from pathlib import Path

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Imprime un header bonito."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}")
    print(f"{text}")
    print(f"{'='*70}{Colors.RESET}\n")

def run_command(cmd, description):
    """
    Ejecuta un comando y retorna True si exitoso.
    """
    print(f"{Colors.BLUE}▶ {description}{Colors.RESET}")
    print(f"{Colors.YELLOW}  Comando: {' '.join(cmd)}{Colors.RESET}\n")
    
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n{Colors.GREEN}✅ {description} - EXITOSO{Colors.RESET}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n{Colors.RED}❌ {description} - FALLO (exit code: {e.returncode}){Colors.RESET}")
        return False
    except FileNotFoundError:
        print(f"\n{Colors.RED}❌ ERROR: pytest no encontrado. Instala: pip install pytest{Colors.RESET}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Runner de Test Suite para LuminoraCore",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python run_tests.py                    # Ejecutar todos los tests
  python run_tests.py --suite 1          # Solo Motor Base
  python run_tests.py --critical         # Solo tests críticos
  python run_tests.py --coverage         # Con reporte de coverage
  python run_tests.py --quick            # Sin API calls ni DB
        """
    )
    
    parser.add_argument(
        '--suite',
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        help='Ejecutar suite específica (1-6)'
    )
    
    parser.add_argument(
        '--critical',
        action='store_true',
        help='Solo tests marcados como critical'
    )
    
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Generar reporte de coverage'
    )
    
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Skip tests que requieren API o DB'
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Output verbose'
    )
    
    parser.add_argument(
        '--html',
        action='store_true',
        help='Generar reporte HTML'
    )
    
    args = parser.parse_args()
    
    # Print header
    print_header("🧪 LUMINORACORE TEST SUITE RUNNER")
    
    # Verificar que pytest esté instalado
    try:
        subprocess.run(['pytest', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Colors.RED}❌ ERROR: pytest no instalado{Colors.RESET}")
        print(f"   Instala: pip install pytest pytest-asyncio pytest-cov")
        sys.exit(1)
    
    # Construir comando pytest
    cmd = ['pytest']
    
    # Suite específica
    if args.suite:
        suite_map = {
            1: "tests/test_1_motor_base.py",
            2: "tests/test_2_cli.py",
            3: "tests/test_3_providers.py",
            4: "tests/test_4_storage.py",
            5: "tests/test_5_sessions.py",
            6: "tests/test_6_integration.py",
        }
        test_file = suite_map[args.suite]
        
        if not os.path.exists(test_file):
            print(f"{Colors.YELLOW}⚠️  WARNING: {test_file} no existe aún{Colors.RESET}")
            print(f"   Suite {args.suite} pendiente de implementación")
            sys.exit(1)
        
        cmd.append(test_file)
        description = f"Test Suite {args.suite}"
    else:
        cmd.append('tests/')
        description = "TODAS las Test Suites"
    
    # Marcas
    if args.critical:
        cmd.extend(['-m', 'critical'])
        description += " (solo críticos)"
    
    if args.quick:
        cmd.extend(['-m', 'not requires_api and not requires_db'])
        description += " (sin API/DB)"
    
    # Verbosidad
    if args.verbose:
        cmd.append('-vv')
    else:
        cmd.append('-v')
    
    # Coverage
    if args.coverage:
        cmd.extend([
            '--cov=luminoracore',
            '--cov-report=term-missing'
        ])
        
        if args.html:
            cmd.append('--cov-report=html')
    
    # Adicionales
    cmd.extend([
        '--tb=short',  # Traceback corto
        '--strict-markers',  # Marcas estrictas
    ])
    
    # Ejecutar
    success = run_command(cmd, description)
    
    # Resumen
    print_header("📊 RESUMEN")
    
    if success:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ TODOS LOS TESTS PASARON{Colors.RESET}\n")
        
        if args.coverage and args.html:
            print(f"{Colors.CYAN}📈 Reporte de coverage generado:{Colors.RESET}")
            print(f"   htmlcov/index.html\n")
        
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ ALGUNOS TESTS FALLARON{Colors.RESET}\n")
        print(f"{Colors.YELLOW}Revisa los errores arriba y corrige.{Colors.RESET}")
        print(f"{Colors.YELLOW}Para más detalles: pytest tests/ -vv{Colors.RESET}\n")
        
        return 1

if __name__ == "__main__":
    sys.exit(main())

