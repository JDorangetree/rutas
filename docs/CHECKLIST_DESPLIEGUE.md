# ✅ Checklist de Despliegue - Sistema de Ruteo MVP

Usa este checklist para asegurar un despliegue exitoso.

## 📋 Pre-Despliegue

### Verificar Archivos
- [ ] `app.py` existe y funciona localmente
- [ ] `requirements.txt` tiene todas las dependencias
- [ ] Carpeta `src/` con todos los módulos
- [ ] Carpeta `templates/` con las 4 plantillas Excel
- [ ] `.streamlit/config.toml` configurado
- [ ] `.gitignore` actualizado
- [ ] `README.md` con descripción del proyecto

### Probar Localmente
- [ ] Ejecutar: `streamlit run app.py`
- [ ] Descargar plantillas funciona
- [ ] Cargar archivos funciona
- [ ] Optimización funciona
- [ ] Exportar resultados funciona
- [ ] No hay errores en consola

## 🔧 Configurar Git

### Inicializar Repositorio
```bash
# Si no tienes Git inicializado
git init

# Agregar todos los archivos
git add .

# Crear primer commit
git commit -m "Initial commit - Sistema de Ruteo MVP"
```

### Conectar con GitHub
- [ ] Crear repositorio en GitHub (público o privado)
- [ ] Copiar URL del repositorio

```bash
# Conectar con repositorio remoto
git remote add origin https://github.com/TU-USUARIO/TU-REPO.git

# Subir código
git push -u origin main
```

## ☁️ Despliegue en Streamlit Cloud

### Cuenta y Acceso
- [ ] Crear cuenta en [share.streamlit.io](https://share.streamlit.io)
- [ ] Conectar cuenta de GitHub
- [ ] Autorizar acceso a repositorios

### Configurar App
1. [ ] Clic en "New app"
2. [ ] Seleccionar repositorio
3. [ ] Configurar:
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** (nombre personalizado si quieres)
4. [ ] Clic en "Deploy"

### Esperar Despliegue
- [ ] Esperar 2-5 minutos mientras despliega
- [ ] Verificar que no haya errores en logs
- [ ] Obtener URL final (ej: `https://tu-app.streamlit.app`)

## 🧪 Pruebas Post-Despliegue

### Verificar Funcionalidad
- [ ] Abrir la URL en navegador
- [ ] Probar descarga de plantillas
- [ ] Probar carga de archivos
- [ ] Probar optimización con datos de ejemplo
- [ ] Verificar que mapas se muestren correctamente
- [ ] Probar exportación de resultados
- [ ] Probar en modo incógnito (sin caché)

### Pruebas de Navegador
- [ ] Chrome
- [ ] Firefox
- [ ] Safari (si tienes Mac)
- [ ] Edge

### Pruebas Móviles (Opcional)
- [ ] Abrir en celular
- [ ] Verificar que sea responsivo
- [ ] Probar funcionalidad básica

## 👥 Preparar para Usuarios

### Documentación
- [ ] Actualizar URL en `GUIA_USUARIOS.md`
- [ ] Agregar tu email de contacto
- [ ] Crear formulario de feedback (Google Forms, Typeform, etc.)

### Plantillas de Prueba
- [ ] Verificar que plantillas tengan datos de ejemplo
- [ ] Crear conjunto de datos de prueba realista
- [ ] Documentar casos de uso esperados

### Comunicación
- [ ] Preparar email/mensaje para testers
- [ ] Incluir URL de la app
- [ ] Incluir instrucciones básicas
- [ ] Incluir canal para reportar problemas

## 📧 Mensaje para Testers (Template)

```
Asunto: Invitación a probar Sistema de Ruteo MVP

Hola [Nombre],

Te invito a ser beta tester de nuestro Sistema de Ruteo para optimizar entregas.

🔗 Aplicación: [TU URL AQUÍ]
📖 Guía: [LINK A GUIA_USUARIOS.md]

¿Qué necesito que pruebes?
1. Descarga las plantillas de Excel (3 archivos)
2. Llénalas con datos (puedes usar los ejemplos incluidos)
3. Carga los archivos y genera rutas optimizadas
4. Reporta cualquier error o sugerencia

⏱️ Tiempo estimado: 15-30 minutos

📝 Feedback: [LINK A FORMULARIO O EMAIL]

¿Dudas? Responde este email.

¡Gracias por tu ayuda!
```

## 🐛 Monitoreo Post-Lanzamiento

### Primeras 24 Horas
- [ ] Revisar logs en Streamlit Cloud cada 2-3 horas
- [ ] Responder preguntas de usuarios rápidamente
- [ ] Documentar bugs reportados
- [ ] Crear lista de mejoras sugeridas

### Primera Semana
- [ ] Revisar analytics (si configuraste)
- [ ] Recolectar feedback estructurado
- [ ] Priorizar bugs críticos
- [ ] Planificar siguientes iteraciones

## 🔄 Actualizaciones

### Para Actualizar la App
```bash
# Hacer cambios en tu código local
# Probar localmente

# Commit y push
git add .
git commit -m "Descripción de cambios"
git push origin main

# Streamlit Cloud se actualiza automáticamente en ~2 min
```

## 📊 Métricas a Monitorear

- [ ] Número de usuarios únicos
- [ ] Número de optimizaciones ejecutadas
- [ ] Tiempo promedio de optimización
- [ ] Tasa de errores
- [ ] Feedback cualitativo de usuarios

## 🚨 Plan de Contingencia

### Si la App Se Cae
1. [ ] Revisar logs en Streamlit Cloud
2. [ ] Identificar error
3. [ ] Hacer rollback si es necesario:
   ```bash
   git revert HEAD
   git push origin main
   ```
4. [ ] Notificar a usuarios afectados

### Si Hay Demasiado Tráfico
1. [ ] Monitorear uso de recursos
2. [ ] Considerar upgrade de plan
3. [ ] O migrar a Railway/Render si necesario

## ✅ Checklist Final

Antes de compartir con usuarios:

- [ ] App desplegada y funcionando
- [ ] URL probada y funcional
- [ ] Plantillas descargables
- [ ] Documentación lista (GUIA_USUARIOS.md)
- [ ] Canal de feedback configurado
- [ ] Email de invitación preparado
- [ ] Plan de monitoreo definido

## 🎉 ¡Listo para Lanzar!

Cuando todos los checkboxes estén marcados, ¡estás listo para compartir tu MVP!

### Recursos Útiles
- [Documentación Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [DESPLIEGUE.md](./DESPLIEGUE.md) - Guía detallada
- [GUIA_USUARIOS.md](./GUIA_USUARIOS.md) - Para tus testers

---

**Fecha de checklist:** _______________
**Desplegado por:** _______________
**URL de producción:** _______________
