#!/usr/bin/env python3
"""
Script de verificación pre-despliegue
Verifica que todos los archivos necesarios estén presentes
"""

import os
import sys

def verificar_archivo(ruta, nombre_descriptivo, requerido=True):
    """Verifica si un archivo existe"""
    existe = os.path.exists(ruta)
    if existe:
        print(f"✅ {nombre_descriptivo}: OK")
        return True
    else:
        simbolo = "❌" if requerido else "⚠️"
        print(f"{simbolo} {nombre_descriptivo}: NO ENCONTRADO")
        return not requerido

def verificar_directorio(ruta, nombre_descriptivo):
    """Verifica si un directorio existe y tiene archivos"""
    existe = os.path.exists(ruta) and os.path.isdir(ruta)
    if existe:
        num_archivos = len([f for f in os.listdir(ruta) if not f.startswith('.')])
        print(f"✅ {nombre_descriptivo}: OK ({num_archivos} archivos)")
        return True
    else:
        print(f"❌ {nombre_descriptivo}: NO ENCONTRADO")
        return False

def main():
    print("=" * 60)
    print("🔍 VERIFICACIÓN PRE-DESPLIEGUE - Sistema de Ruteo MVP")
    print("=" * 60)
    print()

    todo_ok = True

    # Archivos principales
    print("📄 Archivos Principales:")
    todo_ok &= verificar_archivo("app.py", "Aplicación principal (app.py)")
    todo_ok &= verificar_archivo("requirements.txt", "Dependencias (requirements.txt)")
    todo_ok &= verificar_archivo("README.md", "Documentación (README.md)", requerido=False)
    print()

    # Directorio src
    print("📁 Módulos de Código:")
    todo_ok &= verificar_directorio("src", "Directorio src/")
    todo_ok &= verificar_archivo("src/config.py", "Configuración (config.py)")
    todo_ok &= verificar_archivo("src/data_loader.py", "Cargador de datos (data_loader.py)")
    todo_ok &= verificar_archivo("src/route_optimizer.py", "Optimizador (route_optimizer.py)")
    print()

    # Plantillas
    print("📋 Plantillas de Excel:")
    todo_ok &= verificar_directorio("templates", "Directorio templates/")
    todo_ok &= verificar_archivo("templates/plantilla_origenes.xlsx", "Plantilla de orígenes")
    todo_ok &= verificar_archivo("templates/plantilla_destinos.xlsx", "Plantilla de destinos")
    todo_ok &= verificar_archivo("templates/plantilla_vehiculos.xlsx", "Plantilla de vehículos")
    todo_ok &= verificar_archivo("templates/plantilla_configuracion.xlsx", "Plantilla de configuración", requerido=False)
    print()

    # Configuración de Streamlit
    print("⚙️ Configuración de Streamlit:")
    streamlit_config = verificar_archivo(".streamlit/config.toml", "Configuración de tema (.streamlit/config.toml)", requerido=False)
    if not streamlit_config:
        print("   💡 Tip: Crea .streamlit/config.toml para personalizar la app")
    print()

    # Git
    print("🔧 Control de Versiones:")
    tiene_git = verificar_archivo(".gitignore", "Archivo .gitignore", requerido=False)
    if not tiene_git:
        print("   ⚠️ Recomendado: Crea .gitignore para no subir archivos innecesarios")

    es_repo = os.path.exists(".git")
    if es_repo:
        print("✅ Repositorio Git: Inicializado")
    else:
        print("⚠️ Repositorio Git: No inicializado")
        print("   💡 Ejecuta: git init")
    print()

    # Directorios de output
    print("📂 Directorios de Salida:")
    if os.path.exists("output"):
        print("✅ Directorio output/: OK")
    else:
        print("⚠️ Directorio output/: Creando...")
        os.makedirs("output", exist_ok=True)
        print("✅ Directorio output/: Creado")
    print()

    # Guías de despliegue
    print("📚 Documentación de Despliegue:")
    verificar_archivo("DESPLIEGUE.md", "Guía de despliegue", requerido=False)
    verificar_archivo("GUIA_USUARIOS.md", "Guía para usuarios", requerido=False)
    print()

    # Resumen final
    print("=" * 60)
    if todo_ok:
        print("✅ ¡TODO LISTO PARA DESPLEGAR!")
        print()
        print("Próximos pasos:")
        print("1. Sube tu código a GitHub:")
        print("   git add .")
        print("   git commit -m 'Preparar para despliegue'")
        print("   git push origin main")
        print()
        print("2. Ve a https://share.streamlit.io")
        print("3. Conecta tu repositorio y despliega")
        print()
        print("📖 Lee DESPLIEGUE.md para instrucciones detalladas")
    else:
        print("❌ FALTAN ARCHIVOS REQUERIDOS")
        print("Por favor revisa los errores arriba antes de desplegar")
        sys.exit(1)
    print("=" * 60)

if __name__ == "__main__":
    main()
