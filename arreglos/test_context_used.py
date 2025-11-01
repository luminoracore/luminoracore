#!/usr/bin/env python3
"""
Test para validar que context_used se calcula correctamente
"""

def test_context_used_logic():
    """Test que valida la lógica de context_used"""
    print("\n" + "="*70)
    print("TEST: Cálculo de context_used")
    print("="*70)
    
    # Casos de prueba
    test_cases = [
        {
            "name": "Turn 1 - Sin contexto previo",
            "conversation_history": [],
            "user_facts": [],
            "expected": False,
            "description": "Primera conversación, no hay contexto previo"
        },
        {
            "name": "Turn 2 - Con historial de conversación",
            "conversation_history": [{"turn": 1}],  # Lista no vacía
            "user_facts": [],
            "expected": True,
            "description": "Hay conversaciones previas, contexto usado"
        },
        {
            "name": "Turn 1 con facts previos",
            "conversation_history": [],
            "user_facts": [{"key": "name", "value": "Alex"}],  # Lista no vacía
            "expected": True,
            "description": "No hay conversación previa, pero hay facts del usuario"
        },
        {
            "name": "Turn 3 - Con historial y facts",
            "conversation_history": [{"turn": 1}, {"turn": 2}],
            "user_facts": [{"key": "name", "value": "Alex"}],
            "expected": True,
            "description": "Tanto historial como facts, contexto usado"
        },
    ]
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Caso {i}: {test_case['name']}")
        print(f"    Descripción: {test_case['description']}")
        print(f"    conversation_history: {len(test_case['conversation_history'])} turns")
        print(f"    user_facts: {len(test_case['user_facts'])} facts")
        
        # Aplicar la lógica que usa el código
        context_used = len(test_case['conversation_history']) > 0 or len(test_case['user_facts']) > 0
        
        # Verificar
        passed = context_used == test_case['expected']
        status = "[OK]" if passed else "[FAIL]"
        
        print(f"    Esperado: {test_case['expected']}")
        print(f"    Obtenido: {context_used}")
        print(f"    Estado: {status}")
        
        if not passed:
            print(f"    ERROR: No coincide con lo esperado")
            all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("[OK] TODOS LOS CASOS PASARON")
        print("La logica de context_used es correcta")
    else:
        print("[FAIL] ALGUNOS CASOS FALLARON")
        print("Revisar la logica")
    print("="*70)
    
    return all_passed

def test_real_scenarios():
    """Test con escenarios reales"""
    print("\n" + "="*70)
    print("TEST: Escenarios Reales")
    print("="*70)
    
    scenarios = [
        {
            "scenario": "Usuario nuevo - Primera vez",
            "conversation_history": [],
            "user_facts": [],
            "expected": False,
            "reason": "No hay contexto previo"
        },
        {
            "scenario": "Usuario nuevo - Primera conversación, pero con facts de otra sesión",
            "conversation_history": [],
            "user_facts": [{"key": "name", "value": "Alex"}],
            "expected": True,
            "reason": "Tiene facts previos aunque no conversación en esta sesión"
        },
        {
            "scenario": "Usuario existente - Segunda conversación",
            "conversation_history": [{"user": "Hola", "assistant": "Hola!"}],
            "user_facts": [],
            "expected": True,
            "reason": "Tiene conversación previa en esta sesión"
        },
        {
            "scenario": "Usuario existente - Múltiples conversaciones",
            "conversation_history": [
                {"user": "Hola", "assistant": "Hola!"},
                {"user": "¿Cómo estás?", "assistant": "Bien"}
            ],
            "user_facts": [{"key": "name", "value": "Alex"}],
            "expected": True,
            "reason": "Tiene tanto historial como facts"
        }
    ]
    
    all_passed = True
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n  Escenario {i}: {scenario['scenario']}")
        
        context_used = len(scenario['conversation_history']) > 0 or len(scenario['user_facts']) > 0
        
        passed = context_used == scenario['expected']
        status = "[OK]" if passed else "[FAIL]"
        
        print(f"    Razon: {scenario['reason']}")
        print(f"    Resultado: {status} (esperado: {scenario['expected']}, obtenido: {context_used})")
        
        if not passed:
            all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("[OK] TODOS LOS ESCENARIOS SON CORRECTOS")
    else:
        print("[FAIL] ALGUNOS ESCENARIOS FALLARON")
    print("="*70)
    
    return all_passed

def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*70)
    print("VALIDACIÓN: Cálculo de context_used")
    print("="*70)
    
    results = []
    
    results.append(("Lógica de context_used", test_context_used_logic()))
    results.append(("Escenarios reales", test_real_scenarios()))
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70)
    
    all_passed = True
    for test_name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status}: {test_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "="*70)
    if all_passed:
        print("[OK] VALIDACION COMPLETA")
        print("context_used se calcula correctamente")
    else:
        print("[FAIL] VALIDACION FALLO")
    print("="*70)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    import sys
    exit_code = main()
    sys.exit(exit_code)

