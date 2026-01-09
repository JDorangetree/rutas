@echo off
REM Script de despliegue para Windows - Sistema de Ruteo MVP
chcp 65001 >nul
echo.
echo ==========================================
echo 🚀 PREPARACIÓN PARA DESPLIEGUE
echo ==========================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "app.py" (
    echo ❌ Error: No se encuentra app.py
    echo    Ejecuta este script desde el directorio raíz del proyecto
    pause
    exit /b 1
)

echo ✅ Directorio correcto detectado
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado o no está en PATH
    echo    Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python detectado: %PYTHON_VERSION%
echo.

REM Ejecutar script de verificación
echo 📋 Verificando archivos necesarios...
python verificar_despliegue.py
if errorlevel 1 (
    echo.
    echo ❌ Verificación falló. Corrige los errores antes de continuar.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo 🔧 CONFIGURACIÓN DE GIT
echo ==========================================
echo.

REM Verificar Git
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Git no está instalado
    echo    Descarga Git desde: https://git-scm.com/downloads
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('git --version') do set GIT_VERSION=%%i
echo ✅ Git detectado: %GIT_VERSION%
echo.

REM Verificar si es repositorio Git
if not exist ".git" (
    echo 📦 Inicializando repositorio Git...
    git init
    echo ✅ Repositorio Git inicializado
) else (
    echo ✅ Repositorio Git ya existe
)

echo.
echo ==========================================
echo 📝 ESTADO DEL REPOSITORIO
echo ==========================================
echo.
git status --short

echo.
set /p commit_choice="¿Deseas agregar archivos y crear commit? (s/n): "
if /i "%commit_choice%"=="s" (
    echo.
    echo ➕ Agregando archivos...
    git add .

    echo.
    set /p commit_msg="Mensaje de commit (Enter = 'Preparar para despliegue MVP'): "
    if "%commit_msg%"=="" set commit_msg=Preparar para despliegue MVP

    git commit -m "%commit_msg%"
    echo ✅ Commit creado
) else (
    echo ⏭️  Saltando creación de commit
)

echo.
echo ==========================================
echo 🌐 CONFIGURAR REMOTO (GITHUB)
echo ==========================================
echo.

REM Verificar remoto
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo No hay repositorio remoto configurado.
    echo.
    echo Pasos para conectar con GitHub:
    echo 1. Ve a https://github.com/new
    echo 2. Crea un repositorio (público o privado^)
    echo 3. Copia la URL del repositorio
    echo.
    set /p github_url="URL del repositorio de GitHub: "

    if not "%github_url%"=="" (
        git remote add origin "%github_url%"
        echo ✅ Remoto configurado: %github_url%

        echo.
        set /p push_choice="¿Deseas hacer push ahora? (s/n): "
        if /i "!push_choice!"=="s" (
            for /f "tokens=*" %%i in ('git branch --show-current') do set current_branch=%%i
            if "!current_branch!"=="" (
                set current_branch=main
                git branch -M main
            )

            echo 📤 Subiendo código a GitHub...
            git push -u origin !current_branch!

            if errorlevel 1 (
                echo ❌ Error al subir código
            ) else (
                echo ✅ Código subido exitosamente
            )
        )
    )
) else (
    for /f "tokens=*" %%i in ('git remote get-url origin') do set remote_url=%%i
    echo ✅ Remoto ya configurado: %remote_url%

    echo.
    set /p push_choice="¿Deseas hacer push de cambios? (s/n): "
    if /i "%push_choice%"=="s" (
        for /f "tokens=*" %%i in ('git branch --show-current') do set current_branch=%%i

        echo 📤 Subiendo código a GitHub...
        git push origin %current_branch%

        if errorlevel 1 (
            echo ❌ Error al subir código
        ) else (
            echo ✅ Código subido exitosamente
        )
    )
)

echo.
echo ==========================================
echo ✅ PREPARACIÓN COMPLETADA
echo ==========================================
echo.
echo Próximos pasos para desplegar en Streamlit Cloud:
echo.
echo 1. Ve a: https://share.streamlit.io
echo 2. Inicia sesión con GitHub
echo 3. Haz clic en 'New app'
echo 4. Selecciona tu repositorio
echo 5. Configura:
echo    - Branch: main (o tu rama actual^)
echo    - Main file: app.py
echo 6. Haz clic en 'Deploy'
echo.
echo 📖 Para más detalles, lee: DESPLIEGUE.md
echo 👥 Para guía de usuarios, lee: GUIA_USUARIOS.md
echo.
echo ¡Buena suerte con tu MVP! 🚀
echo.
pause
