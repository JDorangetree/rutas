# 🚚 RutaFácil - Guía de Usuario

Bienvenido a **RutaFácil**, tu planificador inteligente de rutas de entrega. Esta guía te ayudará a optimizar tus rutas de manera rápida y sencilla.

## 🚀 Acceso a la Aplicación

**URL:** https://rutafacil.streamlit.app/

---

## 📋 ¿Qué hace RutaFácil?

RutaFácil optimiza las rutas de entrega para tu negocio usando algoritmos avanzados:
- 🗺️ **Encuentra rutas óptimas** - Calcula las mejores rutas según tus criterios
- 🚚 **Asigna entregas automáticamente** - Distribuye pedidos entre tu flota
- 📍 **Soporta múltiples bodegas** - Trabaja con varios puntos de origen
- 📊 **Visualización interactiva** - Mira tus rutas en mapas detallados
- 💾 **Exporta resultados** - Descarga planes de entrega en Excel

---

## 🎯 Cómo Usar (4 Pasos Simples)

### Paso 1: Descargar y Llenar Plantillas

En el **panel lateral izquierdo** verás la sección "📤 Carga de Archivos". Para cada archivo necesario, encontrarás:

#### 1.1 Orígenes (Bodegas/Centros de Distribución)
- Haz clic en **"📥 Descargar Plantilla de Orígenes"**
- Abre el archivo Excel
- Llena con los datos de tus bodegas o centros de distribución

**Columnas principales:**
- `origen_id`: Identificador único (ej: BODEGA_01)
- `nombre_origen`: Nombre de la bodega
- `direccion`: Dirección completa (ej: Calle 80 #70-15 o Cl 80 # 70-15)
- `ciudad`, `pais`: Ciudad y país
- `latitud`, `longitud`: (Opcional, se calculan automáticamente si no los incluyes)

✨ **Nuevo:** El sistema estandariza direcciones colombianas automáticamente (Cl→Calle, Cr→Carrera, etc.)

#### 1.2 Destinos (Clientes/Puntos de Entrega)
- Haz clic en **"📥 Descargar Plantilla de Destinos"**
- Llena con tus clientes o puntos de entrega

**Columnas principales:**
- `destino_id`: Identificador único (ej: CLIENTE_001)
- `nombre_cliente`: Nombre del cliente
- `direccion`: Dirección completa (ej: Cr 45 #50-20 o Carrera 45 #50-20)
- `ciudad`, `pais`: Ciudad y país
- `demanda`: Cantidad a entregar (kg, unidades, cajas, etc.)

✨ **Nuevo:** El sistema estandariza direcciones colombianas automáticamente (Cl→Calle, Cr→Carrera, etc.)

🔒 **Límites de seguridad:** Máximo 500 destinos y 5MB por archivo

#### 1.3 Vehículos (Flota)
- Haz clic en **"📥 Descargar Plantilla de Vehículos"**
- Llena con tu flota disponible

**Columnas principales:**
- `vehiculo_id`: Identificador único (ej: CAMION_01)
- `capacidad`: Capacidad máxima (en las mismas unidades que la demanda)
- `origen_id`: Desde qué bodega parte este vehículo
- `tipo_vehiculo`: Descripción (ej: Camión 3.5T, Van)

💡 **Tip importante:** Las plantillas incluyen datos de ejemplo. Puedes probar primero con esos datos para familiarizarte con la app.

---

### Paso 2: Cargar los Archivos

Una vez que hayas llenado las plantillas:

1. En cada sección (1. Orígenes, 2. Destinos, 3. Vehículos), haz clic en el botón de carga de archivos
2. Selecciona el archivo Excel correspondiente
3. El sistema validará automáticamente tu archivo:
   - ✅ **Validaciones de seguridad**: Tamaño máximo 5MB, máximo 500 filas
   - 🔍 **Validación de direcciones**: Estandarización automática de formatos colombianos
   - 🚫 **Detección de fórmulas**: Bloquea archivos con fórmulas Excel maliciosas
4. Verás un **✅ verde** al lado del título cuando el archivo se cargue correctamente
5. El contador en la parte inferior mostrará tu progreso (ej: "Archivos cargados: 3/3")

⚠️ **Archivo opcional:** La plantilla de "Configuración" es opcional y solo necesaria si quieres personalizar parámetros avanzados.

💡 **Sobre la validación de direcciones:**
- El sistema estandariza abreviaciones: Cl→Calle, Cr→Carrera, Av→Avenida
- Elimina redundancias (si pones "Medellin" en dirección Y en ciudad)
- Formato estandarizado: `[Tipo vía] [Núm] #[Núm]-[Complemento]`
- Verás un resumen de los cambios realizados

---

### Paso 3: Configurar Parámetros (Sidebar)

Antes de optimizar, puedes ajustar los parámetros en el panel lateral:

#### ⚙️ Objetivo de Optimización
Elige qué quieres optimizar:
- **Distancia:** Minimizar kilómetros recorridos
- **Tiempo:** Completar entregas lo más rápido posible
- **Costo:** Reducir costos operativos
- **Vehículos:** Usar la menor cantidad de vehículos
- **Balanceado:** Equilibrio entre distancia (60%) y tiempo (40%)

#### ⏱️ Tiempo Límite
Cuánto tiempo le das al algoritmo para encontrar soluciones:
- **10-60 segundos:** Para pruebas rápidas
- **1-2 minutos:** Ideal para pocos destinos (<10)
- **2-3 minutos:** Recomendado para casos normales (10-30 destinos)
- **3-5 minutos:** Para problemas complejos (30+ destinos)

💡 Más tiempo = mejores soluciones, pero con rendimientos decrecientes.

---

### Paso 4: Optimizar y Ver Resultados

#### 4.1 Ejecutar Optimización
1. Ve a la pestaña **"🚀 Optimización"**
2. Verifica el resumen de capacidades (demanda vs capacidad disponible)
3. Haz clic en **"🚀 Iniciar Optimización"**
4. Espera mientras el algoritmo calcula las mejores rutas

#### 4.2 Visualizar Resultados
Una vez completada la optimización, explora las pestañas:

**📊 Pestaña "Datos":**
- Ve los archivos que cargaste
- Revisa los datos de orígenes, destinos y vehículos

**🗺️ Pestaña "Visualización":**
- Mapa interactivo con todos tus puntos
- Orígenes en naranja, destinos en azul

**📈 Pestaña "Resultados":**
- **Métricas principales:** Distancia total, tiempo estimado, vehículos usados
- **Mapa de rutas:** Cada ruta con un color diferente
- **Detalle por vehículo:** Lista de paradas ordenadas
- **Botón de exportación:** Descarga el plan completo en Excel

#### 4.3 Entender el Archivo Excel Exportado ✨ MEJORADO

El archivo Excel descargado incluye varias hojas:

**Hoja "Resumen":**
- Métricas generales de la optimización
- Total de distancia, tiempo, vehículos usados
- Utilización promedio de flota

**Hojas "Ruta Vehículo X":**
Cada vehículo tiene una hoja con sus paradas ordenadas:

| Columna | Descripción |
|---------|-------------|
| Orden | Secuencia de visita (1, 2, 3...) |
| Tipo | origen o destino |
| ID | Identificador del punto |
| Nombre | Nombre del origen/cliente |
| Ciudad | Ciudad |
| **Direccion** | 🆕 Tu entrada original |
| **Direccion_Geocodificada** | 🆕 Versión estandarizada usada |
| Latitud / Longitud | Coordenadas |
| Demanda | Cantidad a entregar |

**Nueva característica:**
- **Direccion**: Muestra exactamente lo que ingresaste
- **Direccion_Geocodificada**: Versión estandarizada que se usó para geocodificación
- Esto te permite verificar cómo se interpretaron tus direcciones

**Hoja "Destinos no Asignados":**
Si algún destino no pudo ser asignado (falta de capacidad), aparece aquí.

---

## ⚙️ Opciones Avanzadas

Encuentra estas opciones en el panel lateral, en las secciones de configuración antes de la carga de archivos.

### 🌐 Método de Geocodificación
Cómo se convierten direcciones en coordenadas:

- **Nominatim (OpenStreetMap):**
  - ✅ Gratis, sin límites estrictos
  - ✅ No requiere API key
  - ⚠️ Menos preciso en algunas zonas
  - 📌 **Recomendado para:** Pruebas y uso básico

- **Google Maps API:**
  - ✅ Muy preciso globalmente
  - ✅ Incluye $200 USD gratis/mes
  - ⚠️ Requiere configurar API key
  - 📌 **Recomendado para:** Uso profesional

### 📏 Método de Cálculo de Distancias
Cómo se calculan las distancias entre puntos:

- **Haversine (Línea recta):**
  - ✅ Instantáneo
  - ✅ Gratis, sin límites
  - ⚠️ No considera carreteras reales
  - 📌 **Recomendado para:** Pruebas rápidas, áreas urbanas pequeñas

- **Google Directions API (Carretera real):**
  - ✅ Distancias y tiempos reales
  - ✅ Considera tráfico y rutas reales
  - ⚠️ Requiere API key y tiene costos
  - 📌 **Recomendado para:** Planificación precisa de producción

### 🚦 Opciones de Tráfico (Avanzado) ✨ NUEVO

Si usas Google Directions API, puedes considerar tráfico en tus rutas:

**📍 Tráfico Actual:**
- Considera condiciones de tráfico en tiempo real (ahora mismo)
- Ideal para planificación de entregas inmediatas
- 💰 Costo: Duplica los requests de Google API

**📅 Tráfico Predictivo:**
- Simula condiciones de tráfico en una hora específica del día
- Elige la hora de inicio de rutas (ej: 8:00 AM)
- Selecciona modelo de tráfico:
  - **Mejor estimación** (recomendado): Balance entre optimista y pesimista
  - **Optimista**: Condiciones favorables
  - **Pesimista**: Considera peor escenario
- Ideal para planificar rutas para mañana o días futuros
- 💰 Costo: Duplica los requests de Google API

⚠️ **Importante:** El tráfico aumenta significativamente los costos de API. Usa solo cuando sea necesario para máxima precisión.

---

## 💡 Consejos para Mejores Resultados

### 1. Direcciones Completas ✨ MEJORADO
El sistema ahora estandariza direcciones colombianas automáticamente. Puedes usar abreviaciones:
- ✅ **BIEN:** "Calle 45 #23-15" o "Cl 45 # 23-15" → Ambos funcionan
- ✅ **BIEN:** "Carrera 7 #32-16" o "Cr 7 n 32 16" → Se estandarizan automáticamente
- ✅ **BIEN:** "Av Eldorado # 69D-25" → Direcciones con nombres de vías
- ⚠️ **EVITA:** Repetir ciudad en dirección si ya está en columna ciudad
  - Incorrecto: "Cl 80 # 70-15, Medellin" (cuando ciudad="Medellin")
  - Correcto: "Cl 80 # 70-15" (el sistema elimina redundancias automáticamente)
- ❌ **MAL:** "Centro" o "Bogotá" (muy vago)

### 2. Capacidades Realistas
- Asegúrate que la **suma de capacidades** de tus vehículos sea **mayor o igual** a la **suma de demandas**
- Si no, el algoritmo no encontrará solución
- Ejemplo:
  - Demanda total: 500 kg
  - Capacidad total: 600 kg ✅
  - Capacidad total: 400 kg ❌

### 3. Origen de Vehículos
- Cada vehículo debe tener un `origen_id` que coincida con uno de tus orígenes
- Si tienes una bodega con `origen_id = "BODEGA_01"`, tus vehículos deben tener `origen_id = "BODEGA_01"`

### 4. Prueba con Ejemplos Primero
- Las plantillas vienen con datos de ejemplo listos para usar
- Prueba primero con estos datos para familiarizarte
- Luego reemplaza con tus datos reales

### 5. Ajusta el Tiempo según Complejidad
- **5 destinos:** 30-60 segundos es suficiente
- **10 destinos:** 1-2 minutos
- **20 destinos:** 2-3 minutos
- **50+ destinos:** 4-5 minutos

---

## 🐛 Solución de Problemas

### "Error al cargar archivo"
✅ **Solución:**
- Verifica que sea un archivo `.xlsx` (Excel)
- Asegúrate que tenga las columnas requeridas con los nombres exactos
- Descarga la plantilla nuevamente y copia tus datos ahí

### "Archivo muy grande" o "Demasiadas filas" 🔒 NUEVO
✅ **Límites de seguridad:**
- Tamaño máximo: **5 MB** por archivo
- Máximo de filas: **500 destinos**
- Estos límites protegen contra uso excesivo de API y costos elevados

**Si necesitas más:**
- Divide tus destinos en múltiples optimizaciones
- Considera instalar RutaFácil en tu propio servidor

### "Fórmula detectada en Excel" 🔒 NUEVO
✅ **Solución:**
- El sistema bloquea archivos con fórmulas Excel por seguridad
- Copia tus datos y pégalos como **valores** (no fórmulas)
- En Excel: Copiar → Pegado Especial → Valores
- Las fórmulas como `=SUMA()`, `=WEBSERVICE()` no están permitidas

### "No se encontró solución"
✅ **Soluciones:**
- Aumenta el tiempo límite (prueba con 3-5 minutos)
- Verifica que la capacidad total de vehículos ≥ demanda total
- Revisa que cada vehículo tenga un `origen_id` válido
- Reduce el número de destinos si es muy alto

### "Direcciones no geocodificadas"
✅ **Soluciones:**
- Escribe direcciones más completas y específicas
- Incluye ciudad y país
- O agrega manualmente las columnas `latitud` y `longitud` con coordenadas exactas

### "La aplicación está lenta"
✅ **Explicación:**
- La geocodificación de muchas direcciones puede tomar tiempo
- Es normal, especialmente con Nominatim
- Considera usar coordenadas directamente para mayor velocidad

---

## 📞 ¿Necesitas Ayuda?

Si encuentras problemas o tienes sugerencias:

- **Repositorio GitHub:** https://github.com/JDorangetree/rutas
- **Reportar problema:** https://github.com/JDorangetree/rutas/issues
- **Email:** julian.naranjo2014@gmail.com

---

**¡Gracias por usar RutaFácil!** 🚚✨

Optimiza tus rutas, ahorra tiempo y costos.
