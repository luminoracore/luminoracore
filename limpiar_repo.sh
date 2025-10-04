#!/bin/bash
# Script de Limpieza para GitHub - Linux/Mac
# Elimina archivos de desarrollo interno del repositorio

echo "========================================="
echo "  LIMPIEZA DE REPOSITORIO PARA GITHUB  "
echo "========================================="
echo ""

# Confirmación
echo "Este script eliminará 24 archivos de desarrollo interno."
echo "Los archivos esenciales para usuarios se mantendrán."
echo ""
read -p "¿Continuar? (s/n): " confirm

if [ "$confirm" != "s" ] && [ "$confirm" != "S" ]; then
    echo "Operación cancelada."
    exit 0
fi

echo ""
echo "Iniciando limpieza..."
echo ""

eliminados=0

# Función para eliminar archivo
remove_safe() {
    if [ -f "$1" ]; then
        rm -f "$1"
        echo "  ✓ Eliminado: $1"
        eliminados=$((eliminados + 1))
    elif [ -d "$1" ]; then
        rm -rf "$1"
        echo "  ✓ Eliminado (carpeta): $1"
        eliminados=$((eliminados + 1))
    else
        echo "  - No existe: $1"
    fi
}

# Archivos de desarrollo interno
echo "1. Eliminando documentos de proceso interno..."
remove_safe "_ARCHIVOS_NUEVOS_GUIA.md"
remove_safe "CAMBIOS_PROVIDERS.md"
remove_safe "CAMBIOS_REFERENCIAS_DIRECTORIOS.md"
remove_safe "CARACTERISTICAS_TECNICAS_LUMINORACORE.md"
remove_safe "COMO_PROBAR_WIZARD.md"
remove_safe "ESTADO_ACTUAL_PROYECTO.md"
remove_safe "GUIA_SETUP_WEB_DEMO.md"
remove_safe "GUIA_VISUAL_LUMINORACORE.md"
remove_safe "MEJORAS_DOCUMENTACION.md"
remove_safe "PLAN_LIDERAZGO_LUMINORACORE.md"
remove_safe "PROGRESO_LIDERAZGO.md"
remove_safe "RESUMEN_EJECUTIVO.md"
remove_safe "RESUMEN_CAMBIOS_PERSONALIDADES.md"
remove_safe "RESUMEN_SCRIPT_VERIFICACION.md"
remove_safe "RESPUESTA_SCRIPT_VERIFICACION.md"
remove_safe "RESUMEN_SESION_MEJORAS.md"
remove_safe "ROADMAP_IMPLEMENTACION.md"

echo ""
echo "2. Eliminando documentos duplicados..."
remove_safe "COMO_USAR_LUMINORACORE.md"
remove_safe "EMPIEZA_AQUI.txt"
remove_safe "README_DOCUMENTACION.md"
remove_safe "README_EMPEZAR.md"
remove_safe "LEEME_PRIMERO.md"

echo ""
echo "3. Eliminando archivos temporales..."
remove_safe "test_wizard_simple.py"
remove_safe "Lumiracore.zip"
remove_safe "LIMPIEZA_REPO_GITHUB.md"

echo ""
echo "4. Eliminando carpetas de desarrollo..."
remove_safe "Docs"
remove_safe "personalidades"

echo ""
echo "========================================="
echo "  LIMPIEZA COMPLETADA                   "
echo "========================================="
echo ""
echo "Archivos/carpetas eliminados: $eliminados"
echo ""

# Verificar archivos esenciales
echo "Verificando archivos esenciales..."
echo ""

esenciales=(
    "README.md"
    "INICIO_RAPIDO.md"
    "GUIA_INSTALACION_USO.md"
    "GUIA_CREAR_PERSONALIDADES.md"
    "GUIA_VERIFICACION_INSTALACION.md"
    "CHEATSHEET.md"
    "INDICE_DOCUMENTACION.md"
    "ejemplo_quick_start_core.py"
    "ejemplo_quick_start_cli.py"
    "ejemplo_quick_start_sdk.py"
    "verificar_instalacion.py"
    "instalar_todo.ps1"
    "instalar_todo.sh"
)

faltantes=0
for archivo in "${esenciales[@]}"; do
    if [ -f "$archivo" ]; then
        echo "  ✓ $archivo"
    else
        echo "  ✗ FALTA: $archivo"
        faltantes=$((faltantes + 1))
    fi
done

echo ""
if [ $faltantes -eq 0 ]; then
    echo "✓ Todos los archivos esenciales están presentes"
else
    echo "✗ Faltan $faltantes archivos esenciales"
fi

echo ""
echo "Próximos pasos:"
echo "  1. Revisar cambios con: git status"
echo "  2. Añadir cambios: git add ."
echo "  3. Commit: git commit -m 'Clean repo for GitHub release'"
echo "  4. Push: git push origin main"
echo ""

