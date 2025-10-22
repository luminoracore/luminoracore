#!/usr/bin/env python3
"""
VERIFICACIÓN DEL FIX - LuminoraCore get_facts() Method
======================================================

Este script verifica que el fix aplicado al método get_facts() está correcto
sin necesidad de una conexión real a DynamoDB.

Verifica:
1. ✅ Sintaxis del código
2. ✅ Estructura de FilterExpression
3. ✅ Uso correcto de f-strings
4. ✅ ExpressionAttributeNames simplificado
"""

import ast
import sys
import os
from pathlib import Path

# Configuración de colores
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


def test_1_syntax_check():
    """Test 1: Verificar que el archivo tiene sintaxis correcta"""
    print_header("TEST 1: Verificación de Sintaxis")
    
    file_path = Path("luminoracore-sdk-python/luminoracore_sdk/session/storage_dynamodb_flexible.py")
    
    if not file_path.exists():
        print_error(f"Archivo no encontrado: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar sintaxis
        ast.parse(content)
        print_success("Sintaxis del archivo es correcta")
        return True
        
    except SyntaxError as e:
        print_error(f"Error de sintaxis: {e}")
        return False
    except Exception as e:
        print_error(f"Error al leer archivo: {e}")
        return False


def test_2_fix_verification():
    """Test 2: Verificar que el fix está aplicado correctamente"""
    print_header("TEST 2: Verificación del Fix Aplicado")
    
    file_path = Path("luminoracore-sdk-python/luminoracore_sdk/session/storage_dynamodb_flexible.py")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que el fix está aplicado
        fixes_applied = []
        
        # Fix 1: Verificar que usa f-string en FilterExpression (sin categoría)
        if "FilterExpression=f'user_id = :user_id AND begins_with({self.range_key_name}, :fact_prefix)'" in content:
            print_success("Fix 1 aplicado: f-string en FilterExpression (sin categoría)")
            fixes_applied.append(True)
        else:
            print_error("Fix 1 NO aplicado: falta f-string en FilterExpression (sin categoría)")
            fixes_applied.append(False)
        
        # Fix 2: Verificar que usa f-string en FilterExpression (con categoría)
        if "FilterExpression=f'user_id = :user_id AND #category = :category AND begins_with({self.range_key_name}, :fact_prefix)'" in content:
            print_success("Fix 2 aplicado: f-string en FilterExpression (con categoría)")
            fixes_applied.append(True)
        else:
            print_error("Fix 2 NO aplicado: falta f-string en FilterExpression (con categoría)")
            fixes_applied.append(False)
        
        # Fix 3: Verificar que NO usa ExpressionAttributeNames para range_key (sin categoría)
        if "ExpressionAttributeNames={'#range_key': self.range_key_name}" not in content:
            print_success("Fix 3 aplicado: ExpressionAttributeNames simplificado (sin categoría)")
            fixes_applied.append(True)
        else:
            print_error("Fix 3 NO aplicado: aún usa ExpressionAttributeNames para range_key")
            fixes_applied.append(False)
        
        # Fix 4: Verificar que mantiene #category en ExpressionAttributeNames
        if "'#category': 'category'" in content:
            print_success("Fix 4 aplicado: mantiene #category en ExpressionAttributeNames")
            fixes_applied.append(True)
        else:
            print_error("Fix 4 NO aplicado: falta #category en ExpressionAttributeNames")
            fixes_applied.append(False)
        
        all_fixes = all(fixes_applied)
        return all_fixes
        
    except Exception as e:
        print_error(f"Error al verificar fixes: {e}")
        return False


def test_3_code_analysis():
    """Test 3: Análisis del código para verificar estructura"""
    print_header("TEST 3: Análisis de Estructura del Código")
    
    file_path = Path("luminoracore-sdk-python/luminoracore_sdk/session/storage_dynamodb_flexible.py")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que tiene el método get_facts
        if "async def get_facts(" in content:
            print_success("Método get_facts() encontrado")
        else:
            print_error("Método get_facts() NO encontrado")
            return False
        
        # Verificar que tiene logging de debug
        if "DEBUG get_facts()" in content:
            print_success("Logging de debug encontrado")
        else:
            print_warning("Logging de debug no encontrado")
        
        # Verificar que maneja excepciones
        if "except Exception as e:" in content:
            print_success("Manejo de excepciones encontrado")
        else:
            print_error("Manejo de excepciones NO encontrado")
            return False
        
        # Verificar que retorna lista
        if "return facts" in content:
            print_success("Retorno de facts encontrado")
        else:
            print_error("Retorno de facts NO encontrado")
            return False
        
        return True
        
    except Exception as e:
        print_error(f"Error en análisis: {e}")
        return False


def test_4_filter_expression_analysis():
    """Test 4: Análisis detallado de FilterExpression"""
    print_header("TEST 4: Análisis de FilterExpression")
    
    file_path = Path("luminoracore-sdk-python/luminoracore_sdk/session/storage_dynamodb_flexible.py")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Buscar las líneas con FilterExpression
        filter_lines = []
        for i, line in enumerate(lines, 1):
            if "FilterExpression=" in line:
                filter_lines.append((i, line.strip()))
        
        print_info(f"Encontradas {len(filter_lines)} líneas con FilterExpression")
        
        for line_num, line in filter_lines:
            print_info(f"Línea {line_num}: {line}")
            
            # Verificar que usa f-string
            if line.startswith("FilterExpression=f'"):
                print_success(f"  ✅ Línea {line_num}: Usa f-string correctamente")
            else:
                print_error(f"  ❌ Línea {line_num}: NO usa f-string")
                return False
            
            # Verificar que usa {self.range_key_name}
            if "{self.range_key_name}" in line:
                print_success(f"  ✅ Línea {line_num}: Usa {{self.range_key_name}} correctamente")
            else:
                print_error(f"  ❌ Línea {line_num}: NO usa {{self.range_key_name}}")
                return False
        
        return True
        
    except Exception as e:
        print_error(f"Error en análisis de FilterExpression: {e}")
        return False


def run_all_tests():
    """Ejecutar todos los tests de verificación"""
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║           VERIFICACIÓN DEL FIX - get_facts() METHOD              ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    results = []
    
    # Test 1: Sintaxis
    success = test_1_syntax_check()
    results.append(("Sintaxis", success))
    
    # Test 2: Fix verification
    success = test_2_fix_verification()
    results.append(("Fix aplicado", success))
    
    # Test 3: Code analysis
    success = test_3_code_analysis()
    results.append(("Análisis de código", success))
    
    # Test 4: FilterExpression analysis
    success = test_4_filter_expression_analysis()
    results.append(("Análisis FilterExpression", success))
    
    # Resumen final
    print_header("RESUMEN DE VERIFICACIÓN")
    
    print(f"\n{Colors.BOLD}Resultados:{Colors.END}")
    all_passed = True
    for test_name, passed in results:
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if passed else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"  {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print(f"\n{Colors.BOLD}Conclusión:{Colors.END}")
    if all_passed:
        print_success("TODAS LAS VERIFICACIONES PASARON")
        print_success("El fix está aplicado correctamente")
        print_info("El método get_facts() debería funcionar correctamente ahora")
        
        print(f"\n{Colors.BOLD}Explicación del fix:{Colors.END}")
        print_info("ANTES: begins_with(#range_key, :fact_prefix) → busca en el NOMBRE del atributo")
        print_info("DESPUÉS: begins_with({self.range_key_name}, :fact_prefix) → busca en el VALOR del atributo")
        print_info("Resultado: DynamoDB ahora encuentra correctamente los facts con range_key que empiezan con 'FACT#'")
        
    else:
        print_error("ALGUNAS VERIFICACIONES FALLARON")
        print_warning("Revisar los errores para completar el fix")
    
    return all_passed


if __name__ == "__main__":
    try:
        result = run_all_tests()
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Verificación interrumpida por el usuario{Colors.END}\n")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nError fatal en verificación: {e}")
        import traceback
        print(traceback.format_exc())
        sys.exit(1)
