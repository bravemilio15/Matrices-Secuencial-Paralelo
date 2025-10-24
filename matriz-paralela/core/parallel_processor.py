"""
Módulo de procesamiento paralelo para multiplicación de matrices.
Implementa paralelización usando multiprocessing y threading.
"""

import numpy as np
import time
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Tuple, List
import os


class ParallelProcessor:
    """Clase para procesamiento paralelo de multiplicación de matrices."""

    @staticmethod
    def get_cpu_info() -> dict:
        """
        Obtiene información de CPUs disponibles.

        Returns:
            Diccionario con información de CPUs
        """
        return {
            'cpu_count': cpu_count(),
            'available_cores': os.cpu_count(),
        }

    @staticmethod
    def _multiply_chunk(args: Tuple) -> np.ndarray:
        """
        Multiplica un chunk (porción) de la matriz A con toda la matriz B.

        Args:
            args: Tupla (chunk_a, matrix_b)

        Returns:
            Resultado de la multiplicación del chunk
        """
        chunk_a, matrix_b = args
        return np.matmul(chunk_a, matrix_b)

    @staticmethod
    def parallel_multiply_processes(
        matrix_a: np.ndarray,
        matrix_b: np.ndarray,
        num_processes: int
    ) -> Tuple[np.ndarray, float]:
        """
        Multiplicación paralela usando multiprocessing (múltiples procesos).
        Divide matrix_a en chunks horizontales y los procesa en paralelo.

        Args:
            matrix_a: Primera matriz (m x n)
            matrix_b: Segunda matriz (n x p)
            num_processes: Número de procesos paralelos

        Returns:
            Tupla (matriz resultado, tiempo de ejecución en segundos)
        """
        if matrix_a.shape[1] != matrix_b.shape[0]:
            raise ValueError(
                f"Dimensiones incompatibles: {matrix_a.shape} y {matrix_b.shape}"
            )

        start_time = time.perf_counter()

        # Dividir matrix_a en chunks horizontales
        chunks = np.array_split(matrix_a, num_processes, axis=0)

        # Crear argumentos para cada proceso
        args_list = [(chunk, matrix_b) for chunk in chunks]

        # Ejecutar en paralelo usando Pool
        with Pool(processes=num_processes) as pool:
            results = pool.map(ParallelProcessor._multiply_chunk, args_list)

        # Concatenar resultados
        result = np.vstack(results)

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        return result, execution_time

    @staticmethod
    def parallel_multiply_threads(
        matrix_a: np.ndarray,
        matrix_b: np.ndarray,
        num_threads: int
    ) -> Tuple[np.ndarray, float]:
        """
        Multiplicación paralela usando threading (múltiples hilos).
        Nota: En Python, threads no proporcionan verdadero paralelismo
        debido al GIL (Global Interpreter Lock), pero se incluye para comparación.

        Args:
            matrix_a: Primera matriz (m x n)
            matrix_b: Segunda matriz (n x p)
            num_threads: Número de hilos paralelos

        Returns:
            Tupla (matriz resultado, tiempo de ejecución en segundos)
        """
        if matrix_a.shape[1] != matrix_b.shape[0]:
            raise ValueError(
                f"Dimensiones incompatibles: {matrix_a.shape} y {matrix_b.shape}"
            )

        start_time = time.perf_counter()

        # Dividir matrix_a en chunks horizontales
        chunks = np.array_split(matrix_a, num_threads, axis=0)

        # Crear argumentos para cada hilo
        args_list = [(chunk, matrix_b) for chunk in chunks]

        # Ejecutar en paralelo usando ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            results = list(executor.map(
                lambda args: ParallelProcessor._multiply_chunk(args),
                args_list
            ))

        # Concatenar resultados
        result = np.vstack(results)

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        return result, execution_time

    @staticmethod
    def parallel_multiply_executor(
        matrix_a: np.ndarray,
        matrix_b: np.ndarray,
        num_workers: int
    ) -> Tuple[np.ndarray, float]:
        """
        Multiplicación paralela usando ProcessPoolExecutor.
        Alternativa moderna a multiprocessing.Pool.

        Args:
            matrix_a: Primera matriz (m x n)
            matrix_b: Segunda matriz (n x p)
            num_workers: Número de workers paralelos

        Returns:
            Tupla (matriz resultado, tiempo de ejecución en segundos)
        """
        if matrix_a.shape[1] != matrix_b.shape[0]:
            raise ValueError(
                f"Dimensiones incompatibles: {matrix_a.shape} y {matrix_b.shape}"
            )

        start_time = time.perf_counter()

        # Dividir matrix_a en chunks horizontales
        chunks = np.array_split(matrix_a, num_workers, axis=0)

        # Crear argumentos para cada worker
        args_list = [(chunk, matrix_b) for chunk in chunks]

        # Ejecutar en paralelo usando ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            results = list(executor.map(
                ParallelProcessor._multiply_chunk,
                args_list
            ))

        # Concatenar resultados
        result = np.vstack(results)

        end_time = time.perf_counter()
        execution_time = end_time - start_time

        return result, execution_time

    @staticmethod
    def compare_methods(
        matrix_a: np.ndarray,
        matrix_b: np.ndarray,
        workers_list: List[int]
    ) -> dict:
        """
        Compara diferentes métodos de paralelización con distintos números de workers.

        Args:
            matrix_a: Primera matriz
            matrix_b: Segunda matriz
            workers_list: Lista de números de workers a probar

        Returns:
            Diccionario con resultados de comparación
        """
        from core.matrix_operations import MatrixOperations

        results = {
            'sequential': None,
            'multiprocessing': {},
            'threading': {},
            'executor': {}
        }

        # Secuencial (baseline)
        _, seq_time = MatrixOperations.sequential_multiply(matrix_a, matrix_b)
        results['sequential'] = seq_time

        # Probar diferentes números de workers
        for num_workers in workers_list:
            # Multiprocessing
            _, mp_time = ParallelProcessor.parallel_multiply_processes(
                matrix_a, matrix_b, num_workers
            )
            results['multiprocessing'][num_workers] = mp_time

            # Threading
            _, th_time = ParallelProcessor.parallel_multiply_threads(
                matrix_a, matrix_b, num_workers
            )
            results['threading'][num_workers] = th_time

            # Executor
            _, ex_time = ParallelProcessor.parallel_multiply_executor(
                matrix_a, matrix_b, num_workers
            )
            results['executor'][num_workers] = ex_time

        return results
