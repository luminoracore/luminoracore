#!/bin/bash
# Script de limpieza final del repositorio LuminoraCore
# Elimina archivos de desarrollo y deja solo lo esencial

set -e

echo ""
echo "================================================================"
echo "       LIMPIEZA FINAL - LUMINORACORE REPOSITORY"
echo "================================================================"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# Confirmar con el usuario
echo -e "${YELLOW}Este script eliminará:${NC}"
echo -e "${YELLOW}  - 19 archivos de documentación de desarrollo${NC}"
echo -e "${YELLOW}  - Scripts temporales de testing${NC}"
echo -e "${YELLOW}  - Directorios __pycache__ y build${NC}"
echo ""
echo -e "${GREEN}Archivos que se mantendrán:${NC}"
echo -e "${GREEN}  - README.md y guías principales${NC}"
echo -e "${GREEN}  - Scripts de instalación y verificación${NC}"
echo -e "${GREEN}  - Ejemplos y tests${NC}"
echo -e "${GREEN}  - Código fuente completo${NC}"
echo ""

read -p "¿Continuar con la limpieza? (s/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${YELLOW}Limpieza cancelada.${NC}"
    exit 0
fi

echo ""
echo -e "${CYAN}Iniciando limpieza...${NC}"
echo ""

# Contador de archivos eliminados
deleted_count=0

# Función para eliminar archivo con logging
remove_file_with_log() {
    local file=$1
    if [ -f "$file" ]; then
        rm -f "$file"
        echo -e "${GREEN}  ✓ Eliminado: $file${NC}"
        ((deleted_count++))
    else
        echo -e "${GRAY}  ○ No encontrado: $file${NC}"
    fi
}

# Función para eliminar directorio con logging
remove_directory_with_log() {
    local dir=$1
    if [ -d "$dir" ]; then
        rm -rf "$dir"
        echo -e "${GREEN}  ✓ Eliminado: $dir${NC}"
        ((deleted_count++))
    else
        echo -e "${GRAY}  ○ No encontrado: $dir${NC}"
    fi
}

# 1. Eliminar reportes y estados
echo -e "${CYAN}1. Eliminando reportes y estados de desarrollo...${NC}"
remove_file_with_log "CRITICAL_FIXES_AND_VALIDATION.md"
remove_file_with_log "ESTADO_FINAL_COMPLETO.md"
remove_file_with_log "PROGRESO_SESION_ACTUAL.md"
remove_file_with_log "SESION_VALIDACION_RESUMEN.md"
remove_file_with_log "RESUMEN_SESION_TESTS.md"
remove_file_with_log "REPORTE_100_FINAL.md"
remove_file_with_log "REPORTE_CLI_COMPLETO.md"
remove_file_with_log "REPORTE_FINAL_100_PORCIENTO.md"
remove_file_with_log "REPORTE_SDK_ESTADO.md"
remove_file_with_log "REPORTE_SDK_FINAL.md"

# 2. Eliminar documentos de refactoring
echo ""
echo -e "${CYAN}2. Eliminando documentos de refactoring...${NC}"
remove_file_with_log "REFACTORING_COMPLETO.md"
remove_file_with_log "REFACTORING_PLAN.md"
remove_file_with_log "REFACTORING_RESUMEN.md"

# 3. Eliminar planes internos
echo ""
echo -e "${CYAN}3. Eliminando planes internos...${NC}"
remove_file_with_log "PLAN_PRUEBAS_COMPLETO.md"
remove_file_with_log "PLAN_VALIDACION_COMPLETA.md"

# 4. Eliminar explicaciones internas
echo ""
echo -e "${CYAN}4. Eliminando explicaciones internas...${NC}"
remove_file_with_log "EXPLICACION_TESTS_VS_REAL.md"
remove_file_with_log "EXPLICACION_TESTS.md"

# 5. Eliminar scripts de limpieza
echo ""
echo -e "${CYAN}5. Eliminando scripts de limpieza...${NC}"
remove_file_with_log "limpiar_repo.ps1"
remove_file_with_log "limpiar_repo.sh"

# 6. Eliminar scripts temporales
echo ""
echo -e "${CYAN}6. Eliminando scripts temporales...${NC}"
remove_file_with_log "test_imports.py"

# 7. Eliminar directorios de build y cache
echo ""
echo -e "${CYAN}7. Eliminando directorios de build y cache...${NC}"

# Build del motor base
remove_directory_with_log "luminoracore/build"

# __pycache__ en múltiples ubicaciones
find . -type d -name "__pycache__" | while read dir; do
    remove_directory_with_log "$dir"
done

# 8. Eliminar documento de limpieza
echo ""
echo -e "${CYAN}8. Eliminando documentos de limpieza...${NC}"
remove_file_with_log "LIMPIEZA_FINAL.md"

# Resumen
echo ""
echo "================================================================"
echo "                    LIMPIEZA COMPLETADA"
echo "================================================================"
echo ""
echo -e "${GREEN}Archivos/directorios eliminados: $deleted_count${NC}"
echo ""

# Verificar tests después de limpieza
echo -e "${CYAN}Verificando que los tests siguen funcionando...${NC}"
echo ""

if python3 run_tests.py 1 2>&1 | grep -q "passed"; then
    echo -e "${GREEN}✓ Tests verificados correctamente${NC}"
else
    echo -e "${YELLOW}⚠ No se pudieron verificar los tests automáticamente${NC}"
    echo -e "${YELLOW}  Ejecuta manualmente: python3 run_tests.py${NC}"
fi

echo ""
echo -e "${GREEN}Archivos mantenidos:${NC}"
echo -e "${GREEN}  ✓ README.md${NC}"
echo -e "${GREEN}  ✓ GUIA_INSTALACION_USO.md${NC}"
echo -e "${GREEN}  ✓ INICIO_RAPIDO.md${NC}"
echo -e "${GREEN}  ✓ CHEATSHEET.md${NC}"
echo -e "${GREEN}  ✓ Guías específicas (5 archivos)${NC}"
echo -e "${GREEN}  ✓ Scripts de instalación y verificación${NC}"
echo -e "${GREEN}  ✓ Ejemplos (5 archivos)${NC}"
echo -e "${GREEN}  ✓ Tests completos${NC}"
echo -e "${GREEN}  ✓ Código fuente completo${NC}"
echo ""

echo "================================================================"
echo -e "${GREEN}El repositorio está listo para usuarios finales!${NC}"
echo ""
echo -e "${YELLOW}Siguiente paso:${NC}"
echo "  git add ."
echo "  git commit -m 'chore: clean repository for production release'"
echo "  git push origin main"
echo "================================================================"
echo ""

# Preguntar si eliminar este script también
read -p "$(echo -e ${YELLOW}¿Eliminar este script de limpieza también? \(s/n\): ${NC})" -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo -e "${CYAN}Eliminando limpieza_final.sh...${NC}"
    sleep 1
    rm -f "$0"
    echo -e "${GREEN}✓ Script de limpieza eliminado${NC}"
fi

echo ""
echo -e "${GREEN}¡Limpieza finalizada!${NC}"
echo ""

