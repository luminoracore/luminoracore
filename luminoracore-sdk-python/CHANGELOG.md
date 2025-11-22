# Changelog

All notable changes to LuminoraCore SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-11-21

### Added
- **ARQUITECTURA:** Migración a arquitectura de 3 capas
- **Core Integration:** SDK ahora usa Core internamente
- **Optimization:** Integración completa del módulo optimization/ del Core
- **Memory:** MemoryManager usa Core MemorySystem cuando disponible
- **Adapter Pattern:** PersonaBlendAdapter para usar Core PersonaBlend
- **OptimizedStorageWrapper:** Wrapper transparente para aplicar optimization en storage
- **Optimization Config:** Soporte para OptimizationConfig en LuminoraCoreClient
- **get_optimization_stats():** Método para obtener estadísticas de optimización

### Changed
- **PersonalityBlender:** Ahora delega a Core PersonaBlend via adapter (mantiene 100% backward compatibility)
- **MemoryManager:** Usa Core MemorySystem con fallback a implementación SDK
- **Storage:** Wrapping automático con optimizer cuando habilitado
- **Client:** Acepta optimization_config en inicialización

### Fixed
- Eliminada duplicación de código entre Core y SDK
- Mejoras en manejo de errores
- Correcciones en conversión de tipos entre SDK y Core

### Deprecated
- Ninguno (100% backward compatible)

### Breaking Changes
- **NINGUNO** - Esta release es 100% backward compatible

### Migration
- Ver `MIGRATION_1.1_to_1.2.md` para detalles completos
- Código v1.1 funciona sin modificaciones
- Optimization es opcional y se puede habilitar gradualmente

---

## [1.1.0] - 2024-11-20

### Added
- Advanced personality management
- Session management with persistent memory
- Multi-provider LLM support (OpenAI, Anthropic, DeepSeek, Mistral, Cohere, Google, Llama)
- PersonaBlend™ Technology
- Flexible storage backends
- Monitoring & metrics
- Async/await support
- Type safety
- Token usage tracking
- Affinity tracking
- Fact extraction
- Episodic memory
- Memory classification
- Hierarchical personalities
- Feature flags
- Session snapshots

---

## [1.0.0] - 2024-01-01

### Added
- Initial release

