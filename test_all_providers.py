"""
Test Suite Completa - LuminoraCore SDK
Prueba TODOS los providers con APIs reales (requiere API keys)
"""
import asyncio
import os
import sys
from typing import Dict, List, Optional
from datetime import datetime

# Configurar encoding para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from luminoracore import LuminoraCoreClient
from luminoracore.types import ProviderConfig

# Configuración de providers
PROVIDERS = {
    "openai": {
        "env_key": "OPENAI_API_KEY",
        "model": "gpt-3.5-turbo",
        "url": "https://platform.openai.com/api-keys",
    },
    "anthropic": {
        "env_key": "ANTHROPIC_API_KEY",
        "model": "claude-3-haiku-20240307",
        "url": "https://console.anthropic.com/settings/keys",
    },
    "deepseek": {
        "env_key": "DEEPSEEK_API_KEY",
        "model": "deepseek-chat",
        "url": "https://platform.deepseek.com/api_keys",
    },
    "mistral": {
        "env_key": "MISTRAL_API_KEY",
        "model": "mistral-tiny",
        "url": "https://console.mistral.ai/api-keys/",
    },
    "cohere": {
        "env_key": "COHERE_API_KEY",
        "model": "command",
        "url": "https://dashboard.cohere.com/api-keys",
    },
    "google": {
        "env_key": "GOOGLE_API_KEY",
        "model": "gemini-pro",
        "url": "https://makersuite.google.com/app/apikey",
    },
    "llama": {
        "env_key": "REPLICATE_API_TOKEN",
        "model": "llama-2-7b-chat",
        "url": "https://replicate.com/account/api-tokens",
    },
}

# Mensaje de prueba simple
TEST_MESSAGE = "Di 'OK' si me entiendes. Nada más."

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

class TestResult:
    def __init__(self, provider: str):
        self.provider = provider
        self.api_key_configured = False
        self.connection_success = False
        self.response_received = False
        self.response_content = None
        self.error = None
        self.duration = 0.0

async def test_provider(provider_name: str, config: Dict) -> TestResult:
    """
    Prueba un provider específico.
    """
    result = TestResult(provider_name)
    
    print(f"\n{'='*70}")
    print(f"{Colors.CYAN}PROBANDO: {provider_name.upper()}{Colors.RESET}")
    print(f"{'='*70}")
    
    # 1. Verificar API key
    api_key = os.environ.get(config["env_key"])
    if not api_key:
        print(f"{Colors.YELLOW}⚠️  API Key no configurada: {config['env_key']}{Colors.RESET}")
        print(f"   Configura: $env:{config['env_key']}='tu-key'")
        print(f"   Obtén una en: {config['url']}")
        result.error = "API key not configured"
        return result
    
    result.api_key_configured = True
    print(f"{Colors.GREEN}✅ API Key configurada{Colors.RESET}")
    
    # 2. Crear cliente y configuración
    try:
        client = LuminoraCoreClient()
        await client.initialize()
        print(f"{Colors.GREEN}✅ Cliente inicializado{Colors.RESET}")
        
        provider_config = ProviderConfig(
            name=provider_name,
            api_key=api_key,
            model=config["model"]
        )
        
        # 3. Crear personalidad simple
        personality = {
            "name": f"test_{provider_name}",
            "description": "Bot de prueba",
            "system_prompt": "Eres un asistente de prueba. Responde de forma muy breve."
        }
        
        await client.load_personality(f"test_{provider_name}", personality)
        
        # 4. Crear sesión
        session_id = await client.create_session(
            personality_name=f"test_{provider_name}",
            provider_config=provider_config
        )
        
        result.connection_success = True
        print(f"{Colors.GREEN}✅ Conexión exitosa - Sesión: {session_id[:8]}...{Colors.RESET}")
        
        # 5. Enviar mensaje de prueba
        print(f"{Colors.BLUE}💬 Enviando mensaje: '{TEST_MESSAGE}'{Colors.RESET}")
        
        start_time = datetime.now()
        response = await client.send_message(
            session_id=session_id,
            message=TEST_MESSAGE
        )
        end_time = datetime.now()
        
        result.duration = (end_time - start_time).total_seconds()
        result.response_received = True
        result.response_content = response.content
        
        print(f"{Colors.GREEN}✅ Respuesta recibida ({result.duration:.2f}s){Colors.RESET}")
        print(f"{Colors.CYAN}📝 Respuesta:{Colors.RESET} {response.content[:100]}")
        
        # 6. Limpieza
        await client.cleanup()
        
        return result
        
    except Exception as e:
        result.error = str(e)
        print(f"{Colors.RED}❌ ERROR: {e}{Colors.RESET}")
        print(f"{Colors.YELLOW}   Tipo: {type(e).__name__}{Colors.RESET}")
        
        # Intentar limpiar
        try:
            await client.cleanup()
        except:
            pass
        
        return result

async def run_all_tests():
    """
    Ejecuta pruebas de todos los providers.
    """
    print(f"\n{Colors.BOLD}{'='*70}")
    print(f"SUITE DE PRUEBAS COMPLETA - LUMINORACORE SDK")
    print(f"{'='*70}{Colors.RESET}")
    print(f"\n{Colors.CYAN}Probando {len(PROVIDERS)} providers con APIs reales...{Colors.RESET}\n")
    
    results: List[TestResult] = []
    
    for provider_name, config in PROVIDERS.items():
        result = await test_provider(provider_name, config)
        results.append(result)
        
        # Pequeña pausa entre tests
        await asyncio.sleep(1)
    
    # Resumen final
    print(f"\n\n{Colors.BOLD}{'='*70}")
    print(f"RESUMEN DE RESULTADOS")
    print(f"{'='*70}{Colors.RESET}\n")
    
    # Tabla de resultados
    print(f"{'Provider':<12} {'API Key':<10} {'Conexión':<12} {'Respuesta':<12} {'Tiempo':<10} {'Estado'}")
    print(f"{'-'*70}")
    
    success_count = 0
    skipped_count = 0
    failed_count = 0
    
    for result in results:
        api_status = f"{Colors.GREEN}✅{Colors.RESET}" if result.api_key_configured else f"{Colors.YELLOW}⚪{Colors.RESET}"
        conn_status = f"{Colors.GREEN}✅{Colors.RESET}" if result.connection_success else f"{Colors.RED}❌{Colors.RESET}"
        resp_status = f"{Colors.GREEN}✅{Colors.RESET}" if result.response_received else f"{Colors.RED}❌{Colors.RESET}"
        time_str = f"{result.duration:.2f}s" if result.duration > 0 else "-"
        
        if result.response_received:
            status = f"{Colors.GREEN}ÉXITO{Colors.RESET}"
            success_count += 1
        elif not result.api_key_configured:
            status = f"{Colors.YELLOW}OMITIDO{Colors.RESET}"
            skipped_count += 1
        else:
            status = f"{Colors.RED}FALLO{Colors.RESET}"
            failed_count += 1
        
        print(f"{result.provider:<12} {api_status:<10} {conn_status:<12} {resp_status:<12} {time_str:<10} {status}")
    
    print(f"\n{Colors.BOLD}ESTADÍSTICAS:{Colors.RESET}")
    print(f"  {Colors.GREEN}✅ Éxitos:  {success_count}/{len(PROVIDERS)}{Colors.RESET}")
    print(f"  {Colors.RED}❌ Fallos:  {failed_count}/{len(PROVIDERS)}{Colors.RESET}")
    print(f"  {Colors.YELLOW}⚪ Omitidos: {skipped_count}/{len(PROVIDERS)} (sin API key){Colors.RESET}")
    
    # Recomendaciones
    print(f"\n{Colors.BOLD}RECOMENDACIONES:{Colors.RESET}")
    
    if skipped_count > 0:
        print(f"\n{Colors.YELLOW}⚠️  Algunos providers no fueron probados (falta API key):{Colors.RESET}")
        for result in results:
            if not result.api_key_configured:
                config = PROVIDERS[result.provider]
                print(f"  • {result.provider}: {config['url']}")
    
    if failed_count > 0:
        print(f"\n{Colors.RED}❌ Algunos providers fallaron:{Colors.RESET}")
        for result in results:
            if result.error and result.api_key_configured:
                print(f"  • {result.provider}: {result.error[:80]}")
    
    if success_count == len(PROVIDERS):
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ¡TODOS LOS PROVIDERS FUNCIONAN CORRECTAMENTE!{Colors.RESET}")
    elif success_count > 0 and failed_count == 0:
        print(f"\n{Colors.GREEN}✅ Todos los providers configurados funcionan.{Colors.RESET}")
        print(f"{Colors.YELLOW}   Configura más API keys para probar el resto.{Colors.RESET}")
    
    print(f"\n{'='*70}\n")
    
    return results

if __name__ == "__main__":
    print(f"\n{Colors.CYAN}Iniciando suite de pruebas...{Colors.RESET}")
    
    try:
        results = asyncio.run(run_all_tests())
        
        # Exit code basado en resultados
        failed = sum(1 for r in results if r.error and r.api_key_configured)
        sys.exit(0 if failed == 0 else 1)
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Pruebas interrumpidas por el usuario{Colors.RESET}\n")
        sys.exit(2)
    except Exception as e:
        print(f"\n\n{Colors.RED}❌ ERROR FATAL: {e}{Colors.RESET}\n")
        import traceback
        traceback.print_exc()
        sys.exit(3)

