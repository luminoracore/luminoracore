# 🌐 GUÍA COMPLETA: SETUP WEB DEMO LUMINORACORE

## 📁 ESTRUCTURA DE DIRECTORIOS RECOMENDADA

```
~/proyectos/                       # Tu directorio de proyectos
├── luminoracore/                  # ← Proyecto LuminoraCore (Backend/Core)
│   ├── luminoracore/              # Motor principal
│   ├── luminoracore-cli/          # CLI
│   ├── luminoracore-sdk-python/   # SDK Python
│   └── README.md
│
└── luminoracore-web/              # ← NUEVO proyecto (Frontend/Demo)
    ├── frontend/                  # Next.js app
    │   ├── src/
    │   │   ├── pages/
    │   │   ├── components/
    │   │   ├── styles/
    │   │   └── lib/
    │   ├── public/
    │   ├── package.json
    │   └── next.config.js
    │
    ├── backend/                   # FastAPI server
    │   ├── app/
    │   │   ├── main.py
    │   │   ├── routers/
    │   │   ├── services/
    │   │   └── models/
    │   ├── requirements.txt
    │   └── .env.example
    │
    ├── docker/                    # Docker configs
    │   ├── docker-compose.yml
    │   ├── Dockerfile.frontend
    │   └── Dockerfile.backend
    │
    ├── deploy/                    # Deploy configs
    │   └── nginx.conf
    │
    └── README.md
```

---

## 🚀 PASO 1: CREAR ESTRUCTURA BASE

### **1.1 Crear directorio principal**

```bash
# En tu directorio de proyectos
# Windows PowerShell:
cd ~\proyectos
mkdir luminoracore-web
cd luminoracore-web

# Linux/Mac:
cd ~/proyectos
mkdir luminoracore-web
cd luminoracore-web
```

### **1.2 Inicializar Git**

```bash
git init
echo "node_modules/" > .gitignore
echo "__pycache__/" >> .gitignore
echo ".env" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".next/" >> .gitignore
echo "venv/" >> .gitignore
```

---

## 🎨 PASO 2: SETUP DEL FRONTEND (Next.js + TypeScript)

### **2.1 Crear aplicación Next.js**

```bash
# Desde LuminoraCoreWeb/
npx create-next-app@latest frontend --typescript --tailwind --app --import-alias "@/*"

# Durante la instalación, responder:
# ✓ Would you like to use TypeScript? Yes
# ✓ Would you like to use ESLint? Yes
# ✓ Would you like to use Tailwind CSS? Yes
# ✓ Would you like to use `src/` directory? Yes
# ✓ Would you like to use App Router? Yes
# ✓ Would you like to customize the default import alias? No
```

### **2.2 Instalar dependencias adicionales**

```bash
cd frontend

# UI y animaciones
npm install @heroicons/react framer-motion

# Cliente HTTP
npm install axios

# Markdown y syntax highlighting
npm install react-markdown react-syntax-highlighter
npm install --save-dev @types/react-syntax-highlighter

# Utilidades
npm install clsx tailwind-merge

# State management (opcional)
npm install zustand
```

### **2.3 Estructura del frontend**

```bash
# Crear directorios
cd src
mkdir components
mkdir lib
mkdir types
mkdir hooks

# Crear subdirectorios
cd components
mkdir Landing
mkdir Demo
mkdir Docs
mkdir Common

cd ../lib
echo "// Utility functions" > utils.ts
echo "// API client" > api.ts
```

---

## 🐍 PASO 3: SETUP DEL BACKEND (FastAPI + Python)

### **3.1 Crear estructura del backend**

```bash
# Desde LuminoraCoreWeb/
mkdir backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Si da error de permisos, ejecutar como admin:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **3.2 Crear requirements.txt**

```bash
# Crear archivo requirements.txt
cat > requirements.txt << 'EOF'
# FastAPI y servidor
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# CORS
python-dotenv==1.0.0

# Validación
pydantic==2.5.0
pydantic-settings==2.1.0

# HTTP client
httpx==0.25.2
aiohttp==3.9.1

# Utilidades
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# LuminoraCore SDK (local)
# Se instalará con: pip install -e ../../luminoracore/luminoracore-sdk-python/
EOF
```

### **3.3 Instalar dependencias**

```bash
# Instalar dependencias
pip install -r requirements.txt

# Instalar LuminoraCore SDK (desde el proyecto principal)
pip install -e "../../luminoracore/luminoracore-sdk-python/"
```

### **3.4 Crear estructura de carpetas**

```bash
mkdir app
cd app

# Crear archivos principales
echo "# FastAPI main app" > main.py
echo "# Configuration" > config.py

# Crear subdirectorios
mkdir routers
mkdir services
mkdir models
mkdir utils

# Crear archivos en routers
cd routers
echo "# Chat endpoints" > chat.py
echo "# Personality endpoints" > personalities.py
echo "# Compile endpoints" > compile.py

cd ../services
echo "# LLM service integration" > llm_service.py
echo "# Personality service" > personality_service.py

cd ../models
echo "# Request/Response models" > schemas.py

cd ../utils
echo "# Helper functions" > helpers.py
```

---

## ⚙️ PASO 4: CONFIGURAR VARIABLES DE ENTORNO

### **4.1 Backend: Crear `.env.example`**

```bash
# Desde LuminoraCoreWeb/backend/
cat > .env.example << 'EOF'
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# CORS
CORS_ORIGINS=http://localhost:3000,https://luminoracore.com

# LLM Provider API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
COHERE_API_KEY=your_cohere_key_here
MISTRAL_API_KEY=your_mistral_key_here

# Paths
PERSONALITIES_PATH=../../luminoracore/luminoracore/personalities

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=3600

# Logging
LOG_LEVEL=INFO
EOF

# Copiar a .env para uso local
cp .env.example .env

# IMPORTANTE: Editar .env y agregar tus API keys reales
```

### **4.2 Frontend: Crear `.env.local`**

```bash
# Desde LuminoraCoreWeb/frontend/
cat > .env.local.example << 'EOF'
# API Backend URL
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Analytics (opcional)
NEXT_PUBLIC_GA_ID=your_google_analytics_id

# Feature Flags
NEXT_PUBLIC_ENABLE_MARKETPLACE=false
NEXT_PUBLIC_ENABLE_PLAYGROUND=true
EOF

# Copiar para uso local
cp .env.local.example .env.local
```

---

## 📝 PASO 5: IMPLEMENTAR CÓDIGO BASE

### **5.1 Backend - main.py**

```bash
# Desde LuminoraCoreWeb/backend/app/
cat > main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv

from .routers import chat, personalities, compile
from .config import settings

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="LuminoraCore Demo API",
    description="Backend API for LuminoraCore web demo",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(personalities.router, prefix="/api/personalities", tags=["personalities"])
app.include_router(compile.router, prefix="/api/compile", tags=["compile"])

@app.get("/")
async def root():
    return {
        "service": "LuminoraCore Demo API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "api": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )
EOF
```

### **5.2 Backend - config.py**

```bash
cat > config.py << 'EOF'
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # LLM Provider API Keys
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    COHERE_API_KEY: Optional[str] = None
    MISTRAL_API_KEY: Optional[str] = None
    
    # Paths
    PERSONALITIES_PATH: str = "../../luminoracore/luminoracore/personalities"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 3600
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
EOF
```

### **5.3 Frontend - API Client**

```bash
# Desde LuminoraCoreWeb/frontend/src/lib/
cat > api.ts << 'EOF'
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions
export const api = {
  // Chat with personality
  chat: async (personality: string, message: string, provider: string = 'openai') => {
    const response = await apiClient.post('/api/chat', {
      personality,
      message,
      provider
    });
    return response.data;
  },
  
  // List personalities
  getPersonalities: async () => {
    const response = await apiClient.get('/api/personalities');
    return response.data;
  },
  
  // Compile personality
  compile: async (personalityData: any, provider: string) => {
    const response = await apiClient.post('/api/compile', {
      personality: personalityData,
      provider
    });
    return response.data;
  },
  
  // Health check
  health: async () => {
    const response = await apiClient.get('/health');
    return response.data;
  }
};
EOF
```

---

## 🐳 PASO 6: DOCKER SETUP (OPCIONAL)

### **6.1 Crear docker-compose.yml**

```bash
# Desde LuminoraCoreWeb/
mkdir docker
cd docker

cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  frontend:
    build:
      context: ../
      dockerfile: docker/Dockerfile.frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
    volumes:
      - ../frontend:/app
      - /app/node_modules
      - /app/.next

  backend:
    build:
      context: ../
      dockerfile: docker/Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - API_HOST=0.0.0.0
      - API_PORT=8000
    env_file:
      - ../backend/.env
    volumes:
      - ../backend:/app
      - ../../luminoracore:/luminoracore

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ../deploy/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - frontend
      - backend
EOF
```

---

## 🚀 PASO 7: SCRIPTS DE DESARROLLO

### **7.1 Crear scripts de inicio**

```bash
# Desde LuminoraCoreWeb/
cat > start-dev.sh << 'EOF'
#!/bin/bash
# Script para iniciar desarrollo (Linux/Mac)

echo "🚀 Starting LuminoraCore Web Demo..."

# Start backend
echo "📦 Starting backend..."
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "🎨 Starting frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Services started!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
EOF

chmod +x start-dev.sh
```

```powershell
# Desde LuminoraCoreWeb/
cat > start-dev.ps1 << 'EOF'
# Script para iniciar desarrollo (Windows PowerShell)

Write-Host "🚀 Starting LuminoraCore Web Demo..." -ForegroundColor Green

# Start backend
Write-Host "📦 Starting backend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --reload --port 8000"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend
Write-Host "🎨 Starting frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host ""
Write-Host "✅ Services started!" -ForegroundColor Green
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Yellow
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "   API Docs: http://localhost:8000/api/docs" -ForegroundColor Yellow
EOF
```

---

## 📚 PASO 8: CREAR README DEL PROYECTO

```bash
# Desde LuminoraCoreWeb/
cat > README.md << 'EOF'
# 🌐 LuminoraCore Web Demo

Demo web público y landing page para LuminoraCore.

## 🏗️ Estructura

```
LuminoraCoreWeb/
├── frontend/     # Next.js + TypeScript
├── backend/      # FastAPI + Python
├── docker/       # Docker configs
└── deploy/       # Deploy configs
```

## 🚀 Desarrollo Local

### Prerrequisitos

- Node.js 18+
- Python 3.8+
- npm o yarn

### Setup Rápido

1. **Clone el proyecto**
   ```bash
   git clone <repo-url>
   cd LuminoraCoreWeb
   ```

2. **Configurar Backend**
   ```bash
   cd backend
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows
   # source venv/bin/activate    # Linux/Mac
   pip install -r requirements.txt
   pip install -e ../../luminoracore/luminoracore-sdk-python/
   cp .env.example .env
   # Editar .env con tus API keys
   ```

3. **Configurar Frontend**
   ```bash
   cd ../frontend
   npm install
   cp .env.local.example .env.local
   ```

4. **Iniciar servicios**
   ```powershell
   # Opción 1: Script automatizado (Windows)
   .\start-dev.ps1
   
   # Opción 2: Manual
   # Terminal 1 - Backend
   cd backend
   .\venv\Scripts\Activate.ps1
   python -m uvicorn app.main:app --reload
   
   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

5. **Abrir en navegador**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs

## 🐳 Docker

```bash
# Iniciar con Docker Compose
docker-compose -f docker/docker-compose.yml up

# Acceder
# http://localhost (nginx)
# http://localhost:3000 (frontend directo)
# http://localhost:8000 (backend directo)
```

## 📦 Build para Producción

### Frontend
```bash
cd frontend
npm run build
npm run start
```

### Backend
```bash
cd backend
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🌐 Deploy

Ver [DEPLOY.md](DEPLOY.md) para instrucciones de deploy a:
- Vercel (Frontend)
- Railway (Backend)
- DigitalOcean (Full stack)

## 📄 Licencia

MIT License - Ver [LICENSE](../LICENSE)
EOF
```

---

## ✅ PASO 9: VERIFICACIÓN FINAL

### **9.1 Checklist de verificación**

```bash
# Desde LuminoraCoreWeb/

# ✓ Estructura de directorios
ls -R

# ✓ Backend instalado
cd backend
.\venv\Scripts\Activate.ps1
python -c "import fastapi; print('FastAPI OK')"
python -c "import luminoracore; print('LuminoraCore SDK OK')"

# ✓ Frontend instalado
cd ../frontend
npm list next react --depth=0

# ✓ Variables de entorno
cat ../backend/.env
cat .env.local
```

---

## 🎯 RESUMEN DE COMANDOS RÁPIDOS

### **Iniciar Desarrollo (Windows)**
```powershell
cd ~/proyectos/luminoracore-web
.\start-dev.ps1
```

### **Backend Solo**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

### **Frontend Solo**
```powershell
cd frontend
npm run dev
```

### **Ver logs**
```powershell
# Backend logs
cd backend
python -m uvicorn app.main:app --reload --log-level debug

# Frontend logs (ya incluidos en npm run dev)
```

---

## 🔧 TROUBLESHOOTING

### **Error: "venv\Scripts\Activate.ps1 cannot be loaded"**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Error: "Module 'luminoracore' not found"**
```bash
cd backend
.\venv\Scripts\Activate.ps1
pip install -e ../../luminoracore/luminoracore-sdk-python/
```

### **Error: "Port 3000 already in use"**
```powershell
# Cambiar puerto en frontend
cd frontend
# Editar package.json:
# "dev": "next dev -p 3001"
```

### **Error: "CORS policy"**
```bash
# Verificar que CORS_ORIGINS en backend/.env incluye el frontend URL
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

---

## 📞 SOPORTE

- 📚 Documentación: https://docs.luminoracore.com
- 💬 Discord: https://discord.gg/luminoracore
- 🐛 Issues: https://github.com/luminoracore/luminoracore-web/issues

---

**¡Listo para ser el estándar universal de personalidades IA!** 🚀
EOF
```

---

## 🎉 PRÓXIMOS PASOS

Una vez que tengas la estructura base funcionando:

1. **Implementar endpoints del backend** (chat.py, personalities.py)
2. **Crear componentes del frontend** (ChatInterface, PersonalitySelector)
3. **Diseñar la landing page**
4. **Configurar deploy**

¿Quieres que continúe con la implementación completa de alguna parte específica?

