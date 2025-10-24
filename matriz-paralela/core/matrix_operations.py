"""
Módulo de operaciones de matrices optimizadas con NumPy.
Implementa multiplicación de matrices secuencial y paralela.
"""

import numpy as np
import time
from typing import Tuple


class MatrixOperations:
    """Clase para operaciones de multiplicación de matrices."""

    @staticmethod
    def generate_random_matrix(rows: int, cols: int, seed: int = None) -> np.ndarray:
        """
        Genera una matriz aleatoria con valores entre 0 y 100.

        Args:
            rows: Número de filas
            cols: Número de columnas
            seed: Semilla para reproducibilidad

        Returns:
            Matriz NumPy de tamaño (rows, cols)
        """
        if seed is not None:
            np.random.seed(seed)

        return np.random.randint(0, 100, size=(rows, cols), dtype=np.int32)

    @staticmethod
    def sequential_multiply(matrix_a: np.ndarray, matrix_b: np.ndarray) -> Tuple[np.ndarray, float]:
        """
        Multiplicación de matrices secuencial usando NumPy optimizado.

        Args:
            matrix_a: Primera matriz (m x n)
            matrix_b: Segunda matriz (n x p)

        Returns:
            Tupla (matriz resultado, tiempo de ejecución en segundos)
        """
        if matrix_a.shape[1] != matrix_b.shape[0]:
            raise ValueError(
                f"Dimensiones incompatibles: {matrix_a.shape} y {matrix_b.shape}"
            )

        start_time = time.perf_counter()
        result = np.matmul(matrix_a, matrix_b)
        end_time = time.perf_counter()

        execution_time = end_time - start_time

        return result, execution_time

    @staticmethod
    def validate_matrices(matrix_a: np.ndarray, matrix_b: np.ndarray) -> bool:
        """
        Valida que las matrices sean compatibles para multiplicación.

        Args:
            matrix_a: Primera matriz
            matrix_b: Segunda matriz

        Returns:
            True si son compatibles, False en caso contrario
        """
        return matrix_a.shape[1] == matrix_b.shape[0]

    @staticmethod
    def get_matrix_info(matrix: np.ndarray) -> dict:
        """
        Obtiene información detallada de una matriz.

        Args:
            matrix: Matriz NumPy

        Returns:
            Diccionario con información de la matriz
        """
        return {
            'shape': matrix.shape,
            'dtype': str(matrix.dtype),
            'size': matrix.size,
            'memory_mb': matrix.nbytes / (1024 * 1024),
            'min': float(np.min(matrix)),
            'max': float(np.max(matrix)),
            'mean': float(np.mean(matrix))
        }
