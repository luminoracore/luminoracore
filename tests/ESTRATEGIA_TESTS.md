# 🧪 TESTING STRATEGY - 2 LEVELS

**Date**: October 4, 2025  
**Approved by**: User

---

## 📊 OVERVIEW

LuminoraCore uses a **2-level strategy** for testing:

```
┌─────────────────────────────────────────────────────────────┐
│  LEVEL 1: DEVELOPMENT TESTS (Fast, per component)          │
│                                                             │
│  luminoracore/tests/        → Base Engine                  │
│  luminoracore-cli/tests/    → CLI                          │
│  luminoracore-sdk-python/tests/ → SDK                      │
│                                                             │
│  • Run during daily development                             │
│  • Quick feedback                                           │
│  • Basic unit tests                                          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  LEVEL 2: VALIDATION SUITE (Comprehensive, pre-release)    │
│                                                             │
│  tests/                     → 173 complete tests           │
│                                                             │
│  • Run BEFORE v1.0 release                                  │
│  • Comprehensive tests of EVERYTHING                        │
│  • Real APIs, real databases                                │
│  • End-to-end scenarios                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 LEVEL 1: DEVELOPMENT TESTS

### Purpose
**Fast** tests for daily development of each component.

### Location and Execution

#### Base Engine
```bash
cd luminoracore
pytest tests/ -v

# Files:
# - test_personality.py (12 tests)
# - test_validator.py (13 tests)
```

#### CLI
```bash
cd luminoracore-cli
pytest tests/ -v

# Files:
# - test_config.py
# - test_validate.py
# - conftest.py (fixtures)
```

#### SDK
```bash
cd luminoracore-sdk-python
pytest tests/ -v

# Files:
# - unit/test_client.py
# - integration/test_full_session.py
```

### Characteristics
- ✅ **Fast**: < 30 seconds
- ✅ **Mocks**: Use mocks instead of real APIs/databases
- ✅ **Unit**: One component at a time
- ✅ **Immediate feedback**: For daily development

### When to Run
- ✅ After each code change
- ✅ Before each commit
- ✅ During active development
- ✅ For quick debugging

---

## 🏆 LEVEL 2: VALIDATION SUITE

### Purpose
**Comprehensive** tests for complete validation before release.

### Location and Execution

```bash
# From project root
pytest tests/ -v

# Or run specific suites
pytest tests/test_1_motor_base.py -v
pytest tests/test_2_cli.py -v
pytest tests/test_3_providers.py -v
pytest tests/test_4_storage.py -v
pytest tests/test_5_sessions.py -v
pytest tests/test_6_integration.py -v
```

### Structure

| Suite | File | Tests | Description |
|-------|------|-------|-------------|
| 1 | `test_1_motor_base.py` | 30 | Base Engine: load, validation, compilation, blend |
| 2 | `test_2_cli.py` | 25 | CLI: all commands (validate, compile, create, etc.) |
| 3 | `test_3_providers.py` | 49 | Providers: 7 LLMs with **REAL** APIs |
| 4 | `test_4_storage.py` | 36 | Storage: 6 types (memory, json, sqlite, redis, pg, mongo) |
| 5 | `test_5_sessions.py` | 25 | Sessions: create, messages, history, memory |
| 6 | `test_6_integration.py` | 8 | Integration: complete end-to-end scenarios |
| **TOTAL** | | **173** | |

### Characteristics
- ✅ **Comprehensive**: Cover ALL features
- ✅ **Real**: Real APIs, real databases (no mocks)
- ✅ **Integration**: Complete end-to-end tests
- ✅ **Validation**: Acceptance criteria for v1.0

### When to Run
- 🎯 **BEFORE v1.0 release** (mandatory)
- 🎯 Before merge to `main`
- 🎯 In CI/CD (GitHub Actions)
- 🎯 For release validation
- 🎯 After architectural changes

### Requirements

```bash
# Dependencies
pip install pytest pytest-asyncio pytest-cov pytest-benchmark

# API Keys (for test_3_providers.py)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="sk-..."
export MISTRAL_API_KEY="..."
export COHERE_API_KEY="..."
export GOOGLE_API_KEY="..."

# Databases (for test_4_storage.py)
docker-compose -f tests/docker-compose.yml up -d
```

---

## ✅ v1.0 ACCEPTANCE CRITERIA

To release v1.0, the **Validation Suite** must meet:

### Minimum Required
- ✅ **Test Suite 1** (Base Engine): 100% passing
- ✅ **Test Suite 2** (CLI): 100% passing
- ✅ **Test Suite 3** (Providers): ≥ 5/7 providers working
- ✅ **Test Suite 4** (Storage): ≥ 3/6 storage types working (memory, json, sqlite)
- ✅ **Test Suite 5** (Sessions): 100% passing
- ✅ **Test Suite 6** (Integration): ≥ 6/8 scenarios passing

### Ideal
- 🏆 **173/173 tests passing** (100%)
- 🏆 **7/7 providers working**
- 🏆 **6/6 storage types working**
- 🏆 **8/8 end-to-end scenarios**

### Quality Metrics
- ✅ **Coverage**: ≥ 70% (ideal 85%+)
- ✅ **Flaky tests**: 0 (tests that fail intermittently)
- ✅ **Execution time**: < 10 minutes (without real APIs)
- ✅ **Documentation**: README.md in `tests/` updated

---

## 🚀 WORKFLOW

### During Daily Development

```bash
# 1. Work on Base Engine
cd luminoracore
# ... make changes ...

# 2. Run fast tests (Level 1)
pytest tests/ -v

# 3. If they pass, commit
git add .
git commit -m "feat: new functionality"
```

### Before Release

```bash
# 1. Make sure you're at the root
cd /path/to/LuminoraCoreBase

# 2. Run complete Validation Suite (Level 2)
pytest tests/ -v --cov

# 3. Verify that ALL pass
# Expected: 173 passed in X.XXs

# 4. If they pass, you're ready to release v1.0
git tag v1.0.0
git push origin v1.0.0
```

---

## 📋 PRE-RELEASE CHECKLIST

```markdown
- [ ] Development Tests (Level 1) - All passing
  - [ ] luminoracore/tests/ (25 tests)
  - [ ] luminoracore-cli/tests/ (15 tests)
  - [ ] luminoracore-sdk-python/tests/ (27 tests)

- [ ] Validation Suite (Level 2) - Criteria met
  - [ ] Test Suite 1: Base Engine (30 tests)
  - [ ] Test Suite 2: CLI (25 tests)
  - [ ] Test Suite 3: Providers (≥35/49 tests)
  - [ ] Test Suite 4: Storage (≥18/36 tests)
  - [ ] Test Suite 5: Sessions (25 tests)
  - [ ] Test Suite 6: Integration (≥6/8 tests)

- [ ] Documentation
  - [ ] tests/README.md updated
  - [ ] CHANGELOG.md updated
  - [ ] README.md with test badges

- [ ] CI/CD
  - [ ] GitHub Actions configured
  - [ ] Tests running on 3 OS (Windows, Linux, macOS)
  - [ ] Coverage report generated

- [ ] Manual
  - [ ] Installation validated on 3 OS
  - [ ] Examples run manually
  - [ ] Documentation reviewed
```

---

## 🔧 MAINTENANCE

### Adding New Development Test (Level 1)

1. Identify the component (engine, CLI, SDK)
2. Go to the appropriate test directory
3. Add the test to the existing file
4. Run: `pytest tests/ -v`

### Adding New Validation Test (Level 2)

1. Identify the correct suite (1-6)
2. Add the test to `tests/test_X_name.py`
3. Update the counter in `tests/README.md`
4. Run: `pytest tests/test_X_name.py -v`

### Updating Acceptance Criteria

1. Edit this file (`ESTRATEGIA_TESTS.md`)
2. Communicate changes to the team
3. Update `tests/README.md` if necessary

---

## 🎓 PHILOSOPHY

> **"We will not release anything that is garbage."**
> 
> Tests are not just code that validates code.
> They are our **quality guarantee** and **promise to the user**.
> 
> - **Level 1**: Speed to iterate fast
> - **Level 2**: Confidence to release without fear

**Both levels are equally important.**

---

## 📞 CONTACT

**Questions about tests**: See `tests/README.md`

**Test issues**: GitHub Issues with label "tests"

**Propose new tests**: Pull Request with update to this strategy

---

**Last updated**: 2025-01-04  
**Version**: 1.0  
**Status**: ✅ Approved and implemented

