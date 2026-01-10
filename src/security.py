"""
Módulo de seguridad para RutaFácil
Incluye validaciones de archivos, sanitización de datos y protección contra amenazas
"""
import pandas as pd
import re
import html
from typing import Any
import streamlit as st


# Configuración de límites de seguridad
SECURITY_CONFIG = {
    'max_file_size_mb': 5,  # Máximo 5 MB por archivo
    'max_rows': 500,  # Máximo 500 filas por archivo
    'max_string_length': 500,  # Máximo 500 caracteres por campo de texto
}


class SecurityError(Exception):
    """Excepción personalizada para errores de seguridad"""
    pass


def validate_file_size(uploaded_file) -> bool:
    """
    Valida que el archivo no exceda el tamaño máximo permitido

    Args:
        uploaded_file: Archivo subido por Streamlit

    Returns:
        True si es válido

    Raises:
        SecurityError: Si el archivo es muy grande
    """
    max_size_bytes = SECURITY_CONFIG['max_file_size_mb'] * 1024 * 1024

    if uploaded_file.size > max_size_bytes:
        raise SecurityError(
            f"❌ Archivo muy grande: {uploaded_file.size / (1024*1024):.2f} MB. "
            f"Máximo permitido: {SECURITY_CONFIG['max_file_size_mb']} MB"
        )

    return True


def validate_row_count(df: pd.DataFrame, file_type: str = "archivo") -> bool:
    """
    Valida que el DataFrame no tenga demasiadas filas

    Args:
        df: DataFrame a validar
        file_type: Tipo de archivo (para mensaje de error)

    Returns:
        True si es válido

    Raises:
        SecurityError: Si tiene demasiadas filas
    """
    max_rows = SECURITY_CONFIG['max_rows']

    if len(df) > max_rows:
        raise SecurityError(
            f"❌ Demasiadas filas en {file_type}: {len(df)} filas. "
            f"Máximo permitido: {max_rows} filas"
        )

    return True


def detect_excel_formulas(df: pd.DataFrame, file_type: str = "archivo") -> bool:
    """
    Detecta y bloquea fórmulas potencialmente peligrosas en archivos Excel

    Fórmulas bloqueadas:
    - Que empiezan con =, +, -, @ (fórmulas Excel)
    - Funciones peligrosas: WEBSERVICE, HYPERLINK, IMPORTDATA, etc.

    Args:
        df: DataFrame a validar
        file_type: Tipo de archivo (para mensaje de error)

    Returns:
        True si no hay fórmulas peligrosas

    Raises:
        SecurityError: Si detecta fórmulas maliciosas
    """
    dangerous_functions = [
        'WEBSERVICE', 'HYPERLINK', 'IMPORTDATA', 'IMPORTXML',
        'IMPORTHTML', 'IMPORTFEED', 'IMPORTRANGE', 'QUERY',
        'INDIRECT', 'EXEC', 'SYSTEM', 'SHELL', 'CALL'
    ]

    for col in df.columns:
        if df[col].dtype == 'object':  # Solo columnas de texto
            # Convertir a string para análisis
            col_values = df[col].astype(str)

            # Detectar fórmulas que empiezan con caracteres especiales
            formula_pattern = r'^[\s]*[=+\-@]'
            formula_mask = col_values.str.match(formula_pattern, na=False)

            if formula_mask.any():
                # Encontrar la primera fila con fórmula para mostrar ejemplo
                first_formula_idx = formula_mask.idxmax()
                formula_example = col_values.iloc[first_formula_idx]

                raise SecurityError(
                    f"⚠️ Detectada fórmula potencialmente peligrosa en {file_type}\n"
                    f"Columna: '{col}'\n"
                    f"Fila: {first_formula_idx + 2}\n"  # +2 porque Excel empieza en 1 y tiene header
                    f"Contenido: {formula_example[:50]}...\n\n"
                    f"Por seguridad, no se permiten celdas que empiecen con: = + - @"
                )

            # Detectar funciones peligrosas
            for func in dangerous_functions:
                if col_values.str.contains(func, case=False, regex=False, na=False).any():
                    raise SecurityError(
                        f"⚠️ Detectada función Excel peligrosa en {file_type}\n"
                        f"Columna: '{col}'\n"
                        f"Función bloqueada: {func}\n\n"
                        f"Esta función podría comprometer la seguridad del sistema."
                    )

    return True


def sanitize_text_input(text: Any) -> Any:
    """
    Sanitiza entradas de texto para prevenir XSS y otros ataques

    Args:
        text: Texto a sanitizar

    Returns:
        Texto sanitizado
    """
    if not isinstance(text, str):
        return text

    if pd.isna(text) or text == '':
        return text

    # Escapar HTML
    text = html.escape(text)

    # Remover caracteres de control (excepto newline y tab)
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)

    # Limitar longitud
    max_length = SECURITY_CONFIG['max_string_length']
    if len(text) > max_length:
        text = text[:max_length] + '...'

    return text


def sanitize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sanitiza todas las columnas de texto en un DataFrame

    Args:
        df: DataFrame a sanitizar

    Returns:
        DataFrame sanitizado
    """
    df_clean = df.copy()

    for col in df_clean.columns:
        if df_clean[col].dtype == 'object':  # Columnas de texto
            df_clean[col] = df_clean[col].apply(sanitize_text_input)

    return df_clean


def validate_and_sanitize_file(uploaded_file, df: pd.DataFrame, file_type: str = "archivo") -> pd.DataFrame:
    """
    Ejecuta todas las validaciones de seguridad en un archivo subido

    Args:
        uploaded_file: Archivo subido por Streamlit
        df: DataFrame cargado del archivo
        file_type: Tipo de archivo (origenes/destinos/flota/config)

    Returns:
        DataFrame validado y sanitizado

    Raises:
        SecurityError: Si alguna validación falla
    """
    # 1. Validar tamaño de archivo
    validate_file_size(uploaded_file)

    # 2. Validar número de filas
    validate_row_count(df, file_type)

    # 3. Detectar fórmulas peligrosas
    detect_excel_formulas(df, file_type)

    # 4. Sanitizar contenido
    df_clean = sanitize_dataframe(df)

    return df_clean


def safe_log(message: str, level: str = "info"):
    """
    Muestra mensaje en UI con ofuscación de datos sensibles

    Args:
        message: Mensaje a mostrar
        level: Nivel de log (info/warning/error)
    """
    # Ofuscar API keys
    message = re.sub(r'AIza[A-Za-z0-9_-]{35}', 'AIza***[REDACTED]***', message)

    # Ofuscar emails
    message = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        '***@***.***',
        message
    )

    # Mostrar según nivel
    if level == "error":
        st.error(message)
    elif level == "warning":
        st.warning(message)
    else:
        st.info(message)
