"""
Configuración de la aplicación de ruteo
Versión 2.0 - Soporta múltiples orígenes y geocodificación
"""

# Configuración por defecto
# Nota: El tipo de optimización se configura exclusivamente desde la interfaz, no desde el archivo Excel
DEFAULT_CONFIG = {
    'unidad_demanda': 'kg',
    'tiempo_servicio_min': 10,
    'max_destinos_por_ruta': 15,
    'usar_ventanas_horarias': 'no',
    'velocidad_promedio_kmh': 40,
    'costo_km_default': 1.5,
    'radio_tierra_km': 6371,
    'decimales_distancia': 2,
    # Colores Logyca (Manual de marca)
    'color_origen': '#FC4C02',      # Naranja Pantone 1655 C - Origen/Centro de distribución
    'color_destino': '#51534A',     # Gris Pantone 418 C - Destinos
    'color_ruta': [
        '#FC4C02',    # Naranja principal
        '#00A19A',    # Aguamarina (color secundario Logyca)
        '#51534A',    # Gris corporativo
        '#E87722',    # Naranja claro
        '#007B7F',    # Aguamarina oscuro
        '#8B8D8A',    # Gris medio
        '#F4A261',    # Naranja suave
        '#2A9D8F',    # Verde azulado
        '#A8AAAD',    # Gris claro
        '#E76F51'     # Coral/Naranja rojizo
    ]
}

# Validaciones de archivos Excel - Versión 2.0
REQUIRED_COLUMNS = {
    'origenes': ['origen_id', 'nombre_origen', 'direccion', 'ciudad', 'pais'],
    'destinos': ['destino_id', 'nombre_cliente', 'direccion', 'ciudad', 'pais', 'demanda'],
    'flota': ['vehiculo_id', 'capacidad', 'origen_id']
}

OPTIONAL_COLUMNS = {
    'origenes': ['latitud', 'longitud', 'hora_apertura', 'hora_cierre'],
    'destinos': ['latitud', 'longitud', 'hora_inicio', 'hora_fin'],
    'flota': ['tipo_vehiculo', 'costo_km', 'hora_inicio', 'hora_fin']
}

# Mensajes de error
ERROR_MESSAGES = {
    'missing_file': 'Por favor cargue todos los archivos requeridos',
    'invalid_format': 'Formato de archivo inválido',
    'missing_columns': 'Faltan columnas requeridas en el archivo',
    'invalid_coordinates': 'Coordenadas inválidas',
    'invalid_demand': 'Valores de demanda inválidos',
    'invalid_capacity': 'Valores de capacidad inválidos',
    'no_solution': 'No se encontró solución factible. Verifique capacidades de vehículos y tiempo límite',
    'optimization_error': 'Error durante la optimización',
    'geocoding_failed': 'No se pudo geocodificar algunas direcciones',
    'invalid_origen_reference': 'Algunos vehículos referencian orígenes que no existen'
}

# Configuración de la interfaz Streamlit
STREAMLIT_CONFIG = {
    'page_title': 'RutaFácil',
    'page_icon': '🚚',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# Información de plantillas - Versión 2.0
TEMPLATE_INFO = {
    'origenes': {
        'descripcion': 'Centros de distribución, bodegas o puntos de despacho',
        'ejemplo': 'Bodega Central, Centro Distribución Norte',
        'columnas_requeridas': REQUIRED_COLUMNS['origenes'],
        'columnas_opcionales': OPTIONAL_COLUMNS['origenes'],
        'nota': 'Si latitud/longitud están vacíos, se geocodifica automáticamente'
    },
    'destinos': {
        'descripcion': 'Clientes, puntos de entrega o pedidos agregados',
        'ejemplo': 'Supermercado El Sol, Tienda La Esquina',
        'columnas_requeridas': REQUIRED_COLUMNS['destinos'],
        'columnas_opcionales': OPTIONAL_COLUMNS['destinos'],
        'nota': 'Si latitud/longitud están vacíos, se geocodifica automáticamente'
    },
    'flota': {
        'descripcion': 'Vehículos disponibles para ruteo',
        'ejemplo': 'Camión, Camioneta, Van',
        'columnas_requeridas': REQUIRED_COLUMNS['flota'],
        'columnas_opcionales': OPTIONAL_COLUMNS['flota'],
        'nota': 'Cada vehículo debe asociarse a un origen_id válido'
    },
    'config': {
        'descripcion': 'Parámetros técnicos opcionales (NO incluye tipo de optimización)',
        'ejemplo': 'unidad_demanda: kg, tiempo_servicio_min: 10, velocidad_promedio_kmh: 40',
        'columnas': ['parametro', 'valor', 'descripcion'],
        'parametros_disponibles': list(DEFAULT_CONFIG.keys()),
        'nota': 'El tipo de optimización se configura desde la interfaz, no desde este archivo'
    }
}

# Tipos de optimización
OPTIMIZATION_TYPES = {
    'distancia': {
        'nombre': 'Distancia',
        'descripcion': 'Minimiza la distancia total recorrida por todos los vehículos',
        'objetivo': 'Menor kilometraje total'
    },
    'tiempo': {
        'nombre': 'Tiempo',
        'descripcion': 'Minimiza el tiempo total de todas las rutas considerando velocidad promedio',
        'objetivo': 'Menor tiempo total de entrega'
    },
    'costo': {
        'nombre': 'Costo',
        'descripcion': 'Minimiza el costo total basado en costo por km de cada vehículo',
        'objetivo': 'Menor costo operativo'
    },
    'vehiculos': {
        'nombre': 'Vehículos',
        'descripcion': 'Minimiza el número de vehículos utilizados',
        'objetivo': 'Menor cantidad de vehículos en ruta'
    },
    'balanceado': {
        'nombre': 'Balanceado',
        'descripcion': 'Balance entre distancia, tiempo y utilización de vehículos',
        'objetivo': 'Solución equilibrada'
    }
}

# Configuración de cálculos
CALCULATION_CONFIG = {
    'velocidad_promedio_kmh': 40,  # Velocidad promedio urbana en km/h
    'tiempo_servicio_min': 10,  # Tiempo promedio por parada en minutos
    'costo_km_default': 2.5,  # Costo por km si no está especificado en el vehículo (en unidad monetaria local)
    'costo_fijo_vehiculo': 50  # Costo fijo por usar un vehículo
}

# Métodos de cálculo de distancia
DISTANCE_METHODS = {
    'haversine': {
        'nombre': 'Haversine (Línea Recta)',
        'descripcion': 'Calcula distancia en línea recta considerando la curvatura de la Tierra',
        'ventajas': 'Rápido, sin costos, funciona sin internet',
        'desventajas': 'No considera carreteras reales',
        'requiere_api': False
    },
    'google_directions': {
        'nombre': 'Google Directions (Carreteras)',
        'descripcion': 'Calcula distancia y tiempo real por carretera usando Google Maps',
        'ventajas': 'Distancias y tiempos reales, considera carreteras',
        'desventajas': 'Requiere API key, tiene costos, más lento',
        'requiere_api': True,
        'costo_por_request': 0.005  # $5 USD por 1000 requests
    }
}

# Métodos de geocodificación
GEOCODING_METHODS = {
    'nominatim': {
        'nombre': 'Nominatim (OpenStreetMap)',
        'descripcion': 'Servicio gratuito de geocodificación basado en OpenStreetMap',
        'ventajas': '100% gratuito, sin límites, sin configuración, funciona sin API key',
        'desventajas': 'Menor precisión en direcciones complejas, más lento',
        'requiere_api': False,
        'precision': 'Media-Alta',
        'velocidad': 'Media',
        'costo': 'Gratis'
    },
    'google_maps': {
        'nombre': 'Google Maps Geocoding',
        'descripcion': 'Servicio de geocodificación de alta precisión de Google Maps',
        'ventajas': 'Alta precisión, rápido, mejor manejo de direcciones complejas',
        'desventajas': 'Requiere API key, $200 USD/mes gratis luego se cobra',
        'requiere_api': True,
        'precision': 'Muy Alta',
        'velocidad': 'Rápida',
        'costo': '$5 USD por 1000 requests (después de $200 gratis)'
    }
}

# Configuración de geocodificación
GEOCODING_CONFIG = {
    'primary_provider': 'GoogleMaps',  # GoogleMaps o Nominatim
    'fallback_provider': 'Nominatim',
    'google_maps': {
        'api_key_env_var': 'GOOGLE_MAPS_API_KEY',  # Variable de entorno
        'region': 'CO',  # Código del país por defecto
        'timeout': 10
    },
    'nominatim': {
        'user_agent': 'mvp_ruteo_app',
        'timeout': 10,
        'max_retries': 3,
        'delay_between_requests': 1
    }
}
