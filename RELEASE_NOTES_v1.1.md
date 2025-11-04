# LuminoraCore v1.1 — Release Notes and Project Status

Last updated: November 2025

## Overview

This document summarizes the real status of the project and highlights what changed from v1.0 to v1.1.

## Project status (v1.1)
- Core engine, SDK, and CLI are included in this repository.
- Installation is per component using pip (see INSTALLATION_GUIDE.md).
- Documentation consolidated and cleaned; build artifacts, backups, and temporary data removed.
- Wiki pages aligned and translated to English.

## What’s new in v1.1 (vs v1.0)
- Personality system improvements
  - Refined JSON schema and validation paths
  - Clearer personality templates (see `luminoracore/luminoracore/personalities/_template.json`)
- Memory system v1.1
  - Optional automatic fact extraction via SDK flows
  - Sentiment analysis integration path clarified
  - Affinity tracking clarified and made more consistent
- Storage backends
  - Flexible storage interfaces consolidated and documented
  - Guidance for SQLite, Redis, PostgreSQL, DynamoDB, MongoDB
- SDK enhancements
  - `LuminoraCoreClientV11` usage streamlined
  - Session and memory helpers refined
- CLI tooling
  - Validation, compile, and blend flows stabilized
- Documentation
  - Installation and Quick Start updated to pip-per-component
  - Troubleshooting updated with Windows guidance
  - Wiki content deduplicated and translated

## Migration notes (v1.0 → v1.1)
- Installation:
  - Prefer `pip install .` per component (avoid `-e` on Windows for Core)
- Personalities:
  - Verify custom JSONs against the updated template/schema
- SDK usage:
  - `LuminoraCoreClientV11` expected for v1.1 memory features
  - Consider explicit provider configuration per session
- Storage configuration:
  - Re-check environment variables and connection strings

## Known limitations
- Automatic memory extraction requires valid provider configuration and incurs extra latency
- Some advanced provider features depend on external API availability

## Links
- Installation: `INSTALLATION_GUIDE.md`
- Quick Start: `QUICK_START.md`
- Memory Deep Dive: `MEMORY_SYSTEM_DEEP_DIVE.md`
- Wiki: `wiki/`

---

If you find discrepancies or missing items, please open an issue with details.

