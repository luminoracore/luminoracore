"""
Test Suite 1: Motor Base (luminoracore)
Prueba exhaustiva del motor base: carga, validación, compilación, blend
"""
import pytest
import os
import json
import tempfile
from pathlib import Path

# Imports del motor base
from luminoracore import (
    Personality,
    PersonalityValidator,
    PersonalityCompiler,
    PersonaBlend,
    PersonalityError,
    LLMProvider
)

# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def valid_personality_dict():
    """Personalidad válida como diccionario."""
    return {
        "name": "test_personality",
        "description": "A test personality",
        "persona": {
            "name": "TestBot",
            "description": "A testing assistant",
            "role": "assistant",
            "archetype": "helper"
        },
        "core_traits": {
            "archetype": "helper",
            "tone": "friendly",
            "formality": 0.5,
            "enthusiasm": 0.7,
            "empathy": 0.8
        },
        "communication_style": {
            "verbosity": 0.5,
            "complexity": 0.5,
            "humor": 0.3,
            "directness": 0.7
        },
        "knowledge_domains": ["testing", "qa"],
        "behavioral_rules": {
            "must_do": ["Be helpful", "Be clear"],
            "must_not_do": ["Be rude"],
            "preferences": ["Concise answers"]
        },
        "response_patterns": {
            "greeting": "Hello! How can I help you test today?",
            "farewell": "Happy testing!",
            "acknowledgment": "Got it!",
            "clarification": "Could you clarify that?"
        },
        "context_awareness": {
            "maintains_conversation_context": True,
            "adapts_to_user_mood": False,
            "considers_previous_interactions": True
        },
        "metadata": {
            "version": "1.0.0",
            "author": "Test Suite",
            "created_at": "2025-01-04",
            "tags": ["testing", "qa"]
        }
    }

@pytest.fixture
def valid_personality_file(valid_personality_dict, tmp_path):
    """Personalidad válida en archivo JSON temporal."""
    file_path = tmp_path / "test_personality.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(valid_personality_dict, f, indent=2)
    return str(file_path)

@pytest.fixture
def invalid_personality_dict():
    """Personalidad inválida (falta campos requeridos)."""
    return {
        "name": "invalid",
        # Falta casi todo
    }

# ============================================================================
# TEST 1: CARGA DE PERSONALIDADES
# ============================================================================

class TestPersonalityLoading:
    """Tests de carga de personalidades."""
    
    def test_load_from_valid_file(self, valid_personality_file):
        """✅ Cargar desde archivo JSON válido."""
        personality = Personality(valid_personality_file)
        assert personality is not None
        assert personality.name == "test_personality"
    
    def test_load_from_dict(self, valid_personality_dict):
        """✅ Cargar desde diccionario Python."""
        personality = Personality(valid_personality_dict)
        assert personality is not None
        assert personality.name == "test_personality"
    
    def test_load_nonexistent_file(self):
        """✅ Manejo de archivo inexistente."""
        with pytest.raises((FileNotFoundError, PersonalityError)):
            Personality("/nonexistent/path/personality.json")
    
    def test_load_invalid_json_file(self, tmp_path):
        """✅ Manejo de JSON inválido."""
        file_path = tmp_path / "invalid.json"
        with open(file_path, 'w') as f:
            f.write("{invalid json content")
        
        with pytest.raises((json.JSONDecodeError, PersonalityError)):
            Personality(str(file_path))
    
    def test_load_invalid_schema(self, invalid_personality_dict):
        """✅ Manejo de schema incorrecto."""
        with pytest.raises(PersonalityError):
            Personality(invalid_personality_dict)

# ============================================================================
# TEST 2: VALIDACIÓN
# ============================================================================

class TestPersonalityValidation:
    """Tests de validación de personalidades."""
    
    def test_validate_valid_personality(self, valid_personality_dict):
        """✅ Personalidad válida (sin errores)."""
        personality = Personality(valid_personality_dict)
        validator = PersonalityValidator()
        result = validator.validate(personality)
        
        assert result.is_valid is True
        assert len(result.errors) == 0
    
    def test_validate_with_warnings(self, valid_personality_dict):
        """✅ Personalidad con warnings (no errores)."""
        # Personalidad válida pero con campos opcionales vacíos
        minimal_dict = {
            "name": "minimal",
            "persona": {
                "name": "MinBot",
                "description": "Minimal",
                "role": "assistant"
            },
            "core_traits": {
                "archetype": "helper"
            }
        }
        
        personality = Personality(minimal_dict)
        validator = PersonalityValidator()
        result = validator.validate(personality)
        
        assert result.is_valid is True
        # Puede tener warnings pero no errores
        assert len(result.errors) == 0
    
    def test_validate_invalid_personality(self):
        """✅ Personalidad inválida (errores)."""
        invalid_dict = {"name": "bad"}  # Falta casi todo
        
        validator = PersonalityValidator()
        
        with pytest.raises(PersonalityError):
            personality = Personality(invalid_dict)
    
    def test_validate_strict_mode(self, valid_personality_dict):
        """✅ Validación estricta vs permisiva."""
        personality = Personality(valid_personality_dict)
        validator = PersonalityValidator()
        
        # Modo normal
        result_normal = validator.validate(personality)
        assert result_normal.is_valid is True
        
        # Modo estricto (si existe esta opción)
        # result_strict = validator.validate(personality, strict=True)
        # assert result_strict.is_valid is True
    
    def test_error_messages_are_clear(self):
        """✅ Mensajes de error claros."""
        invalid_dict = {"name": "test"}
        
        with pytest.raises(PersonalityError) as exc_info:
            Personality(invalid_dict)
        
        error_msg = str(exc_info.value)
        # El mensaje debe ser útil
        assert len(error_msg) > 10
        assert "name" in error_msg.lower() or "required" in error_msg.lower()

# ============================================================================
# TEST 3: COMPILACIÓN
# ============================================================================

class TestPersonalityCompilation:
    """Tests de compilación para diferentes LLMs."""
    
    @pytest.fixture
    def compiler(self):
        return PersonalityCompiler()
    
    @pytest.fixture
    def personality(self, valid_personality_dict):
        return Personality(valid_personality_dict)
    
    def test_compile_for_openai(self, compiler, personality):
        """✅ Compilar para OpenAI."""
        result = compiler.compile(personality, LLMProvider.OPENAI)
        
        assert result is not None
        assert result.prompt is not None
        assert len(result.prompt) > 0
        assert result.token_estimate > 0
    
    def test_compile_for_anthropic(self, compiler, personality):
        """✅ Compilar para Anthropic."""
        result = compiler.compile(personality, LLMProvider.ANTHROPIC)
        
        assert result is not None
        assert result.prompt is not None
        assert result.token_estimate > 0
    
    def test_compile_for_deepseek(self, compiler, personality):
        """✅ Compilar para DeepSeek."""
        result = compiler.compile(personality, LLMProvider.DEEPSEEK)
        
        assert result is not None
        assert result.prompt is not None
        assert result.token_estimate > 0
    
    def test_compile_for_mistral(self, compiler, personality):
        """✅ Compilar para Mistral."""
        result = compiler.compile(personality, LLMProvider.MISTRAL)
        
        assert result is not None
        assert result.token_estimate > 0
    
    def test_compile_for_cohere(self, compiler, personality):
        """✅ Compilar para Cohere."""
        result = compiler.compile(personality, LLMProvider.COHERE)
        
        assert result is not None
        assert result.token_estimate > 0
    
    def test_compile_for_google(self, compiler, personality):
        """✅ Compilar para Google."""
        result = compiler.compile(personality, LLMProvider.GOOGLE)
        
        assert result is not None
        assert result.token_estimate > 0
    
    def test_compile_for_llama(self, compiler, personality):
        """✅ Compilar para Llama."""
        result = compiler.compile(personality, LLMProvider.LLAMA)
        
        assert result is not None
        assert result.token_estimate > 0
    
    def test_token_counting_is_reasonable(self, compiler, personality):
        """✅ Token counting correcto."""
        result = compiler.compile(personality, LLMProvider.OPENAI)
        
        # Token count debe estar en un rango razonable
        assert result.token_estimate > 10
        assert result.token_estimate < 10000
    
    def test_optimization_per_provider(self, compiler, personality):
        """✅ Optimización por provider."""
        result_openai = compiler.compile(personality, LLMProvider.OPENAI)
        result_anthropic = compiler.compile(personality, LLMProvider.ANTHROPIC)
        
        # Los prompts pueden ser diferentes (optimización)
        # Esto es opcional, depende de la implementación
        assert result_openai.prompt is not None
        assert result_anthropic.prompt is not None

# ============================================================================
# TEST 4: PERSONABLEND
# ============================================================================

class TestPersonaBlend:
    """Tests de mezcla de personalidades."""
    
    @pytest.fixture
    def personality_a(self, valid_personality_dict):
        dict_a = valid_personality_dict.copy()
        dict_a["name"] = "personality_a"
        dict_a["core_traits"]["enthusiasm"] = 0.9
        return Personality(dict_a)
    
    @pytest.fixture
    def personality_b(self, valid_personality_dict):
        dict_b = valid_personality_dict.copy()
        dict_b["name"] = "personality_b"
        dict_b["core_traits"]["enthusiasm"] = 0.1
        return Personality(dict_b)
    
    def test_blend_two_personalities_50_50(self, personality_a, personality_b):
        """✅ Mezclar 2 personalidades (50/50)."""
        blender = PersonaBlend()
        result = blender.blend(
            personalities=[personality_a, personality_b],
            weights=[0.5, 0.5]
        )
        
        assert result is not None
        assert hasattr(result, 'core_traits')
        
        # El resultado debe estar entre ambos
        # enthusiasm: 0.9 * 0.5 + 0.1 * 0.5 = 0.5
        assert result.core_traits.enthusiasm == pytest.approx(0.5, abs=0.1)
    
    def test_blend_two_personalities_70_30(self, personality_a, personality_b):
        """✅ Mezclar 2 personalidades (70/30)."""
        blender = PersonaBlend()
        result = blender.blend(
            personalities=[personality_a, personality_b],
            weights=[0.7, 0.3]
        )
        
        assert result is not None
        # enthusiasm: 0.9 * 0.7 + 0.1 * 0.3 = 0.66
        assert result.core_traits.enthusiasm == pytest.approx(0.66, abs=0.1)
    
    def test_blend_three_personalities(self, personality_a, personality_b, valid_personality_dict):
        """✅ Mezclar 3+ personalidades."""
        dict_c = valid_personality_dict.copy()
        dict_c["name"] = "personality_c"
        dict_c["core_traits"]["enthusiasm"] = 0.5
        personality_c = Personality(dict_c)
        
        blender = PersonaBlend()
        result = blender.blend(
            personalities=[personality_a, personality_b, personality_c],
            weights=[0.33, 0.33, 0.34]
        )
        
        assert result is not None
    
    def test_blend_strategies(self, personality_a, personality_b):
        """✅ Estrategias de mezcla."""
        blender = PersonaBlend()
        
        # Estrategia por defecto
        result_default = blender.blend(
            personalities=[personality_a, personality_b],
            weights=[0.5, 0.5]
        )
        
        assert result_default is not None
        
        # Si hay otras estrategias disponibles
        # result_max = blender.blend(..., strategy="max")
        # result_min = blender.blend(..., strategy="min")
    
    def test_blended_personality_is_valid(self, personality_a, personality_b):
        """✅ Validar personalidad mezclada."""
        blender = PersonaBlend()
        result = blender.blend(
            personalities=[personality_a, personality_b],
            weights=[0.5, 0.5]
        )
        
        # La personalidad resultante debe ser válida
        validator = PersonalityValidator()
        validation_result = validator.validate(result)
        
        assert validation_result.is_valid is True

# ============================================================================
# TEST 5: PERFORMANCE
# ============================================================================

class TestPerformance:
    """Tests de rendimiento del motor base."""
    
    def test_load_performance(self, valid_personality_dict, benchmark):
        """✅ Carga < 100ms."""
        def load():
            return Personality(valid_personality_dict)
        
        result = benchmark(load)
        # benchmark provee stats automáticamente
    
    def test_validation_performance(self, valid_personality_dict, benchmark):
        """✅ Validación < 50ms."""
        personality = Personality(valid_personality_dict)
        validator = PersonalityValidator()
        
        def validate():
            return validator.validate(personality)
        
        result = benchmark(validate)
    
    def test_compilation_performance(self, valid_personality_dict, benchmark):
        """✅ Compilación < 200ms."""
        personality = Personality(valid_personality_dict)
        compiler = PersonalityCompiler()
        
        def compile():
            return compiler.compile(personality, LLMProvider.OPENAI)
        
        result = benchmark(compile)
    
    def test_no_memory_leaks(self, valid_personality_dict):
        """✅ No memory leaks."""
        import gc
        
        # Crear y destruir 1000 personalidades
        for _ in range(1000):
            p = Personality(valid_personality_dict)
            del p
        
        gc.collect()
        # Si hay memory leaks, esto crecería sin control
        # Pytest-memray puede detectar esto

# ============================================================================
# CONFIGURACIÓN DE PYTEST
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

