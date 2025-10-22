#!/usr/bin/env python3
"""
EJECUTOR DE PRUEBAS COMPLETAS PARA LUMINORACORE SDK

Este archivo ejecuta todas las pruebas de manera organizada y proporciona
un resumen completo de los resultados.
"""

import unittest
import sys
import os
import time
from datetime import datetime

# Agregar el directorio actual al path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar todos los tests
from test_logging_fix import run_all_tests as run_logging_tests
from test_validation_fix import run_all_tests as run_validation_tests
from test_aws_credentials_fix import run_all_tests as run_aws_credentials_tests
from test_improved_methods import run_all_tests as run_improved_methods_tests
from test_complete_integration import run_all_tests as run_integration_tests


class TestRunner:
    """Ejecutor de pruebas completo."""
    
    def __init__(self):
        """Inicializar el ejecutor de pruebas."""
        self.test_results = {}
        self.start_time = None
        self.end_time = None
    
    def run_all_tests(self):
        """Ejecutar todas las pruebas."""
        print("🚀 INICIANDO EJECUCIÓN COMPLETA DE PRUEBAS LUMINORACORE SDK")
        print("=" * 80)
        print(f"⏰ Hora de inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        self.start_time = time.time()
        
        # Ejecutar cada suite de pruebas
        test_suites = [
            ("Logging Fix", run_logging_tests),
            ("Validation Fix", run_validation_tests),
            ("AWS Credentials Fix", run_aws_credentials_tests),
            ("Improved Methods", run_improved_methods_tests),
            ("Complete Integration", run_integration_tests)
        ]
        
        for suite_name, test_function in test_suites:
            print(f"\n🧪 EJECUTANDO PRUEBAS: {suite_name}")
            print("-" * 60)
            
            try:
                success = test_function()
                self.test_results[suite_name] = {
                    "success": success,
                    "error": None
                }
                
                if success:
                    print(f"✅ {suite_name}: TODAS LAS PRUEBAS PASARON")
                else:
                    print(f"❌ {suite_name}: ALGUNAS PRUEBAS FALLARON")
                    
            except Exception as e:
                print(f"💥 {suite_name}: ERROR EN EJECUCIÓN - {str(e)}")
                self.test_results[suite_name] = {
                    "success": False,
                    "error": str(e)
                }
        
        self.end_time = time.time()
        self.print_final_summary()
        
        return self.all_tests_passed()
    
    def print_final_summary(self):
        """Imprimir resumen final."""
        print("\n" + "=" * 80)
        print("📊 RESUMEN FINAL DE TODAS LAS PRUEBAS")
        print("=" * 80)
        
        total_suites = len(self.test_results)
        passed_suites = sum(1 for result in self.test_results.values() if result["success"])
        failed_suites = total_suites - passed_suites
        
        print(f"⏰ Tiempo total de ejecución: {self.end_time - self.start_time:.2f} segundos")
        print(f"📦 Total de suites de pruebas: {total_suites}")
        print(f"✅ Suites exitosas: {passed_suites}")
        print(f"❌ Suites fallidas: {failed_suites}")
        
        print("\n📋 DETALLE POR SUITE:")
        for suite_name, result in self.test_results.items():
            status = "✅ ÉXITO" if result["success"] else "❌ FALLO"
            print(f"  {suite_name}: {status}")
            if result["error"]:
                print(f"    Error: {result['error']}")
        
        print("\n" + "=" * 80)
        
        if self.all_tests_passed():
            print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
            print("✨ El SDK está listo para producción")
        else:
            print("💥 ALGUNAS PRUEBAS FALLARON")
            print("🔧 Revisar los errores antes de continuar")
        
        print("=" * 80)
    
    def all_tests_passed(self):
        """Verificar si todas las pruebas pasaron."""
        return all(result["success"] for result in self.test_results.values())
    
    def get_test_summary(self):
        """Obtener resumen de las pruebas."""
        return {
            "total_suites": len(self.test_results),
            "passed_suites": sum(1 for result in self.test_results.values() if result["success"]),
            "failed_suites": sum(1 for result in self.test_results.values() if not result["success"]),
            "execution_time": self.end_time - self.start_time if self.end_time and self.start_time else 0,
            "all_passed": self.all_tests_passed(),
            "results": self.test_results
        }


def main():
    """Función principal."""
    try:
        runner = TestRunner()
        success = runner.run_all_tests()
        
        # Retornar código de salida apropiado
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Ejecución interrumpida por el usuario")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n💥 Error inesperado en el ejecutor de pruebas: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
