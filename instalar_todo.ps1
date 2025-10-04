# Script de instalación completa para LuminoraCore
# Windows PowerShell
# Ejecuta esto para instalar todos los componentes de una vez

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  LuminoraCore - Instalación Completa" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Función para mostrar mensajes de éxito
function Write-Success {
    param($Message)
    Write-Host "  ✅ $Message" -ForegroundColor Green
}

# Función para mostrar mensajes de error
function Write-Error-Custom {
    param($Message)
    Write-Host "  ❌ $Message" -ForegroundColor Red
}

# Función para mostrar mensajes de información
function Write-Info {
    param($Message)
    Write-Host "  ℹ️  $Message" -ForegroundColor Yellow
}

# Verificar Python
Write-Host "1️⃣  Verificando Python..." -ForegroundColor White
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Python instalado: $pythonVersion"
    } else {
        Write-Error-Custom "Python no encontrado. Instala Python 3.8+ primero."
        exit 1
    }
} catch {
    Write-Error-Custom "Error al verificar Python: $_"
    exit 1
}

# Verificar pip
Write-Host ""
Write-Host "2️⃣  Verificando pip..." -ForegroundColor White
try {
    $pipVersion = pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "pip instalado: $pipVersion"
    } else {
        Write-Error-Custom "pip no encontrado"
        exit 1
    }
} catch {
    Write-Error-Custom "Error al verificar pip: $_"
    exit 1
}

# Crear entorno virtual
Write-Host ""
Write-Host "3️⃣  Creando entorno virtual..." -ForegroundColor White
if (Test-Path "venv") {
    Write-Info "El entorno virtual ya existe"
    $respuesta = Read-Host "¿Deseas recrearlo? (s/n)"
    if ($respuesta -eq "s" -or $respuesta -eq "S") {
        Remove-Item -Recurse -Force "venv"
        python -m venv venv
        Write-Success "Entorno virtual recreado"
    } else {
        Write-Info "Usando entorno virtual existente"
    }
} else {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Entorno virtual creado"
    } else {
        Write-Error-Custom "Error al crear entorno virtual"
        exit 1
    }
}

# Activar entorno virtual
Write-Host ""
Write-Host "4️⃣  Activando entorno virtual..." -ForegroundColor White
& .\venv\Scripts\Activate.ps1
if ($LASTEXITCODE -eq 0) {
    Write-Success "Entorno virtual activado"
} else {
    Write-Error-Custom "Error al activar entorno virtual"
    Write-Info "Puede que necesites cambiar la política de ejecución:"
    Write-Info "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    exit 1
}

# Instalar luminoracore (motor base)
Write-Host ""
Write-Host "5️⃣  Instalando luminoracore (motor base)..." -ForegroundColor White
Push-Location luminoracore
try {
    pip install -e . --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Success "luminoracore instalado"
    } else {
        Write-Error-Custom "Error al instalar luminoracore"
        Pop-Location
        exit 1
    }
} catch {
    Write-Error-Custom "Error: $_"
    Pop-Location
    exit 1
}
Pop-Location

# Instalar luminoracore-cli
Write-Host ""
Write-Host "6️⃣  Instalando luminoracore-cli..." -ForegroundColor White
Push-Location luminoracore-cli
try {
    pip install -e . --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Success "luminoracore-cli instalado"
    } else {
        Write-Error-Custom "Error al instalar luminoracore-cli"
        Pop-Location
        exit 1
    }
} catch {
    Write-Error-Custom "Error: $_"
    Pop-Location
    exit 1
}
Pop-Location

# Preguntar qué proveedores instalar para el SDK
Write-Host ""
Write-Host "7️⃣  Instalando luminoracore-sdk..." -ForegroundColor White
Write-Host ""
Write-Host "   ¿Qué proveedores LLM deseas instalar?" -ForegroundColor Cyan
Write-Host "   1) Todos los proveedores (OpenAI, Anthropic, Cohere, Google, etc.)" -ForegroundColor White
Write-Host "   2) Solo OpenAI" -ForegroundColor White
Write-Host "   3) Solo Anthropic" -ForegroundColor White
Write-Host "   4) Solo las dependencias base (sin proveedores)" -ForegroundColor White
Write-Host ""
$opcion = Read-Host "   Selecciona una opción (1-4)"

Push-Location luminoracore-sdk-python
try {
    switch ($opcion) {
        "1" {
            pip install -e ".[all]" --quiet
            Write-Success "SDK instalado con todos los proveedores"
        }
        "2" {
            pip install -e ".[openai]" --quiet
            Write-Success "SDK instalado con OpenAI"
        }
        "3" {
            pip install -e ".[anthropic]" --quiet
            Write-Success "SDK instalado con Anthropic"
        }
        "4" {
            pip install -e . --quiet
            Write-Success "SDK instalado (solo dependencias base)"
        }
        default {
            pip install -e . --quiet
            Write-Success "SDK instalado (solo dependencias base)"
        }
    }
} catch {
    Write-Error-Custom "Error al instalar SDK: $_"
    Pop-Location
    exit 1
}
Pop-Location

# Verificar instalaciones
Write-Host ""
Write-Host "8️⃣  Verificando instalaciones..." -ForegroundColor White

# Verificar luminoracore
try {
    python -c "import luminoracore; print(f'luminoracore v{luminoracore.__version__}')" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Success "luminoracore funcionando"
    } else {
        Write-Error-Custom "luminoracore no funciona correctamente"
    }
} catch {
    Write-Error-Custom "Error al verificar luminoracore"
}

# Verificar CLI
try {
    $cliCheck = luminoracore --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "luminoracore-cli funcionando"
    } else {
        Write-Error-Custom "luminoracore-cli no funciona correctamente"
    }
} catch {
    Write-Error-Custom "Error al verificar CLI"
}

# Verificar SDK
try {
    python -c "from luminoracore import LuminoraCoreClient" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Success "luminoracore-sdk funcionando"
    } else {
        Write-Error-Custom "luminoracore-sdk no funciona correctamente"
    }
} catch {
    Write-Error-Custom "Error al verificar SDK"
}

# Resumen final
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  ✅ INSTALACIÓN COMPLETADA" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📦 Componentes instalados:" -ForegroundColor White
Write-Host "   ✅ luminoracore (motor base)" -ForegroundColor Green
Write-Host "   ✅ luminoracore-cli (herramienta CLI)" -ForegroundColor Green
Write-Host "   ✅ luminoracore-sdk (SDK completo)" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 Próximos pasos:" -ForegroundColor White
Write-Host ""
Write-Host "   1. Prueba los componentes:" -ForegroundColor Cyan
Write-Host "      python ejemplo_quick_start_core.py" -ForegroundColor Yellow
Write-Host "      python ejemplo_quick_start_cli.py" -ForegroundColor Yellow
Write-Host "      python ejemplo_quick_start_sdk.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "   2. Lee la guía completa:" -ForegroundColor Cyan
Write-Host "      GUIA_INSTALACION_USO.md" -ForegroundColor Yellow
Write-Host ""
Write-Host "   3. Explora los ejemplos:" -ForegroundColor Cyan
Write-Host "      luminoracore/examples/" -ForegroundColor Yellow
Write-Host "      luminoracore-sdk-python/examples/" -ForegroundColor Yellow
Write-Host ""
Write-Host "   4. Prueba el CLI:" -ForegroundColor Cyan
Write-Host "      luminoracore --help" -ForegroundColor Yellow
Write-Host "      luminoracore list" -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "⚠️  IMPORTANTE: No olvides activar el entorno virtual cada vez:" -ForegroundColor Yellow
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""

