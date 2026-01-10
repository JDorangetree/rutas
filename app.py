"""
Aplicación Streamlit para optimización de rutas
Sistema de ruteo para microempresas v2.0
Soporta múltiples orígenes y geocodificación automática
"""
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
import sys
import os

# Agregar directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_loader import DataLoader
from route_optimizer import RouteOptimizer
from config import STREAMLIT_CONFIG, TEMPLATE_INFO, DEFAULT_CONFIG, OPTIMIZATION_TYPES, DISTANCE_METHODS, GEOCODING_METHODS

# Configurar página
st.set_page_config(**STREAMLIT_CONFIG)

# Inicializar session state para data_loader temporalmente
# Se inicializará con la API key después de cargar el sidebar
if 'optimizer' not in st.session_state:
    st.session_state.optimizer = None

if 'solution' not in st.session_state:
    st.session_state.solution = None

# Título principal
st.title("🚚 RutaFácil")
st.markdown("### Planificador inteligente de rutas")
st.divider()

# Sidebar para configuración
with st.sidebar:
    st.header("⚙️ Configuración del Sistema")

    # Sección de Geocodificación
    st.subheader("🗺️ Geocodificación")
    metodo_geocodificacion = st.selectbox(
        "Método de geocodificación:",
        options=list(GEOCODING_METHODS.keys()),
        format_func=lambda x: GEOCODING_METHODS[x]['nombre'],
        index=0,  # Por defecto Nominatim (gratis)
        help="Selecciona el servicio para convertir direcciones en coordenadas"
    )

    # Mostrar información del método seleccionado
    st.caption(f"ℹ️ {GEOCODING_METHODS[metodo_geocodificacion]['descripcion']}")
    st.caption(f"✅ {GEOCODING_METHODS[metodo_geocodificacion]['ventajas']}")
    st.caption(f"⚠️ {GEOCODING_METHODS[metodo_geocodificacion]['desventajas']}")

    # API key si es necesario
    google_api_key_geocoding = None
    if GEOCODING_METHODS[metodo_geocodificacion]['requiere_api']:
        google_api_key_geocoding = st.text_input(
            "Google Maps API Key (Geocoding)",
            type="password",
            help="Ingresa tu API key de Google Maps para geocodificación. Incluye $200 USD gratis mensuales."
        )
        if google_api_key_geocoding:
            st.success("✓ API key para geocodificación ingresada")
        else:
            st.warning("⚠️ Requiere API key para usar Google Maps")
    else:
        st.info("🌍 Nominatim es gratuito y no requiere configuración")

    st.divider()

    # Sección de Método de Distancia
    st.subheader("📏 Cálculo de Distancias")
    metodo_distancia = st.selectbox(
        "Método de cálculo:",
        options=list(DISTANCE_METHODS.keys()),
        format_func=lambda x: DISTANCE_METHODS[x]['nombre'],
        index=0,
        help="Selecciona cómo calcular distancias entre puntos"
    )

    # Mostrar información del método seleccionado
    st.caption(f"ℹ️ {DISTANCE_METHODS[metodo_distancia]['descripcion']}")
    st.caption(f"✅ {DISTANCE_METHODS[metodo_distancia]['ventajas']}")
    st.caption(f"⚠️ {DISTANCE_METHODS[metodo_distancia]['desventajas']}")

    # API key para Google Directions si es necesario
    google_api_key_directions = None
    considerar_trafico = False
    hora_salida_rutas = None

    if DISTANCE_METHODS[metodo_distancia]['requiere_api']:
        google_api_key_directions = st.text_input(
            "Google Maps API Key (Directions)",
            type="password",
            help="Ingresa tu API key de Google Maps para calcular distancias reales por carretera."
        )
        if google_api_key_directions:
            st.success("✓ API key para Directions ingresada")

            # Opciones de tráfico
            with st.expander("🚦 Opciones de Tráfico (Avanzado)"):
                considerar_trafico = st.checkbox(
                    "Considerar condiciones de tráfico",
                    value=False,
                    help="Incluye tráfico en el cálculo de tiempos. Esto duplica el costo de las solicitudes."
                )

                if considerar_trafico:
                    st.info("💡 Al activar tráfico, se usarán tiempos reales de conducción en lugar de promedios")

                    tipo_trafico = st.radio(
                        "Tipo de análisis de tráfico:",
                        options=['actual', 'predictivo'],
                        format_func=lambda x: "Tráfico actual (ahora mismo)" if x == 'actual' else "Tráfico predictivo (hora específica)",
                        help="Actual: condiciones de tráfico en este momento. Predictivo: estima tráfico para una hora futura."
                    )

                    if tipo_trafico == 'predictivo':
                        col1, col2 = st.columns(2)
                        with col1:
                            hora_salida = st.time_input(
                                "Hora de inicio de rutas",
                                value=None,
                                help="Hora aproximada cuando los vehículos saldrán. Google estimará el tráfico para esa hora."
                            )
                        with col2:
                            modelo_trafico = st.selectbox(
                                "Modelo de tráfico:",
                                options=['best_guess', 'pessimistic', 'optimistic'],
                                format_func=lambda x: {
                                    'best_guess': 'Mejor estimación',
                                    'pessimistic': 'Pesimista (peor caso)',
                                    'optimistic': 'Optimista (mejor caso)'
                                }[x],
                                help="Cómo estimar el tráfico futuro"
                            )

                        if hora_salida:
                            hora_salida_rutas = hora_salida
                            st.session_state.modelo_trafico = modelo_trafico
                    else:
                        st.session_state.modelo_trafico = 'best_guess'

            # Calcular costo estimado
            num_locations_estimate = 20  # Estimado por defecto
            num_requests = num_locations_estimate ** 2
            costo_base = num_requests * DISTANCE_METHODS['google_directions']['costo_por_request']
            costo_con_trafico = costo_base * 2 if considerar_trafico else costo_base

            if considerar_trafico:
                st.warning(f"💰 Costo estimado para ~{num_locations_estimate} ubicaciones: ${costo_con_trafico:.2f} USD (con tráfico)")
            else:
                st.info(f"💰 Costo estimado para ~{num_locations_estimate} ubicaciones: ${costo_base:.2f} USD")
        else:
            st.warning("⚠️ Requiere API key para usar distancias reales")

    st.divider()
    st.info("💡 Las coordenadas se geocodifican automáticamente si no están presentes")

# Inicializar DataLoader con la API key del usuario según el método seleccionado
# O reinicializar si cambió la API key o el método
current_geocoding_state = f"{metodo_geocodificacion}_{google_api_key_geocoding}"
if 'data_loader' not in st.session_state or ('current_geocoding_state' in st.session_state and st.session_state.current_geocoding_state != current_geocoding_state):
    # Solo pasar API key si el método es Google Maps
    api_key_to_use = google_api_key_geocoding if metodo_geocodificacion == 'google_maps' else None
    st.session_state.data_loader = DataLoader(google_api_key=api_key_to_use)
    st.session_state.current_geocoding_state = current_geocoding_state

with st.sidebar:
    # Sección de carga de archivos
    st.header("📤 Carga de Archivos")

    # Contador de archivos cargados
    archivos_cargados = 0
    archivos_requeridos = 3

    st.subheader("1. Orígenes" + (" ✅" if 'origenes' in st.session_state and st.session_state.origenes else ""))
    st.caption(TEMPLATE_INFO['origenes']['descripcion'])
    st.caption(f"🔍 {TEMPLATE_INFO['origenes']['nota']}")

    # Botón de descarga de plantilla
    try:
        with open("templates/plantilla_origenes.xlsx", "rb") as file:
            st.download_button(
                label="📥 Descargar Plantilla de Orígenes",
                data=file,
                file_name="plantilla_origenes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Descarga la plantilla con ejemplos y columnas requeridas"
            )
    except FileNotFoundError:
        st.warning("⚠️ Plantilla no encontrada")

    file_origenes = st.file_uploader(
        "Archivo de Orígenes (Excel)",
        type=['xlsx', 'xls'],
        key='origenes',
        help="Centros de distribución, bodegas o puntos de despacho"
    )
    if file_origenes:
        archivos_cargados += 1

    st.subheader("2. Destinos/Clientes" + (" ✅" if 'destinos' in st.session_state and st.session_state.destinos else ""))
    st.caption(TEMPLATE_INFO['destinos']['descripcion'])
    st.caption(f"🔍 {TEMPLATE_INFO['destinos']['nota']}")

    # Botón de descarga de plantilla
    try:
        with open("templates/plantilla_destinos.xlsx", "rb") as file:
            st.download_button(
                label="📥 Descargar Plantilla de Destinos",
                data=file,
                file_name="plantilla_destinos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Descarga la plantilla con ejemplos y columnas requeridas"
            )
    except FileNotFoundError:
        st.warning("⚠️ Plantilla no encontrada")

    file_destinos = st.file_uploader(
        "Archivo de Destinos (Excel)",
        type=['xlsx', 'xls'],
        key='destinos',
        help="Clientes, puntos de entrega o pedidos"
    )
    if file_destinos:
        archivos_cargados += 1

    st.subheader("3. Flota/Vehículos" + (" ✅" if 'flota' in st.session_state and st.session_state.flota else ""))
    st.caption(TEMPLATE_INFO['flota']['descripcion'])
    st.caption(f"🔍 {TEMPLATE_INFO['flota']['nota']}")

    # Botón de descarga de plantilla
    try:
        with open("templates/plantilla_vehiculos.xlsx", "rb") as file:
            st.download_button(
                label="📥 Descargar Plantilla de Vehículos",
                data=file,
                file_name="plantilla_vehiculos.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Descarga la plantilla con ejemplos y columnas requeridas"
            )
    except FileNotFoundError:
        st.warning("⚠️ Plantilla no encontrada")

    file_flota = st.file_uploader(
        "Archivo de Flota (Excel)",
        type=['xlsx', 'xls'],
        key='flota',
        help="Vehículos disponibles con su origen asignado"
    )
    if file_flota:
        archivos_cargados += 1

    st.subheader("4. Configuración (Opcional)" + (" ✅" if 'config' in st.session_state and st.session_state.config else ""))
    st.caption(TEMPLATE_INFO['config']['descripcion'])

    # Botón de descarga de plantilla
    try:
        with open("templates/plantilla_configuracion.xlsx", "rb") as file:
            st.download_button(
                label="📥 Descargar Plantilla de Configuración",
                data=file,
                file_name="plantilla_configuracion.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Descarga la plantilla con parámetros opcionales"
            )
    except FileNotFoundError:
        st.warning("⚠️ Plantilla no encontrada")

    file_config = st.file_uploader(
        "Archivo de Configuración (Excel)",
        type=['xlsx', 'xls'],
        key='config',
        help="Parámetros técnicos opcionales. NOTA: El tipo de optimización se configura desde 'Objetivo de Optimización' más abajo, no desde este archivo."
    )

    st.caption("💡 Este archivo solo configura parámetros técnicos (unidades, velocidades, etc.). El tipo de optimización se elige más abajo en '⚙️ Parámetros'")

    # Mostrar progreso
    st.divider()
    if archivos_cargados == archivos_requeridos:
        st.success(f"✅ Archivos cargados: {archivos_cargados}/{archivos_requeridos} - ¡Listo para optimizar!")
    elif archivos_cargados > 0:
        st.info(f"📂 Archivos cargados: {archivos_cargados}/{archivos_requeridos} - Falta(n) {archivos_requeridos - archivos_cargados}")
    else:
        st.warning(f"⚠️ Ningún archivo cargado - Por favor carga los {archivos_requeridos} archivos requeridos")

    st.divider()

    # Parámetros de optimización
    st.header("⚙️ Parámetros")

    # Selector de tipo de optimización
    st.subheader("Objetivo de Optimización")
    tipo_optimizacion = st.selectbox(
        "Optimizar por:",
        options=list(OPTIMIZATION_TYPES.keys()),
        format_func=lambda x: f"{OPTIMIZATION_TYPES[x]['nombre']} - {OPTIMIZATION_TYPES[x]['objetivo']}",
        index=0,
        key='tipo_optimizacion',
        help="Selecciona el criterio principal para optimizar las rutas"
    )

    # Mostrar descripción del tipo seleccionado
    st.caption(f"ℹ️ {OPTIMIZATION_TYPES[tipo_optimizacion]['descripcion']}")

    st.divider()

    st.subheader("⏱️ Tiempo de Optimización")

    st.markdown("""
    **¿Qué significa el tiempo límite?**

    El tiempo límite define cuántos segundos el sistema buscará la mejor solución posible.
    Un tiempo mayor permite explorar más opciones y generalmente encuentra mejores rutas.

    **¿Cómo elegir el tiempo adecuado?**
    """)

    tiempo_limite = st.slider(
        "Tiempo límite de búsqueda",
        min_value=10,
        max_value=300,
        value=180,
        help="El sistema busca continuamente mejores soluciones durante este tiempo. Más tiempo = mayor probabilidad de encontrar la mejor ruta, pero no siempre es necesario."
    )

    # Convertir a minutos para mostrar
    minutos = tiempo_limite / 60

    # Mostrar recomendación visual detallada
    if tiempo_limite < 60:
        st.info(f"""
        ⚡ **{tiempo_limite} segundos (~{minutos:.1f} min) - Prueba Rápida**

        **Recomendado para:**
        - Validar que los archivos están correctos
        - Menos de 10 destinos
        - Pruebas iniciales del sistema

        **Resultado esperado:** Solución aceptable pero probablemente no óptima
        """)
    elif tiempo_limite < 120:
        st.info(f"""
        ⚙️ **{tiempo_limite} segundos (~{minutos:.1f} min) - Estándar**

        **Recomendado para:**
        - Problemas pequeños (10-20 destinos)
        - Entregas locales en una sola ciudad
        - Cuando necesita respuesta rápida

        **Resultado esperado:** Buena solución, cerca del óptimo
        """)
    elif tiempo_limite < 240:
        st.success(f"""
        ✅ **{tiempo_limite} segundos (~{minutos:.1f} min) - Recomendado (Valor predeterminado)**

        **Recomendado para:**
        - Problemas medianos (20-50 destinos)
        - Múltiples orígenes y vehículos
        - Uso en producción diaria
        - Balance ideal entre tiempo y calidad

        **Resultado esperado:** Excelente solución, muy cerca del óptimo
        """)
    else:
        st.warning(f"""
        🔬 **{tiempo_limite} segundos (~{minutos:.1f} min) - Exhaustivo**

        **Recomendado para:**
        - Problemas grandes (50+ destinos)
        - Planificación estratégica importante
        - Cuando cada kilómetro ahorrado es crítico
        - Optimizaciones complejas (minimizar vehículos, balance de carga)

        **Resultado esperado:** La mejor solución posible

        ⚠️ **Nota:** El tiempo de espera será mayor, asegúrese de que lo necesita.
        """)

    st.caption("💡 **Consejo:** El sistema puede terminar antes si encuentra la solución óptima. Empiece con 180 segundos (3 min) y ajuste según necesite.")

# Tabs principales
tab1, tab2, tab3, tab4 = st.tabs(["📊 Datos", "🗺️ Visualización", "🚀 Optimización", "📈 Resultados"])

# TAB 1: Carga y visualización de datos
with tab1:
    st.header("Datos Cargados")

    # Cargar orígenes
    if file_origenes:
        with st.spinner("Cargando orígenes..."):
            df_origenes = st.session_state.data_loader.load_origenes(file_origenes)
            if df_origenes is not None:
                st.success(f"✅ Orígenes: {len(df_origenes)} puntos cargados")
                with st.expander("Ver datos de orígenes"):
                    st.dataframe(df_origenes, use_container_width=True)

    # Cargar destinos
    if file_destinos:
        with st.spinner("Cargando destinos..."):
            df_destinos = st.session_state.data_loader.load_destinos(file_destinos)
            if df_destinos is not None:
                st.success(f"✅ Destinos: {len(df_destinos)} puntos cargados")
                with st.expander("Ver datos de destinos"):
                    st.dataframe(df_destinos, use_container_width=True)

    # Cargar flota
    if file_flota:
        with st.spinner("Cargando flota..."):
            df_flota = st.session_state.data_loader.load_flota(file_flota)
            if df_flota is not None:
                st.success(f"✅ Flota: {len(df_flota)} vehículos cargados")
                with st.expander("Ver datos de flota"):
                    st.dataframe(df_flota, use_container_width=True)

    # Cargar configuración
    if file_config:
        config = st.session_state.data_loader.load_config(file_config)
        if config is not None:
            st.info("✅ Configuración personalizada cargada")
            with st.expander("Ver configuración"):
                config_df = pd.DataFrame(list(config.items()), columns=['Parámetro', 'Valor'])
                st.dataframe(config_df, use_container_width=True)

    # Resumen
    is_valid, message = st.session_state.data_loader.validate_all_loaded()
    if is_valid:
        st.divider()
        st.subheader("📋 Resumen de Datos")
        summary = st.session_state.data_loader.get_summary()

        # Métricas principales
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Orígenes", summary['origenes']['cantidad'])
            if summary['origenes']['ciudades']:
                st.caption(f"Ciudades: {', '.join(summary['origenes']['ciudades'])}")

        with col2:
            st.metric("Destinos", summary['destinos']['cantidad'])
            st.metric("Demanda Total", summary['destinos']['demanda_total'])
            if summary['destinos']['ciudades']:
                st.caption(f"Ciudades: {', '.join(summary['destinos']['ciudades'])}")

        with col3:
            st.metric("Vehículos", summary['flota']['cantidad'])
            st.metric("Capacidad Total", summary['flota']['capacidad_total'])

        # Distribución de vehículos por origen
        st.subheader("Distribución de Vehículos por Origen")
        if 'por_origen' in summary['flota']:
            dist_df = pd.DataFrame(list(summary['flota']['por_origen'].items()),
                                   columns=['Origen', 'Cantidad de Vehículos'])
            st.dataframe(dist_df, use_container_width=True)

        # Validar capacidad
        st.divider()
        if summary['destinos']['demanda_total'] > summary['flota']['capacidad_total']:
            st.error(f"⚠️ La demanda total ({summary['destinos']['demanda_total']}) supera la capacidad de la flota ({summary['flota']['capacidad_total']})")
        else:
            capacity_usage = (summary['destinos']['demanda_total'] / summary['flota']['capacidad_total']) * 100
            st.success(f"✅ Capacidad suficiente (Uso estimado: {capacity_usage:.1f}%)")

# TAB 2: Visualización en mapa
with tab2:
    st.header("Visualización de Puntos")

    if st.session_state.data_loader.validate_all_loaded()[0]:
        # Crear mapa centrado en el promedio de coordenadas
        all_lats = list(st.session_state.data_loader.origenes['latitud']) + \
                   list(st.session_state.data_loader.destinos['latitud'])
        all_lons = list(st.session_state.data_loader.origenes['longitud']) + \
                   list(st.session_state.data_loader.destinos['longitud'])

        center_lat = sum(all_lats) / len(all_lats)
        center_lon = sum(all_lons) / len(all_lons)

        m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

        # Agregar orígenes
        for _, row in st.session_state.data_loader.origenes.iterrows():
            # Contar vehículos en este origen
            num_vehiculos = len(st.session_state.data_loader.flota[
                st.session_state.data_loader.flota['origen_id'] == row['origen_id']
            ])

            folium.Marker(
                location=[row['latitud'], row['longitud']],
                popup=f"<b>{row['nombre_origen']}</b><br>"
                      f"Origen: {row['origen_id']}<br>"
                      f"Ciudad: {row['ciudad']}<br>"
                      f"Vehículos: {num_vehiculos}",
                tooltip=f"{row['nombre_origen']} ({num_vehiculos} vehículos)",
                icon=folium.Icon(color='green', icon='home', prefix='fa')
            ).add_to(m)

        # Agregar destinos
        for _, row in st.session_state.data_loader.destinos.iterrows():
            folium.Marker(
                location=[row['latitud'], row['longitud']],
                popup=f"<b>{row['nombre_cliente']}</b><br>"
                      f"ID: {row['destino_id']}<br>"
                      f"Ciudad: {row['ciudad']}<br>"
                      f"Demanda: {row['demanda']}",
                tooltip=f"{row['nombre_cliente']} (Demanda: {row['demanda']})",
                icon=folium.Icon(color='blue', icon='shopping-cart', prefix='fa')
            ).add_to(m)

        st_folium(m, width=1200, height=600)

        # Leyenda
        st.markdown("""
        **Leyenda:**
        - 🏠 Verde: Orígenes/Depósitos
        - 🛒 Azul: Destinos de entrega
        """)

    else:
        st.warning("Por favor cargue todos los archivos para visualizar el mapa")

# TAB 3: Optimización
with tab3:
    st.header("Optimización de Rutas")

    if st.session_state.data_loader.validate_all_loaded()[0]:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Configuración")
            st.write(f"⏱️ Tiempo límite: {tiempo_limite}s")
            # Mostrar objetivo seleccionado dinámicamente
            tipo_opt_seleccionado = st.session_state.get('tipo_optimizacion', 'balanced')
            objetivo_texto = OPTIMIZATION_TYPES[tipo_opt_seleccionado]['objetivo']
            st.write(f"🎯 Objetivo: {objetivo_texto}")
            st.write(f"🚚 Múltiples orígenes: Sí")

            # Mostrar resumen de capacidades
            summary = st.session_state.data_loader.get_summary()
            st.write(f"📊 Demanda: {summary['destinos']['demanda_total']}")
            st.write(f"📦 Capacidad: {summary['flota']['capacidad_total']}")

            if st.button("🚀 Iniciar Optimización", type="primary", use_container_width=True):
                with st.spinner("Optimizando rutas... Esto puede tomar unos momentos"):
                    # Crear optimizador
                    config = st.session_state.data_loader.config or DEFAULT_CONFIG
                    optimizer = RouteOptimizer(
                        st.session_state.data_loader.origenes,
                        st.session_state.data_loader.destinos,
                        st.session_state.data_loader.flota,
                        config,
                        optimization_type=st.session_state.get('tipo_optimizacion', 'balanced'),
                        distance_method=metodo_distancia,
                        google_api_key_directions=google_api_key_directions,
                        considerar_trafico=considerar_trafico,
                        hora_salida_rutas=hora_salida_rutas
                    )

                    # Resolver
                    solution = optimizer.solve(time_limit_seconds=tiempo_limite)

                    if solution:
                        st.session_state.solution = solution
                        st.session_state.optimizer = optimizer
                        st.success("✅ Optimización completada")
                        st.rerun()

        with col2:
            if st.session_state.solution:
                st.subheader("📊 Resultados de Optimización")

                # Métricas principales
                metric_col1, metric_col2, metric_col3 = st.columns(3)

                with metric_col1:
                    st.metric(
                        "Distancia Total",
                        f"{st.session_state.solution['total_distance']:.2f} km"
                    )

                with metric_col2:
                    num_routes = len([r for r in st.session_state.solution['routes'] if len(r['route']) > 2])
                    st.metric("Vehículos Usados", num_routes)

                with metric_col3:
                    destinos_asignados = len(st.session_state.data_loader.destinos) - len(st.session_state.solution.get('unassigned', []))
                    st.metric("Destinos Atendidos", destinos_asignados)

                # Advertencia si hay destinos no asignados
                if st.session_state.solution.get('unassigned'):
                    st.warning(f"⚠️ {len(st.session_state.solution['unassigned'])} destinos NO fueron asignados. "
                             "Revisa la capacidad de la flota o aumenta el tiempo límite.")

                # Detalle por vehículo
                st.subheader("Detalle de Rutas")
                for route_info in st.session_state.solution['routes']:
                    if len(route_info['route']) > 2:
                        with st.expander(
                            f"🚚 {route_info['vehicle_id']} - {route_info['vehicle_type']} "
                            f"({route_info['distance_km']:.2f} km)"
                        ):
                            # Información del vehículo y origen
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.write(f"**Origen:** {route_info['origen_nombre']} ({route_info['origen_id']})")
                                st.write(f"**Carga:** {route_info['load']} / {route_info['capacity']}")
                            with col_b:
                                st.write(f"**Utilización:** {route_info['utilization']:.1f}%")
                                st.write(f"**Paradas:** {len(route_info['route']) - 2}")

                            # Tabla de ruta
                            route_data = []
                            for i, loc in enumerate(route_info['route']):
                                route_data.append({
                                    'Orden': i + 1,
                                    'Tipo': loc['type'].capitalize(),
                                    'Nombre': loc['nombre'],
                                    'Ciudad': loc['ciudad'],
                                    'Demanda': loc['demanda']
                                })
                            st.dataframe(pd.DataFrame(route_data), use_container_width=True, hide_index=True)

    else:
        st.warning("Por favor cargue todos los archivos antes de optimizar")

# TAB 4: Resultados y exportación
with tab4:
    st.header("Resultados y Exportación")

    if st.session_state.solution:
        # Mapa con rutas
        st.subheader("🗺️ Mapa de Rutas Optimizadas")

        all_lats = list(st.session_state.data_loader.origenes['latitud']) + \
                   list(st.session_state.data_loader.destinos['latitud'])
        all_lons = list(st.session_state.data_loader.origenes['longitud']) + \
                   list(st.session_state.data_loader.destinos['longitud'])

        center_lat = sum(all_lats) / len(all_lats)
        center_lon = sum(all_lons) / len(all_lons)

        m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

        # Colores para rutas
        colors = DEFAULT_CONFIG['color_ruta']

        # Dibujar rutas
        for i, route_info in enumerate(st.session_state.solution['routes']):
            if len(route_info['route']) > 2:
                color = colors[i % len(colors)]

                # Línea de ruta
                route_coords = [[loc['latitud'], loc['longitud']] for loc in route_info['route']]
                folium.PolyLine(
                    route_coords,
                    color=color,
                    weight=3,
                    opacity=0.7,
                    popup=f"{route_info['vehicle_id']}<br>{route_info['distance_km']:.2f} km"
                ).add_to(m)

                # Marcadores numerados
                for j, loc in enumerate(route_info['route']):
                    if loc['type'] == 'origen':
                        icon_color = 'green'
                        icon_name = 'home'
                        icon_prefix = 'fa'
                    else:
                        icon_color = color
                        icon_name = 'info-sign'
                        icon_prefix = 'glyphicon'

                    folium.Marker(
                        location=[loc['latitud'], loc['longitud']],
                        popup=f"<b>{loc['nombre']}</b><br>"
                              f"Vehículo: {route_info['vehicle_id']}<br>"
                              f"Orden: {j + 1}<br>"
                              f"Ciudad: {loc['ciudad']}<br>"
                              f"Demanda: {loc['demanda']}",
                        tooltip=f"{j + 1}. {loc['nombre']}",
                        icon=folium.Icon(color=icon_color, icon=icon_name, prefix=icon_prefix)
                    ).add_to(m)

        st_folium(m, width=1200, height=600)

        # Exportar resultados
        st.divider()
        st.subheader("💾 Exportar Resultados")

        col1, col2 = st.columns(2)

        with col1:
            filename = f"rutas_optimizadas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            filepath = os.path.join('output', filename)

            if st.button("📥 Exportar a Excel", use_container_width=True):
                with st.spinner("Exportando..."):
                    if st.session_state.optimizer.export_to_excel(filepath):
                        st.success(f"✅ Archivo exportado: {filepath}")

                        # Ofrecer descarga
                        try:
                            with open(filepath, 'rb') as f:
                                st.download_button(
                                    label="⬇️ Descargar Archivo",
                                    data=f,
                                    file_name=filename,
                                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Error al preparar descarga: {str(e)}")

        # Resumen final
        st.divider()
        st.subheader("📊 Resumen Final")

        summary_data = {
            'Métrica': [
                'Distancia Total',
                'Vehículos Utilizados',
                'Destinos Asignados',
                'Destinos No Asignados',
                'Utilización Promedio'
            ],
            'Valor': [
                f"{st.session_state.solution['total_distance']:.2f} km",
                len([r for r in st.session_state.solution['routes'] if len(r['route']) > 2]),
                len(st.session_state.data_loader.destinos) - len(st.session_state.solution.get('unassigned', [])),
                len(st.session_state.solution.get('unassigned', [])),
                f"{sum([r['utilization'] for r in st.session_state.solution['routes']]) / len(st.session_state.solution['routes']):.1f}%"
            ]
        }
        st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

    else:
        st.info("Ejecute la optimización primero para ver los resultados aquí")

# Footer
st.divider()
col_footer1, col_footer2 = st.columns([3, 1])
with col_footer1:
    st.caption("RutaFácil - Planificador inteligente de rutas con múltiples orígenes y geocodificación automática")
with col_footer2:
    if st.button("🔄 Reiniciar Sesión"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
