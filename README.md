# Sistema de Ruteo v2.2

Sistema avanzado de optimización de rutas para microempresas. Permite cargar archivos Excel con información de múltiples orígenes, destinos y flota para generar planes de ruteo optimizados con 5 criterios diferentes: distancia, tiempo, costo, vehículos o balanceado.

## Características v2.2

- **Distancias reales por carretera** ⭐ NUEVO: Google Directions API para cálculos precisos de distancia y tiempo
- **Selector de método de distancia**: Elige entre Haversine (línea recta) o Google Directions (carreteras)
- **Múltiples orígenes**: Soporte para múltiples centros de distribución
- **Múltiples objetivos de optimización**: Elige entre 5 criterios diferentes
  - 🎯 **Distancia**: Minimiza kilómetros totales
  - ⏱️ **Tiempo**: Minimiza tiempo total de entregas
  - 💰 **Costo**: Minimiza costo operativo
  - 🚚 **Vehículos**: Usa menos vehículos
  - ⚖️ **Balanceado**: Equilibrio entre distancia y tiempo
- **Geocodificación automática**: Usa Google Maps o OpenStreetMap (gratuito)
- **Carga de archivos Excel**: Importa fácilmente tus datos desde archivos Excel
- **Optimización avanzada**: Usa algoritmos avanzados (OR-Tools de Google) con múltiples depósitos
- **Prioridades de clientes**: Asigna prioridades (alta, media, baja) a destinos
- **Visualización en mapas**: Muestra las rutas optimizadas en mapas interactivos con colores por vehículo
- **Exportación de resultados**: Descarga los planes de ruteo en formato Excel detallado
- **Interfaz web intuitiva**: Aplicación Streamlit fácil de usar

## Requisitos

- Python 3.9 o superior
- Windows, Linux o macOS
- Conexión a internet (para geocodificación y mapas)

## Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd "MVP ruteo"
   ```

2. **El entorno virtual ya está creado** (carpeta `env`)

   Para activarlo:

   En Windows:
   ```bash
   .\env\Scripts\activate
   ```

   En Linux/macOS:
   ```bash
   source env/bin/activate
   ```

3. **Instalar dependencias** (si es necesario)
   ```bash
   pip install -r requirements.txt
   ```

## Uso Rápido

### Iniciar la aplicación

**Opción A - Más fácil (Windows):**
```bash
iniciar.bat
```

**Opción B - Desde terminal:**
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en: `http://localhost:8501`

### Flujo de trabajo

1. **Preparar archivos Excel**
   - Usa las plantillas en la carpeta `templates/`
   - Modifica con tus datos reales

2. **Cargar archivos**
   - Orígenes (obligatorio)
   - Destinos (obligatorio)
   - Vehículos (obligatorio)
   - Configuración (opcional)

3. **Verificar datos**
   - Pestaña "Datos": Revisa que todo se haya cargado correctamente
   - Las coordenadas faltantes se geocodifican automáticamente

4. **Visualizar**
   - Pestaña "Visualización": Ve los puntos en el mapa
   - Verifica que las ubicaciones sean correctas

5. **Optimizar**
   - Pestaña "Optimización": Ejecuta el algoritmo
   - Ajusta el tiempo límite según necesites

6. **Exportar**
   - Pestaña "Resultados": Ve las rutas optimizadas
   - Descarga el plan en Excel

## Estructura de Archivos Excel v2.0

### 1. Orígenes (origenes.xlsx)

**Columnas obligatorias:**
| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `origen_id` | Identificador único | ORG_01 |
| `nombre_origen` | Nombre del origen | Bodega Central |
| `direccion` | Dirección completa | Cra 50 #45-20 |
| `ciudad` | Ciudad | Medellín |
| `pais` | País | Colombia |

**Columnas opcionales:**
| Columna | Descripción |
|---------|-------------|
| `latitud` | Coordenada (se geocodifica si está vacía) |
| `longitud` | Coordenada (se geocodifica si está vacía) |
| `hora_apertura` | Horario de apertura (HH:MM) |
| `hora_cierre` | Horario de cierre (HH:MM) |

### 2. Destinos/Clientes (destinos.xlsx)

**Columnas obligatorias:**
| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `destino_id` | Identificador único | CLI_101 |
| `nombre_cliente` | Nombre del cliente | Supermercado El Sol |
| `direccion` | Dirección completa | Calle 80 #70-15 |
| `ciudad` | Ciudad | Medellín |
| `pais` | País | Colombia |
| `demanda` | Cantidad a entregar | 120 |

**Columnas opcionales:**
| Columna | Descripción | Valores |
|---------|-------------|---------|
| `latitud` | Coordenada | Se geocodifica si está vacía |
| `longitud` | Coordenada | Se geocodifica si está vacía |
| `hora_inicio` | Inicio ventana horaria | HH:MM |
| `hora_fin` | Fin ventana horaria | HH:MM |
| `prioridad` | Prioridad del cliente | 1=Alta, 2=Media, 3=Baja |

### 3. Flota/Vehículos (vehiculos.xlsx)

**Columnas obligatorias:**
| Columna | Descripción | Ejemplo |
|---------|-------------|---------|
| `vehiculo_id` | Identificador único | V_01 |
| `capacidad` | Capacidad máxima | 1000 |
| `origen_id` | Origen asignado | ORG_01 |

**Columnas opcionales:**
| Columna | Descripción |
|---------|-------------|
| `tipo_vehiculo` | Tipo de vehículo (Camión, Van, etc.) |
| `costo_km` | Costo por kilómetro |
| `hora_inicio` | Inicio de disponibilidad |
| `hora_fin` | Fin de disponibilidad |

### 4. Configuración (configuracion.xlsx) - Opcional

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `unidad_demanda` | kg | Unidad de medida (kg, m3, unidades) |
| `tiempo_servicio_min` | 10 | Tiempo promedio por parada (minutos) |
| `max_destinos_por_ruta` | 15 | Número máximo de destinos por ruta |
| `optimizar_por` | distancia | Criterio: distancia, tiempo o costo |
| `tiempo_limite_optimizacion` | 60 | Tiempo máximo del algoritmo (segundos) |
| `usar_ventanas_horarias` | no | Usar restricciones horarias (si/no) |

## Geocodificación Automática

El sistema incluye geocodificación automática con **selector de método** en la interfaz. Puedes elegir entre:

### 🗺️ Google Maps Geocoding
- **Descripción**: Servicio de geocodificación de alta precisión de Google Maps
- **Precisión**: Muy Alta
- **Velocidad**: Rápida
- **Ventajas**:
  - ✅ Alta precisión en todas las direcciones
  - ✅ Rápido y confiable
  - ✅ Mejor manejo de direcciones complejas
  - ✅ Incluye **$200 USD gratis mensuales**
- **Desventajas**:
  - ⚠️ Requiere API key
  - ⚠️ Tiene costos después de $200 USD ($5 por 1000 requests)
- **Costo**: $5 USD por 1000 requests (después de crédito gratuito)
- **Configuración**: Ver [GOOGLE_MAPS_SETUP.md](GOOGLE_MAPS_SETUP.md)

### 🌍 Nominatim (OpenStreetMap)
- **Descripción**: Servicio gratuito basado en OpenStreetMap
- **Precisión**: Media-Alta
- **Velocidad**: Media
- **Ventajas**:
  - ✅ 100% gratuito
  - ✅ Sin límites de uso
  - ✅ Sin configuración necesaria
  - ✅ Funciona sin API key
- **Desventajas**:
  - ⚠️ Menor precisión en direcciones complejas
  - ⚠️ Más lento que Google Maps
- **Costo**: Gratis
- **Uso recomendado**: Para pruebas rápidas o cuando no requieres máxima precisión

### Cómo Usar

**En la interfaz (sidebar):**
1. Selecciona el método de geocodificación en el dropdown
2. Verás las características de cada método (precisión, velocidad, costo)
3. Si eliges Google Maps, ingresa tu API key
4. Si eliges Nominatim, no necesitas configuración adicional

**Funcionamiento automático:**
- Si las columnas `latitud` y `longitud` están **vacías**, el sistema las calcula automáticamente
- Usa los campos `direccion`, `ciudad` y `pais` para buscar las coordenadas
- Muestra el progreso durante la geocodificación
- **Fallback inteligente**: Si Google Maps falla en alguna dirección, intenta con Nominatim

**Consejos para mejor geocodificación:**
- Usa direcciones completas y precisas
- Incluye números de calle cuando sea posible
- Para máxima precisión, usa Google Maps
- Para pruebas rápidas, Nominatim es suficiente
- Verifica los resultados en la pestaña "Visualización"

## Tipos de Optimización

El sistema ofrece **5 objetivos diferentes** para optimizar tus rutas:

### 🎯 Distancia
- **Objetivo**: Minimizar la distancia total recorrida por todos los vehículos
- **Ideal para**: Reducir costos de combustible y desgaste
- **Resultado**: Menor kilometraje total

### ⏱️ Tiempo
- **Objetivo**: Minimizar el tiempo total de todas las rutas
- **Considera**: Velocidad promedio de 40 km/h + tiempo de servicio por parada
- **Ideal para**: Cumplir ventanas horarias y hacer más entregas
- **Resultado**: Menor tiempo total de operación

### 💰 Costo
- **Objetivo**: Minimizar el costo operativo total
- **Considera**: Costo por kilómetro de cada vehículo (configurable en archivo de flota)
- **Ideal para**: Cuando tienes vehículos con diferentes costos operativos
- **Resultado**: Menor costo total (asigna rutas más largas a vehículos económicos)

### 🚚 Vehículos
- **Objetivo**: Usar la menor cantidad de vehículos posible
- **Ideal para**: Reducir costos fijos (conductores, seguros, etc.)
- **Resultado**: Rutas más consolidadas con menos vehículos activos

### ⚖️ Balanceado
- **Objetivo**: Balance entre distancia y tiempo (60% distancia, 40% tiempo)
- **Ideal para**: Solución equilibrada cuando ambos factores son importantes
- **Resultado**: Optimización mixta que considera ambos criterios

## Características Técnicas

### Algoritmo de Optimización

El sistema utiliza **OR-Tools de Google** con las siguientes capacidades:

- **Tipo de problema**: VRP (Vehicle Routing Problem) con múltiples depósitos
- **Objetivos flexibles**: 5 criterios diferentes de optimización
- **Restricciones**:
  - Capacidad máxima de cada vehículo
  - Todos los destinos deben ser visitados (o reportados como no asignados)
  - Cada vehículo sale y regresa a su origen asignado

- **Método de solución**:
  - First Solution Strategy: PATH_CHEAPEST_ARC
  - Local Search: GUIDED_LOCAL_SEARCH
  - Soporte para soluciones parciales con penalizaciones
  - Callbacks personalizados según objetivo de optimización

### Métodos de Cálculo de Distancia

El sistema ofrece **2 métodos** para calcular distancias:

#### 📏 Haversine (Línea Recta)
- **Descripción**: Calcula distancia en línea recta considerando la curvatura de la Tierra
- **Fórmula**: Distancia del gran círculo usando radio terrestre de 6371 km
- **Ventajas**:
  - ✅ Rápido - Cálculo instantáneo
  - ✅ Sin costos
  - ✅ Funciona sin internet
  - ✅ No requiere configuración
- **Desventajas**:
  - ⚠️ No considera carreteras reales
  - ⚠️ Puede subestimar distancias en zonas urbanas
- **Uso recomendado**: Para optimización rápida o cuando no se requiere precisión exacta

#### 🗺️ Google Directions (Carreteras Reales)
- **Descripción**: Calcula distancia y tiempo real por carretera usando Google Maps Directions API
- **Ventajas**:
  - ✅ Distancias reales de carretera
  - ✅ Tiempos de viaje reales
  - ✅ Considera tipo de vía
  - ✅ Mayor precisión
- **Desventajas**:
  - ⚠️ Requiere API key de Google
  - ⚠️ Tiene costos ($5 USD por 1000 requests)
  - ⚠️ Más lento (hace requests a API)
  - ⚠️ Requiere internet
- **Costos estimados**:
  - 10 ubicaciones: ~100 requests = $0.50 USD
  - 20 ubicaciones: ~400 requests = $2.00 USD
  - 50 ubicaciones: ~2500 requests = $12.50 USD
- **Uso recomendado**: Cuando se requiere precisión máxima y planificación final

**Configuración**: En el sidebar, selecciona el método en "Cálculo de Distancias" e ingresa tu API key si usas Google Directions.

### Estructura del Proyecto

```
MVP ruteo/
├── app.py                          # Aplicación principal Streamlit v2.0
├── iniciar.bat                     # Script para iniciar fácilmente
├── requirements.txt                # Dependencias Python
├── README.md                       # Esta documentación
├── INICIO_RAPIDO.md               # Guía rápida de uso
├── .gitignore                     # Archivos a ignorar en git
├── src/                           # Código fuente
│   ├── data_loader.py             # Carga, validación y geocodificación
│   ├── route_optimizer.py         # Algoritmo VRP con múltiples depósitos
│   ├── config.py                  # Configuración del sistema v2.0
│   └── create_templates.py        # Script para crear plantillas
├── templates/                     # Plantillas Excel de ejemplo v2.0
│   ├── plantilla_origenes.xlsx    # Ejemplo de orígenes
│   ├── plantilla_destinos.xlsx    # Ejemplo de destinos
│   ├── plantilla_vehiculos.xlsx   # Ejemplo de vehículos
│   └── plantilla_configuracion.xlsx # Ejemplo de configuración
├── data/                          # Carpeta para tus datos
├── output/                        # Carpeta para resultados
└── env/                           # Entorno virtual Python
```

## Solución de Problemas

### Error: "No se encontró solución factible"
- **Causa**: Capacidad insuficiente o tiempo límite muy corto
- **Solución**:
  - Aumenta el tiempo límite de optimización
  - Verifica que la capacidad total sea mayor a la demanda total
  - Agrega más vehículos o aumenta sus capacidades

### Error: "No se pudo geocodificar"
- **Causa**: Dirección no encontrada en OpenStreetMap
- **Solución**:
  - Verifica que la dirección sea correcta y completa
  - Intenta incluir más detalles (número de calle, barrio)
  - Como alternativa, agrega manualmente latitud y longitud
  - Usa Google Maps para obtener coordenadas: clic derecho → "¿Qué hay aquí?"

### Coordenadas incorrectas en el mapa
- Verifica que latitud esté entre -90 y 90
- Verifica que longitud esté entre -180 y 180
- Asegúrate de usar punto (.) como separador decimal
- Para Colombia, latitudes ~4-12 y longitudes ~-74 a -77

### Error: "Algunos vehículos tienen origen_id que no existe"
- Verifica que todos los `origen_id` en el archivo de vehículos existan en el archivo de orígenes
- Los IDs deben coincidir exactamente (respeta mayúsculas/minúsculas)

### Destinos no asignados
- **Causa**: Capacidad insuficiente o ubicaciones muy lejanas
- **Solución**:
  - Revisa la capacidad total vs demanda total
  - Aumenta el tiempo límite
  - Considera agregar más vehículos
  - Verifica que las coordenadas sean correctas

## Dependencias Principales

- **streamlit** (>=1.31.0): Interfaz web
- **pandas** (>=2.2.0): Procesamiento de datos Excel
- **openpyxl** (>=3.1.2): Lectura/escritura de archivos Excel
- **ortools** (>=9.8.0): Optimización de rutas (VRP solver)
- **folium** (>=0.15.0): Visualización de mapas
- **streamlit-folium** (>=0.16.0): Integración de mapas en Streamlit
- **numpy** (>=1.26.0): Cálculos numéricos
- **geopy** (>=2.4.0): Geocodificación con Nominatim (fallback)
- **googlemaps** (>=4.10.0): Geocodificación con Google Maps (opcional)
- **python-dotenv** (>=1.0.0): Manejo de variables de entorno (.env)

## Novedades v2.2

### Mejoras Principales

1. **Distancias Reales por Carretera** ⭐ NUEVO v2.2
   - Google Directions API para distancias reales
   - Tiempos de viaje precisos por carretera
   - Selector de método: Haversine vs Google Directions
   - Estimador de costos en tiempo real
   - Fallback automático a Haversine

2. **Selector de Método de Geocodificación** ⭐ NUEVO v2.2
   - Elige entre Google Maps (alta precisión) o Nominatim (gratuito)
   - Comparación de características en la interfaz
   - Métricas de precisión, velocidad y costo por método
   - Sin checkbox, ahora con selector intuitivo tipo dropdown
   - Fallback automático entre servicios

3. **5 Objetivos de Optimización**
   - Distancia: Minimiza kilómetros totales
   - Tiempo: Minimiza duración de entregas
   - Costo: Minimiza costo operativo
   - Vehículos: Usa menos vehículos
   - Balanceado: Equilibrio entre factores
   - Selector intuitivo en la interfaz

4. **Múltiples Orígenes**
   - Cada vehículo puede salir de un origen diferente
   - Ideal para empresas con varias bodegas o centros de distribución
   - Asignación flexible de vehículos a orígenes

5. **Prioridades de Clientes**
   - Asigna prioridades a destinos (1=Alta, 2=Media, 3=Baja)
   - Visualización con colores en el mapa

6. **Mejor Interfaz**
   - Información más detallada en cada pestaña
   - Indicadores de ciudades y distribución de vehículos
   - Resumen de utilización de capacidad
   - Selectores con métricas visuales

7. **Exportación Mejorada**
   - Excel con información detallada por vehículo
   - Incluye origen, ciudad y direcciones
   - Hoja adicional para destinos no asignados

## Próximas Mejoras (Roadmap)

- [x] ~~Optimización por tiempo, costo y vehículos~~ ✅ v2.1
- [x] ~~Integración con Google Maps API~~ ✅ v2.1
- [x] ~~Distancias reales por carretera (Google Directions)~~ ✅ v2.2
- [ ] Ventanas horarias estrictas (restricciones de tiempo)
- [ ] Restricciones de jornada laboral
- [ ] Histórico de rutas
- [ ] Reportes y KPIs avanzados
- [ ] API REST para integración con otros sistemas

## Soporte

Para preguntas o problemas:

- Consulta primero este README y [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
- Revisa la documentación de las librerías utilizadas:
  - [OR-Tools](https://developers.google.com/optimization)
  - [Streamlit](https://docs.streamlit.io)
  - [Pandas](https://pandas.pydata.org/docs)
  - [Geopy](https://geopy.readthedocs.io)

## Licencia

Este es un proyecto MVP (Minimum Viable Product) para uso de microempresas.

---

**Sistema de Ruteo v2.2** - Desarrollado con Python, OR-Tools y Streamlit
