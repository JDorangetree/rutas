#!/bin/bash
# Script de despliegue rápido para Sistema de Ruteo MVP
# Este script automatiza los pasos básicos de preparación para despliegue

echo "=========================================="
echo "🚀 PREPARACIÓN PARA DESPLIEGUE"
echo "=========================================="
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: No se encuentra app.py"
    echo "   Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

echo "✅ Directorio correcto detectado"
echo ""

# Verificar que Python está disponible
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python no está instalado o no está en PATH"
    exit 1
fi

echo "✅ Python detectado: $(python --version)"
echo ""

# Ejecutar script de verificación
echo "📋 Verificando archivos necesarios..."
python verificar_despliegue.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Verificación falló. Por favor corrige los errores antes de continuar."
    exit 1
fi

echo ""
echo "=========================================="
echo "🔧 CONFIGURACIÓN DE GIT"
echo "=========================================="
echo ""

# Verificar si Git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git no está instalado"
    echo "   Instala Git desde: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git detectado: $(git --version)"
echo ""

# Verificar si ya es un repositorio Git
if [ ! -d ".git" ]; then
    echo "📦 Inicializando repositorio Git..."
    git init
    echo "✅ Repositorio Git inicializado"
else
    echo "✅ Repositorio Git ya existe"
fi

echo ""
echo "=========================================="
echo "📝 PREPARAR COMMIT"
echo "=========================================="
echo ""

# Mostrar estado actual
echo "Estado actual del repositorio:"
git status --short

echo ""
read -p "¿Deseas agregar todos los archivos y crear un commit? (s/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Ss]$ ]]; then
    # Agregar archivos
    echo "➕ Agregando archivos..."
    git add .

    # Solicitar mensaje de commit
    echo ""
    read -p "Mensaje de commit (Enter para usar 'Preparar para despliegue MVP'): " commit_msg

    if [ -z "$commit_msg" ]; then
        commit_msg="Preparar para despliegue MVP"
    fi

    # Crear commit
    git commit -m "$commit_msg"

    echo "✅ Commit creado"
else
    echo "⏭️  Saltando creación de commit"
fi

echo ""
echo "=========================================="
echo "🌐 CONFIGURAR REMOTO (GITHUB)"
echo "=========================================="
echo ""

# Verificar si ya tiene remoto configurado
remote_url=$(git remote get-url origin 2>/dev/null)

if [ -z "$remote_url" ]; then
    echo "No hay repositorio remoto configurado."
    echo ""
    echo "Pasos para conectar con GitHub:"
    echo "1. Ve a https://github.com/new"
    echo "2. Crea un repositorio (público o privado)"
    echo "3. Copia la URL del repositorio"
    echo ""
    read -p "URL del repositorio de GitHub: " github_url

    if [ ! -z "$github_url" ]; then
        git remote add origin "$github_url"
        echo "✅ Remoto configurado: $github_url"

        echo ""
        read -p "¿Deseas hacer push ahora? (s/n): " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[Ss]$ ]]; then
            # Detectar rama actual
            current_branch=$(git branch --show-current)
            if [ -z "$current_branch" ]; then
                current_branch="main"
                git branch -M main
            fi

            echo "📤 Subiendo código a GitHub..."
            git push -u origin "$current_branch"

            if [ $? -eq 0 ]; then
                echo "✅ Código subido exitosamente"
            else
                echo "❌ Error al subir código. Verifica tu conexión y permisos."
            fi
        fi
    fi
else
    echo "✅ Remoto ya configurado: $remote_url"

    echo ""
    read -p "¿Deseas hacer push de los cambios? (s/n): " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Ss]$ ]]; then
        current_branch=$(git branch --show-current)
        echo "📤 Subiendo código a GitHub..."
        git push origin "$current_branch"

        if [ $? -eq 0 ]; then
            echo "✅ Código subido exitosamente"
        else
            echo "❌ Error al subir código"
        fi
    fi
fi

echo ""
echo "=========================================="
echo "✅ PREPARACIÓN COMPLETADA"
echo "=========================================="
echo ""
echo "Próximos pasos para desplegar en Streamlit Cloud:"
echo ""
echo "1. Ve a: https://share.streamlit.io"
echo "2. Inicia sesión con GitHub"
echo "3. Haz clic en 'New app'"
echo "4. Selecciona tu repositorio"
echo "5. Configura:"
echo "   - Branch: main (o tu rama actual)"
echo "   - Main file: app.py"
echo "6. Haz clic en 'Deploy'"
echo ""
echo "📖 Para más detalles, lee: DESPLIEGUE.md"
echo "👥 Para guía de usuarios, lee: GUIA_USUARIOS.md"
echo ""
echo "¡Buena suerte con tu MVP! 🚀"
