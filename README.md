# LuminoraCore — Open framework for portable AI personalities and conversation data

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://github.com/luminoracore)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)](https://github.com/luminoracore)
[![Architecture](https://img.shields.io/badge/architecture-3--layer-orange.svg)](#architecture-v120)

**Last Updated:** November 21, 2025

LuminoraCore lets every user build their own portable "AI conversation data lake" and evolve AI personalities over time — independent from any single LLM vendor. Your conversations are your data: capture them, analyze what matters, and use those insights to make your AI personalities grow with you.

## 🆕 What's New in v1.2.0

**FASE 0: REFACTOR ARQUITECTURA — ✅ COMPLETADA**

- ✅ **Unified 3-Layer Architecture:** Core, SDK, CLI separation
- ✅ **Core Integration:** SDK now uses Core internally via adapters
- ✅ **Optimization Module:** 25-45% token reduction (key mapping, compact format, deduplication, cache)
- ✅ **Memory System:** MemoryManager uses Core MemorySystem when available
- ✅ **100% Backward Compatible:** v1.1 code works without modifications

📖 **Migration Guide:** See [`MIGRATION_1.1_to_1.2.md`](MIGRATION_1.1_to_1.2.md) for complete details.

## The Shift We're Making

Most AI systems today are learning to remember — but each platform remembers in isolation. Your ChatGPT might recall a conversation. Claude or Gemini might, too. None of them know it’s still you.

LuminoraCore is not trying to bolt memory into a single model. We’re building continuity across them. Real evolution doesn’t happen inside a single session; it happens through data, persistence, and relationships that survive time, tools, and providers.

## Why

- Data ownership: conversations should be portable, not locked inside a single LLM history.
- Consistency: personalities should be defined structurally, not as vendor‑specific prompts.
- Evolution: your daily interactions should make personalities know you better.

## What we do (three pillars)

1) Data capture: store each conversation turn and its context, in your chosen storage backend.
2) Analysis layer: extract relevant knowledge from conversations (facts, memorable episodes) and sentiment signals.
3) Personality evolution: apply the extracted knowledge to refine and evolve the active personality you use with LLMs.

Result: a portable repository of conversations + insights that you can export, move, and reuse across tools.

## How it works

- v1.0: Standard JSON personalities. We introduced a universal, simple JSON schema to define personalities once, independent of prompts and providers.
- v1.1: Personality evolution begins. We capture data from conversations, extract facts/episodes/sentiment, persist them, and make them available to inform personality evolution and LLM usage.
- Portability: choose your storage backend (SQLite, Redis, PostgreSQL, MongoDB, DynamoDB, in-memory) and keep the same personality/identity across any LLM provider.


## Honest capability status (v1.2)

- Personality schema & compilation: PRODUCTION-READY (100%)
  - Stable JSON schema, compiler, validator, and personality blending
- Memory system & storage adapters: PRODUCTION-READY (90%)
  - Fact, episodic, and affinity subsystems run against SQLite/Redis/PostgreSQL/MongoDB/DynamoDB once configured
- Analytics & snapshots: BETA (~60%)
  - SDK-level exports/imports are available; CLI snapshot commands currently return demo payloads until the SDK wiring ships
  - Session analytics and metrics operate on real data when storage is enabled
- Mood System: SEMI‑READY (~40%)
  - Data structures, persistence, feature flags exist; application logic to traits is partial and not yet enforced in compiler flows
- Semantic Search: PLACEHOLDER (~15%)
  - API and flags exist; no vector‑store or embeddings implementation yet

See `RELEASE_NOTES_v1.1.md` for details and migration notes from v1.0.

## Architecture (high‑level)

Capture → Analyze → Store → Evolve → Use

- Capture: conversation messages and metadata
- Analyze: sentiment, learned facts, memorable episodes, relationship/affinity
- Store: pluggable backends (SQLite, Redis, PostgreSQL, MongoDB, DynamoDB, in-memory)
- Evolve: update personality state and configuration over time
- Use: Core/CLI/SDK interfaces for apps and workflows

## Storage flexibility

- Plug-and-play adapters for `SQLite`, `Redis`, `PostgreSQL`, `MongoDB`, `DynamoDB`, and `InMemoryStorage`.
- Swap storage without touching personality logic. The `FlexibleStorageManager` auto-detects configuration via JSON or environment variables.
- Export snapshots (facts, episodes, affinity, moods) through the SDK regardless of the backend you choose. Future CLI releases will connect the same pipeline for turnkey portability.

## Architecture v1.2.0

LuminoraCore uses a **3-layer architecture** for clean separation of concerns:

### Layer 1: Core (`luminoracore/`)

**Pure business logic layer** — no external dependencies

- **Personality Management:** JSON schema, validation, compilation, blending
- **Memory System:** Facts, episodes, affinity tracking
- **Optimization Module:** Token reduction (key mapping, compact format, deduplication, cache)
- **Storage Interfaces:** Pluggable storage backends
- **Migration System:** Database migration management

**Key Principle:** Core is independent and can be used standalone.

### Layer 2: SDK (`luminoracore-sdk-python/`)

**Client layer with LLM integration** — uses Core internally

- **LLM Provider Integration:** OpenAI, Anthropic, DeepSeek, Mistral, Cohere, Google, Llama
- **Session Management:** Stateful conversations with persistent memory
- **Storage Adapters:** SQLite, Redis, PostgreSQL, MongoDB, DynamoDB, InMemory
- **Analytics & Metrics:** Token tracking, performance monitoring
- **Uses Core via Adapters:** PersonalityBlender → PersonaBlendAdapter → Core PersonaBlend

**Key Principle:** SDK maintains public API while using Core internally.

### Layer 3: CLI (`luminoracore-cli/`)

**User interface layer** — built on top of Core

- **Validation Tools:** Personality validation and compilation
- **Memory Commands:** Fact/episode/affinity management
- **Migration Tools:** Database migration commands
- **Developer Tools:** Interactive mode, snapshots

**Key Principle:** CLI provides user-friendly interface to Core functionality.

### Architecture Flow

```
┌─────────────────────────────────────┐
│         CLI (luminoracore-cli)      │
│         User Interface Layer        │
│    • Validation commands             │
│    • Memory management               │
│    • Migration tools                 │
└──────────────┬──────────────────────┘
               │ uses
┌──────────────▼──────────────────────┐
│      SDK (luminoracore-sdk)          │
│      Client Layer + LLM Integration  │
│    • LLM providers (7)                │
│    • Session management                │
│    • Uses Core via adapters           │
└──────────────┬──────────────────────┘
               │ uses
┌──────────────▼──────────────────────┐
│      Core (luminoracore)             │
│      Business Logic Layer            │
│    • Personality blending             │
│    • Memory system                    │
│    • Optimization                     │
│    • Storage interfaces               │
└─────────────────────────────────────┘
```

📖 **Detailed Architecture:** See [`ARCHITECTURE.md`](ARCHITECTURE.md) for complete documentation.

## Installation (per component)

See `INSTALLATION_GUIDE.md` for full details. Summary:

```bash
# Core (required)
cd luminoracore && pip install . && cd ..

# SDK (optional)
cd luminoracore-sdk-python && pip install . && cd ..

# CLI (optional)
cd luminoracore-cli && pip install . && cd ..
```

Windows note: install Core without editable mode (no `-e`) to avoid namespace issues.

## Quick start

See `QUICK_START.md` for a minimal SDK example and first CLI commands.

## Data ownership and portability

- Your data is yours: choose the backend, and export snapshots to JSON.
- Feature flags let you opt into memory/affinity modules per deployment.
- Future formats: CSV/TXT and LLM‑optimized exports are planned.

## Roadmap (selected)

- Apply Mood System modifiers in compiler/runtime
- Semantic Search (embeddings + vector store integrations)
- Additional snapshot export formats (CSV/TXT)
- Longer‑term memory tiers (short/medium/long‑range)

## Documentation

### Getting Started
- **Installation Guide:** [`INSTALLATION_GUIDE.md`](INSTALLATION_GUIDE.md)
- **Quick Start:** [`QUICK_START.md`](QUICK_START.md)
- **Migration Guide v1.1→v1.2:** [`MIGRATION_1.1_to_1.2.md`](MIGRATION_1.1_to_1.2.md)

### Architecture & Design
- **Architecture Documentation:** [`ARCHITECTURE.md`](ARCHITECTURE.md) (NEW in v1.2.0)
- **Memory System Deep Dive:** `MEMORY_SYSTEM_DEEP_DIVE.md`

### Release Information
- **Release Notes v1.1:** [`RELEASE_NOTES_v1.1.md`](RELEASE_NOTES_v1.1.md)
- **Changelog Core:** [`luminoracore/CHANGELOG.md`](luminoracore/CHANGELOG.md)
- **Changelog SDK:** [`luminoracore-sdk-python/CHANGELOG.md`](luminoracore-sdk-python/CHANGELOG.md)
- **Changelog CLI:** [`luminoracore-cli/CHANGELOG.md`](luminoracore-cli/CHANGELOG.md)

### Development & Roadmap
- **Fase 0 Documentation:** [`evolucion/FASE_0_REFACTOR_ARQUITECTURA_PROMPTS.md`](evolucion/FASE_0_REFACTOR_ARQUITECTURA_PROMPTS.md)
- **Phase 1 Roadmap:** [`evolucion/CURSOR_PROMPTS_01_PHASE_1_PART1.md`](evolucion/CURSOR_PROMPTS_01_PHASE_1_PART1.md)

## License

MIT — see headers and component licenses as applicable.