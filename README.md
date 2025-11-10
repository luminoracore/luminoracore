# LuminoraCore — Open framework for portable AI personalities and conversation data

LuminoraCore lets every user build their own portable “AI conversation data lake” and evolve AI personalities over time — independent from any single LLM vendor. Your conversations are your data: capture them, analyze what matters, and use those insights to make your AI personalities grow with you.

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

## Honest capability status (v1.1)

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

## Components

- `luminoracore/` (Core): JSON personalities, validation, compilation, blending
- `luminoracore-sdk-python/` (SDK): sessions, storage integrations, analytics, snapshots, v1.1 flows
- `luminoracore-cli/` (CLI): validate/compile/blend, snapshot export/import, developer tools

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

- Installation Guide (EN): `INSTALLATION_GUIDE.md`
- Quick Start (EN): `QUICK_START.md`
- Memory System Deep Dive (EN): `MEMORY_SYSTEM_DEEP_DIVE.md`
- Release Notes v1.1 (EN): `RELEASE_NOTES_v1.1.md`

## License

MIT — see headers and component licenses as applicable.