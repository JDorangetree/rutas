# Guía de Despliegue - Sistema de Ruteo MVP

Esta guía te ayudará a publicar tu aplicación para que usuarios externos puedan probarla.

## Opción 1: Streamlit Community Cloud ⭐ RECOMENDADO

### Requisitos Previos
- Cuenta de GitHub
- Código subido a un repositorio público o privado

### Pasos para Desplegar

#### 1. Preparar el Repositorio

Asegúrate de tener estos archivos en tu repositorio:
- ✅ `app.py` - Aplicación principal
- ✅ `requirements.txt` - Dependencias
- ✅ `src/` - Carpeta con módulos
- ✅ `templates/` - Plantillas de Excel
- ✅ `.streamlit/config.toml` - Configuración (opcional)

#### 2. Subir a GitHub

```bash
# Inicializar git si no lo has hecho
git init

# Agregar archivos
git add .

# Crear commit
git commit -m "Preparar para despliegue en Streamlit Cloud"

# Crear repositorio en GitHub y conectar
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git

# Subir código
git push -u origin main
```

#### 3. Desplegar en Streamlit Cloud

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con tu cuenta de GitHub
3. Haz clic en "New app"
4. Selecciona:
   - **Repository:** Tu repositorio
   - **Branch:** main
   - **Main file path:** app.py
5. Haz clic en "Deploy"

#### 4. Configurar Variables de Entorno (Opcional)

Si quieres preconfigurar una API key de Google Maps:

1. En la página de tu app, ve a "Settings" > "Secrets"
2. Agrega:
```toml
GOOGLE_MAPS_API_KEY = "tu-api-key-aqui"
```

#### 5. Compartir con Usuarios

Una vez desplegada, obtendrás una URL como:
```
https://tu-usuario-tu-repo-main-xxxxx.streamlit.app
```

Comparte esta URL con tus usuarios de prueba.

---

## Opción 2: Render (Alternativa Gratuita)

### Pasos para Desplegar en Render

1. Ve a [render.com](https://render.com)
2. Crea una cuenta
3. Clic en "New" > "Web Service"
4. Conecta tu repositorio de GitHub
5. Configura:
   - **Name:** sistema-ruteo-mvp
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Selecciona "Free" plan
7. Haz clic en "Create Web Service"

**Nota:** La app se dormirá después de 15 minutos sin uso (tarda ~30 segundos en despertar).

---

## Opción 3: Railway.app (Mejor Performance)

### Pasos para Desplegar en Railway

1. Ve a [railway.app](https://railway.app)
2. Crea una cuenta
3. Haz clic en "New Project" > "Deploy from GitHub repo"
4. Selecciona tu repositorio
5. Railway detectará automáticamente que es una app Python
6. Agrega las variables de entorno si es necesario
7. La app se desplegará automáticamente

**Costo:** Tienes $5 USD gratis al mes.

---

## Configuración Adicional para Producción

### 1. Archivo `.streamlit/config.toml`

Este archivo mejora la experiencia del usuario:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 200
enableXsrfProtection = true
enableCORS = false
```

### 2. Archivo `.gitignore`

Para no subir archivos innecesarios:

```
env/
venv/
__pycache__/
*.pyc
.env
output/*.xlsx
.DS_Store
*.log
.streamlit/secrets.toml
```

---

## Pruebas con Usuarios

### Preparación para Usuarios de Prueba

1. **Crea una guía rápida** para tus testers:
   - URL de la aplicación
   - Credenciales si es necesario
   - Qué probar específicamente
   - Dónde reportar problemas

2. **Plantillas de ejemplo listas:**
   - Asegúrate de que las plantillas descargables tengan datos de ejemplo

3. **Monitoreo:**
   - Streamlit Cloud te muestra logs en tiempo real
   - Puedes ver cuándo hay errores

### Ejemplo de Mensaje para Testers

```
Hola,

Te invito a probar nuestro Sistema de Ruteo MVP:

🔗 URL: https://tu-app.streamlit.app

📋 Qué probar:
1. Descarga las plantillas de Excel
2. Llénalas con tus propios datos (o usa los ejemplos)
3. Carga los archivos y genera rutas optimizadas
4. Reporta cualquier error o sugerencia

Para reportar problemas: [tu-email] o [GitHub Issues]

¡Gracias por tu ayuda!
```

---

## Solución de Problemas Comunes

### App muy lenta
- **Causa:** Recursos limitados en plan gratuito
- **Solución:** Considera Railway o aumenta el plan de Streamlit

### Error al cargar archivos grandes
- **Causa:** Límite de tamaño de archivo
- **Solución:** Configura `maxUploadSize` en `.streamlit/config.toml`

### API de Google Maps no funciona
- **Causa:** API key no configurada
- **Solución:** Los usuarios deben ingresar su propia API key en la interfaz

### App se cae con muchos usuarios
- **Causa:** Plan gratuito tiene límites
- **Solución:** Monitorea uso y considera upgrade si es necesario

---

## Costos Estimados por Plataforma

| Plataforma | Plan Gratis | Limitaciones | Plan Pagado |
|-----------|-------------|--------------|-------------|
| **Streamlit Cloud** | Sí (Ilimitado) | 1 GB RAM, 1 CPU | $0/mes |
| **Render** | Sí | Se duerme, 750 hrs/mes | $7/mes |
| **Railway** | $5 crédito/mes | Pay-as-you-go después | ~$10-20/mes |
| **Google Cloud Run** | 2M requests/mes | Requiere conocimiento técnico | ~$10-30/mes |

---

## Recomendación Final

Para tu MVP y pruebas con usuarios:

1. **Empieza con Streamlit Community Cloud** - Es gratis y fácil
2. **Si necesitas mejor performance** - Usa Railway ($5 gratis/mes)
3. **Para producción seria** - Migra a Google Cloud Run o Railway

## Próximos Pasos

1. ✅ Revisa que todos los archivos estén listos
2. ✅ Sube tu código a GitHub
3. ✅ Despliega en Streamlit Cloud
4. ✅ Prueba la URL generada
5. ✅ Comparte con tus usuarios beta
6. ✅ Recolecta feedback
7. ✅ Itera y mejora

¡Buena suerte con tu MVP! 🚀
