# 📂 Estructura del Proyecto - Sistema de Ruteo v2.2

Este documento describe la organización de archivos y carpetas del proyecto.

## 🗂️ Vista General

```
sistema-ruteo/
│
├── 📄 Archivos Principales
│   ├── app.py                         # Aplicación principal Streamlit
│   ├── requirements.txt               # Dependencias Python
│   ├── README.md                      # Documentación principal
│   └── .gitignore                     # Archivos ignorados por Git
│
├── 🚀 Scripts de Ejecución
│   ├── iniciar.bat                    # Iniciar app (Windows)
│   ├── deploy.bat                     # Script de despliegue (Windows)
│   ├── deploy.sh                      # Script de despliegue (Linux/Mac)
│   └── verificar_despliegue.py        # Verificar archivos antes de deploy
│
├── 📁 src/                            # Código fuente
│   ├── config.py                      # Configuración del sistema
│   ├── data_loader.py                 # Carga y validación de datos
│   ├── route_optimizer.py             # Algoritmo de optimización VRP
│   └── create_templates.py            # Generador de plantillas Excel
│
├── 📁 templates/                      # Plantillas Excel
│   ├── plantilla_origenes.xlsx        # Template de orígenes
│   ├── plantilla_destinos.xlsx        # Template de destinos
│   ├── plantilla_vehiculos.xlsx       # Template de vehículos
│   └── plantilla_configuracion.xlsx   # Template de configuración
│
├── 📁 docs/                           # Documentación
│   ├── README.md                      # Índice de documentación
│   ├── DESPLIEGUE.md                  # Guía de despliegue
│   ├── GUIA_USUARIOS.md               # Manual de usuario
│   ├── COMPARACION_PLATAFORMAS.md     # Comparativa de hosting
│   └── CHECKLIST_DESPLIEGUE.md        # Checklist de deploy
│
├── 📁 .streamlit/                     # Configuración Streamlit
│   └── config.toml                    # Tema y configuración UI
│
├── 📁 output/                         # Resultados (Git ignore)
│   └── *.xlsx                         # Archivos exportados
│
├── 📁 data/                           # Datos del usuario (Git ignore)
│   └── *.xlsx                         # Tus archivos de datos
│
├── 📁 env/                            # Entorno virtual (Git ignore)
│   └── ...                            # Librerías Python
│
└── 📁 .git/                           # Control de versiones
    └── ...                            # Historia de Git

```

## 📋 Descripción de Archivos

### Aplicación Principal

| Archivo | Descripción | Modificar |
|---------|-------------|-----------|
| `app.py` | Aplicación principal de Streamlit. Contiene toda la interfaz web | ✅ Sí |
| `requirements.txt` | Lista de dependencias Python necesarias | ⚠️ Solo si agregas librerías |
| `README.md` | Documentación principal del proyecto para GitHub | ✅ Sí |

### Código Fuente (`src/`)

| Archivo | Descripción | Modificar |
|---------|-------------|-----------|
| `config.py` | Configuración global del sistema (colores, métodos, etc.) | ✅ Sí |
| `data_loader.py` | Carga archivos Excel, valida datos, geocodifica | ⚠️ Con cuidado |
| `route_optimizer.py` | Implementa algoritmo VRP con OR-Tools | ⚠️ Con cuidado |
| `create_templates.py` | Script para generar plantillas Excel | ❌ Rara vez |

### Documentación (`docs/`)

| Archivo | Descripción | Para quién |
|---------|-------------|------------|
| `DESPLIEGUE.md` | Guía completa de despliegue en cloud | 👨‍💻 Desarrolladores |
| `GUIA_USUARIOS.md` | Manual de usuario final | 👥 Usuarios |
| `COMPARACION_PLATAFORMAS.md` | Análisis de opciones de hosting | 👨‍💻 Desarrolladores |
| `CHECKLIST_DESPLIEGUE.md` | Lista de verificación pre-deploy | 👨‍💻 Desarrolladores |

### Scripts de Utilidad

| Archivo | Descripción | Cuándo usar |
|---------|-------------|-------------|
| `iniciar.bat` | Inicia la aplicación en Windows | Desarrollo local |
| `deploy.bat` | Automatiza despliegue (Windows) | Antes de subir a GitHub |
| `deploy.sh` | Automatiza despliegue (Linux/Mac) | Antes de subir a GitHub |
| `verificar_despliegue.py` | Verifica que todo esté listo | Antes de desplegar |

### Configuración

| Archivo | Descripción | Git |
|---------|-------------|-----|
| `.gitignore` | Define qué archivos NO subir a Git | ✅ Incluir |
| `.streamlit/config.toml` | Tema y configuración de Streamlit | ✅ Incluir |
| `.env` | Variables de entorno (API keys) | ❌ NO incluir |
| `.env.example` | Ejemplo de .env (sin datos reales) | ✅ Incluir |

## 🚫 Archivos NO Versionados (Git Ignore)

Estos archivos/carpetas NO se suben a GitHub:

```
env/                  # Entorno virtual (muy pesado, se recrea)
__pycache__/          # Archivos compilados Python
*.pyc                 # Bytecode Python
.env                  # API keys y secretos
output/*.xlsx         # Resultados generados por usuarios
data/*                # Datos privados de usuarios
*.log                 # Archivos de log
.streamlit/secrets.toml  # Secretos de Streamlit
```

**¿Por qué?**
- Son archivos generados automáticamente
- Contienen datos sensibles (API keys)
- Son muy grandes
- Son específicos de cada usuario

## ✅ Archivos que SÍ se Suben a GitHub

```
✅ app.py                    # Código principal
✅ src/*.py                  # Código fuente
✅ templates/*.xlsx          # Plantillas vacías
✅ docs/*.md                 # Documentación
✅ requirements.txt          # Dependencias
✅ README.md                 # Documentación principal
✅ .gitignore                # Configuración Git
✅ .streamlit/config.toml    # Configuración Streamlit
✅ iniciar.bat               # Scripts de inicio
✅ deploy.bat/sh             # Scripts de deploy
```

## 📦 Cómo Agregar Nuevos Archivos

### Nuevo Módulo Python
```bash
# 1. Crear archivo en src/
src/nuevo_modulo.py

# 2. Importar en app.py
from nuevo_modulo import funcion

# 3. Commit a Git
git add src/nuevo_modulo.py
git commit -m "Agregar nuevo módulo"
```

### Nueva Plantilla Excel
```bash
# 1. Crear en templates/
templates/nueva_plantilla.xlsx

# 2. Commit a Git
git add templates/nueva_plantilla.xlsx
git commit -m "Agregar nueva plantilla"
```

### Nueva Documentación
```bash
# 1. Crear en docs/
docs/NUEVA_GUIA.md

# 2. Agregar link en docs/README.md
# 3. Commit a Git
git add docs/
git commit -m "Agregar nueva guía"
```

## 🔍 Encontrar Archivos

### Por Funcionalidad

**Quiero modificar la interfaz:**
→ `app.py`

**Quiero cambiar colores o configuración:**
→ `src/config.py`

**Quiero mejorar el algoritmo:**
→ `src/route_optimizer.py`

**Quiero cambiar cómo se cargan los archivos:**
→ `src/data_loader.py`

**Quiero actualizar las plantillas:**
→ `templates/*.xlsx`

**Quiero mejorar la documentación:**
→ `docs/*.md` o `README.md`

### Por Problema

**"No se geocodifica bien":**
→ Revisar `src/data_loader.py` (función `geocode_*`)

**"El algoritmo no encuentra solución":**
→ Revisar `src/route_optimizer.py` (función `solve`)

**"Error al cargar Excel":**
→ Revisar `src/data_loader.py` (funciones `load_*`)

**"La app se ve fea":**
→ Revisar `.streamlit/config.toml` y `app.py`

## 📊 Tamaño del Proyecto

```
Archivos de código Python:     ~2,500 líneas
Archivos de documentación:      ~3,000 líneas
Plantillas Excel:               4 archivos
Total archivos versionados:     ~30 archivos
Total carpetas:                 8 carpetas
```

## 🎯 Próximos Pasos

1. **Desarrollo local:**
   - Modifica `app.py` y `src/*.py`
   - Prueba con `streamlit run app.py`

2. **Preparar para deploy:**
   - Ejecuta `verificar_despliegue.py`
   - Revisa `.gitignore`
   - Actualiza `README.md` si es necesario

3. **Subir a GitHub:**
   - `git add .`
   - `git commit -m "Descripción"`
   - `git push origin main`

4. **Desplegar:**
   - Sigue `docs/DESPLIEGUE.md`
   - Usa `docs/CHECKLIST_DESPLIEGUE.md`

---

📖 **Ver también:**
- [README.md](README.md) - Documentación principal
- [docs/README.md](docs/README.md) - Índice de documentación
- [docs/DESPLIEGUE.md](docs/DESPLIEGUE.md) - Guía de despliegue

---

**Última actualización:** Enero 2026
