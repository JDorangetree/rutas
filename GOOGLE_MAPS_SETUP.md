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

### 3. Habilitar la API de Geocodificación

1. En el menú lateral, ve a **"APIs y servicios" → "Biblioteca"**
2. Busca: `Geocoding API`
3. Haz clic en "Geocoding API"
4. Clic en el botón **"HABILITAR"**

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
   - Selecciona "Direcciones IP"
   - Agrega tu IP (o usa `0.0.0.0/0` para desarrollo)

3. En "Restricciones de API":
   - Selecciona "Restringir clave"
   - Marca solo: **Geocoding API**

4. Guarda los cambios

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

### Error: "API key not valid"
- Verifica que copiaste la API key completa
- Verifica que habilitaste la "Geocoding API"
- Espera unos minutos (las APIs pueden tardar en activarse)

### Error: "This API project is not authorized to use this API"
- Asegúrate de habilitar la "Geocoding API" en tu proyecto
- Verifica que la facturación esté configurada

### Error: "You have exceeded your daily request quota"
- Superaste los créditos gratuitos mensuales
- Ve a Google Cloud Console para ver tu uso
- Considera optimizar (cachear coordenadas ya geocodificadas)

### No se ve el mensaje de Google Maps
- Verifica que el archivo `.env` esté en la raíz del proyecto
- Verifica que no haya espacios antes o después de la API key
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

¿Problemas? Revisa que:
1. ✅ La API key esté en el archivo `.env`
2. ✅ Habilitaste "Geocoding API"
3. ✅ Configuraste facturación
4. ✅ Reinstalaste dependencias: `pip install -r requirements.txt`
