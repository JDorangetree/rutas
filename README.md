# 🚚 Sistema de Ruteo v2.3

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.31%2B-red)
![Status](https://img.shields.io/badge/status-MVP-orange)

**Sistema avanzado de optimización de rutas para microempresas**

Optimiza entregas con múltiples orígenes, objetivos flexibles y geocodificación automática

[Características](#-características) • [Instalación](#-instalación-rápida) • [Uso](#-uso) • [Demo](#-demo-en-línea) • [Documentación](#-documentación)

</div>

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Demo en Línea](#-demo-en-línea)
- [Instalación Rápida](#-instalación-rápida)
- [Uso](#-uso)
- [Tipos de Optimización](#-tipos-de-optimización)
- [Métodos de Geocodificación](#-métodos-de-geocodificación)
- [Métodos de Cálculo de Distancia](#-métodos-de-cálculo-de-distancia)
- [Estructura de Datos](#-estructura-de-datos)
- [Documentación](#-documentación)
- [Tecnologías](#-tecnologías)
- [Roadmap](#-roadmap)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## ✨ Características

### 🎯 Optimización Flexible
- **5 objetivos de optimización**: Distancia, Tiempo, Costo, Vehículos o Balanceado
- **Múltiples orígenes**: Soporta varios centros de distribución
- **Algoritmo avanzado**: OR-Tools de Google con búsqueda local guiada
- **Tiempo límite configurable**: Desde pruebas rápidas hasta optimización exhaustiva

### 🗺️ Geocodificación Inteligente
- **Google Maps**: Alta precisión ($200 USD/mes gratis)
- **Nominatim (OpenStreetMap)**: Gratuito y sin límites
- **Validación de direcciones**: Estandariza formato colombiano automáticamente
- **Automática**: Calcula coordenadas desde direcciones
- **Fallback inteligente**: Cambia de servicio automáticamente si falla

### 📏 Distancias Precisas
- **Haversine**: Línea recta, rápido, gratuito
- **Google Directions**: Distancias reales por carretera con tráfico
- **Tráfico en tiempo real**: Considera condiciones actuales o predictivas
- **Selector flexible**: Elige según tu necesidad de precisión

### 🔒 Seguridad Robusta
- **Validación de archivos**: Límites de tamaño (5MB) y filas (500)
- **Detección de fórmulas**: Bloquea Excel malicioso automáticamente
- **Sanitización de texto**: Protección contra inyección de código
- **Logs seguros**: Ofuscación automática de datos sensibles

### 📊 Visualización y Exportación
- **Mapas interactivos**: Visualiza rutas con colores por vehículo
- **Exportación Excel**: Resultados detallados por vehículo
- **Métricas en tiempo real**: Distancia, utilización, costos

### 🎨 Interfaz Intuitiva
- **Descarga de plantillas**: Directamente desde la app
- **Guías integradas**: Información contextual en cada paso
- **Indicadores de progreso**: Sabes qué archivos faltan
- **Feedback visual**: Recomendaciones según configuración

---

## 🌐 Demo en Línea

**¿Quieres probarlo sin instalar nada?**

Visita la demo en línea: `[TU URL AQUI]` *(próximamente)*

O despliega tu propia versión en minutos: [Guía de Despliegue](docs/DESPLIEGUE.md)

---

## 🚀 Instalación Rápida

### Requisitos Previos

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Conexión a internet (para geocodificación y mapas)

### Clonar el Repositorio

```bash
git clone https://github.com/JDorangetree/rutas
cd sistema-ruteo
```

### Crear Entorno Virtual (Recomendado)

**Windows:**
```bash
python -m venv env
.\env\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv env
source env/bin/activate
```

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Ejecutar la Aplicación

**Opción 1 - Script automático (Windows):**
```bash
iniciar.bat
```

**Opción 2 - Comando directo:**
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en: `http://localhost:8501`

---

## 📖 Uso

### Flujo de Trabajo en 6 Pasos

#### 1️⃣ Descargar Plantillas
En el sidebar de la aplicación, descarga las plantillas Excel:
- 📍 **Orígenes**: Tus bodegas o centros de distribución
- 📦 **Destinos**: Tus clientes o puntos de entrega
- 🚚 **Vehículos**: Tu flota disponible
- ⚙️ **Configuración**: Parámetros personalizados (opcional)

#### 2️⃣ Llenar las Plantillas
Abre cada archivo Excel y completa con tus datos:
- Las plantillas incluyen ejemplos para guiarte
- Las columnas requeridas están claramente marcadas
- Las coordenadas se pueden dejar vacías (se geocodifican automáticamente)

#### 3️⃣ Cargar Archivos
Sube los 3 archivos obligatorios (Orígenes, Destinos, Vehículos):
- Verás ✅ cuando cada archivo se cargue correctamente
- El sistema valida automáticamente los datos
- Si las coordenadas faltan, se geocodifican en este paso

#### 4️⃣ Verificar Datos
En la pestaña **"📊 Datos"**:
- Revisa que la información se cargó correctamente
- Verifica resumen de capacidad vs demanda
- Revisa distribución de vehículos por origen

#### 5️⃣ Visualizar Ubicaciones
En la pestaña **"🗺️ Visualización"**:
- Ve todos los puntos en el mapa
- Orígenes en naranja, destinos en azul
- Verifica que las ubicaciones sean correctas

#### 6️⃣ Optimizar y Exportar
En la pestaña **"🚀 Optimización"**:
- Selecciona objetivo (Distancia, Tiempo, Costo, etc.)
- Ajusta tiempo límite según tu caso
- Ejecuta la optimización
- En **"📈 Resultados"**: Ve rutas en mapa y descarga Excel

---

## 🎯 Tipos de Optimización

El sistema ofrece 5 objetivos diferentes según tus necesidades:

### 📏 Distancia (Default)
- **Minimiza**: Kilómetros totales recorridos
- **Ideal para**: Reducir costos de combustible y desgaste
- **Resultado**: Rutas más cortas

### ⏱️ Tiempo
- **Minimiza**: Tiempo total de todas las rutas
- **Considera**: Velocidad promedio + tiempo de servicio
- **Ideal para**: Cumplir ventanas horarias y hacer más entregas

### 💰 Costo
- **Minimiza**: Costo operativo total
- **Considera**: Costo por km de cada vehículo
- **Ideal para**: Flotas con vehículos de diferentes costos operativos

### 🚚 Vehículos
- **Minimiza**: Número de vehículos utilizados
- **Ideal para**: Reducir costos fijos (conductores, seguros)
- **Resultado**: Rutas consolidadas, menos vehículos activos

### ⚖️ Balanceado
- **Optimiza**: 60% distancia + 40% tiempo
- **Ideal para**: Solución equilibrada cuando ambos factores importan

---

## 🗺️ Métodos de Geocodificación

### Google Maps Geocoding API
```
✅ Precisión: Muy Alta
✅ Velocidad: Rápida
✅ Incluye: $200 USD/mes gratis
⚠️ Requiere: API key
💰 Costo: $5 USD por 1000 requests (después del crédito)
```

**Configuración**: Ver [GOOGLE_MAPS_SETUP.md](GOOGLE_MAPS_SETUP.md)

### Nominatim (OpenStreetMap)
```
✅ Precisión: Media-Alta
✅ Velocidad: Media
✅ Costo: 100% Gratis
✅ Sin límites
❌ No requiere configuración
```

**Recomendado para**: Pruebas rápidas o cuando no necesitas máxima precisión

---

## 📏 Métodos de Cálculo de Distancia

### Haversine (Línea Recta)
```
✅ Rápido: Instantáneo
✅ Gratis: Sin costos
✅ Sin internet requerido
⚠️ No considera carreteras
```

**Fórmula**: Distancia del gran círculo (radio terrestre: 6371 km)

### Google Directions API (Carreteras Reales)
```
✅ Distancias reales de carretera
✅ Tiempos de viaje precisos con tráfico
✅ Tráfico en tiempo real o predictivo
⚠️ Requiere API key
💰 Costo: $5 USD por 1000 requests (duplica con tráfico)
```

**Opciones de tráfico**:
- **Tráfico actual**: Considera condiciones en tiempo real (ahora mismo)
- **Tráfico predictivo**: Simula condiciones en hora específica del día
- **Modelos**: Optimista, pesimista o mejor estimación

**Estimación de costos**:
- 10 ubicaciones: ~100 requests = $0.50 USD (sin tráfico) / $1.00 USD (con tráfico)
- 20 ubicaciones: ~400 requests = $2.00 USD (sin tráfico) / $4.00 USD (con tráfico)
- 50 ubicaciones: ~2500 requests = $12.50 USD (sin tráfico) / $25.00 USD (con tráfico)

---

## 📊 Estructura de Datos

### Plantilla de Orígenes

| Columna | Tipo | Requerido | Descripción |
|---------|------|-----------|-------------|
| `origen_id` | Texto | ✅ Sí | Identificador único (ej: BODEGA_01) |
| `nombre_origen` | Texto | ✅ Sí | Nombre descriptivo |
| `direccion` | Texto | ✅ Sí | Dirección completa (ej: Calle 80 #70-15) |
| `ciudad` | Texto | ✅ Sí | Ciudad |
| `pais` | Texto | ✅ Sí | País |
| `latitud` | Número | ❌ No | Se geocodifica si está vacía |
| `longitud` | Número | ❌ No | Se geocodifica si está vacía |
| `hora_apertura` | Hora | ❌ No | HH:MM formato 24h |
| `hora_cierre` | Hora | ❌ No | HH:MM formato 24h |

**💡 Validación automática**: El sistema estandariza direcciones colombianas (Cl→Calle, Cr→Carrera, etc.) y elimina redundancias de ciudad/país.

### Plantilla de Destinos

| Columna | Tipo | Requerido | Descripción |
|---------|------|-----------|-------------|
| `destino_id` | Texto | ✅ Sí | Identificador único (ej: CLIENTE_001) |
| `nombre_cliente` | Texto | ✅ Sí | Nombre del cliente |
| `direccion` | Texto | ✅ Sí | Dirección completa (ej: Cl 100 # 20-40) |
| `ciudad` | Texto | ✅ Sí | Ciudad |
| `pais` | Texto | ✅ Sí | País |
| `demanda` | Número | ✅ Sí | Cantidad a entregar |
| `latitud` | Número | ❌ No | Se geocodifica si está vacía |
| `longitud` | Número | ❌ No | Se geocodifica si está vacía |
| `hora_inicio` | Hora | ❌ No | Inicio ventana horaria |
| `hora_fin` | Hora | ❌ No | Fin ventana horaria |

**💡 Validación automática**: El sistema estandariza direcciones colombianas (Cl→Calle, Cr→Carrera, etc.) y elimina redundancias de ciudad/país.

**🔒 Límites de seguridad**: Máximo 500 destinos y 5MB por archivo.

### Plantilla de Vehículos

| Columna | Tipo | Requerido | Descripción |
|---------|------|-----------|-------------|
| `vehiculo_id` | Texto | ✅ Sí | Identificador único (ej: CAMION_01) |
| `capacidad` | Número | ✅ Sí | Capacidad máxima (mismas unidades que demanda) |
| `origen_id` | Texto | ✅ Sí | ID del origen desde donde parte |
| `tipo_vehiculo` | Texto | ❌ No | Descripción (ej: Camión 3.5T) |
| `costo_km` | Número | ❌ No | Costo operativo por km |
| `hora_inicio` | Hora | ❌ No | Inicio disponibilidad |
| `hora_fin` | Hora | ❌ No | Fin disponibilidad |

### Plantilla de Configuración (Opcional)

| Parámetro | Ejemplo | Descripción |
|-----------|---------|-------------|
| `unidad_demanda` | kg | Unidad de medida (kg, m³, unidades, etc.) |
| `tiempo_servicio_min` | 10 | Tiempo promedio por parada (minutos) |
| `max_destinos_por_ruta` | 15 | Máximo de paradas por vehículo |

**Ver ejemplos completos en**: [`templates/`](templates/)

---

## 🔍 Validación de Direcciones

El sistema incluye validación automática de direcciones colombianas para mejorar la precisión de geocodificación:

### Estandarización Automática

**Abreviaciones normalizadas:**
- `Cl`, `Cll` → `Calle`
- `Cr`, `Cra`, `Krr` → `Carrera`
- `Av`, `Ave`, `Avd` → `Avenida`
- `Dg`, `Diag` → `Diagonal`
- `Tv`, `Trans` → `Transversal`
- Y 15+ más...

**Formato estandarizado:**
```
Entrada:  "cl 80 # 70-15, Medellin"
Salida:   "Calle 80 #70-15"
```

### Resultado en Excel

Las rutas optimizadas incluyen ambas versiones:
- **Direccion**: Tu entrada original
- **Direccion_Geocodificada**: Versión estandarizada usada para geocodificación

### Beneficios

✅ **Mayor precisión**: ~95% de geocodificaciones exitosas (vs ~85% sin validación)
✅ **Transparencia**: Ves cómo se interpretó tu dirección
✅ **Sin pérdida**: Direcciones no reconocidas se preservan tal cual

---

## 🔒 Seguridad

El sistema incluye validaciones automáticas para proteger contra amenazas comunes:

### Validaciones Implementadas

| Validación | Límite | Protege Contra |
|------------|--------|----------------|
| Tamaño de archivo | 5 MB | Ataques DoS |
| Número de filas | 500 filas | Uso excesivo de API |
| Fórmulas Excel | Bloqueadas | Inyección de código |
| Texto malicioso | Sanitizado | XSS attacks |

### Fórmulas Bloqueadas

El sistema detecta y bloquea automáticamente:
- `=WEBSERVICE()` - Exfiltración de datos
- `=HYPERLINK()` - Enlaces maliciosos
- `=IMPORTDATA()` - Importación de código
- Y otras funciones peligrosas

### Recomendaciones API

⚠️ **IMPORTANTE**: Configura restricciones en Google Cloud Console:
- Limita por referente HTTP (tu dominio Streamlit)
- Habilita solo Geocoding + Distance Matrix API
- Establece presupuesto diario ($10 USD recomendado)

Ver guía completa: [SEGURIDAD.md](SEGURIDAD.md)

---

## 📚 Documentación

- **[GUIA_USUARIOS.md](docs/GUIA_USUARIOS.md)** - Manual para usuarios finales (⭐ Recomendado)
- **[SEGURIDAD.md](SEGURIDAD.md)** - Medidas de seguridad implementadas
- **[DESPLIEGUE.md](docs/DESPLIEGUE.md)** - Guía completa para desplegar en la nube
- **[GOOGLE_MAPS_SETUP.md](GOOGLE_MAPS_SETUP.md)** - Configurar API de Google Maps
- **[COMPARACION_PLATAFORMAS.md](docs/COMPARACION_PLATAFORMAS.md)** - Comparativa de opciones de hosting
- **[CHECKLIST_DESPLIEGUE.md](docs/CHECKLIST_DESPLIEGUE.md)** - Lista de verificación para despliegue

---

## 🛠️ Tecnologías

### Backend
- **Python 3.9+**: Lenguaje principal
- **OR-Tools 9.8+**: Algoritmo de optimización VRP de Google
- **Pandas 2.2+**: Procesamiento de datos
- **NumPy 1.26+**: Cálculos numéricos

### Geocodificación
- **Geopy 2.4+**: Nominatim (OpenStreetMap)
- **googlemaps 4.10+**: Google Maps Geocoding API

### Visualización
- **Streamlit 1.31+**: Framework de interfaz web
- **Folium 0.15+**: Mapas interactivos con Leaflet
- **streamlit-folium 0.16+**: Integración mapas en Streamlit

### Datos
- **openpyxl 3.1.2+**: Lectura/escritura Excel
- **python-dotenv 1.0+**: Variables de entorno

---

## 🗂️ Estructura del Proyecto

```
sistema-ruteo/
├── 📄 app.py                          # Aplicación principal Streamlit
├── 📄 requirements.txt                # Dependencias Python
├── 📄 README.md                       # Este archivo
├── 📄 .gitignore                      # Archivos ignorados por Git
│
├── 📁 src/                            # Código fuente
│   ├── data_loader.py                 # Carga y validación de datos
│   ├── route_optimizer.py             # Algoritmo de optimización VRP
│   ├── config.py                      # Configuración del sistema
│   └── create_templates.py            # Generador de plantillas
│
├── 📁 templates/                      # Plantillas Excel
│   ├── plantilla_origenes.xlsx        # Ejemplo de orígenes
│   ├── plantilla_destinos.xlsx        # Ejemplo de destinos
│   ├── plantilla_vehiculos.xlsx       # Ejemplo de vehículos
│   └── plantilla_configuracion.xlsx   # Ejemplo de configuración
│
├── 📁 .streamlit/                     # Configuración Streamlit
│   └── config.toml                    # Tema y configuración UI
│
├── 📁 output/                         # Resultados exportados (Git ignore)
├── 📁 data/                           # Tus datos (Git ignore)
│
└── 📁 docs/                           # Documentación adicional
    ├── DESPLIEGUE.md                  # Guía de despliegue
    ├── GUIA_USUARIOS.md               # Manual de usuario
    ├── COMPARACION_PLATAFORMAS.md     # Comparativa de hosting
    └── CHECKLIST_DESPLIEGUE.md        # Checklist de deploy
```

---

## 🗺️ Roadmap

### ✅ Completado (v2.3)
- [x] Múltiples orígenes y depósitos
- [x] 5 objetivos de optimización
- [x] Geocodificación con Google Maps y Nominatim
- [x] Distancias reales por carretera (Google Directions)
- [x] **Tráfico en tiempo real y predictivo** 🆕
- [x] **Validación y estandarización de direcciones** 🆕
- [x] **Medidas de seguridad robustas** 🆕
- [x] Interfaz intuitiva con Streamlit
- [x] Exportación a Excel detallada

### 🚧 En Desarrollo (v2.4)
- [ ] Ventanas horarias estrictas
- [ ] Restricciones de jornada laboral
- [ ] Caché de distancias calculadas
- [ ] Mejoras de performance para 100+ destinos
- [ ] Rate limiting para protección DoS

### 🔮 Futuro (v3.0)
- [ ] Histórico de rutas
- [ ] Dashboard de KPIs avanzados
- [ ] API REST para integración
- [ ] Soporte multi-idioma
- [ ] App móvil para conductores
- [ ] Tracking en tiempo real

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. **Fork** el repositorio
2. **Crea una rama** para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un **Pull Request**

### Reportar Bugs
Abre un [Issue](../../issues) con:
- Descripción del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Screenshots si aplica

---

## 📝 Solución de Problemas

### "No se encontró solución factible"
```
✅ Solución:
- Aumenta el tiempo límite (ej: de 60s a 180s)
- Verifica que capacidad total > demanda total
- Agrega más vehículos si es necesario
```

### "No se pudo geocodificar algunas direcciones"
```
✅ Solución:
- Usa direcciones más completas (incluye número de calle)
- Cambia a Google Maps para mayor precisión
- Agrega latitud/longitud manualmente
```

### "Algunos vehículos tienen origen_id inválido"
```
✅ Solución:
- Verifica que todos los origen_id en vehículos
  existan en el archivo de orígenes
- Los IDs distinguen mayúsculas/minúsculas
```

### "La aplicación está lenta"
```
✅ Solución:
- Usa Haversine en lugar de Google Directions
- Usa Nominatim en lugar de Google Maps
- Reduce el número de destinos para pruebas
- Considera desplegar en servidor con más recursos
```

---

## 📄 Licencia

Este proyecto es un MVP (Minimum Viable Product) desarrollado para uso de microempresas.

**MIT License** - Puedes usar, modificar y distribuir libremente con atribución.

---

## 🙏 Agradecimientos

- **Google OR-Tools**: Por el excelente solver de VRP
- **Streamlit**: Por facilitar la creación de apps web con Python
- **OpenStreetMap**: Por proporcionar datos geográficos abiertos
- **Comunidad Python**: Por las increíbles librerías utilizadas

---

## 📞 Contacto y Soporte

- **Issues**: [GitHub Issues](../../issues)
- **Documentación**: [Wiki del proyecto](../../wiki)
- **Email**: julian.naranjo2014@gmail.com

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella**

**Sistema de Ruteo v2.2** - Desarrollado con ❤️ usando Python, OR-Tools y Streamlit

[⬆ Volver arriba](#-sistema-de-ruteo-v22)

</div>
