"""
Módulo para validación y estandarización de direcciones
Mejora la precisión de la geocodificación mediante normalización de formatos
"""
import re
from typing import Tuple, Optional
import pandas as pd


# Diccionario de abreviaciones de vías en Colombia
VIA_TYPES = {
    # Abreviaciones comunes -> Tipo completo
    'cl': 'Calle',
    'cll': 'Calle',
    'calle': 'Calle',
    'cr': 'Carrera',
    'cra': 'Carrera',
    'krr': 'Carrera',
    'carrera': 'Carrera',
    'av': 'Avenida',
    'ave': 'Avenida',
    'avd': 'Avenida',
    'avenida': 'Avenida',
    'ak': 'Avenida Calle',
    'ac': 'Avenida Calle',
    'dg': 'Diagonal',
    'diag': 'Diagonal',
    'diagonal': 'Diagonal',
    'tv': 'Transversal',
    'trans': 'Transversal',
    'tranv': 'Transversal',
    'transversal': 'Transversal',
    'kr': 'Carrera',
    'ct': 'Carretera',
    'ctra': 'Carretera',
    'carretera': 'Carretera',
    'km': 'Kilómetro',
    'via': 'Vía',
    'autopista': 'Autopista',
    'circunvalar': 'Circunvalar',
    'circular': 'Circular',
}

# Palabras que indican ciudad/país y deben eliminarse de la dirección
LOCATION_INDICATORS = [
    # Ciudades principales Colombia
    'bogota', 'bogotá', 'medellin', 'medellín', 'cali', 'barranquilla',
    'cartagena', 'bucaramanga', 'pereira', 'cucuta', 'cúcuta', 'ibague',
    'ibagué', 'santa marta', 'villavicencio', 'manizales', 'neiva', 'pasto',
    'armenia', 'valledupar', 'monteria', 'montería', 'sincelejo', 'popayan',
    'popayán', 'tunja', 'florencia', 'quibdo', 'quibdó',
    # Países
    'colombia', 'ecuador', 'peru', 'perú', 'venezuela', 'panama', 'panamá',
    'costa rica', 'mexico', 'méxico', 'chile', 'argentina', 'brasil',
    # Departamentos
    'cundinamarca', 'antioquia', 'valle del cauca', 'atlantico', 'atlántico',
    'bolivar', 'bolívar', 'santander',
    # Palabras comunes que indican ubicación
    'ciudad', 'municipio', 'localidad', 'barrio', 'vereda', 'sector',
]


def normalize_via_type(via_type: str) -> str:
    """
    Normaliza el tipo de vía de abreviación a nombre completo

    Args:
        via_type: Tipo de vía (puede estar abreviado)

    Returns:
        Tipo de vía completo

    Examples:
        'cl' -> 'Calle'
        'cr' -> 'Carrera'
        'av' -> 'Avenida'
    """
    via_lower = via_type.lower().strip()
    return VIA_TYPES.get(via_lower, via_type.capitalize())


def remove_redundant_location(direccion: str, ciudad: str, pais: str) -> str:
    """
    Elimina referencias redundantes a ciudad/país de la dirección

    Args:
        direccion: Dirección original
        ciudad: Ciudad del registro
        pais: País del registro

    Returns:
        Dirección sin redundancias

    Examples:
        'Calle 80 #70-15, Medellin' + ciudad='Medellin' -> 'Calle 80 #70-15'
        'Av 6 Norte Cali Colombia' + ciudad='Cali' -> 'Av 6 Norte'
    """
    direccion_clean = direccion.strip()

    # Crear lista de términos a eliminar (ciudad, país, y palabras genéricas)
    terms_to_remove = []

    if ciudad:
        terms_to_remove.append(ciudad.lower())
    if pais:
        terms_to_remove.append(pais.lower())

    # Agregar indicadores de ubicación genéricos
    terms_to_remove.extend(LOCATION_INDICATORS)

    # Eliminar términos al final de la dirección
    direccion_lower = direccion_clean.lower()

    for term in terms_to_remove:
        # Buscar el término al final (posiblemente precedido por coma o espacio)
        patterns = [
            rf',\s*{re.escape(term)}\s*$',  # ", Medellin" al final
            rf'\s+{re.escape(term)}\s*$',   # " Medellin" al final
            rf',\s*{re.escape(term)}\s*,',  # ", Medellin," en medio
            rf'\s+{re.escape(term)}\s*,',   # " Medellin," en medio
        ]

        for pattern in patterns:
            direccion_clean = re.sub(pattern, '', direccion_clean, flags=re.IGNORECASE)

    return direccion_clean.strip().rstrip(',').strip()


def standardize_address_format(direccion: str) -> Tuple[str, list]:
    """
    Estandariza el formato de una dirección colombiana al formato:
    [Tipo de vía completo] + [Número principal] # [Número secundario-complemento]

    Args:
        direccion: Dirección original

    Returns:
        Tupla (dirección_estandarizada, lista_de_advertencias)

    Examples:
        'Cl 80 # 70-15' -> 'Calle 80 #70-15'
        'cr 45 n 50 20' -> 'Carrera 45 #50-20'
        'Av. 6ta Norte No. 25-15' -> 'Avenida 6 Norte #25-15'
    """
    warnings = []
    direccion_original = direccion
    direccion = direccion.strip()

    # Patrón para detectar direcciones colombianas
    # Formato: [TipoVia] [NumeroPrincipal] [#/-/N/No./°] [NumeroSecundario][-][Complemento]

    # Normalizar separadores comunes
    direccion = direccion.replace('°', '#')
    direccion = direccion.replace('No.', '#')
    direccion = direccion.replace('No ', '#')
    direccion = direccion.replace(' N ', ' #')
    direccion = direccion.replace(' n ', ' #')

    # Quitar puntos después de abreviaciones
    direccion = re.sub(r'([A-Za-z]+)\.', r'\1', direccion)

    # Patrón 1: Direcciones con nombre de vía compuesto (Ej: "Avenida Ciudad de Cali # 24-30", "Avenida 1 Mayo # 41-50")
    pattern_nombre = r'^(Avenida|Av|Calle|Carrera|Diagonal|Transversal)\s+([A-Za-z0-9\s]+?)\s*([#])\s*(\d+[A-Za-z]?)[\s\-]*(\d+[A-Za-z]?)?(.*)$'
    match_nombre = re.match(pattern_nombre, direccion, re.IGNORECASE)

    if match_nombre:
        via_type = match_nombre.group(1).strip()
        nombre_via = match_nombre.group(2).strip()
        separador = match_nombre.group(3)
        num_secundario = match_nombre.group(4) or ''
        complemento = match_nombre.group(5) or ''
        resto = match_nombre.group(6).strip() if match_nombre.group(6) else ''

        via_normalizada = normalize_via_type(via_type)

        if num_secundario:
            if complemento:
                direccion_std = f"{via_normalizada} {nombre_via} #{num_secundario}-{complemento}"
            else:
                direccion_std = f"{via_normalizada} {nombre_via} #{num_secundario}"
        else:
            direccion_std = f"{via_normalizada} {nombre_via}"
            warnings.append(f"Dirección sin número secundario: '{direccion_original}'")

        if resto:
            resto_clean = resto.strip(',-#').strip()
            if resto_clean and len(resto_clean) < 30:
                direccion_std = f"{direccion_std} {resto_clean}"

        return direccion_std, warnings

    # Patrón 2: Direcciones estándar con sufijo opcional (Sur/Norte/Este/Oeste)
    # Ejemplos: "Calle 80 # 70-15", "Calle 63 Sur # 18-30", "Carrera 3 Este # 10-45"
    pattern = r'^([A-Za-z]+\.?\s?[A-Za-z]*)\s+(\d+[A-Za-z]?)\s*(Sur|Norte|Este|Oeste|Bis|[A-Z])?\s*([#\-])\s*(\d+[A-Za-z]?)[\s\-]*(\d+[A-Za-z]?)?(.*)$'

    match = re.match(pattern, direccion, re.IGNORECASE)

    if match:
        via_type = match.group(1).strip()
        num_principal = match.group(2).strip()
        sufijo_direccion = match.group(3) or ''  # Sur, Norte, Este, Oeste, Bis, etc.
        separador = match.group(4) or '#'
        num_secundario = match.group(5) or ''
        complemento = match.group(6) or ''
        resto = match.group(7).strip() if match.group(7) else ''

        # Normalizar tipo de vía
        via_normalizada = normalize_via_type(via_type)

        # Construir número principal con sufijo si existe
        if sufijo_direccion:
            num_principal_completo = f"{num_principal} {sufijo_direccion.capitalize()}"
        else:
            num_principal_completo = num_principal

        # Construir dirección estandarizada
        if num_secundario:
            if complemento:
                direccion_std = f"{via_normalizada} {num_principal_completo} #{num_secundario}-{complemento}"
            else:
                direccion_std = f"{via_normalizada} {num_principal_completo} #{num_secundario}"
        else:
            direccion_std = f"{via_normalizada} {num_principal_completo}"
            warnings.append(f"Dirección sin número secundario: '{direccion_original}'")

        # Agregar resto si hay información adicional (Ej: "Sur", "Norte", "Este", "Oeste", "Bis", etc.)
        if resto:
            # Limpiar y agregar solo si es relevante
            resto_clean = resto.strip(',-#').strip()
            if resto_clean and len(resto_clean) < 30:  # Evitar agregar textos muy largos
                direccion_std = f"{direccion_std} {resto_clean}"

        return direccion_std, warnings

    else:
        # No coincide con el patrón esperado
        warnings.append(f"Formato de dirección no reconocido: '{direccion_original}'")
        return direccion, warnings


def validate_and_standardize_address(direccion: str, ciudad: str, pais: str) -> Tuple[str, list]:
    """
    Valida y estandariza una dirección completa

    Proceso:
    1. Elimina redundancias de ciudad/país
    2. Estandariza el formato de la dirección
    3. Retorna dirección limpia y lista de advertencias

    Args:
        direccion: Dirección original
        ciudad: Ciudad del registro
        pais: País del registro

    Returns:
        Tupla (dirección_estandarizada, lista_de_advertencias)

    Examples:
        'Cl 80 # 70-15, Medellin' + ciudad='Medellin'
        -> ('Calle 80 #70-15', [])

        'cr 45 n 50 20 Bogota Colombia' + ciudad='Bogota'
        -> ('Carrera 45 #50-20', [])
    """
    warnings = []

    # Paso 1: Eliminar redundancias
    direccion_clean = remove_redundant_location(direccion, ciudad, pais)

    if direccion_clean != direccion:
        # Se eliminó algo
        eliminated = direccion.replace(direccion_clean, '').strip(' ,')
        if eliminated:
            warnings.append(f"Se eliminó redundancia: '{eliminated}'")

    # Paso 2: Estandarizar formato
    direccion_std, std_warnings = standardize_address_format(direccion_clean)
    warnings.extend(std_warnings)

    return direccion_std, warnings


def validate_address_dataframe(df: pd.DataFrame, tipo: str = "destinos") -> Tuple[pd.DataFrame, dict]:
    """
    Valida y estandariza todas las direcciones en un DataFrame

    Args:
        df: DataFrame con columnas 'direccion', 'ciudad', 'pais'
        tipo: Tipo de archivo (para mensajes)

    Returns:
        Tupla (DataFrame con direcciones estandarizadas, diccionario con estadísticas)
    """
    if 'direccion' not in df.columns:
        return df, {'error': 'No se encontró columna "direccion"'}

    df_clean = df.copy()

    # Crear columna para dirección original (si no existe)
    if 'direccion_original' not in df_clean.columns:
        df_clean['direccion_original'] = df_clean['direccion']

    stats = {
        'total': len(df),
        'estandarizadas': 0,
        'sin_cambios': 0,
        'warnings': [],
        'ejemplos_cambios': []
    }

    for idx, row in df.iterrows():
        direccion_original = row['direccion']
        ciudad = row.get('ciudad', '')
        pais = row.get('pais', '')

        direccion_std, warnings = validate_and_standardize_address(
            str(direccion_original),
            str(ciudad),
            str(pais)
        )

        # Actualizar DataFrame con dirección estandarizada
        df_clean.at[idx, 'direccion'] = direccion_std
        # Preservar dirección original
        df_clean.at[idx, 'direccion_original'] = str(direccion_original)

        # Registrar estadísticas
        # Normalizar para comparación: eliminar espacios extra y alrededor de #
        def normalizar_para_comparar(s):
            s = re.sub(r'\s+', ' ', str(s).strip())  # Espacios múltiples a uno
            s = re.sub(r'\s*#\s*', '#', s)  # Sin espacios alrededor de #
            return s.lower()

        orig_normalizada = normalizar_para_comparar(direccion_original)
        std_normalizada = normalizar_para_comparar(direccion_std)

        # Solo contar como cambio si hay diferencia significativa (no solo espacios)
        if orig_normalizada != std_normalizada:
            stats['estandarizadas'] += 1

            # Guardar algunos ejemplos de cambios significativos
            if len(stats['ejemplos_cambios']) < 5:
                stats['ejemplos_cambios'].append({
                    'fila': idx + 2,  # +2 porque Excel empieza en 1 y tiene header
                    'original': str(direccion_original)[:60],
                    'estandarizada': str(direccion_std)[:60]
                })
        else:
            stats['sin_cambios'] += 1

        # Agregar warnings si los hay
        if warnings:
            for warning in warnings:
                stats['warnings'].append(f"Fila {idx + 2}: {warning}")

    return df_clean, stats


def get_address_validation_summary(stats: dict) -> str:
    """
    Genera un resumen legible de las validaciones de direcciones

    Args:
        stats: Diccionario con estadísticas de validación

    Returns:
        String con resumen formateado
    """
    if 'error' in stats:
        return f"❌ Error: {stats['error']}"

    summary = f"📍 Validación de Direcciones:\n"
    summary += f"   • Total de direcciones: {stats['total']}\n"
    summary += f"   • Estandarizadas: {stats['estandarizadas']}\n"
    summary += f"   • Sin cambios: {stats['sin_cambios']}\n"

    if stats['ejemplos_cambios']:
        summary += f"\n   Ejemplos de cambios:\n"
        for ejemplo in stats['ejemplos_cambios']:
            summary += f"   - Fila {ejemplo['fila']}:\n"
            summary += f"     Original: {ejemplo['original']}\n"
            summary += f"     Estandarizada: {ejemplo['estandarizada']}\n"

    if stats['warnings'] and len(stats['warnings']) <= 10:
        summary += f"\n   ⚠️ Advertencias:\n"
        for warning in stats['warnings'][:10]:
            summary += f"   - {warning}\n"
    elif len(stats.get('warnings', [])) > 10:
        summary += f"\n   ⚠️ {len(stats['warnings'])} advertencias (mostrando primeras 10):\n"
        for warning in stats['warnings'][:10]:
            summary += f"   - {warning}\n"

    return summary
