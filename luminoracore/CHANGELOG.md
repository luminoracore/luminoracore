# Changelog

All notable changes to LuminoraCore will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-11-21

### Added
- **ARQUITECTURA:** Migración a arquitectura de 3 capas (Core, SDK, CLI)
- **Optimization Module:** Módulo completo de optimización de tokens (key_mapping, minifier, compact_format, deduplicator, cache, optimizer)
- **Core Integration:** SDK ahora usa Core internamente via adapters
- **Memory System:** Sistema avanzado de memoria con Core MemorySystem
- **Storage Migrations:** Sistema de migraciones para storage backends

### Changed
- **PersonalityBlend:** Mejoras en blending de personalidades
- **Validator:** Mejoras en validación de personalidades
- **Storage:** Mejoras en interfaces de storage

### Fixed
- Eliminada duplicación de código entre Core y SDK
- Mejoras en manejo de errores
- Correcciones en validación de datos

### Deprecated
- Ninguno (100% backward compatible)

### Breaking Changes
- **NINGUNO** - Esta release es 100% backward compatible

---

## [1.1.0] - 2024-11-20

### Added
- Initial release with core personality management
- Personality blending capabilities
- Storage backends (InMemory, JSON, SQLite)
- Validation system

---

## [1.0.0] - 2024-01-01

### Added
- Initial release

