# Inicio Rápido - Sistema de Ruteo

## Pasos para usar el sistema

### 1. Iniciar la aplicación

**Opción A - Hacer doble clic en:**
```
iniciar.bat
```

**Opción B - Desde la terminal:**
```bash
# Activar entorno virtual
.\env\Scripts\activate

# Iniciar aplicación
streamlit run app.py
```

### 2. Se abrirá automáticamente en tu navegador

La aplicación se abrirá en: `http://localhost:8501`

### 3. Cargar tus archivos Excel

En la barra lateral izquierda, carga los siguientes archivos:

1. **Orígenes** (obligatorio)
   - Usa la plantilla: `templates/plantilla_origenes.xlsx`
   - Modifica con tus centros de distribución

2. **Destinos** (obligatorio)
   - Usa la plantilla: `templates/plantilla_destinos.xlsx`
   - Modifica con tus clientes y demandas

3. **Flota** (obligatorio)
   - Usa la plantilla: `templates/plantilla_flota.xlsx`
   - Modifica con tus vehículos y capacidades

4. **Configuración** (opcional)
   - Usa la plantilla: `templates/plantilla_config.xlsx`

### 4. Navegar por las pestañas

- **📊 Datos**: Verifica que los datos se hayan cargado correctamente
- **🗺️ Visualización**: Ve los puntos en el mapa
- **🚀 Optimización**: Ejecuta el algoritmo de ruteo
- **📈 Resultados**: Ve las rutas optimizadas y descarga el Excel

### 5. Exportar resultados

En la pestaña "Resultados", haz clic en:
- **Exportar a Excel**: Guarda el plan de ruteo
- **Descargar Archivo**: Descarga el archivo generado

Los archivos se guardan en la carpeta `output/`

## Requisitos de datos

### Coordenadas (latitud, longitud)

Puedes obtener las coordenadas de tus ubicaciones en:
- Google Maps: Clic derecho → Ver coordenadas
- https://www.latlong.net/

**Formato:**
- Latitud: -90 a 90 (ej: 4.6097)
- Longitud: -180 a 180 (ej: -74.0817)

### Demanda y Capacidad

- Deben estar en las mismas unidades (kg, m³, unidades, etc.)
- La capacidad total de la flota debe ser mayor o igual a la demanda total

## Consejos

1. **Empieza con las plantillas**: Modifica los archivos de ejemplo
2. **Verifica coordenadas**: Usa la pestaña Visualización para confirmar
3. **Ajusta tiempo límite**: Si no encuentra solución, aumenta el tiempo
4. **Capacidad suficiente**: Asegúrate de tener capacidad para toda la demanda

## Problemas comunes

### "No se encontró solución factible"
- Aumenta el tiempo límite de optimización
- Verifica que la capacidad total sea suficiente
- Revisa que todos los datos sean correctos

### Coordenadas incorrectas en el mapa
- Verifica el formato de latitud/longitud
- Asegúrate de usar punto (.) como separador decimal
- Confirma que latitud esté entre -90 y 90
- Confirma que longitud esté entre -180 y 180

### Error al cargar archivos
- Verifica que el archivo sea .xlsx o .xls
- Confirma que las columnas requeridas existan
- Asegúrate de que no haya valores vacíos

## Contacto y Soporte

Para más información, consulta el archivo [README.md](README.md)
