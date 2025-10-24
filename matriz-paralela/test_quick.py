"""
Script de prueba rápida para verificar que todos los módulos funcionan correctamente.
"""

import sys
import numpy as np
from core.matrix_operations import MatrixOperations
from core.parallel_processor import ParallelProcessor
from core.performance_metrics import PerformanceMetrics
from utils.helpers import get_system_info, estimate_memory_usage

def test_basic_functionality():
    """Prueba básica de funcionalidad."""
    print("=" * 60)
    print("PRUEBA RÁPIDA DEL SISTEMA")
    print("=" * 60)

    # Información del sistema
    print("\n1. Información del Sistema:")
    print("-" * 60)
    system_info = get_system_info()
    print(f"Procesador: {system_info['processor']}")
    print(f"Núcleos físicos: {system_info['cpu_count_physical']}")
    print(f"Núcleos lógicos: {system_info['cpu_count_logical']}")
    print(f"RAM total: {system_info['ram_total']}")

    # Generar matrices pequeñas para prueba rápida
    print("\n2. Generando Matrices de Prueba (500x500):")
    print("-" * 60)
    size = 500
    print(f"Tamaño: {size}x{size}")
    print(f"Memoria estimada: {estimate_memory_usage(size)}")

    matrix_a = MatrixOperations.generate_random_matrix(size, size, seed=42)
    matrix_b = MatrixOperations.generate_random_matrix(size, size, seed=43)

    print(f"Matriz A: {matrix_a.shape}, dtype: {matrix_a.dtype}")
    print(f"Matriz B: {matrix_b.shape}, dtype: {matrix_b.dtype}")

    # Multiplicación secuencial
    print("\n3. Multiplicación Secuencial:")
    print("-" * 60)
    result_seq, time_seq = MatrixOperations.sequential_multiply(matrix_a, matrix_b)
    print(f"Tiempo: {PerformanceMetrics.format_time(time_seq)}")
    print(f"Resultado: {result_seq.shape}")

    # Multiplicación paralela con diferentes workers
    print("\n4. Multiplicación Paralela:")
    print("-" * 60)
    workers_list = [2, 4]

    for num_workers in workers_list:
        result_par, time_par = ParallelProcessor.parallel_multiply_processes(
            matrix_a, matrix_b, num_workers
        )
        speedup = PerformanceMetrics.calculate_speedup(time_seq, time_par)
        efficiency = PerformanceMetrics.calculate_efficiency(speedup, num_workers)

        print(f"\nWorkers: {num_workers}")
        print(f"  Tiempo: {PerformanceMetrics.format_time(time_par)}")
        print(f"  Speedup: {speedup:.3f}x")
        print(f"  Eficiencia: {efficiency * 100:.2f}%")

        # Verificar que los resultados son iguales
        if np.allclose(result_seq, result_par):
            print(f"  Verificación: ✓ CORRECTO")
        else:
            print(f"  Verificación: ✗ ERROR - Resultados no coinciden")

    # Ley de Amdahl
    print("\n5. Ley de Amdahl:")
    print("-" * 60)
    for parallel_fraction in [0.6, 0.9]:
        speedup_4 = PerformanceMetrics.amdahl_law(parallel_fraction, 4)
        speedup_8 = PerformanceMetrics.amdahl_law(parallel_fraction, 8)
        speedup_max = PerformanceMetrics.calculate_max_theoretical_speedup(parallel_fraction)

        print(f"\nParalelismo {parallel_fraction * 100:.0f}%:")
        print(f"  Speedup con 4 procesadores: {speedup_4:.3f}x")
        print(f"  Speedup con 8 procesadores: {speedup_8:.3f}x")
        print(f"  Speedup máximo teórico: {speedup_max:.3f}x")

    # Taxonomía de Flynn
    print("\n6. Taxonomía de Flynn:")
    print("-" * 60)
    flynn_info = PerformanceMetrics.get_flynn_taxonomy()
    print(f"Clasificación: {flynn_info['classification']}")
    print(f"Nombre completo: {flynn_info['full_name']}")

    print("\n" + "=" * 60)
    print("TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
    print("=" * 60)
    print("\nPara ejecutar la aplicación completa, usa:")
    print("  streamlit run app.py")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_basic_functionality()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
