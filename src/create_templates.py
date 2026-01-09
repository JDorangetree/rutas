"""
Script para crear plantillas Excel de ejemplo
"""
import pandas as pd
import os
import sys

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Crear directorio templates si no existe
os.makedirs('../templates', exist_ok=True)

# Plantilla de Orígenes
origenes_data = {
    'origen_id': ['ORG_01', 'ORG_02'],
    'nombre_origen': ['Bodega Central', 'Centro Distribución Norte'],
    'direccion': ['Cra 50 #45-20', 'Calle 100 #15-30'],
    'ciudad': ['Medellin', 'Bogota'],
    'pais': ['Colombia', 'Colombia'],
    'latitud': [6.2442, 4.6867],  # Medellín y Bogotá
    'longitud': [-75.5812, -74.0548],
    'hora_apertura': ['06:00', '07:00'],
    'hora_cierre': ['18:00', '19:00']
}
df_origenes = pd.DataFrame(origenes_data)
df_origenes.to_excel('../templates/plantilla_origenes.xlsx', index=False, engine='openpyxl')
print("OK - Plantilla de origenes creada")

# Plantilla de Destinos
destinos_data = {
    'destino_id': ['CLI_101', 'CLI_102', 'CLI_103', 'CLI_104', 'CLI_105', 'CLI_106', 'CLI_107', 'CLI_108'],
    'nombre_cliente': [
        'Supermercado El Sol', 'Tienda La Esquina', 'Minimarket Central', 'Drogueria Salud',
        'Supermercado Norte', 'Tienda El Progreso', 'Minimercado Sur', 'Farmacia Vida'
    ],
    'direccion': [
        'Calle 80 #70-15', 'Cra 45 #50-20', 'Calle 53 #48-10', 'Calle 72 #60-30',
        'Calle 100 #20-40', 'Cra 30 #40-50', 'Calle 40 #55-25', 'Calle 90 #65-35'
    ],
    'ciudad': ['Medellin', 'Medellin', 'Medellin', 'Medellin', 'Bogota', 'Bogota', 'Medellin', 'Bogota'],
    'pais': ['Colombia', 'Colombia', 'Colombia', 'Colombia', 'Colombia', 'Colombia', 'Colombia', 'Colombia'],
    'demanda': [120, 85, 150, 95, 200, 75, 180, 110],
    'latitud': [6.2500, 6.2400, 6.2350, 6.2550, 4.6900, 4.6750, 6.2300, 4.7000],
    'longitud': [-75.5700, -75.5850, -75.5750, -75.5650, -74.0500, -74.0650, -75.5900, -74.0450],
    'hora_inicio': ['08:00', '09:00', '08:30', '10:00', '07:00', '09:30', '08:00', '07:30'],
    'hora_fin': ['17:00', '18:00', '16:30', '19:00', '18:00', '17:30', '16:00', '18:30'],
    'prioridad': [1, 2, 1, 3, 1, 2, 2, 1]
}
df_destinos = pd.DataFrame(destinos_data)
df_destinos.to_excel('../templates/plantilla_destinos.xlsx', index=False, engine='openpyxl')
print("OK - Plantilla de destinos creada")

# Plantilla de Flota
flota_data = {
    'vehiculo_id': ['V_01', 'V_02', 'V_03', 'V_04'],
    'tipo_vehiculo': ['Camion', 'Camioneta', 'Van', 'Camion'],
    'capacidad': [1000, 500, 700, 1200],
    'origen_id': ['ORG_01', 'ORG_01', 'ORG_02', 'ORG_02'],
    'costo_km': [2.5, 1.8, 2.0, 2.8],
    'hora_inicio': ['06:00', '07:00', '07:00', '06:30'],
    'hora_fin': ['18:00', '17:00', '19:00', '18:30']
}
df_flota = pd.DataFrame(flota_data)
df_flota.to_excel('../templates/plantilla_vehiculos.xlsx', index=False, engine='openpyxl')
print("OK - Plantilla de vehiculos creada")

# Plantilla de Configuración
config_data = {
    'parametro': [
        'unidad_demanda',
        'tiempo_servicio_min',
        'max_destinos_por_ruta',
        'optimizar_por',
        'tiempo_limite_optimizacion',
        'usar_ventanas_horarias'
    ],
    'valor': [
        'kg',
        10,
        15,
        'distancia',
        60,
        'no'
    ],
    'descripcion': [
        'Unidad de medida de la demanda (kg, m3, unidades)',
        'Tiempo promedio de servicio en cada destino (minutos)',
        'Numero maximo de destinos por ruta',
        'Criterio de optimizacion: distancia o tiempo',
        'Tiempo limite para el algoritmo (segundos)',
        'Usar restricciones de ventanas horarias (si/no)'
    ]
}
df_config = pd.DataFrame(config_data)
df_config.to_excel('../templates/plantilla_configuracion.xlsx', index=False, engine='openpyxl')
print("OK - Plantilla de configuracion creada")

print("\nOK - Todas las plantillas creadas en la carpeta 'templates'")
