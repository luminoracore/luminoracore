# Quick Reference: Distribution & Publishing

## 🎯 Para usar LuminoraCore en otro proyecto LOCAL

### Opción 1: Desde wheels locales (SIN publicar en PyPI)

```bash
# 1. Compilar paquetes (solo una vez)
.\build_all_packages.ps1

# 2. En tu OTRO proyecto:
pip install D:/Proyectos Ereace/LuminoraCoreBase/releases/luminoracore-1.0.0-py3-none-any.whl
pip install D:/Proyectos Ereace/LuminoraCoreBase/releases/luminoracore_cli-1.0.0-py3-none-any.whl
pip install D:/Proyectos Ereace/LuminoraCoreBase/releases/luminoracore_sdk-1.0.0-py3-none-any.whl
```

### Opción 2: Desde directorio local

```bash
# En tu OTRO proyecto:
pip install D:/Proyectos Ereace/LuminoraCoreBase/luminoracore
pip install D:/Proyectos Ereace/LuminoraCoreBase/luminoracore-cli
pip install D:/Proyectos Ereace/LuminoraCoreBase/luminoracore-sdk-python
```

---

## 🌐 Para publicar en PyPI (distribución mundial)

### Paso 1: Crear cuenta en PyPI
1. Ir a: https://pypi.org/account/register/
2. Verificar email
3. Crear API token: https://pypi.org/manage/account/token/
4. Guardar token (empieza con `pypi-`)

### Paso 2: Compilar y publicar

```bash
# 1. Compilar paquetes
.\build_all_packages.ps1

# 2. Probar localmente (opcional)
.\install_from_local.ps1
python verify_installation.py

# 3. Publicar en PyPI
.\publish_to_pypi.ps1
# Usuario: __token__
# Password: pypi-TU-TOKEN-AQUI
```

### Paso 3: Listo

Desde ese momento, CUALQUIER persona puede instalar:
```bash
pip install luminoracore
pip install luminoracore-cli
pip install luminoracore-sdk
```

---

## 📁 Archivos y scripts disponibles

| Script | Propósito |
|--------|-----------|
| `build_all_packages.ps1` | Compila los 3 paquetes → crea .whl en `releases/` |
| `install_from_local.ps1` | Instala desde wheels locales (para probar) |
| `publish_to_pypi.ps1` | Publica en PyPI (distribución mundial) |
| `install_all.ps1` | Instala desde código fuente (desarrollo) |
| `verify_installation.py` | Verifica que todo esté instalado correctamente |

---

## 🔄 Workflow completo

```
┌─────────────────────────────────────────┐
│ 1. DESARROLLO                           │
│    - Editar código                      │
│    - Ejecutar tests: pytest tests/ -v   │
│    - Verificar: verify_installation.py  │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 2. COMPILAR PAQUETES                    │
│    .\build_all_packages.ps1             │
│    → Genera .whl en releases/           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 3. PROBAR LOCALMENTE                    │
│    .\install_from_local.ps1             │
│    python verify_installation.py        │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│ 4. PUBLICAR EN PyPI (opcional)          │
│    .\publish_to_pypi.ps1                │
│    → Disponible para TODO EL MUNDO      │
└─────────────────────────────────────────┘
```

---

## ⚠️ Importante

### Antes de publicar en PyPI:

- ✅ Todos los tests pasan (`pytest tests/ -v`)
- ✅ `verify_installation.py` muestra: `🎉 INSTALLATION COMPLETE AND CORRECT`
- ✅ Documentación actualizada
- ✅ README.md correcto
- ✅ Versiones correctas en `setup.py`
- ✅ Sin datos sensibles (API keys, passwords)

### Versionado

**No puedes sobrescribir versiones en PyPI.**

Si ya publicaste `1.0.0`, la próxima debe ser `1.0.1`, `1.1.0`, o `2.0.0`.

Actualizar versiones en:
- `luminoracore/setup.py` → `version="1.0.1"`
- `luminoracore-cli/luminoracore_cli/__version__.py` → `__version__ = "1.0.1"`
- `luminoracore-sdk-python/luminoracore_sdk/__version__.py` → `__version__ = "1.0.1"`

---

## 📖 Guías completas

- **[DOWNLOAD.md](DOWNLOAD.md)** - Opciones de descarga para usuarios
- **[PUBLISHING_GUIDE.md](PUBLISHING_GUIDE.md)** - Guía completa de publicación
- **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Instalación detallada

---

**Cuando estés listo para publicar, ejecuta: `.\build_all_packages.ps1` y después `.\publish_to_pypi.ps1`**

