"""
Módulo de métricas de rendimiento y análisis de paralelización.
Implementa cálculos de Ley de Amdahl, speedup y eficiencia.
"""

import numpy as np
from typing import Dict, List


class PerformanceMetrics:
    """Clase para calcular métricas de rendimiento de paralelización."""

    @staticmethod
    def calculate_speedup(sequential_time: float, parallel_time: float) -> float:
        """
        Calcula el speedup (aceleración) de la ejecución paralela.
        Speedup = T_secuencial / T_paralelo

        Args:
            sequential_time: Tiempo de ejecución secuencial
            parallel_time: Tiempo de ejecución paralela

        Returns:
            Factor de speedup
        """
        if parallel_time == 0:
            return 0.0

        return sequential_time / parallel_time

    @staticmethod
    def calculate_efficiency(speedup: float, num_processors: int) -> float:
        """
        Calcula la eficiencia de la paralelización.
        Eficiencia = Speedup / Número_de_procesadores

        Args:
            speedup: Factor de speedup calculado
            num_processors: Número de procesadores usados

        Returns:
            Eficiencia (valor entre 0 y 1, donde 1 es eficiencia perfecta)
        """
        if num_processors == 0:
            return 0.0

        return speedup / num_processors

    @staticmethod
    def amdahl_law(parallel_fraction: float, num_processors: int) -> float:
        """
        Calcula el speedup teórico máximo según la Ley de Amdahl.

        Ley de Amdahl: Speedup = 1 / ((1 - P) + P/N)
        Donde:
            P = fracción paralelizable del programa (0 a 1)
            N = número de procesadores

        Args:
            parallel_fraction: Fracción del código que es paralelizable (0.0 a 1.0)
            num_processors: Número de procesadores

        Returns:
            Speedup teórico máximo
        """
        if parallel_fraction < 0 or parallel_fraction > 1:
            raise ValueError("parallel_fraction debe estar entre 0 y 1")

        if num_processors <= 0:
            raise ValueError("num_processors debe ser mayor que 0")

        serial_fraction = 1.0 - parallel_fraction

        speedup = 1.0 / (serial_fraction + (parallel_fraction / num_processors))

        return speedup

    @staticmethod
    def calculate_amdahl_for_range(
        parallel_fraction: float,
        max_processors: int
    ) -> Dict[int, float]:
        """
        Calcula la Ley de Amdahl para un rango de procesadores.

        Args:
            parallel_fraction: Fracción paralelizable
            max_processors: Número máximo de procesadores

        Returns:
            Diccionario {num_processors: speedup_teorico}
        """
        results = {}

        for num_proc in range(1, max_processors + 1):
            results[num_proc] = PerformanceMetrics.amdahl_law(
                parallel_fraction, num_proc
            )

        return results

    @staticmethod
    def analyze_results(
        sequential_time: float,
        parallel_times: Dict[int, float],
        parallel_fractions: List[float] = None
    ) -> Dict:
        """
        Analiza resultados completos de ejecuciones paralelas.

        Args:
            sequential_time: Tiempo secuencial de referencia
            parallel_times: Diccionario {num_workers: tiempo_paralelo}
            parallel_fractions: Lista de fracciones paralelas para Amdahl (ej: [0.6, 0.9])

        Returns:
            Diccionario con análisis completo
        """
        if parallel_fractions is None:
            parallel_fractions = [0.6, 0.9]

        analysis = {
            'sequential_time': sequential_time,
            'parallel_times': parallel_times,
            'speedups': {},
            'efficiencies': {},
            'amdahl_predictions': {}
        }

        # Calcular speedup y eficiencia para cada número de workers
        for num_workers, p_time in parallel_times.items():
            speedup = PerformanceMetrics.calculate_speedup(sequential_time, p_time)
            efficiency = PerformanceMetrics.calculate_efficiency(speedup, num_workers)

            analysis['speedups'][num_workers] = speedup
            analysis['efficiencies'][num_workers] = efficiency

        # Calcular predicciones de Amdahl para diferentes fracciones paralelas
        max_workers = max(parallel_times.keys())

        for fraction in parallel_fractions:
            analysis['amdahl_predictions'][fraction] = \
                PerformanceMetrics.calculate_amdahl_for_range(fraction, max_workers)

        return analysis

    @staticmethod
    def get_optimal_workers(
        speedups: Dict[int, float],
        efficiency_threshold: float = 0.7
    ) -> int:
        """
        Determina el número óptimo de workers basado en eficiencia.

        Args:
            speedups: Diccionario {num_workers: speedup}
            efficiency_threshold: Umbral mínimo de eficiencia aceptable

        Returns:
            Número óptimo de workers
        """
        optimal = 1

        for num_workers, speedup in speedups.items():
            efficiency = PerformanceMetrics.calculate_efficiency(speedup, num_workers)

            if efficiency >= efficiency_threshold:
                optimal = num_workers

        return optimal

    @staticmethod
    def calculate_max_theoretical_speedup(parallel_fraction: float) -> float:
        """
        Calcula el speedup teórico máximo con infinitos procesadores.
        Según Amdahl: Speedup_max = 1 / (1 - P)

        Args:
            parallel_fraction: Fracción paralelizable del programa

        Returns:
            Speedup máximo teórico
        """
        if parallel_fraction < 0 or parallel_fraction > 1:
            raise ValueError("parallel_fraction debe estar entre 0 y 1")

        serial_fraction = 1.0 - parallel_fraction

        if serial_fraction == 0:
            return float('inf')

        return 1.0 / serial_fraction

    @staticmethod
    def get_flynn_taxonomy() -> dict:
        """
        Retorna información sobre la taxonomía de Flynn aplicable.

        Returns:
            Diccionario con clasificación de Flynn
        """
        return {
            'classification': 'MIMD',
            'full_name': 'Multiple Instruction, Multiple Data',
            'description': (
                'Múltiples procesadores ejecutan diferentes instrucciones '
                'sobre diferentes datos de forma simultánea. '
                'Es el modelo más común en sistemas paralelos modernos.'
            ),
            'examples': [
                'Sistemas multiprocesador',
                'Clusters de computadoras',
                'Sistemas multicore como el Intel i5-10210U'
            ],
            'justification': (
                'En este ejercicio utilizamos múltiples procesos (multiprocessing) '
                'donde cada proceso ejecuta la multiplicación de su chunk de matriz '
                'de forma independiente con sus propias instrucciones y datos. '
                'Cada core del procesador puede ejecutar diferentes instrucciones '
                'sobre diferentes porciones de datos simultáneamente.'
            )
        }

    @staticmethod
    def format_time(seconds: float) -> str:
        """
        Formatea tiempo en segundos a formato legible.

        Args:
            seconds: Tiempo en segundos

        Returns:
            String formateado
        """
        if seconds < 0.001:
            return f"{seconds * 1_000_000:.2f} μs"
        elif seconds < 1:
            return f"{seconds * 1_000:.2f} ms"
        else:
            return f"{seconds:.4f} s"
