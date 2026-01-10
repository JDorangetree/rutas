"""
Módulo para optimización de rutas usando OR-Tools
Versión 2.2 - Soporta múltiples depósitos, múltiples objetivos y distancias reales por carretera
Resuelve el Vehicle Routing Problem (VRP) con diferentes criterios: distancia, tiempo, costo, vehículos y balanceado
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import streamlit as st
from config import CALCULATION_CONFIG

# Intentar importar googlemaps para Directions API
try:
    import googlemaps
    GOOGLEMAPS_AVAILABLE = True
except ImportError:
    GOOGLEMAPS_AVAILABLE = False


class RouteOptimizer:
    """Clase para optimizar rutas de vehículos con múltiples depósitos y objetivos"""

    def __init__(self, origenes: pd.DataFrame, destinos: pd.DataFrame, flota: pd.DataFrame,
                 config: Dict = None, optimization_type: str = 'distancia',
                 distance_method: str = 'haversine', google_api_key_directions: Optional[str] = None,
                 considerar_trafico: bool = False, hora_salida_rutas: Optional[object] = None):
        self.origenes = origenes
        self.destinos = destinos
        self.flota = flota
        self.config = config or {}
        self.optimization_type = optimization_type
        self.distance_method = distance_method
        self.google_api_key_directions = google_api_key_directions
        self.considerar_trafico = considerar_trafico
        self.hora_salida_rutas = hora_salida_rutas
        self.distance_matrix = None
        self.time_matrix = None
        self.duration_matrix = None  # Tiempos reales de Google Directions
        self.cost_matrix = None
        self.solution = None

        # Inicializar cliente de Google Directions si es necesario
        if self.distance_method == 'google_directions' and self.google_api_key_directions:
            if GOOGLEMAPS_AVAILABLE:
                try:
                    self.gmaps_client = googlemaps.Client(key=self.google_api_key_directions)
                except Exception as e:
                    st.error(f"❌ Error al inicializar Google Directions: {str(e)}")
                    st.warning("⚠️ Usando método Haversine como alternativa")
                    self.distance_method = 'haversine'
            else:
                st.error("❌ Librería googlemaps no disponible")
                st.warning("⚠️ Usando método Haversine como alternativa")
                self.distance_method = 'haversine'

    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calcula distancia haversine entre dos puntos en km
        """
        R = 6371  # Radio de la Tierra en km

        lat1_rad = np.radians(lat1)
        lat2_rad = np.radians(lat2)
        delta_lat = np.radians(lat2 - lat1)
        delta_lon = np.radians(lon2 - lon1)

        a = np.sin(delta_lat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(delta_lon / 2) ** 2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        return R * c

    def calculate_time(self, distance_km: float) -> float:
        """
        Calcula tiempo estimado en minutos basado en distancia y velocidad promedio
        """
        velocidad_kmh = self.config.get('velocidad_promedio_kmh', CALCULATION_CONFIG['velocidad_promedio_kmh'])
        tiempo_viaje_min = (distance_km / velocidad_kmh) * 60
        tiempo_servicio_min = self.config.get('tiempo_servicio_min', CALCULATION_CONFIG['tiempo_servicio_min'])
        return tiempo_viaje_min + tiempo_servicio_min

    def calculate_cost(self, distance_km: float, vehicle_id: int) -> float:
        """
        Calcula costo estimado basado en distancia y costo por km del vehículo
        """
        # Obtener costo por km del vehículo si existe
        vehiculo = self.flota.iloc[vehicle_id]
        costo_km = vehiculo.get('costo_km', CALCULATION_CONFIG['costo_km_default'])
        if pd.isna(costo_km):
            costo_km = CALCULATION_CONFIG['costo_km_default']

        return distance_km * costo_km

    def create_distance_matrix_google_directions(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Crea matriz de distancias usando Google Directions API (distancias reales por carretera)
        Retorna (distance_matrix en metros, duration_matrix en segundos)
        """
        # Combinar orígenes y destinos
        all_locations = pd.concat([
            self.origenes[['latitud', 'longitud']],
            self.destinos[['latitud', 'longitud']]
        ], ignore_index=True)

        n = len(all_locations)
        distance_matrix = np.zeros((n, n))
        duration_matrix = np.zeros((n, n))

        # Preparar lista de coordenadas
        origins = [(row['latitud'], row['longitud']) for _, row in all_locations.iterrows()]

        # Procesar en lotes para respetar límites de API
        batch_size = 25  # Google permite máximo 25 origins × 25 destinations por request
        total_requests = (n // batch_size + 1) ** 2

        if self.considerar_trafico:
            if self.hora_salida_rutas:
                st.info(f"🚦 Calculando distancias Y tiempos con tráfico predictivo para {self.hora_salida_rutas.strftime('%H:%M')}...")
            else:
                st.info(f"🚦 Calculando distancias Y tiempos con tráfico actual (ahora)...")
            costo_por_request = 0.010  # Con tráfico cuesta el doble
        else:
            st.info(f"📡 Calculando distancias reales con Google Directions...")
            costo_por_request = 0.005

        st.info(f"💰 Esto realizará aproximadamente {total_requests} requests (~${total_requests * costo_por_request:.2f} USD)")

        progress_bar = st.progress(0)
        total_processed = 0
        total_pairs = n * n

        try:
            for i in range(0, n, batch_size):
                for j in range(0, n, batch_size):
                    # Obtener batch de orígenes y destinos
                    batch_origins = origins[i:min(i + batch_size, n)]
                    batch_destinations = origins[j:min(j + batch_size, n)]

                    # Preparar parámetros para Directions API
                    api_params = {
                        'origins': batch_origins,
                        'destinations': batch_destinations,
                        'mode': 'driving',
                        'units': 'metric'
                    }

                    # Agregar parámetros de tráfico si está habilitado
                    if self.considerar_trafico:
                        if self.hora_salida_rutas:
                            # Tráfico predictivo: usar hora específica
                            import datetime
                            now = datetime.datetime.now()
                            departure = now.replace(
                                hour=self.hora_salida_rutas.hour,
                                minute=self.hora_salida_rutas.minute,
                                second=0,
                                microsecond=0
                            )
                            # Si la hora ya pasó hoy, usar mañana
                            if departure < now:
                                departure += datetime.timedelta(days=1)
                            api_params['departure_time'] = departure
                            api_params['traffic_model'] = st.session_state.get('modelo_trafico', 'best_guess')
                        else:
                            # Tráfico actual
                            api_params['departure_time'] = 'now'
                            api_params['traffic_model'] = 'best_guess'

                    # Llamar a Distance Matrix API
                    result = self.gmaps_client.distance_matrix(**api_params)

                    # Procesar resultados
                    for bi, row in enumerate(result['rows']):
                        for bj, element in enumerate(row['elements']):
                            actual_i = i + bi
                            actual_j = j + bj

                            if element['status'] == 'OK':
                                distance_matrix[actual_i][actual_j] = element['distance']['value']  # metros

                                # Usar duration_in_traffic si está disponible (cuando se considera tráfico)
                                if 'duration_in_traffic' in element:
                                    duration_matrix[actual_i][actual_j] = element['duration_in_traffic']['value']  # segundos con tráfico
                                else:
                                    duration_matrix[actual_i][actual_j] = element['duration']['value']  # segundos sin tráfico
                            else:
                                # Si falla, usar Haversine como fallback
                                distance_km = self.calculate_distance(
                                    all_locations.iloc[actual_i]['latitud'],
                                    all_locations.iloc[actual_i]['longitud'],
                                    all_locations.iloc[actual_j]['latitud'],
                                    all_locations.iloc[actual_j]['longitud']
                                )
                                distance_matrix[actual_i][actual_j] = distance_km * 1000
                                # Estimar duración basada en velocidad promedio
                                velocidad_kmh = CALCULATION_CONFIG['velocidad_promedio_kmh']
                                duration_matrix[actual_i][actual_j] = (distance_km / velocidad_kmh) * 3600

                            total_processed += 1
                            progress_bar.progress(min(total_processed / total_pairs, 1.0))

            progress_bar.empty()
            st.success("✅ Distancias reales calculadas correctamente")

        except Exception as e:
            st.error(f"❌ Error al calcular distancias con Google Directions: {str(e)}")
            st.warning("⚠️ Usando método Haversine como alternativa")
            # Fallback a Haversine
            return self.create_distance_matrix_haversine()

        self.distance_matrix = distance_matrix.astype(int)
        self.duration_matrix = duration_matrix.astype(int)
        return self.distance_matrix, self.duration_matrix

    def create_distance_matrix_haversine(self) -> np.ndarray:
        """
        Crea matriz de distancias usando Haversine (línea recta)
        """
        # Combinar orígenes y destinos
        all_locations = pd.concat([
            self.origenes[['latitud', 'longitud']],
            self.destinos[['latitud', 'longitud']]
        ], ignore_index=True)

        n = len(all_locations)
        distance_matrix = np.zeros((n, n))

        # Calcular distancias
        for i in range(n):
            for j in range(n):
                if i != j:
                    distance_matrix[i][j] = self.calculate_distance(
                        all_locations.iloc[i]['latitud'],
                        all_locations.iloc[i]['longitud'],
                        all_locations.iloc[j]['latitud'],
                        all_locations.iloc[j]['longitud']
                    )

        # Convertir a enteros (metros) para OR-Tools
        self.distance_matrix = (distance_matrix * 1000).astype(int)
        return self.distance_matrix

    def create_distance_matrix(self) -> np.ndarray:
        """
        Crea matriz de distancias según el método configurado
        """
        if self.distance_method == 'google_directions' and self.google_api_key_directions:
            dist_matrix, dur_matrix = self.create_distance_matrix_google_directions()
            return dist_matrix
        else:
            return self.create_distance_matrix_haversine()

    def create_time_matrix(self) -> np.ndarray:
        """
        Crea matriz de tiempos entre todos los puntos (en segundos)
        Si se usó Google Directions, usa los tiempos reales; si no, calcula basado en velocidad
        """
        if self.distance_matrix is None:
            self.create_distance_matrix()

        # Si tenemos tiempos reales de Google Directions, usarlos
        if self.duration_matrix is not None:
            self.time_matrix = self.duration_matrix
            return self.time_matrix

        # Si no, calcular basado en distancia y velocidad promedio
        # Convertir distancias (metros) a km y calcular tiempo
        distance_km_matrix = self.distance_matrix / 1000.0
        velocidad_kmh = self.config.get('velocidad_promedio_kmh', CALCULATION_CONFIG['velocidad_promedio_kmh'])

        # Tiempo de viaje en minutos
        time_matrix = (distance_km_matrix / velocidad_kmh) * 60

        # Convertir a enteros (segundos) para OR-Tools
        self.time_matrix = (time_matrix * 60).astype(int)
        return self.time_matrix

    def create_cost_matrix(self) -> List[np.ndarray]:
        """
        Crea matrices de costos por vehículo (cada vehículo puede tener diferente costo/km)
        Retorna una lista de matrices, una por vehículo
        """
        if self.distance_matrix is None:
            self.create_distance_matrix()

        distance_km_matrix = self.distance_matrix / 1000.0
        cost_matrices = []

        for vehicle_id in range(len(self.flota)):
            vehiculo = self.flota.iloc[vehicle_id]
            costo_km = vehiculo.get('costo_km', CALCULATION_CONFIG['costo_km_default'])
            if pd.isna(costo_km):
                costo_km = CALCULATION_CONFIG['costo_km_default']

            # Costo en unidades monetarias * 100 para trabajar con enteros
            cost_matrix = (distance_km_matrix * costo_km * 100).astype(int)
            cost_matrices.append(cost_matrix)

        self.cost_matrix = cost_matrices
        return self.cost_matrix

    def create_data_model(self) -> Dict:
        """
        Crea el modelo de datos para OR-Tools con soporte para múltiples depósitos
        """
        data = {}

        # Matriz de distancias
        if self.distance_matrix is None:
            self.create_distance_matrix()

        data['distance_matrix'] = self.distance_matrix.tolist()

        # Demandas (0 para orígenes, demanda real para destinos)
        demands = [0] * len(self.origenes) + self.destinos['demanda'].tolist()
        data['demands'] = demands

        # Capacidades de vehículos
        data['vehicle_capacities'] = self.flota['capacidad'].tolist()

        # Número de vehículos
        data['num_vehicles'] = len(self.flota)

        # Depósitos de inicio y fin por vehículo
        # Mapear origen_id a índice en la lista de orígenes
        origen_id_to_index = {origen_id: idx for idx, origen_id in enumerate(self.origenes['origen_id'])}

        data['starts'] = []
        data['ends'] = []

        for _, vehiculo in self.flota.iterrows():
            depot_index = origen_id_to_index[vehiculo['origen_id']]
            data['starts'].append(depot_index)
            data['ends'].append(depot_index)

        # Información adicional para referencia
        data['num_origenes'] = len(self.origenes)
        data['num_destinos'] = len(self.destinos)

        return data

    def solve(self, time_limit_seconds: int = 30) -> Dict:
        """
        Resuelve el VRP con múltiples depósitos usando OR-Tools
        Soporta diferentes objetivos: distancia, tiempo, costo, vehículos, balanceado
        """
        try:
            # Crear modelo de datos
            data = self.create_data_model()

            # Crear el routing index manager con múltiples depósitos
            manager = pywrapcp.RoutingIndexManager(
                len(data['distance_matrix']),
                data['num_vehicles'],
                data['starts'],
                data['ends']
            )

            # Crear el routing model
            routing = pywrapcp.RoutingModel(manager)

            # Configurar función de costo según el tipo de optimización
            if self.optimization_type == 'distancia':
                # Optimizar por distancia (comportamiento original)
                def cost_callback(from_index, to_index):
                    from_node = manager.IndexToNode(from_index)
                    to_node = manager.IndexToNode(to_index)
                    return data['distance_matrix'][from_node][to_node]

                transit_callback_index = routing.RegisterTransitCallback(cost_callback)
                routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

            elif self.optimization_type == 'tiempo':
                # Optimizar por tiempo
                time_matrix = self.create_time_matrix()
                data['time_matrix'] = time_matrix.tolist()

                def time_callback(from_index, to_index):
                    from_node = manager.IndexToNode(from_index)
                    to_node = manager.IndexToNode(to_index)
                    return data['time_matrix'][from_node][to_node]

                transit_callback_index = routing.RegisterTransitCallback(time_callback)
                routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

            elif self.optimization_type == 'costo':
                # Optimizar por costo (diferente para cada vehículo)
                cost_matrices = self.create_cost_matrix()

                # Registrar callbacks por vehículo
                transit_callback_indices = []
                for vehicle_id in range(data['num_vehicles']):
                    cost_matrix = cost_matrices[vehicle_id]

                    def make_cost_callback(v_id):
                        def cost_callback(from_index, to_index):
                            from_node = manager.IndexToNode(from_index)
                            to_node = manager.IndexToNode(to_index)
                            return int(cost_matrices[v_id][from_node][to_node])
                        return cost_callback

                    callback_index = routing.RegisterTransitCallback(make_cost_callback(vehicle_id))
                    transit_callback_indices.append(callback_index)
                    routing.SetArcCostEvaluatorOfVehicle(callback_index, vehicle_id)

            elif self.optimization_type == 'vehiculos':
                # Minimizar número de vehículos - usar distancia pero con costo fijo alto por vehículo
                def cost_callback(from_index, to_index):
                    from_node = manager.IndexToNode(from_index)
                    to_node = manager.IndexToNode(to_index)
                    return data['distance_matrix'][from_node][to_node]

                transit_callback_index = routing.RegisterTransitCallback(cost_callback)
                routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

                # Agregar costo fijo alto por usar cada vehículo
                for vehicle_id in range(data['num_vehicles']):
                    routing.SetFixedCostOfVehicle(CALCULATION_CONFIG['costo_fijo_vehiculo'] * 100000, vehicle_id)

            elif self.optimization_type == 'balanceado':
                # Balance entre distancia y tiempo (promedio ponderado)
                time_matrix = self.create_time_matrix()
                data['time_matrix'] = time_matrix.tolist()

                def balanced_callback(from_index, to_index):
                    from_node = manager.IndexToNode(from_index)
                    to_node = manager.IndexToNode(to_index)
                    # 60% distancia, 40% tiempo (normalizado)
                    distance_norm = data['distance_matrix'][from_node][to_node] / 1000  # metros a "unidades"
                    time_norm = data['time_matrix'][from_node][to_node] / 60  # segundos a "unidades"
                    return int(distance_norm * 0.6 + time_norm * 0.4)

                transit_callback_index = routing.RegisterTransitCallback(balanced_callback)
                routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

            else:
                # Por defecto, usar distancia
                def cost_callback(from_index, to_index):
                    from_node = manager.IndexToNode(from_index)
                    to_node = manager.IndexToNode(to_index)
                    return data['distance_matrix'][from_node][to_node]

                transit_callback_index = routing.RegisterTransitCallback(cost_callback)
                routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

            # Agregar restricción de capacidad
            def demand_callback(from_index):
                from_node = manager.IndexToNode(from_index)
                return data['demands'][from_node]

            demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

            routing.AddDimensionWithVehicleCapacity(
                demand_callback_index,
                0,  # slack nulo
                data['vehicle_capacities'],
                True,  # start cumul to zero
                'Capacity'
            )

            # Penalizar destinos no visitados (permitir soluciones parciales si es necesario)
            penalty = 1000000
            for node in range(data['num_origenes'], len(data['distance_matrix'])):
                routing.AddDisjunction([manager.NodeToIndex(node)], penalty)

            # Configurar estrategia de búsqueda
            search_parameters = pywrapcp.DefaultRoutingSearchParameters()
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
            )
            search_parameters.local_search_metaheuristic = (
                routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
            )
            search_parameters.time_limit.seconds = time_limit_seconds

            # Resolver
            solution = routing.SolveWithParameters(search_parameters)

            if solution:
                self.solution = self.extract_solution(data, manager, routing, solution)
                return self.solution
            else:
                st.error("No se encontró solución factible. Intenta aumentar el tiempo límite o ajustar capacidades.")
                return None

        except Exception as e:
            st.error(f"Error en optimización: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            return None

    def extract_solution(self, data, manager, routing, solution) -> Dict:
        """
        Extrae y formatea la solución del solver
        """
        result = {
            'total_distance': 0,
            'routes': [],
            'vehicle_loads': [],
            'unassigned': []
        }

        total_distance = 0
        num_origenes = data['num_origenes']

        # Identificar nodos no asignados
        all_nodes = set(range(num_origenes, num_origenes + data['num_destinos']))
        visited_nodes = set()

        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            route = []
            route_distance = 0
            route_load = 0

            # Obtener información del vehículo
            vehiculo_info = self.flota.iloc[vehicle_id]
            origen_id = vehiculo_info['origen_id']

            # Encontrar el origen correspondiente
            origen_row = self.origenes[self.origenes['origen_id'] == origen_id].iloc[0]

            while not routing.IsEnd(index):
                node_index = manager.IndexToNode(index)
                route_load += data['demands'][node_index]

                # Agregar información del nodo
                if node_index < num_origenes:
                    # Es un origen
                    origen_row_temp = self.origenes.iloc[node_index]
                    location_info = {
                        'type': 'origen',
                        'id': origen_row_temp['origen_id'],
                        'nombre': origen_row_temp['nombre_origen'],
                        'direccion': origen_row_temp['direccion'],
                        'ciudad': origen_row_temp['ciudad'],
                        'latitud': origen_row_temp['latitud'],
                        'longitud': origen_row_temp['longitud'],
                        'demanda': 0
                    }
                else:
                    # Es un destino
                    dest_index = node_index - num_origenes
                    dest_row = self.destinos.iloc[dest_index]
                    visited_nodes.add(node_index)

                    location_info = {
                        'type': 'destino',
                        'id': dest_row['destino_id'],
                        'nombre': dest_row['nombre_cliente'],
                        'direccion': dest_row['direccion'],
                        'ciudad': dest_row['ciudad'],
                        'latitud': dest_row['latitud'],
                        'longitud': dest_row['longitud'],
                        'demanda': dest_row['demanda']
                    }

                route.append(location_info)

                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

            # Agregar nodo final (depósito de llegada)
            node_index = manager.IndexToNode(index)
            origen_row_final = self.origenes.iloc[node_index]
            route.append({
                'type': 'origen',
                'id': origen_row_final['origen_id'],
                'nombre': origen_row_final['nombre_origen'],
                'direccion': origen_row_final['direccion'],
                'ciudad': origen_row_final['ciudad'],
                'latitud': origen_row_final['latitud'],
                'longitud': origen_row_final['longitud'],
                'demanda': 0
            })

            # Solo incluir rutas con al menos un destino
            if len(route) > 2:
                result['routes'].append({
                    'vehicle_id': vehiculo_info['vehiculo_id'],
                    'vehicle_type': vehiculo_info['tipo_vehiculo'],
                    'origen_id': origen_id,
                    'origen_nombre': origen_row['nombre_origen'],
                    'route': route,
                    'distance_km': route_distance / 1000,
                    'load': route_load,
                    'capacity': data['vehicle_capacities'][vehicle_id],
                    'utilization': (route_load / data['vehicle_capacities'][vehicle_id] * 100) if data['vehicle_capacities'][vehicle_id] > 0 else 0
                })
                total_distance += route_distance

        result['total_distance'] = total_distance / 1000  # Convertir a km

        # Identificar destinos no asignados
        unassigned_nodes = all_nodes - visited_nodes
        if unassigned_nodes:
            result['unassigned'] = []
            for node in unassigned_nodes:
                dest_index = node - num_origenes
                dest_row = self.destinos.iloc[dest_index]
                result['unassigned'].append({
                    'id': dest_row['destino_id'],
                    'nombre': dest_row['nombre_cliente'],
                    'demanda': dest_row['demanda']
                })

        return result

    def export_to_excel(self, filepath: str) -> bool:
        """
        Exporta la solución a un archivo Excel
        """
        if self.solution is None:
            st.error("No hay solución para exportar")
            return False

        try:
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Resumen general
                summary_data = {
                    'Métrica': [
                        'Distancia Total (km)',
                        'Número de Vehículos Usados',
                        'Número de Destinos Asignados',
                        'Número de Destinos No Asignados',
                        'Número de Orígenes'
                    ],
                    'Valor': [
                        round(self.solution['total_distance'], 2),
                        len([r for r in self.solution['routes'] if len(r['route']) > 2]),
                        len(self.destinos) - len(self.solution.get('unassigned', [])),
                        len(self.solution.get('unassigned', [])),
                        len(self.origenes)
                    ]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Resumen', index=False)

                # Detalle de rutas por vehículo
                for i, route_info in enumerate(self.solution['routes']):
                    if len(route_info['route']) > 2:
                        route_data = []
                        for j, location in enumerate(route_info['route']):
                            route_data.append({
                                'Orden': j + 1,
                                'Tipo': location['type'],
                                'ID': location['id'],
                                'Nombre': location['nombre'],
                                'Ciudad': location['ciudad'],
                                'Direccion': location['direccion'],
                                'Latitud': location['latitud'],
                                'Longitud': location['longitud'],
                                'Demanda': location['demanda']
                            })

                        df_route = pd.DataFrame(route_data)

                        # Información del vehículo en las primeras filas
                        info_df = pd.DataFrame({
                            'Orden': ['', ''],
                            'Tipo': ['Vehículo:', 'Origen:'],
                            'ID': [route_info['vehicle_id'], route_info['origen_id']],
                            'Nombre': [route_info['vehicle_type'], route_info['origen_nombre']],
                            'Ciudad': [f"Carga: {route_info['load']}/{route_info['capacity']}", f"Utilización: {route_info['utilization']:.1f}%"],
                            'Direccion': [f"Distancia: {route_info['distance_km']:.2f} km", ''],
                            'Latitud': ['', ''],
                            'Longitud': ['', ''],
                            'Demanda': ['', '']
                        })

                        # Combinar información y ruta
                        final_df = pd.concat([info_df, df_route], ignore_index=True)

                        sheet_name = f"Ruta_{i+1}_{route_info['vehicle_id']}"[:31]  # Límite de Excel
                        final_df.to_excel(writer, sheet_name=sheet_name, index=False)

                # Destinos no asignados (si hay)
                if self.solution.get('unassigned'):
                    unassigned_data = []
                    for dest in self.solution['unassigned']:
                        unassigned_data.append({
                            'ID': dest['id'],
                            'Nombre': dest['nombre'],
                            'Demanda': dest['demanda']
                        })

                    pd.DataFrame(unassigned_data).to_excel(writer, sheet_name='No_Asignados', index=False)

            return True

        except Exception as e:
            st.error(f"Error al exportar: {str(e)}")
            import traceback
            st.error(traceback.format_exc())
            return False
