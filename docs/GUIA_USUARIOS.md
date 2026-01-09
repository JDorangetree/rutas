# Guía Rápida para Usuarios - Sistema de Ruteo MVP

¡Gracias por probar nuestro Sistema de Ruteo! Esta guía te ayudará a usar la aplicación.

## 🚀 Acceso Rápido

**URL de la aplicación:** `[INSERTAR URL AQUÍ]`

---

## 📋 ¿Qué hace esta aplicación?

El Sistema de Ruteo optimiza las rutas de entrega para tu negocio:
- 🗺️ Encuentra las rutas más eficientes
- 🚚 Asigna pedidos a vehículos automáticamente
- 📊 Visualiza las rutas en mapas interactivos
- 💾 Exporta los planes de entrega a Excel

---

## 🎯 Cómo Usar (5 Pasos Simples)

### Paso 1: Descargar Plantillas
1. Ve al panel lateral izquierdo
2. En "📥 Plantillas de Excel", haz clic en:
   - 📍 **Orígenes** (tus bodegas o centros de distribución)
   - 📦 **Destinos** (tus clientes)
   - 🚚 **Vehículos** (tu flota)

### Paso 2: Llenar las Plantillas
- Abre cada archivo Excel descargado
- Llena los datos con tu información real
- **Tip:** Las plantillas vienen con ejemplos que puedes usar primero

**Columnas importantes:**
- **Orígenes:** Necesitas dirección completa o coordenadas (lat/lon)
- **Destinos:** Dirección + demanda (kg, unidades, etc.)
- **Vehículos:** Capacidad + desde qué origen sale

### Paso 3: Cargar los Archivos
1. En "📤 Carga de Archivos"
2. Sube los 3 archivos Excel (Orígenes, Destinos, Vehículos)
3. Verás ✅ verde cuando cada archivo esté cargado correctamente

### Paso 4: Configurar Optimización
1. Ve a la pestaña **"🚀 Optimización"**
2. Revisa el tiempo límite (3 minutos es recomendado)
3. Haz clic en **"🚀 Iniciar Optimización"**
4. Espera mientras el sistema calcula las mejores rutas

### Paso 5: Ver y Descargar Resultados
1. Ve a la pestaña **"📈 Resultados"**
2. Verás:
   - Mapa con todas las rutas optimizadas
   - Resumen de kilómetros totales
   - Detalle de cada vehículo
3. Haz clic en **"📥 Exportar a Excel"** para descargar el plan

---

## ⚙️ Opciones Avanzadas (Opcional)

### Método de Geocodificación
- **Nominatim (OpenStreetMap):** Gratis, no requiere API key
- **Google Maps:** Más preciso, requiere API key (incluye $200 USD gratis/mes)

### Método de Cálculo de Distancias
- **Haversine:** Línea recta, rápido, gratis
- **Google Directions:** Distancia real por carretera (requiere API key)

### Tipo de Optimización
Puedes elegir qué optimizar:
- 🎯 **Distancia:** Menos kilómetros
- ⏱️ **Tiempo:** Entregas más rápidas
- 💰 **Costo:** Menor costo operativo
- 🚚 **Vehículos:** Usar menos vehículos
- ⚖️ **Balanceado:** Mix de todo

---

## 💡 Consejos para Mejores Resultados

1. **Direcciones completas:** Mientras más detalle, mejor
   - ✅ BIEN: "Calle 45 #23-15, Bogotá, Colombia"
   - ❌ MAL: "Centro"

2. **Capacidad realista:** No pongas más carga que la capacidad real de tus vehículos

3. **Tiempo límite:**
   - Pocos destinos (<10): 1 minuto
   - Destinos medios (10-30): 3 minutos
   - Muchos destinos (30+): 5 minutos

4. **Prueba con ejemplos primero:** Las plantillas vienen con datos de ejemplo

---

## 🐛 ¿Encontraste un Problema?

### Problemas Comunes

**"Error al cargar archivo"**
- Verifica que sea un archivo .xlsx (Excel)
- Revisa que tenga las columnas requeridas

**"No se encontró solución"**
- Aumenta el tiempo límite
- Verifica que la capacidad de vehículos sea suficiente
- Revisa que cada vehículo tenga un origen_id válido

**"Direcciones no geocodificadas"**
- Escribe direcciones más completas
- O agrega manualmente latitud/longitud

**"La app está lenta"**
- La geocodificación de muchas direcciones puede tomar tiempo
- Espera unos momentos o considera agregar coordenadas manualmente

### Reportar Problemas

Si encuentras un error:
1. Toma captura de pantalla
2. Anota qué estabas haciendo
3. Envía a: **[TU EMAIL AQUÍ]**

O crea un issue en: **[TU GITHUB REPO]/issues**

---

## 📊 ¿Qué Estamos Probando?

Tu feedback es muy valioso. Nos interesa saber:

1. **Facilidad de uso:**
   - ¿Fue fácil entender cómo usarla?
   - ¿Las instrucciones fueron claras?

2. **Funcionalidad:**
   - ¿Las rutas generadas tienen sentido?
   - ¿Los resultados son útiles?

3. **Rendimiento:**
   - ¿Cuánto tiempo tardó?
   - ¿La app fue rápida o lenta?

4. **Errores:**
   - ¿Encontraste errores?
   - ¿Algo no funcionó como esperabas?

5. **Sugerencias:**
   - ¿Qué agregarías?
   - ¿Qué quitarías?

---

## 📞 Contacto

- **Email:** [tu-email@ejemplo.com]
- **GitHub:** [tu-usuario/tu-repo]
- **Issues:** [github.com/tu-usuario/tu-repo/issues]

---

## 🙏 ¡Gracias por Probar!

Tu feedback nos ayuda a mejorar el sistema para todos.

**Tiempo estimado de prueba:** 15-30 minutos

**Fecha de esta versión:** [FECHA]

---

## 📝 Checklist de Prueba

Marca lo que has probado:

- [ ] Descargar plantillas
- [ ] Llenar datos con ejemplos incluidos
- [ ] Cargar archivos
- [ ] Optimizar rutas
- [ ] Ver mapa de resultados
- [ ] Exportar a Excel
- [ ] Probar con mis propios datos reales
- [ ] Probar diferentes tiempos límite
- [ ] Probar diferentes tipos de optimización
- [ ] Reportar feedback

---

¡Esperamos que la herramienta te sea útil! 🚀
