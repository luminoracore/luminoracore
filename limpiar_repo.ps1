# Script de Limpieza para GitHub - Windows PowerShell
# Elimina archivos de desarrollo interno del repositorio

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  LIMPIEZA DE REPOSITORIO PARA GITHUB  " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Confirmación
Write-Host "Este script eliminará 24 archivos de desarrollo interno." -ForegroundColor Yellow
Write-Host "Los archivos esenciales para usuarios se mantendrán." -ForegroundColor Green
Write-Host ""
$confirm = Read-Host "¿Continuar? (s/n)"

if ($confirm -ne "s" -and $confirm -ne "S") {
    Write-Host "Operación cancelada." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Iniciando limpieza..." -ForegroundColor Green
Write-Host ""

$eliminados = 0
$errores = 0

# Función para eliminar archivo
function Remove-SafeItem {
    param($path)
    if (Test-Path $path) {
        try {
            Remove-Item $path -Force
            Write-Host "  ✓ Eliminado: $path" -ForegroundColor Green
            return 1
        } catch {
            Write-Host "  ✗ Error al eliminar: $path" -ForegroundColor Red
            return 0
        }
    } else {
        Write-Host "  - No existe: $path" -ForegroundColor Gray
        return 0
    }
}

# Función para eliminar carpeta
function Remove-SafeFolder {
    param($path)
    if (Test-Path $path) {
        try {
            Remove-Item $path -Recurse -Force
            Write-Host "  ✓ Eliminado (carpeta): $path" -ForegroundColor Green
            return 1
        } catch {
            Write-Host "  ✗ Error al eliminar (carpeta): $path" -ForegroundColor Red
            return 0
        }
    } else {
        Write-Host "  - No existe (carpeta): $path" -ForegroundColor Gray
        return 0
    }
}

# Archivos de desarrollo interno
Write-Host "1. Eliminando documentos de proceso interno..." -ForegroundColor Cyan
$eliminados += Remove-SafeItem "_ARCHIVOS_NUEVOS_GUIA.md"
$eliminados += Remove-SafeItem "CAMBIOS_PROVIDERS.md"
$eliminados += Remove-SafeItem "CAMBIOS_REFERENCIAS_DIRECTORIOS.md"
$eliminados += Remove-SafeItem "CARACTERISTICAS_TECNICAS_LUMINORACORE.md"
$eliminados += Remove-SafeItem "COMO_PROBAR_WIZARD.md"
$eliminados += Remove-SafeItem "ESTADO_ACTUAL_PROYECTO.md"
$eliminados += Remove-SafeItem "GUIA_SETUP_WEB_DEMO.md"
$eliminados += Remove-SafeItem "GUIA_VISUAL_LUMINORACORE.md"
$eliminados += Remove-SafeItem "MEJORAS_DOCUMENTACION.md"
$eliminados += Remove-SafeItem "PLAN_LIDERAZGO_LUMINORACORE.md"
$eliminados += Remove-SafeItem "PROGRESO_LIDERAZGO.md"
$eliminados += Remove-SafeItem "RESUMEN_EJECUTIVO.md"
$eliminados += Remove-SafeItem "RESUMEN_CAMBIOS_PERSONALIDADES.md"
$eliminados += Remove-SafeItem "RESUMEN_SCRIPT_VERIFICACION.md"
$eliminados += Remove-SafeItem "RESPUESTA_SCRIPT_VERIFICACION.md"
$eliminados += Remove-SafeItem "RESUMEN_SESION_MEJORAS.md"
$eliminados += Remove-SafeItem "ROADMAP_IMPLEMENTACION.md"

Write-Host ""
Write-Host "2. Eliminando documentos duplicados..." -ForegroundColor Cyan
$eliminados += Remove-SafeItem "COMO_USAR_LUMINORACORE.md"
$eliminados += Remove-SafeItem "EMPIEZA_AQUI.txt"
$eliminados += Remove-SafeItem "README_DOCUMENTACION.md"
$eliminados += Remove-SafeItem "README_EMPEZAR.md"
$eliminados += Remove-SafeItem "LEEME_PRIMERO.md"

Write-Host ""
Write-Host "3. Eliminando archivos temporales..." -ForegroundColor Cyan
$eliminados += Remove-SafeItem "test_wizard_simple.py"
$eliminados += Remove-SafeItem "Lumiracore.zip"
$eliminados += Remove-SafeItem "LIMPIEZA_REPO_GITHUB.md"

Write-Host ""
Write-Host "4. Eliminando carpetas de desarrollo..." -ForegroundColor Cyan
$eliminados += Remove-SafeFolder "Docs"
$eliminados += Remove-SafeFolder "personalidades"

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  LIMPIEZA COMPLETADA                   " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Archivos/carpetas eliminados: $eliminados" -ForegroundColor Green
Write-Host ""

# Verificar archivos esenciales
Write-Host "Verificando archivos esenciales..." -ForegroundColor Cyan
Write-Host ""

$esenciales = @(
    "README.md",
    "INICIO_RAPIDO.md",
    "GUIA_INSTALACION_USO.md",
    "GUIA_CREAR_PERSONALIDADES.md",
    "GUIA_VERIFICACION_INSTALACION.md",
    "CHEATSHEET.md",
    "INDICE_DOCUMENTACION.md",
    "ejemplo_quick_start_core.py",
    "ejemplo_quick_start_cli.py",
    "ejemplo_quick_start_sdk.py",
    "verificar_instalacion.py",
    "instalar_todo.ps1",
    "instalar_todo.sh"
)

$faltantes = 0
foreach ($archivo in $esenciales) {
    if (Test-Path $archivo) {
        Write-Host "  ✓ $archivo" -ForegroundColor Green
    } else {
        Write-Host "  ✗ FALTA: $archivo" -ForegroundColor Red
        $faltantes++
    }
}

Write-Host ""
if ($faltantes -eq 0) {
    Write-Host "✓ Todos los archivos esenciales están presentes" -ForegroundColor Green
} else {
    Write-Host "✗ Faltan $faltantes archivos esenciales" -ForegroundColor Red
}

Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Cyan
Write-Host "  1. Revisar cambios con: git status" -ForegroundColor White
Write-Host "  2. Añadir cambios: git add ." -ForegroundColor White
Write-Host "  3. Commit: git commit -m 'Clean repo for GitHub release'" -ForegroundColor White
Write-Host "  4. Push: git push origin main" -ForegroundColor White
Write-Host ""

