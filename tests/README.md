# 🧪 LuminoraCore Test Suite

## 📋 Suite Completa de Pruebas

Esta es la **suite de validación exhaustiva** antes del lanzamiento v1.0.

### 🎯 Filosofía

> "No lanzaremos nada que sea una mierda. Se probarán todas las características exhaustivamente."

---

## 📊 Test Suites

| Suite | Archivo | Tests | Estado | Prioridad |
|-------|---------|-------|--------|-----------|
| 1. Motor Base | `test_1_motor_base.py` | 30 | ⏳ | 🔴 CRÍTICO |
| 2. CLI | `test_2_cli.py` | 25 | ⏳ | 🟡 ALTO |
| 3. Providers | `test_3_providers.py` | 49 | ⏳ | 🔴 CRÍTICO |
| 4. Storage | `test_4_storage.py` | 36 | ⏳ | 🔴 CRÍTICO |
| 5. Sessions | `test_5_sessions.py` | 25 | ⏳ | 🟡 ALTO |
| 6. Integration | `test_6_integration.py` | 8 | ⏳ | 🔴 CRÍTICO |
| **TOTAL** | | **173** | | |

---

## 🚀 Instalación

### Requisitos

```bash
pip install pytest pytest-asyncio pytest-cov pytest-benchmark
```

### Setup

```bash
# 1. Instalar LuminoraCore en modo desarrollo
cd luminoracore
pip install -e ".[all]"

# 2. Configurar API keys (para test_3_providers.py)
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="sk-..."
# ... etc

# 3. Setup de databases (para test_4_storage.py)
docker-compose -f tests/docker-compose.yml up -d
```

---

## 🧪 Ejecución

### Ejecutar TODO

```bash
# Desde el directorio raíz del proyecto
pytest tests/ -v

# Con coverage
pytest tests/ -v --cov=luminoracore --cov-report=html

# En paralelo (más rápido)
pytest tests/ -n auto
```

### Ejecutar Suite Específica

```bash
# Solo Motor Base
pytest tests/test_1_motor_base.py -v

# Solo Providers
pytest tests/test_3_providers.py -v

# Solo con marca específica
pytest tests/ -m "critical" -v
```

### Ejecutar Test Específico

```bash
# Un test particular
pytest tests/test_1_motor_base.py::TestPersonalityLoading::test_load_from_valid_file -v
```

---

## 📈 Coverage

### Generar Reporte

```bash
pytest tests/ --cov=luminoracore --cov-report=html

# Abrir reporte
open htmlcov/index.html  # Mac
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

### Objetivo

- **Mínimo aceptable**: 70% coverage
- **Ideal**: 85%+ coverage
- **Core critical paths**: 100% coverage

---

## 🐳 Docker para Testing

### Setup de Databases

```bash
cd tests
docker-compose up -d
```

Esto levanta:
- Redis (puerto 6379)
- PostgreSQL (puerto 5432)
- MongoDB (puerto 27017)

### Cleanup

```bash
docker-compose down -v
```

---

## 🔍 Estructura de Tests

### Convenciones

```python
# tests/test_X_nombre.py

class TestFeatureGroup:
    """Tests de un grupo de funcionalidades."""
    
    @pytest.fixture
    def setup_data(self):
        """Fixture para datos de prueba."""
        return {"key": "value"}
    
    def test_specific_behavior(self, setup_data):
        """✅ Descripción clara del test."""
        # Given (setup)
        # When (acción)
        # Then (assert)
        assert True

# Marcas
@pytest.mark.critical  # Test crítico para lanzamiento
@pytest.mark.slow  # Test lento (> 1s)
@pytest.mark.integration  # Test de integración
@pytest.mark.requires_api  # Requiere API key
```

### Nombres de Tests

- ✅ `test_load_from_valid_file` - Descriptivo
- ❌ `test_1` - No descriptivo

---

## ⚙️ Configuración

### pytest.ini

```ini
[pytest]
minversion = 6.0
addopts = -ra -q --strict-markers
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    critical: Critical tests for v1.0 release
    slow: Tests que tardan > 1s
    integration: Integration tests
    requires_api: Requires API key
    requires_db: Requires database
```

### conftest.py

Fixtures compartidas para todos los tests.

---

## 🚨 Tests Críticos

### MUST PASS para lanzar v1.0

```bash
pytest tests/ -m "critical" -v
```

Todos estos tests DEBEN pasar antes de lanzar:

1. **Motor Base**: Carga, validación, compilación
2. **Providers**: Al menos 5/7 providers funcionando
3. **Storage**: Memory, JSON, SQLite funcionando
4. **Sessions**: Crear, enviar mensajes, historial
5. **Integration**: Chatbot básico funciona end-to-end

---

## 🐛 Troubleshooting

### Tests fallan con "module not found"

```bash
# Asegúrate de instalar en modo desarrollo
pip install -e "luminoracore/[all]"
```

### Tests de providers fallan con "API key not configured"

```bash
# Configura la API key
export PROVIDER_API_KEY="your-key"

# O skip esos tests
pytest tests/ -m "not requires_api"
```

### Tests de storage fallan con "connection refused"

```bash
# Levanta las databases
cd tests
docker-compose up -d

# Verifica que estén corriendo
docker-compose ps
```

### Tests lentos

```bash
# Skip tests lentos
pytest tests/ -m "not slow"

# O ejecuta en paralelo
pytest tests/ -n auto
```

---

## 📊 CI/CD

### GitHub Actions

Los tests se ejecutan automáticamente en cada push:

```yaml
# .github/workflows/test.yml
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python: ['3.9', '3.10', '3.11']
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -e ".[all]"
      - run: pytest tests/ -v --cov
```

### Pre-commit Hook

```bash
# Instalar pre-commit
pip install pre-commit

# Activar
pre-commit install

# Los tests se ejecutarán antes de cada commit
```

---

## 📝 Contribuir

### Agregar Nuevo Test

1. Identifica la suite correcta (`test_X_nombre.py`)
2. Agrega el test con nombre descriptivo
3. Marca apropiadamente (`@pytest.mark.critical`)
4. Ejecuta la suite: `pytest tests/test_X_nombre.py -v`
5. Verifica coverage: `pytest tests/test_X_nombre.py --cov`

### Reportar Test que Falla

1. Anota el nombre completo del test
2. Copia el error completo
3. Documenta en GitHub Issues con label "test-failure"
4. Indica prioridad (critical/high/medium/low)

---

## 🎯 Objetivos de Calidad

### Antes del Lanzamiento

- ✅ **173/173 tests passing** (o justificar por qué no)
- ✅ **0 tests críticos fallando**
- ✅ **Coverage > 70%**
- ✅ **0 flaky tests** (tests que fallan intermitentemente)
- ✅ **Suite completa < 5 minutos** (sin API calls reales)

### Métricas de Éxito

```bash
# Ejecutar y generar reporte
pytest tests/ -v --cov --cov-report=term-missing

# Resultado esperado:
# ============= 173 passed in 180.00s =============
# Coverage: 75%
```

---

## 📞 Contacto

**Test Suite Owner**: Responsable de mantener los tests

**Issues**: GitHub Issues con label "tests"

**Docs**: Ver `MASTER_TEST_SUITE.md` para plan completo

---

**Última actualización**: 2025-01-04  
**Estado**: 🟡 En construcción  
**Cobertura actual**: 0% (tests pendientes)

