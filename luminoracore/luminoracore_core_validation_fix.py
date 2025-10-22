"""
SOLUCIÓN PARA PROBLEMAS DE VALIDACIÓN EN LUMINORACORE CORE

Este archivo resuelve los problemas de validación y manejo de errores en los métodos críticos del core.
"""

import logging
import traceback
from typing import List, Optional, Dict, Any, Union
from datetime import datetime


logger = logging.getLogger(__name__)


class CoreValidationError(Exception):
    """Excepción personalizada para errores de validación del core."""
    pass


class LuminoraCoreValidationManager:
    """
    Manager de validación para LuminoraCore Core que proporciona validación robusta
    y manejo de errores para todas las operaciones del core.
    """
    
    def __init__(self):
        self.validation_enabled = True
        self.debug_mode = False
    
    def enable_debug_mode(self, enabled: bool = True):
        """Habilitar modo debug para logging detallado."""
        self.debug_mode = enabled
        if enabled:
            logger.info("Modo debug habilitado para validación del core")
    
    def validate_personality_data(self, personality_data: Dict[str, Any]) -> bool:
        """
        Validar datos de personalidad.
        
        Args:
            personality_data: Datos de personalidad a validar
            
        Returns:
            True si los datos son válidos
            
        Raises:
            CoreValidationError: Si los datos son inválidos
        """
        if not self.validation_enabled:
            return True
        
        if not personality_data:
            error_msg = "Datos de personalidad no pueden estar vacíos"
            logger.error(error_msg)
            raise CoreValidationError(error_msg)
        
        # Validar estructura básica
        required_fields = ['persona', 'core_traits', 'linguistic_profile', 'behavioral_rules']
        for field in required_fields:
            if field not in personality_data:
                error_msg = f"Campo requerido '{field}' no encontrado en datos de personalidad"
                logger.error(error_msg)
                raise CoreValidationError(error_msg)
        
        if self.debug_mode:
            logger.debug("Datos de personalidad válidos")
        
        return True
    
    def validate_fact_data(self, fact_data: Dict[str, Any]) -> bool:
        """
        Validar datos de fact.
        
        Args:
            fact_data: Datos de fact a validar
            
        Returns:
            True si los datos son válidos
            
        Raises:
            CoreValidationError: Si los datos son inválidos
        """
        if not self.validation_enabled:
            return True
        
        if not fact_data:
            error_msg = "Datos de fact no pueden estar vacíos"
            logger.error(error_msg)
            raise CoreValidationError(error_msg)
        
        # Validar campos requeridos
        required_fields = ['user_id', 'category', 'key', 'value']
        for field in required_fields:
            if field not in fact_data:
                error_msg = f"Campo requerido '{field}' no encontrado en datos de fact"
                logger.error(error_msg)
                raise CoreValidationError(error_msg)
        
        # Validar confidence
        confidence = fact_data.get('confidence', 1.0)
        if not isinstance(confidence, (int, float)) or not (0.0 <= confidence <= 1.0):
            error_msg = f"Confidence debe ser un número entre 0.0 y 1.0, recibido: {confidence}"
            logger.error(error_msg)
            raise CoreValidationError(error_msg)
        
        if self.debug_mode:
            logger.debug("Datos de fact válidos")
        
        return True
    
    def validate_user_id(self, user_id: str) -> bool:
        """
        Validar user_id.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            True si el user_id es válido
            
        Raises:
            CoreValidationError: Si el user_id es inválido
        """
        if not self.validation_enabled:
            return True
        
        if not user_id:
            error_msg = "user_id no puede estar vacío"
            logger.error(error_msg)
            raise CoreValidationError(error_msg)
        
        if not isinstance(user_id, str):
            error_msg = f"user_id debe ser string, recibido: {type(user_id)}"
            logger.error(error_msg)
            raise CoreValidationError(error_msg)
        
        if len(user_id.strip()) == 0:
            error_msg = "user_id no puede ser solo espacios en blanco"
            logger.error(error_msg)
            raise CoreValidationError(error_msg)
        
        if self.debug_mode:
            logger.debug(f"user_id válido: {user_id}")
        
        return True
    
    def safe_extract_facts(
        self,
        user_id: str,
        message: str,
        message_id: Optional[str] = None,
        context: Optional[List[str]] = None,
        operation_context: str = "extract_facts"
    ) -> Dict[str, Any]:
        """
        Versión segura de extract_facts() con validación completa y manejo de errores.
        
        Args:
            user_id: ID del usuario
            message: Mensaje del usuario
            message_id: ID del mensaje (opcional)
            context: Contexto previo (opcional)
            operation_context: Contexto de la operación para logging
            
        Returns:
            Dict con resultado de la operación:
            {
                "success": bool,
                "data": List[Dict] | None,
                "error": str | None,
                "error_type": str | None,
                "validation_errors": List[str],
                "debug_info": Dict | None
            }
        """
        start_time = datetime.now()
        debug_info = {}
        validation_errors = []
        
        try:
            # 1. VALIDACIONES PREVIAS
            logger.info(f"{operation_context}: Iniciando validaciones para user_id={user_id}")
            
            # Validar user_id
            try:
                self.validate_user_id(user_id)
            except CoreValidationError as e:
                validation_errors.append(str(e))
                return {
                    "success": False,
                    "data": None,
                    "error": str(e),
                    "error_type": "CoreValidationError",
                    "validation_errors": validation_errors,
                    "debug_info": debug_info
                }
            
            # Validar message
            if not message or not isinstance(message, str) or len(message.strip()) == 0:
                error_msg = "message no puede estar vacío"
                validation_errors.append(error_msg)
                return {
                    "success": False,
                    "data": None,
                    "error": error_msg,
                    "error_type": "ValidationError",
                    "validation_errors": validation_errors,
                    "debug_info": debug_info
                }
            
            # 2. AGREGAR INFORMACIÓN DE DEBUG
            if self.debug_mode:
                debug_info.update({
                    "user_id": user_id,
                    "message_length": len(message),
                    "message_id": message_id,
                    "context_length": len(context) if context else 0,
                    "start_time": start_time.isoformat()
                })
            
            # 3. SIMULAR EXTRACCIÓN DE FACTS (aquí iría la lógica real)
            logger.info(f"{operation_context}: Validaciones pasadas, ejecutando extracción de facts")
            
            # Simular extracción básica
            facts = []
            
            # Extracción simple por patrones
            message_lower = message.lower()
            
            # Detectar nombre
            if "i'm " in message_lower or "my name is" in message_lower:
                parts = message.split()
                for i, word in enumerate(parts):
                    if word.lower() in ["i'm", "im", "name"]:
                        if i + 1 < len(parts):
                            name = parts[i + 1].strip(",.")
                            facts.append({
                                "user_id": user_id,
                                "category": "personal_info",
                                "key": "name",
                                "value": name,
                                "confidence": 0.8,
                                "source_message_id": message_id,
                                "created_at": datetime.now().isoformat()
                            })
                            break
            
            # Detectar edad
            if "i'm " in message_lower and any(char.isdigit() for char in message):
                import re
                age_match = re.search(r'\b(\d{1,2})\b', message)
                if age_match:
                    age = int(age_match.group(1))
                    if 1 <= age <= 120:  # Rango válido de edad
                        facts.append({
                            "user_id": user_id,
                            "category": "personal_info",
                            "key": "age",
                            "value": age,
                            "confidence": 0.7,
                            "source_message_id": message_id,
                            "created_at": datetime.now().isoformat()
                        })
            
            if self.debug_mode:
                debug_info["facts_extracted"] = len(facts)
                debug_info["execution_time_ms"] = (datetime.now() - start_time).total_seconds() * 1000
            
            logger.info(f"{operation_context}: Extracción completada exitosamente, {len(facts)} facts extraídos")
            
            return {
                "success": True,
                "data": facts,
                "error": None,
                "error_type": None,
                "validation_errors": validation_errors,
                "debug_info": debug_info
            }
            
        except Exception as e:
            # Capturar cualquier otra excepción
            error_msg = f"{operation_context}: Error inesperado en extracción de facts: {str(e)}"
            logger.error(error_msg)
            logger.error(f"{operation_context}: Traceback: {traceback.format_exc()}")
            
            if self.debug_mode:
                debug_info["exception_type"] = type(e).__name__
                debug_info["exception_message"] = str(e)
                debug_info["traceback"] = traceback.format_exc()
                debug_info["execution_time_ms"] = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "success": False,
                "data": None,
                "error": error_msg,
                "error_type": type(e).__name__,
                "validation_errors": validation_errors,
                "debug_info": debug_info
            }
    
    def safe_compile_personality(
        self,
        personality_data: Dict[str, Any],
        provider: str = "openai",
        operation_context: str = "compile_personality"
    ) -> Dict[str, Any]:
        """
        Versión segura de compile_personality() con validación completa y manejo de errores.
        
        Args:
            personality_data: Datos de personalidad
            provider: Proveedor LLM
            operation_context: Contexto de la operación para logging
            
        Returns:
            Dict con resultado de la operación
        """
        start_time = datetime.now()
        debug_info = {}
        validation_errors = []
        
        try:
            # 1. VALIDACIONES PREVIAS
            logger.info(f"{operation_context}: Iniciando validaciones para provider={provider}")
            
            # Validar datos de personalidad
            try:
                self.validate_personality_data(personality_data)
            except CoreValidationError as e:
                validation_errors.append(str(e))
                return {
                    "success": False,
                    "data": None,
                    "error": str(e),
                    "error_type": "CoreValidationError",
                    "validation_errors": validation_errors,
                    "debug_info": debug_info
                }
            
            # 2. AGREGAR INFORMACIÓN DE DEBUG
            if self.debug_mode:
                debug_info.update({
                    "provider": provider,
                    "personality_name": personality_data.get("persona", {}).get("name", "unknown"),
                    "start_time": start_time.isoformat()
                })
            
            # 3. SIMULAR COMPILACIÓN (aquí iría la lógica real)
            logger.info(f"{operation_context}: Validaciones pasadas, ejecutando compilación")
            
            # Simular compilación básica
            compiled_prompt = f"""You are {personality_data.get("persona", {}).get("name", "Assistant")}.
{personality_data.get("persona", {}).get("description", "A helpful assistant")}.

Core traits:
{chr(10).join(f"- {trait}" for trait in personality_data.get("core_traits", []))}

Communication style:
- Tone: {personality_data.get("linguistic_profile", {}).get("tone", "friendly")}
- Formality: {personality_data.get("linguistic_profile", {}).get("formality_level", "neutral")}

Behavioral rules:
{chr(10).join(f"{i+1}. {rule}" for i, rule in enumerate(personality_data.get("behavioral_rules", [])))}

Stay in character at all times."""
            
            compilation_result = {
                "provider": provider,
                "prompt": compiled_prompt,
                "token_estimate": len(compiled_prompt) // 4,  # Estimación aproximada
                "metadata": {
                    "compiled_at": datetime.now().isoformat(),
                    "personality_name": personality_data.get("persona", {}).get("name", "unknown"),
                    "format": "system_prompt"
                }
            }
            
            if self.debug_mode:
                debug_info["compilation_successful"] = True
                debug_info["token_estimate"] = compilation_result["token_estimate"]
                debug_info["execution_time_ms"] = (datetime.now() - start_time).total_seconds() * 1000
            
            logger.info(f"{operation_context}: Compilación completada exitosamente")
            
            return {
                "success": True,
                "data": compilation_result,
                "error": None,
                "error_type": None,
                "validation_errors": validation_errors,
                "debug_info": debug_info
            }
            
        except Exception as e:
            # Capturar cualquier otra excepción
            error_msg = f"{operation_context}: Error inesperado en compilación: {str(e)}"
            logger.error(error_msg)
            logger.error(f"{operation_context}: Traceback: {traceback.format_exc()}")
            
            if self.debug_mode:
                debug_info["exception_type"] = type(e).__name__
                debug_info["exception_message"] = str(e)
                debug_info["traceback"] = traceback.format_exc()
                debug_info["execution_time_ms"] = (datetime.now() - start_time).total_seconds() * 1000
            
            return {
                "success": False,
                "data": None,
                "error": error_msg,
                "error_type": type(e).__name__,
                "validation_errors": validation_errors,
                "debug_info": debug_info
            }
    
    def create_error_response(
        self,
        error_message: str,
        error_type: str,
        validation_errors: List[str] = None,
        debug_info: Dict = None
    ) -> Dict[str, Any]:
        """
        Crear respuesta de error estandarizada.
        
        Args:
            error_message: Mensaje de error
            error_type: Tipo de error
            validation_errors: Lista de errores de validación
            debug_info: Información de debug
            
        Returns:
            Dict con respuesta de error estandarizada
        """
        return {
            "success": False,
            "data": None,
            "error": error_message,
            "error_type": error_type,
            "validation_errors": validation_errors or [],
            "debug_info": debug_info or {}
        }


# Instancia global del manager de validación
core_validation_manager = LuminoraCoreValidationManager()


# Función de conveniencia para configurar validación
def configure_core_validation(debug_mode: bool = False, validation_enabled: bool = True):
    """
    Configurar el sistema de validación del core.
    
    Args:
        debug_mode: Habilitar modo debug
        validation_enabled: Habilitar validaciones
    """
    core_validation_manager.enable_debug_mode(debug_mode)
    core_validation_manager.validation_enabled = validation_enabled
    
    logger.info(f"Validación del core configurada - Debug: {debug_mode}, Validaciones: {validation_enabled}")


# Ejemplo de uso
if __name__ == "__main__":
    print("=== TESTING LUMINORACORE CORE VALIDATION FIX ===")
    
    # Configurar logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Configurar validación
    configure_core_validation(debug_mode=True)
    
    # Test de validaciones
    core_validation_manager.validate_user_id("test_user")
    
    # Test de extracción de facts
    result = core_validation_manager.safe_extract_facts(
        user_id="test_user",
        message="I'm John, I'm 25 years old and I love programming"
    )
    
    print(f"Resultado de extracción: {result}")
    
    print("=== CORE VALIDATION TEST COMPLETED ===")
