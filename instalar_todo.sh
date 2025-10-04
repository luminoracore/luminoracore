#!/bin/bash
# Script de instalación completa para LuminoraCore
# Linux/Mac
# Ejecuta esto para instalar todos los componentes de una vez

set -e  # Salir si hay algún error

echo "============================================================"
echo "  🧠 LuminoraCore - Instalación Completa"
echo "============================================================"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Función para mensajes de éxito
success() {
    echo -e "  ${GREEN}✅ $1${NC}"
}

# Función para mensajes de error
error() {
    echo -e "  ${RED}❌ $1${NC}"
}

# Función para mensajes de información
info() {
    echo -e "  ${YELLOW}ℹ️  $1${NC}"
}

# Verificar Python
echo "1️⃣  Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    success "Python instalado: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version)
    success "Python instalado: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    error "Python no encontrado. Instala Python 3.8+ primero."
    exit 1
fi

# Verificar pip
echo ""
echo "2️⃣  Verificando pip..."
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    success "pip instalado: $PIP_VERSION"
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_VERSION=$(pip --version)
    success "pip instalado: $PIP_VERSION"
    PIP_CMD="pip"
else
    error "pip no encontrado"
    exit 1
fi

# Crear entorno virtual
echo ""
echo "3️⃣  Creando entorno virtual..."
if [ -d "venv" ]; then
    info "El entorno virtual ya existe"
    read -p "¿Deseas recrearlo? (s/n): " respuesta
    if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
        rm -rf venv
        $PYTHON_CMD -m venv venv
        success "Entorno virtual recreado"
    else
        info "Usando entorno virtual existente"
    fi
else
    $PYTHON_CMD -m venv venv
    success "Entorno virtual creado"
fi

# Activar entorno virtual
echo ""
echo "4️⃣  Activando entorno virtual..."
source venv/bin/activate
success "Entorno virtual activado"

# Instalar luminoracore (motor base)
echo ""
echo "5️⃣  Instalando luminoracore (motor base)..."
cd luminoracore
$PIP_CMD install -e . --quiet
if [ $? -eq 0 ]; then
    success "luminoracore instalado"
else
    error "Error al instalar luminoracore"
    exit 1
fi
cd ..

# Instalar luminoracore-cli
echo ""
echo "6️⃣  Instalando luminoracore-cli..."
cd luminoracore-cli
$PIP_CMD install -e . --quiet
if [ $? -eq 0 ]; then
    success "luminoracore-cli instalado"
else
    error "Error al instalar luminoracore-cli"
    exit 1
fi
cd ..

# Preguntar qué proveedores instalar para el SDK
echo ""
echo "7️⃣  Instalando luminoracore-sdk..."
echo ""
echo -e "   ${CYAN}¿Qué proveedores LLM deseas instalar?${NC}"
echo "   1) Todos los proveedores (OpenAI, Anthropic, Cohere, Google, etc.)"
echo "   2) Solo OpenAI"
echo "   3) Solo Anthropic"
echo "   4) Solo las dependencias base (sin proveedores)"
echo ""
read -p "   Selecciona una opción (1-4): " opcion

cd luminoracore-sdk-python
case $opcion in
    1)
        $PIP_CMD install -e ".[all]" --quiet
        success "SDK instalado con todos los proveedores"
        ;;
    2)
        $PIP_CMD install -e ".[openai]" --quiet
        success "SDK instalado con OpenAI"
        ;;
    3)
        $PIP_CMD install -e ".[anthropic]" --quiet
        success "SDK instalado con Anthropic"
        ;;
    *)
        $PIP_CMD install -e . --quiet
        success "SDK instalado (solo dependencias base)"
        ;;
esac
cd ..

# Verificar instalaciones
echo ""
echo "8️⃣  Verificando instalaciones..."

# Verificar luminoracore
if $PYTHON_CMD -c "import luminoracore; print(f'luminoracore v{luminoracore.__version__}')" &> /dev/null; then
    success "luminoracore funcionando"
else
    error "luminoracore no funciona correctamente"
fi

# Verificar CLI
if luminoracore --version &> /dev/null; then
    success "luminoracore-cli funcionando"
else
    error "luminoracore-cli no funciona correctamente"
fi

# Verificar SDK
if $PYTHON_CMD -c "from luminoracore import LuminoraCoreClient" &> /dev/null; then
    success "luminoracore-sdk funcionando"
else
    error "luminoracore-sdk no funciona correctamente"
fi

# Resumen final
echo ""
echo "============================================================"
echo -e "  ${GREEN}✅ INSTALACIÓN COMPLETADA${NC}"
echo "============================================================"
echo ""
echo "📦 Componentes instalados:"
echo -e "   ${GREEN}✅ luminoracore (motor base)${NC}"
echo -e "   ${GREEN}✅ luminoracore-cli (herramienta CLI)${NC}"
echo -e "   ${GREEN}✅ luminoracore-sdk (SDK completo)${NC}"
echo ""
echo "🚀 Próximos pasos:"
echo ""
echo -e "   ${CYAN}1. Prueba los componentes:${NC}"
echo -e "      ${YELLOW}python ejemplo_quick_start_core.py${NC}"
echo -e "      ${YELLOW}python ejemplo_quick_start_cli.py${NC}"
echo -e "      ${YELLOW}python ejemplo_quick_start_sdk.py${NC}"
echo ""
echo -e "   ${CYAN}2. Lee la guía completa:${NC}"
echo -e "      ${YELLOW}GUIA_INSTALACION_USO.md${NC}"
echo ""
echo -e "   ${CYAN}3. Explora los ejemplos:${NC}"
echo -e "      ${YELLOW}luminoracore/examples/${NC}"
echo -e "      ${YELLOW}luminoracore-sdk-python/examples/${NC}"
echo ""
echo -e "   ${CYAN}4. Prueba el CLI:${NC}"
echo -e "      ${YELLOW}luminoracore --help${NC}"
echo -e "      ${YELLOW}luminoracore list${NC}"
echo ""
echo "============================================================"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANTE: No olvides activar el entorno virtual cada vez:${NC}"
echo "   source venv/bin/activate"
echo ""

