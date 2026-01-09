# 📤 Qué Subir a Git - Guía Completa

Esta guía te indica exactamente qué archivos DEBES y NO DEBES subir al repositorio de GitHub.

## ✅ ARCHIVOS QUE SÍ DEBES SUBIR

### 📄 Archivos Principales (Raíz)
```
✅ app.py                         # Aplicación principal
✅ requirements.txt               # Dependencias Python
✅ README.md                      # Documentación principal
✅ ESTRUCTURA_PROYECTO.md         # Guía de estructura
✅ GOOGLE_MAPS_SETUP.md           # Setup Google Maps
✅ INICIO_RAPIDO.md               # Guía rápida
✅ .gitignore                     # Configuración Git (IMPORTANTE)
✅ iniciar.bat                    # Script de inicio Windows
✅ deploy.bat                     # Script de despliegue Windows
✅ deploy.sh                      # Script de despliegue Linux/Mac
✅ verificar_despliegue.py        # Script de verificación
✅ QUE_SUBIR_A_GIT.md            # Este archivo
```

### 📁 Carpeta src/ (Código Fuente)
```
✅ src/config.py                  # Configuración del sistema
✅ src/data_loader.py             # Carga de datos
✅ src/route_optimizer.py         # Algoritmo de optimización
✅ src/create_templates.py        # Generador de plantillas
✅ src/__init__.py                # Si existe
```

### 📁 Carpeta templates/ (Plantillas Excel)
```
✅ templates/plantilla_origenes.xlsx
✅ templates/plantilla_destinos.xlsx
✅ templates/plantilla_vehiculos.xlsx
✅ templates/plantilla_configuracion.xlsx
```

**Importante:** Estas plantillas deben tener datos de EJEMPLO, NO datos reales.

### 📁 Carpeta docs/ (Documentación)
```
✅ docs/README.md
✅ docs/DESPLIEGUE.md
✅ docs/GUIA_USUARIOS.md
✅ docs/COMPARACION_PLATAFORMAS.md
✅ docs/CHECKLIST_DESPLIEGUE.md
```

### 📁 Carpeta .streamlit/ (Configuración)
```
✅ .streamlit/config.toml         # Configuración UI
```

### 📁 Carpetas Vacías con .gitkeep
```
✅ output/.gitkeep                # Mantener carpeta vacía
✅ data/.gitkeep                  # Mantener carpeta vacía
```

---

## ❌ ARCHIVOS QUE NO DEBES SUBIR

### 🚫 Entorno Virtual
```
❌ env/                           # TODO el entorno virtual
❌ venv/
❌ .venv/
```
**Razón:** Es MUY pesado (~500 MB) y se recrea con `pip install -r requirements.txt`

### 🚫 Archivos Compilados Python
```
❌ __pycache__/                   # Carpetas de caché
❌ *.pyc                          # Bytecode Python
❌ *.pyo
❌ *.pyd
❌ .Python
```
**Razón:** Se generan automáticamente al ejecutar Python

### 🚫 Variables de Entorno y Secretos
```
❌ .env                           # API keys y secretos
❌ .streamlit/secrets.toml        # Secretos de Streamlit
❌ credentials.json               # Credenciales
❌ *.key                          # Archivos de llaves
```
**Razón:** Contienen información SENSIBLE (API keys, contraseñas)

### 🚫 Datos de Usuario
```
❌ data/*.xlsx                    # Datos reales de usuarios
❌ data/*.csv
❌ output/*.xlsx                  # Resultados generados
❌ output/*.pdf
```
**Razón:** Son datos privados de cada usuario

### 🚫 Archivos del Sistema Operativo
```
❌ .DS_Store                      # macOS
❌ Thumbs.db                      # Windows
❌ desktop.ini                    # Windows
```
**Razón:** Son específicos del sistema operativo

### 🚫 Archivos de IDEs
```
❌ .vscode/                       # Visual Studio Code
❌ .idea/                         # PyCharm/IntelliJ
❌ *.swp                          # Vim
❌ *.swo
❌ *~
```
**Razón:** Son específicos de cada desarrollador

### 🚫 Archivos de Log y Temporales
```
❌ *.log                          # Archivos de log
❌ *.tmp                          # Archivos temporales
❌ *.bak                          # Backups
```
**Razón:** Se generan durante la ejecución

### 🚫 Git
```
❌ .git/                          # Carpeta de Git (pero SÍ existe localmente)
```
**Nota:** `.git/` existe localmente pero NO se sube (Git lo maneja automáticamente)

---

## 🔍 Verificar Tu .gitignore

Tu archivo `.gitignore` debe contener:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Entorno virtual
env/
venv/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Sistema operativo
.DS_Store
Thumbs.db

# Datos
data/*
!data/.gitkeep
output/*
!output/.gitkeep

# Jupyter Notebook
.ipynb_checkpoints

# Logs
*.log

# Archivos temporales
*.tmp
*.bak

# Variables de entorno (contiene API keys)
.env

# Streamlit
.streamlit/secrets.toml
```

---

## 📝 Comandos Git Recomendados

### Ver qué se va a subir
```bash
git status
```

### Ver qué archivos están siendo ignorados
```bash
git status --ignored
```

### Verificar archivos específicos
```bash
# Ver si un archivo está siendo ignorado
git check-ignore -v nombre_archivo.txt
```

### Subir archivos correctos
```bash
# Ver cambios
git status

# Agregar TODO (respetando .gitignore)
git add .

# Crear commit
git commit -m "Descripción de cambios"

# Subir a GitHub
git push origin main
```

---

## ⚠️ IMPORTANTE: Antes de Hacer el Primer Push

### 1. Verificar .gitignore
```bash
# Asegúrate de que .gitignore existe y está correcto
cat .gitignore
```

### 2. Revisar qué se va a subir
```bash
git status
```

**DEBE aparecer:**
- ✅ app.py
- ✅ requirements.txt
- ✅ src/
- ✅ templates/
- ✅ docs/
- ✅ .streamlit/config.toml
- ✅ README.md

**NO DEBE aparecer:**
- ❌ env/
- ❌ __pycache__/
- ❌ .env
- ❌ data/*.xlsx (archivos reales)
- ❌ output/*.xlsx

### 3. Si aparece algo que NO debe subirse
```bash
# Quitar del staging
git reset HEAD nombre_archivo

# O agregar al .gitignore
echo "nombre_archivo" >> .gitignore
```

---

## 🔧 Casos Especiales

### Si ya subiste archivos que no debías

#### Caso 1: Subiste .env con API keys
```bash
# 🚨 URGENTE - Cambiar tus API keys INMEDIATAMENTE
# Luego:
git rm --cached .env
echo ".env" >> .gitignore
git commit -m "Remover .env del repositorio"
git push origin main
```

#### Caso 2: Subiste la carpeta env/
```bash
git rm -r --cached env/
git commit -m "Remover entorno virtual"
git push origin main
```

#### Caso 3: Subiste datos sensibles
```bash
git rm --cached data/datos_reales.xlsx
git commit -m "Remover datos sensibles"
git push origin main

# IMPORTANTE: Esto NO borra el historial
# Si había datos MUY sensibles, considera:
# - Hacer el repo privado
# - O crear repo nuevo
```

---

## ✨ Crear Carpetas Vacías en Git

Git no versiona carpetas vacías. Para mantenerlas:

### Crear .gitkeep
```bash
# Crear carpetas vacías
mkdir -p data output

# Crear .gitkeep
touch data/.gitkeep
touch output/.gitkeep

# Agregar a Git
git add data/.gitkeep output/.gitkeep
git commit -m "Agregar carpetas data y output"
```

---

## 📊 Resumen Visual

```
TU REPOSITORIO EN GITHUB
│
├── ✅ app.py
├── ✅ requirements.txt
├── ✅ README.md
├── ✅ .gitignore
│
├── ✅ src/
│   ├── config.py
│   ├── data_loader.py
│   └── route_optimizer.py
│
├── ✅ templates/
│   └── *.xlsx (con ejemplos)
│
├── ✅ docs/
│   └── *.md
│
├── ✅ .streamlit/
│   └── config.toml
│
├── ✅ data/
│   └── .gitkeep (solo esto)
│
└── ✅ output/
    └── .gitkeep (solo esto)

NO ESTÁ EN GITHUB:
❌ env/ (entorno virtual)
❌ __pycache__/ (caché Python)
❌ .env (API keys)
❌ data/*.xlsx (tus datos)
❌ output/*.xlsx (resultados)
```

---

## 🎯 Checklist Final

Antes de hacer `git push`, verifica:

- [ ] `.gitignore` existe y está correcto
- [ ] Ejecutaste `git status` y revisaste la lista
- [ ] NO aparece `env/` en la lista
- [ ] NO aparece `.env` en la lista
- [ ] NO aparecen archivos `.pyc` o `__pycache__`
- [ ] Las plantillas tienen datos de EJEMPLO, no reales
- [ ] README.md tiene tu información actualizada
- [ ] Todos los archivos de código (.py) están incluidos
- [ ] Toda la documentación (docs/) está incluida

---

## 📞 ¿Dudas?

**¿Un archivo debería subirse?**
- ¿Es código? → ✅ Sí
- ¿Es documentación? → ✅ Sí
- ¿Es plantilla con ejemplos? → ✅ Sí
- ¿Se genera automáticamente? → ❌ No
- ¿Contiene datos sensibles? → ❌ No
- ¿Es muy pesado (>50 MB)? → ❌ No

---

## 🚀 Comando Final para Subir

```bash
# 1. Ver estado
git status

# 2. Agregar archivos (respeta .gitignore automáticamente)
git add .

# 3. Crear commit
git commit -m "Preparar proyecto para GitHub"

# 4. Subir
git push origin main
```

**¡Listo!** Tu repositorio estará limpio y profesional. ✨

---

📖 **Ver también:**
- [README.md](README.md) - Documentación principal
- [ESTRUCTURA_PROYECTO.md](ESTRUCTURA_PROYECTO.md) - Estructura del proyecto
- [docs/DESPLIEGUE.md](docs/DESPLIEGUE.md) - Guía de despliegue
