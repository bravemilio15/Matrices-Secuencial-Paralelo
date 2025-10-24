"""
Módulo de funciones auxiliares para la aplicación.
"""

import platform
import psutil
import numpy as np
from typing import Dict


def get_system_info() -> Dict:
    """
    Obtiene información detallada del sistema.

    Returns:
        Diccionario con información del sistema
    """
    return {
        'platform': platform.system(),
        'platform_release': platform.release(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'cpu_count_physical': psutil.cpu_count(logical=False),
        'cpu_count_logical': psutil.cpu_count(logical=True),
        'cpu_freq_current': f"{psutil.cpu_freq().current:.2f} MHz" if psutil.cpu_freq() else "N/A",
        'cpu_freq_max': f"{psutil.cpu_freq().max:.2f} MHz" if psutil.cpu_freq() else "N/A",
        'ram_total': f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
        'ram_available': f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
        'ram_percent': f"{psutil.virtual_memory().percent}%"
    }


def format_matrix_size(size: int) -> str:
    """
    Formatea el tamaño de matriz a string legible.

    Args:
        size: Tamaño de la dimensión

    Returns:
        String formateado
    """
    return f"{size} x {size}"


def estimate_memory_usage(matrix_size: int, dtype=np.int32) -> str:
    """
    Estima el uso de memoria para dos matrices cuadradas.

    Args:
        matrix_size: Tamaño de cada dimensión de la matriz
        dtype: Tipo de dato de NumPy

    Returns:
        String con estimación de memoria
    """
    # Dos matrices de entrada + una matriz resultado
    bytes_per_element = np.dtype(dtype).itemsize
    total_elements = 3 * (matrix_size ** 2)
    total_bytes = total_elements * bytes_per_element

    # Convertir a MB o GB
    if total_bytes < 1024 ** 2:
        return f"{total_bytes / 1024:.2f} KB"
    elif total_bytes < 1024 ** 3:
        return f"{total_bytes / (1024 ** 2):.2f} MB"
    else:
        return f"{total_bytes / (1024 ** 3):.2f} GB"


def validate_matrix_size(size: int, max_size: int = 2000) -> bool:
    """
    Valida que el tamaño de matriz esté en el rango permitido.

    Args:
        size: Tamaño a validar
        max_size: Tamaño máximo permitido

    Returns:
        True si es válido, False en caso contrario
    """
    return 1 <= size <= max_size


def get_recommended_workers() -> list:
    """
    Obtiene lista recomendada de números de workers basada en el sistema.

    Returns:
        Lista de números de workers recomendados
    """
    logical_cpus = psutil.cpu_count(logical=True)

    if logical_cpus <= 2:
        return [1, 2]
    elif logical_cpus <= 4:
        return [1, 2, 4]
    elif logical_cpus <= 8:
        return [1, 2, 4, 8]
    else:
        return [1, 2, 4, 8, 16]
