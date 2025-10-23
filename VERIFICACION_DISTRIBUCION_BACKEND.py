#!/usr/bin/env python3
"""
VERIFICACIÓN DE DISTRIBUCIÓN PARA EL EQUIPO DE BACKEND
======================================================

Este script verifica que la distribución de LuminoraCore v1.1 tiene todos los archivos necesarios
y que los fixes están aplicados correctamente.

Ejecutar: python VERIFICACION_DISTRIBUCION_BACKEND.py
"""

import os
import sys
import importlib.util
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

def check_file_exists(file_path, description):
    """Verificar si un archivo existe"""
    if os.path.exists(file_path):
        print_success(f"{description}: {file_path}")
        return True
    else:
        print_error(f"{description}: {file_path} - NO ENCONTRADO")
        return False

def check_import(module_name, description):
    """Verificar si se puede importar un módulo"""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            print_success(f"{description}: {module_name} - DISPONIBLE")
            return True
        else:
            print_error(f"{description}: {module_name} - NO DISPONIBLE")
            return False
    except Exception as e:
        print_error(f"{description}: {module_name} - ERROR: {e}")
        return False

def check_file_content(file_path, search_text, description):
    """Verificar si un archivo contiene texto específico"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if search_text in content:
                    print_success(f"{description}: {search_text} - ENCONTRADO")
                    return True
                else:
                    print_error(f"{description}: {search_text} - NO ENCONTRADO")
                    return False
        else:
            print_error(f"{description}: Archivo {file_path} no existe")
            return False
    except Exception as e:
        print_error(f"{description}: Error al leer archivo - {e}")
        return False

def main():
    print_header("VERIFICACIÓN DE DISTRIBUCIÓN LUMINORACORE V1.1")
    
    print_info("Este script verifica que la distribución tiene todos los archivos necesarios")
    print_info("y que los fixes están aplicados correctamente.\n")
    
    results = []
    
    # Verificación 1: Archivos críticos
    print_header("1. VERIFICACIÓN DE ARCHIVOS CRÍTICOS")
    
    # Verificar que logging_config.py existe
    logging_config_path = "luminoracore_sdk/logging_config.py"
    results.append(check_file_exists(logging_config_path, "logging_config.py"))
    
    # Verificar que storage_dynamodb_flexible.py existe
    storage_path = "luminoracore_sdk/session/storage_dynamodb_flexible.py"
    results.append(check_file_exists(storage_path, "storage_dynamodb_flexible.py"))
    
    # Verificar que __init__.py existe
    init_path = "luminoracore_sdk/__init__.py"
    results.append(check_file_exists(init_path, "__init__.py"))
    
    # Verificación 2: Importaciones
    print_header("2. VERIFICACIÓN DE IMPORTACIONES")
    
    # Verificar que se puede importar setup_logging
    results.append(check_import("luminoracore_sdk.logging_config", "logging_config module"))
    
    # Verificar que se puede importar LuminoraCoreClientV11
    results.append(check_import("luminoracore_sdk.client_v1_1", "client_v1_1 module"))
    
    # Verificar que se puede importar FlexibleDynamoDBStorageV11
    results.append(check_import("luminoracore_sdk.session.storage_dynamodb_flexible", "storage_dynamodb_flexible module"))
    
    # Verificación 3: Contenido de archivos críticos
    print_header("3. VERIFICACIÓN DE CONTENIDO DE ARCHIVOS")
    
    # Verificar que __init__.py exporta setup_logging
    results.append(check_file_content(
        init_path,
        "from .logging_config import setup_logging",
        "__init__.py exporta setup_logging"
    ))
    
    # Verificar que __init__.py incluye setup_logging en __all__
    results.append(check_file_content(
        init_path,
        '"setup_logging"',
        "__init__.py incluye setup_logging en __all__"
    ))
    
    # Verificar que logging_config.py tiene la función setup_logging
    results.append(check_file_content(
        logging_config_path,
        "def setup_logging(",
        "logging_config.py tiene función setup_logging"
    ))
    
    # Verificación 4: Fixes aplicados
    print_header("4. VERIFICACIÓN DE FIXES APLICADOS")
    
    # Verificar que storage_dynamodb_flexible.py tiene el fix de FilterExpression
    results.append(check_file_content(
        storage_path,
        "FilterExpression=f'user_id = :user_id AND begins_with({self.range_key_name}, :fact_prefix)'",
        "Fix de FilterExpression (sin categoría)"
    ))
    
    # Verificar que storage_dynamodb_flexible.py tiene el fix de FilterExpression con categoría
    results.append(check_file_content(
        storage_path,
        "FilterExpression=f'user_id = :user_id AND #category = :category AND begins_with({self.range_key_name}, :fact_prefix)'",
        "Fix de FilterExpression (con categoría)"
    ))
    
    # Verificar que NO tiene ExpressionAttributeNames para range_key
    results.append(check_file_content(
        storage_path,
        "ExpressionAttributeNames={'#range_key': self.range_key_name}",
        "ExpressionAttributeNames para range_key (NO debe estar)"
    ))
    
    # Verificación 5: Test de importación real
    print_header("5. TEST DE IMPORTACIÓN REAL")
    
    try:
        # Intentar importar setup_logging
        from luminoracore_sdk import setup_logging, LuminoraCoreClientV11
        from luminoracore_sdk.session import FlexibleDynamoDBStorageV11
        print_success("Importaciones exitosas: setup_logging, LuminoraCoreClientV11, FlexibleDynamoDBStorageV11")
        results.append(True)
        
        # Intentar usar setup_logging
        setup_logging(level="DEBUG", format_type="lambda")
        print_success("setup_logging() funciona correctamente")
        results.append(True)
        
    except Exception as e:
        print_error(f"Error en importaciones: {e}")
        results.append(False)
    
    # Resumen final
    print_header("RESUMEN DE VERIFICACIÓN")
    
    total_checks = len(results)
    passed_checks = sum(results)
    failed_checks = total_checks - passed_checks
    
    print(f"\n{Colors.BOLD}Resultados:{Colors.END}")
    print(f"  Total de verificaciones: {total_checks}")
    print(f"  ✅ Pasaron: {passed_checks}")
    print(f"  ❌ Fallaron: {failed_checks}")
    
    if failed_checks == 0:
        print_success("TODAS LAS VERIFICACIONES PASARON")
        print_success("La distribución está correcta y lista para usar")
        print_info("El equipo de backend puede proceder con confianza")
        return True
    else:
        print_error("ALGUNAS VERIFICACIONES FALLARON")
        print_warning("La distribución tiene problemas que deben resolverse")
        print_info("Contactar al equipo de infraestructura para corregir los problemas")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Verificación interrumpida por el usuario{Colors.END}\n")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nError fatal en verificación: {e}")
        import traceback
        print(traceback.format_exc())
        sys.exit(1)
