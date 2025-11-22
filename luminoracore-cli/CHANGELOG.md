# Changelog

All notable changes to LuminoraCore CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-11-21

### Added
- **ARQUITECTURA:** Migración a arquitectura de 3 capas
- **Core Dependency:** Dependencia oficial de `luminoracore>=1.2.0`
- **Core Integration:** CLI ahora usa Core directamente para validación y migraciones
- **Migration Commands:** Comandos de migración usando Core MigrationManager

### Changed
- **Dependencies:** `luminoracore` ahora es dependencia requerida (no opcional)
- **Imports:** Limpieza de imports temporales (sys.path hacks removidos)
- **Validator:** Usa Core PersonalityValidator directamente
- **Memory Commands:** Usa Core MemorySystem cuando disponible

### Fixed
- CLI ahora tiene dependencias correctas en pyproject.toml
- Eliminados hacks temporales de sys.path
- Imports limpios y organizados

### Deprecated
- Ninguno (100% backward compatible)

### Breaking Changes
- **NINGUNO** - Esta release es 100% backward compatible
- **Nota:** CLI ahora requiere `luminoracore>=1.2.0` instalado (antes era opcional)

### Migration
- Ver `MIGRATION_1.1_to_1.2.md` para detalles completos
- Reinstalar CLI: `pip install --upgrade luminoracore-cli`
- Asegurar que `luminoracore>=1.2.0` está instalado

---

## [1.1.0] - 2024-11-20

### Added
- Initial CLI release
- Personality validation commands
- Memory management commands
- Migration commands
- Interactive mode

---

## [1.0.0] - 2024-01-01

### Added
- Initial release

