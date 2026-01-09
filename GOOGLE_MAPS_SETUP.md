# Configuración de Google Maps API

Esta guía te ayudará a configurar la API de Google Maps para obtener geocodificación de alta precisión en el Sistema de Ruteo.

## ¿Por qué usar Google Maps?

**Ventajas:**
- ✅ Mayor precisión en geocodificación
- ✅ Mejor cobertura global
- ✅ Datos actualizados constantemente
- ✅ Manejo de direcciones complejas
- ✅ Sin límites estrictos de velocidad

**Costos:**
- 💰 Google ofrece **$200 USD en créditos gratuitos mensuales**
- 💰 Después de eso: $5 USD por cada 1,000 solicitudes de geocodificación
- 💰 Para la mayoría de microempresas, el crédito gratuito es suficiente

## Pasos para Configurar

### 1. Crear una Cuenta en Google Cloud Platform

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Inicia sesión con tu cuenta de Google
3. Acepta los términos de servicio si es tu primera vez

### 2. Crear un Proyecto

1. En la parte superior, haz clic en el selector de proyectos
2. Clic en "Nuevo Proyecto"
3. Nombre del proyecto: `Sistema de Ruteo` (o el que prefieras)
4. Clic en "Crear"

### 3. Habilitar las APIs Necesarias

**RutaFácil usa dos APIs de Google Maps:**

#### A. Geocoding API (Convierte direcciones en coordenadas)

1. En el menú lateral, ve a **"APIs y servicios" → "Biblioteca"**
2. Busca: `Geocoding API`
3. Haz clic en "Geocoding API"
4. Clic en el botón **"HABILITAR"**

#### B. Distance Matrix API (Calcula distancias reales por carretera)

1. En la misma "Biblioteca", busca: `Distance Matrix API`
2. Haz clic en "Distance Matrix API"
3. Clic en el botón **"HABILITAR"**

**⚠️ IMPORTANTE:** Si no habilitas Distance Matrix API y intentas usar "Google Directions" para calcular distancias, verás un error `REQUEST_DENIED`. En ese caso, la app usará automáticamente el método Haversine (línea recta) como alternativa.

### 4. Crear Credenciales (API Key)

1. Ve a **"APIs y servicios" → "Credenciales"**
2. Clic en **"+ CREAR CREDENCIALES"**
3. Selecciona **"Clave de API"**
4. Se creará una API key (una cadena larga como: `AIzaSyD...`)
5. **Importante**: Copia esta clave inmediatamente

### 5. (Recomendado) Restringir la API Key

Para mayor seguridad:

1. En la lista de credenciales, haz clic en tu API key
2. En "Restricciones de aplicación":
   - Para desarrollo local: Selecciona "Ninguna"
   - Para producción: Selecciona "Referentes HTTP" y agrega tu dominio

3. En "Restricciones de API":
   - Selecciona "Restringir clave"
   - Marca **ambas APIs**:
     - ✅ **Geocoding API**
     - ✅ **Distance Matrix API**

4. Guarda los cambios

**Nota:** Si solo marcas Geocoding API, el cálculo de distancias reales no funcionará.

### 6. Configurar Facturación (Requerido)

Aunque hay créditos gratuitos, Google requiere una tarjeta para activar las APIs:

1. Ve a **"Facturación"** en el menú
2. Clic en "Vincular una cuenta de facturación"
3. Sigue los pasos para agregar tu tarjeta
4. **No te preocupes**: No te cobrarán automáticamente después del crédito gratuito

**Consejo**: Configura alertas de presupuesto:
- Ve a "Facturación → Presupuestos y alertas"
- Crea un presupuesto de $200 con alertas al 50%, 90% y 100%

### 7. Configurar en el Sistema de Ruteo

Tienes **dos opciones** para configurar tu API key:

#### Opción A - Directamente en la interfaz (Más fácil) ✨

1. **Inicia la aplicación**:
   ```bash
   streamlit run app.py
   ```

2. **En el sidebar de la aplicación**:
   - Marca el checkbox "Usar Google Maps (mayor precisión)"
   - Ingresa tu API key en el campo que aparece

3. **¡Listo!** El sistema usará Google Maps inmediatamente

**Ventajas:**
- No necesitas editar archivos
- Puedes cambiar entre Google Maps y Nominatim fácilmente
- Ideal si compartes la aplicación con otros usuarios

#### Opción B - Archivo de configuración (Permanente) 🔧

1. **Abre el archivo `.env`** en la raíz del proyecto:
   ```bash
   notepad .env
   ```

2. **Reemplaza** `tu_api_key_aqui` con tu API key real:
   ```
   GOOGLE_MAPS_API_KEY=AIzaSyD-TuClaveAquí123456789
   ```

3. **Guarda el archivo**

4. **Reinicia la aplicación** si ya estaba corriendo:
   ```bash
   streamlit run app.py
   ```

**Ventajas:**
- La configuración se mantiene entre sesiones
- No necesitas ingresar la API key cada vez
- Ideal para uso personal

## Verificar que Funciona

**Si usaste la Opción A (interfaz):**
- Después de ingresar tu API key, verás un mensaje "✓ API key ingresada"
- Durante la geocodificación, el sistema usará Google Maps automáticamente

**Si usaste la Opción B (archivo .env):**
- Al iniciar la aplicación, el sistema detectará la API key automáticamente
- Puedes verificar que está activa si ves que la geocodificación es más rápida y precisa

**Si no funciona:**
- Verás el mensaje "Usando Nominatim (OpenStreetMap) - Gratuito"
- Esto significa que no se detectó una API key válida o hay un error

## Solución de Problemas

### Error: "REQUEST_DENIED - You're calling a legacy API"

**Síntoma:** Al intentar calcular distancias reales con Google Directions, aparece:
```
Error: REQUEST_DENIED (You're calling a legacy API, which is not enabled for your project...)
```

**Solución:**
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Asegúrate de estar en el proyecto correcto
3. Ve a **"APIs y servicios" → "Biblioteca"**
4. Busca y habilita: **"Distance Matrix API"** (no "Directions API")
5. Espera 2-3 minutos para que se propague
6. Reinicia la aplicación

**Alternativa temporal:** Usa el método "Haversine (Línea recta)" para calcular distancias mientras tanto.

### Error: "API key not valid"
- Verifica que copiaste la API key completa (sin espacios)
- Verifica que habilitaste ambas APIs: **Geocoding API** y **Distance Matrix API**
- Espera 2-5 minutos (las APIs nuevas tardan en activarse)
- Verifica que la facturación esté configurada

### Error: "This API project is not authorized to use this API"
- Asegúrate de habilitar las APIs correctas en tu proyecto:
  - ✅ Geocoding API (para direcciones → coordenadas)
  - ✅ Distance Matrix API (para distancias reales)
- Verifica que la facturación esté activa

### Error: "You have exceeded your daily request quota"
- Superaste los $200 USD de crédito gratuito mensual
- Ve a Google Cloud Console → Facturación para ver tu uso
- Soluciones:
  - Usa coordenadas directamente (latitud/longitud) en lugar de direcciones
  - Usa método Haversine en lugar de Google Directions
  - Configura un límite de presupuesto

### Las distancias parecen incorrectas
- Si usas **Haversine**: Las distancias son en línea recta, no por carretera
- Si usas **Google Directions**:
  - Verifica que Distance Matrix API esté habilitada
  - Verifica que ingresaste la API key correcta
  - Revisa que la facturación esté configurada

### No se ve el mensaje de Google Maps
- Verifica que el archivo `.env` esté en la raíz del proyecto
- Verifica que no haya espacios antes o después de la API key
- Formato correcto: `GOOGLE_MAPS_API_KEY=AIzaSy...` (sin comillas)
- Reinstala las dependencias: `pip install -r requirements.txt`

## Monitoreo de Uso

Para ver cuántas solicitudes has hecho:

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Selecciona tu proyecto
3. Ve a **"APIs y servicios" → "Panel"**
4. Busca "Geocoding API" y verás las estadísticas

## Costos Estimados

Ejemplos de uso típico:

| Escenario | Destinos/mes | Costo estimado |
|-----------|-------------|----------------|
| Microempresa pequeña | 50-100 | **Gratis** ($0) |
| Microempresa mediana | 500 | **Gratis** ($0) |
| Empresa grande | 5,000 | ~$20 USD |
| Empresa muy grande | 50,000 | ~$200 USD |

**Nota**: Solo pagas por direcciones que geocodificas. Si usas las plantillas con coordenadas ya incluidas, no consumes API.

## Alternativa: Seguir Usando Nominatim

Si no quieres configurar Google Maps:

1. **No hagas nada**: El sistema usará Nominatim automáticamente
2. **Ventaja**: 100% gratuito
3. **Desventaja**: Menor precisión y límites de velocidad (~1 req/seg)

Para uso ocasional o con pocas direcciones, Nominatim es suficiente.

## Recursos Adicionales

- [Documentación de Geocoding API](https://developers.google.com/maps/documentation/geocoding)
- [Precios de Google Maps](https://mapsplatform.google.com/pricing/)
- [Consola de Google Cloud](https://console.cloud.google.com/)

---

## 📝 Checklist de Configuración

Para que RutaFácil funcione completamente con Google Maps, verifica:

### APIs Habilitadas:
- [ ] **Geocoding API** - Para convertir direcciones en coordenadas
- [ ] **Distance Matrix API** - Para calcular distancias reales por carretera

### Configuración:
- [ ] API Key creada y copiada
- [ ] Facturación configurada (tarjeta agregada)
- [ ] API Key ingresada en la app o en archivo `.env`
- [ ] (Opcional) Restricciones de API configuradas

### Verificación:
- [ ] Probaste geocodificación con una dirección
- [ ] Probaste cálculo de distancias (si usas Google Directions)
- [ ] Configuraste alertas de presupuesto

---

**¿Problemas?** Revisa que:
1. ✅ **Ambas APIs** estén habilitadas (Geocoding + Distance Matrix)
2. ✅ La API key esté correctamente ingresada
3. ✅ La facturación esté activa
4. ✅ Esperaste 2-3 minutos después de habilitar las APIs

**Error REQUEST_DENIED?** → Necesitas habilitar **Distance Matrix API** específicamente
