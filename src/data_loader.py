"""
Módulo para cargar y validar archivos maestros de Excel
Versión 2.1 - Soporta geocodificación con Google Maps y fallback a Nominatim
"""
import pandas as pd
import streamlit as st
from typing import Dict, Tuple, Optional
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Intentar importar googlemaps
try:
    import googlemaps
    GOOGLEMAPS_AVAILABLE = True
except ImportError:
    GOOGLEMAPS_AVAILABLE = False


class DataLoader:
    """Clase para cargar y validar archivos Excel de entrada"""

    def __init__(self, google_api_key: Optional[str] = None):
        """
        Inicializa el DataLoader con configuración de geocodificación

        Args:
            google_api_key: API key de Google Maps (opcional). Si no se proporciona,
                          intenta cargar desde variable de entorno GOOGLE_MAPS_API_KEY
        """
        self.origenes = None
        self.destinos = None
        self.flota = None
        self.config = None

        # Configurar geocodificadores
        # Prioridad: 1) API key pasada como parámetro, 2) Variable de entorno
        self.google_api_key = google_api_key or os.getenv('GOOGLE_MAPS_API_KEY')
        self.use_google_maps = GOOGLEMAPS_AVAILABLE and self.google_api_key and self.google_api_key != ''

        if self.use_google_maps:
            try:
                self.gmaps_client = googlemaps.Client(key=self.google_api_key)
                # Validar que la API key funcione haciendo una prueba simple
                # Solo si fue proporcionada explícitamente por el usuario
                if google_api_key and google_api_key != '':
                    try:
                        # Test básico: geocodificar una dirección conocida
                        test = self.gmaps_client.geocode("1600 Amphitheatre Parkway, Mountain View, CA")
                        if not test:
                            raise Exception("La API key no permite geocodificación")
                    except Exception as test_error:
                        # Si falla el test, mostrar error específico
                        error_msg = str(test_error)
                        if "REQUEST_DENIED" in error_msg or "Invalid" in error_msg:
                            st.error("❌ API key de Google Maps inválida o sin permisos")
                            st.info("Verifica que:\n- La API key sea correcta\n- La Geocoding API esté habilitada\n- La facturación esté configurada")
                        else:
                            st.warning(f"⚠️ Error al validar Google Maps: {error_msg}")

                        st.info("🌍 Usando Nominatim (OpenStreetMap) como alternativa")
                        self.use_google_maps = False
                        self.geocoder_nominatim = Nominatim(user_agent="mvp_ruteo_app", timeout=10)
            except Exception as e:
                # Error al crear el cliente
                if google_api_key and google_api_key != '':
                    st.error(f"❌ No se pudo inicializar Google Maps: {str(e)}")
                    st.info("🌍 Usando Nominatim (OpenStreetMap) como alternativa")
                self.use_google_maps = False
                self.geocoder_nominatim = Nominatim(user_agent="mvp_ruteo_app", timeout=10)
        else:
            # Usar Nominatim como alternativa
            self.geocoder_nominatim = Nominatim(user_agent="mvp_ruteo_app", timeout=10)

    def geocode_address_google(self, direccion: str, ciudad: str, pais: str) -> Tuple[Optional[float], Optional[float]]:
        """
        Geocodifica una dirección usando Google Maps API
        Retorna (latitud, longitud) o (None, None) si falla
        """
        full_address = f"{direccion}, {ciudad}, {pais}"

        try:
            result = self.gmaps_client.geocode(full_address, region=pais.lower()[:2])

            if result and len(result) > 0:
                location = result[0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                return None, None

        except Exception as e:
            st.warning(f"Error en Google Maps para '{full_address}': {str(e)}")
            return None, None

    def geocode_address_nominatim(self, direccion: str, ciudad: str, pais: str, retries: int = 3) -> Tuple[Optional[float], Optional[float]]:
        """
        Geocodifica una dirección usando Nominatim (OpenStreetMap)
        Retorna (latitud, longitud) o (None, None) si falla
        """
        full_address = f"{direccion}, {ciudad}, {pais}"

        for attempt in range(retries):
            try:
                location = self.geocoder_nominatim.geocode(full_address)
                if location:
                    return location.latitude, location.longitude
                else:
                    return None, None
            except (GeocoderTimedOut, GeocoderServiceError) as e:
                if attempt < retries - 1:
                    time.sleep(1)  # Esperar antes de reintentar
                    continue
                else:
                    st.warning(f"No se pudo geocodificar: {full_address}")
                    return None, None

        return None, None

    def geocode_address(self, direccion: str, ciudad: str, pais: str, retries: int = 3) -> Tuple[Optional[float], Optional[float]]:
        """
        Geocodifica una dirección usando el proveedor configurado
        Intenta Google Maps primero, luego Nominatim como fallback
        Retorna (latitud, longitud) o (None, None) si falla
        """
        # Intentar con Google Maps si está disponible
        if self.use_google_maps:
            lat, lon = self.geocode_address_google(direccion, ciudad, pais)
            if lat is not None and lon is not None:
                return lat, lon
            else:
                # Fallback a Nominatim
                st.caption(f"🔄 Reintentando con Nominatim: {direccion}")
                return self.geocode_address_nominatim(direccion, ciudad, pais, retries)
        else:
            # Usar Nominatim directamente
            return self.geocode_address_nominatim(direccion, ciudad, pais, retries)

    def load_origenes(self, file) -> pd.DataFrame:
        """
        Carga archivo de orígenes (centros de distribución, bodegas, tiendas)
        Columnas requeridas: origen_id, nombre_origen, direccion, ciudad, pais
        Columnas opcionales: latitud, longitud, hora_apertura, hora_cierre
        """
        try:
            df = pd.read_excel(file)
            required_columns = ['origen_id', 'nombre_origen', 'direccion', 'ciudad', 'pais']

            # Validar columnas requeridas
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Faltan columnas requeridas: {missing_cols}")

            # Agregar columnas opcionales si no existen
            if 'latitud' not in df.columns:
                df['latitud'] = None
            if 'longitud' not in df.columns:
                df['longitud'] = None
            if 'hora_apertura' not in df.columns:
                df['hora_apertura'] = '00:00'
            if 'hora_cierre' not in df.columns:
                df['hora_cierre'] = '23:59'

            # Geocodificar direcciones sin coordenadas
            needs_geocoding = df['latitud'].isnull() | df['longitud'].isnull()

            if needs_geocoding.any():
                st.info(f"Geocodificando {needs_geocoding.sum()} orígenes sin coordenadas...")
                progress_bar = st.progress(0)

                for idx, row in df[needs_geocoding].iterrows():
                    lat, lon = self.geocode_address(
                        row['direccion'],
                        row['ciudad'],
                        row['pais']
                    )

                    if lat is not None and lon is not None:
                        df.at[idx, 'latitud'] = lat
                        df.at[idx, 'longitud'] = lon
                    else:
                        raise ValueError(
                            f"No se pudo geocodificar el origen: {row['nombre_origen']} "
                            f"en {row['direccion']}, {row['ciudad']}"
                        )

                    progress_bar.progress((idx + 1) / needs_geocoding.sum())

                progress_bar.empty()
                st.success("Geocodificación completada")

            # Validar coordenadas
            if df['latitud'].isnull().any() or df['longitud'].isnull().any():
                raise ValueError("Algunas coordenadas no pudieron ser obtenidas")

            if not (-90 <= df['latitud'].min() <= 90 and -90 <= df['latitud'].max() <= 90):
                raise ValueError("Latitudes deben estar entre -90 y 90")

            if not (-180 <= df['longitud'].min() <= 180 and -180 <= df['longitud'].max() <= 180):
                raise ValueError("Longitudes deben estar entre -180 y 180")

            self.origenes = df
            return df

        except Exception as e:
            st.error(f"Error al cargar archivo de orígenes: {str(e)}")
            return None

    def load_destinos(self, file) -> pd.DataFrame:
        """
        Carga archivo de destinos/clientes (puntos de entrega, pedidos)
        Columnas requeridas: destino_id, nombre_cliente, direccion, ciudad, pais, demanda
        Columnas opcionales: latitud, longitud, hora_inicio, hora_fin, prioridad
        """
        try:
            df = pd.read_excel(file)
            required_columns = ['destino_id', 'nombre_cliente', 'direccion', 'ciudad', 'pais', 'demanda']

            # Validar columnas requeridas
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Faltan columnas requeridas: {missing_cols}")

            # Agregar columnas opcionales si no existen
            if 'latitud' not in df.columns:
                df['latitud'] = None
            if 'longitud' not in df.columns:
                df['longitud'] = None
            if 'hora_inicio' not in df.columns:
                df['hora_inicio'] = '00:00'
            if 'hora_fin' not in df.columns:
                df['hora_fin'] = '23:59'
            if 'prioridad' not in df.columns:
                df['prioridad'] = 2  # Prioridad media por defecto

            # Geocodificar direcciones sin coordenadas
            needs_geocoding = df['latitud'].isnull() | df['longitud'].isnull()

            if needs_geocoding.any():
                st.info(f"Geocodificando {needs_geocoding.sum()} destinos sin coordenadas...")
                progress_bar = st.progress(0)
                total = needs_geocoding.sum()

                for i, (idx, row) in enumerate(df[needs_geocoding].iterrows()):
                    lat, lon = self.geocode_address(
                        row['direccion'],
                        row['ciudad'],
                        row['pais']
                    )

                    if lat is not None and lon is not None:
                        df.at[idx, 'latitud'] = lat
                        df.at[idx, 'longitud'] = lon
                    else:
                        st.warning(
                            f"No se pudo geocodificar: {row['nombre_cliente']} "
                            f"en {row['direccion']}, {row['ciudad']}. Se omitirá."
                        )

                    progress_bar.progress((i + 1) / total)

                progress_bar.empty()
                st.success("Geocodificación completada")

            # Eliminar filas sin coordenadas
            df = df.dropna(subset=['latitud', 'longitud'])

            if len(df) == 0:
                raise ValueError("No hay destinos válidos con coordenadas")

            # Validar datos
            if df['demanda'].isnull().any():
                raise ValueError("La demanda no puede estar vacía")

            if (df['demanda'] <= 0).any():
                raise ValueError("La demanda debe ser mayor a 0")

            self.destinos = df
            return df

        except Exception as e:
            st.error(f"Error al cargar archivo de destinos: {str(e)}")
            return None

    def load_flota(self, file) -> pd.DataFrame:
        """
        Carga archivo de flota/capacidades (vehículos disponibles)
        Columnas requeridas: vehiculo_id, capacidad, origen_id
        Columnas opcionales: tipo_vehiculo, costo_km, hora_inicio, hora_fin
        """
        try:
            df = pd.read_excel(file)
            required_columns = ['vehiculo_id', 'capacidad', 'origen_id']

            # Validar columnas requeridas
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Faltan columnas requeridas: {missing_cols}")

            # Agregar columnas opcionales si no existen
            if 'tipo_vehiculo' not in df.columns:
                df['tipo_vehiculo'] = 'Vehiculo'
            if 'costo_km' not in df.columns:
                df['costo_km'] = 1.0
            if 'hora_inicio' not in df.columns:
                df['hora_inicio'] = '00:00'
            if 'hora_fin' not in df.columns:
                df['hora_fin'] = '23:59'

            # Validar datos
            if df['capacidad'].isnull().any():
                raise ValueError("La capacidad no puede estar vacía")

            if (df['capacidad'] <= 0).any():
                raise ValueError("La capacidad debe ser mayor a 0")

            self.flota = df
            return df

        except Exception as e:
            st.error(f"Error al cargar archivo de flota: {str(e)}")
            return None

    def load_config(self, file) -> Dict:
        """
        Carga archivo de configuración
        Formato: columnas (parametro, valor, descripcion)
        """
        try:
            df = pd.read_excel(file)

            if 'parametro' not in df.columns or 'valor' not in df.columns:
                raise ValueError("El archivo debe tener columnas 'parametro' y 'valor'")

            # Convertir a diccionario
            config_dict = dict(zip(df['parametro'], df['valor']))

            self.config = config_dict
            return config_dict

        except Exception as e:
            st.error(f"Error al cargar archivo de configuración: {str(e)}")
            return None

    def validate_all_loaded(self) -> Tuple[bool, str]:
        """Valida que todos los archivos necesarios estén cargados"""
        if self.origenes is None:
            return False, "Falta cargar archivo de orígenes"

        if self.destinos is None:
            return False, "Falta cargar archivo de destinos"

        if self.flota is None:
            return False, "Falta cargar archivo de flota"

        # Validar que los origen_id de flota existan en orígenes
        if not all(self.flota['origen_id'].isin(self.origenes['origen_id'])):
            return False, "Algunos vehiculos tienen origen_id que no existe en orígenes"

        return True, "Todos los archivos están cargados correctamente"

    def get_summary(self) -> Dict:
        """Retorna un resumen de los datos cargados"""
        summary = {}

        if self.origenes is not None:
            summary['origenes'] = {
                'cantidad': len(self.origenes),
                'nombres': self.origenes['nombre_origen'].tolist(),
                'ciudades': self.origenes['ciudad'].unique().tolist()
            }

        if self.destinos is not None:
            summary['destinos'] = {
                'cantidad': len(self.destinos),
                'demanda_total': self.destinos['demanda'].sum(),
                'ciudades': self.destinos['ciudad'].unique().tolist(),
                'prioridades': self.destinos['prioridad'].value_counts().to_dict()
            }

        if self.flota is not None:
            summary['flota'] = {
                'cantidad': len(self.flota),
                'capacidad_total': self.flota['capacidad'].sum(),
                'tipos': self.flota['tipo_vehiculo'].unique().tolist(),
                'por_origen': self.flota.groupby('origen_id').size().to_dict()
            }

        if self.config is not None:
            summary['config'] = self.config

        return summary
