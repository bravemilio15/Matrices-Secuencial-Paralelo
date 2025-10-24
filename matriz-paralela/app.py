"""
Aplicación Streamlit para Multiplicación de Matrices Paralelas.
Incluye análisis de rendimiento, Ley de Amdahl y Taxonomía de Flynn.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from core.matrix_operations import MatrixOperations
from core.parallel_processor import ParallelProcessor
from core.performance_metrics import PerformanceMetrics
from utils.helpers import (
    get_system_info,
    format_matrix_size,
    estimate_memory_usage,
    get_recommended_workers
)

# Configuración de la página
st.set_page_config(
    page_title="Multiplicación de Matrices Paralelas",
    page_icon="🔢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2ca02c;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Función principal de la aplicación."""

    # Título principal
    st.markdown('<p class="main-header">🔢 Multiplicación de Matrices Paralelas</p>',
                unsafe_allow_html=True)

    st.markdown("""
    **Ejercicio de Programación Paralela**: Análisis de rendimiento de multiplicación
    de matrices usando múltiples procesos y comparación con la Ley de Amdahl.
    """)

    # Sidebar con configuración
    st.sidebar.title("⚙️ Configuración")

    # Información del sistema
    with st.sidebar.expander("💻 Información del Sistema", expanded=False):
        system_info = get_system_info()
        st.write(f"**Procesador:** {system_info['processor']}")
        st.write(f"**Núcleos físicos:** {system_info['cpu_count_physical']}")
        st.write(f"**Núcleos lógicos:** {system_info['cpu_count_logical']}")
        st.write(f"**Frecuencia actual:** {system_info['cpu_freq_current']}")
        st.write(f"**RAM total:** {system_info['ram_total']}")
        st.write(f"**RAM disponible:** {system_info['ram_available']}")

    st.sidebar.markdown("---")

    # Configuración de matrices
    st.sidebar.subheader("📊 Configuración de Matrices")

    matrix_size = st.sidebar.slider(
        "Tamaño de matriz (N x N)",
        min_value=100,
        max_value=2000,
        value=500,
        step=100,
        help="Tamaño de las matrices cuadradas a multiplicar"
    )

    st.sidebar.info(f"**Memoria estimada:** {estimate_memory_usage(matrix_size)}")

    # Configuración de paralelización
    st.sidebar.subheader("⚡ Configuración de Paralelización")

    workers_options = get_recommended_workers()
    selected_workers = st.sidebar.multiselect(
        "Número de workers a probar",
        options=workers_options,
        default=workers_options,
        help="Selecciona los números de workers para comparar"
    )

    if not selected_workers:
        st.sidebar.error("Selecciona al menos un número de workers")
        return

    parallel_method = st.sidebar.selectbox(
        "Método de paralelización",
        options=["Multiprocessing", "Threading", "ProcessPoolExecutor"],
        index=0,
        help="Método de paralelización a utilizar"
    )

    # Semilla para reproducibilidad
    use_seed = st.sidebar.checkbox("Usar semilla aleatoria fija", value=True)
    seed = 42 if use_seed else None

    st.sidebar.markdown("---")

    # Botón para ejecutar
    run_button = st.sidebar.button("🚀 Ejecutar Multiplicación", type="primary",
                                    use_container_width=True)

    # Tabs principales
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Resultados",
        "📈 Análisis de Amdahl",
        "🏛️ Taxonomía de Flynn",
        "ℹ️ Información"
    ])

    # Tab 1: Resultados de ejecución
    with tab1:
        if run_button:
            execute_multiplication(matrix_size, selected_workers, parallel_method, seed)
        else:
            st.info("👈 Configura los parámetros en el panel lateral y presiona 'Ejecutar Multiplicación'")

    # Tab 2: Análisis de Amdahl
    with tab2:
        display_amdahl_analysis(selected_workers)

    # Tab 3: Taxonomía de Flynn
    with tab3:
        display_flynn_taxonomy()

    # Tab 4: Información
    with tab4:
        display_information()


def execute_multiplication(matrix_size: int, workers_list: list, method: str, seed: int):
    """
    Ejecuta la multiplicación de matrices y muestra resultados.

    Args:
        matrix_size: Tamaño de las matrices
        workers_list: Lista de números de workers
        method: Método de paralelización
        seed: Semilla aleatoria
    """
    st.markdown('<p class="section-header">🔄 Ejecutando Multiplicación de Matrices</p>',
                unsafe_allow_html=True)

    # Generar matrices
    with st.spinner("Generando matrices aleatorias..."):
        matrix_a = MatrixOperations.generate_random_matrix(matrix_size, matrix_size, seed)
        matrix_b = MatrixOperations.generate_random_matrix(matrix_size, matrix_size, seed)

    # Información de matrices
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tamaño de Matriz A", format_matrix_size(matrix_size))
    with col2:
        st.metric("Tamaño de Matriz B", format_matrix_size(matrix_size))
    with col3:
        st.metric("Tamaño de Resultado", format_matrix_size(matrix_size))

    st.markdown("---")

    # Ejecución secuencial
    st.subheader("1️⃣ Ejecución Secuencial (Baseline)")
    with st.spinner("Ejecutando versión secuencial..."):
        result_seq, time_seq = MatrixOperations.sequential_multiply(matrix_a, matrix_b)

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"✅ **Tiempo secuencial:** {PerformanceMetrics.format_time(time_seq)}")
    with col2:
        st.info(f"**Workers:** 1 (sin paralelización)")

    st.markdown("---")

    # Ejecución paralela
    st.subheader(f"2️⃣ Ejecución Paralela - {method}")

    results = {}
    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, num_workers in enumerate(sorted(workers_list)):
        status_text.text(f"Procesando con {num_workers} workers...")

        with st.spinner(f"Ejecutando con {num_workers} workers..."):
            if method == "Multiprocessing":
                _, time_parallel = ParallelProcessor.parallel_multiply_processes(
                    matrix_a, matrix_b, num_workers
                )
            elif method == "Threading":
                _, time_parallel = ParallelProcessor.parallel_multiply_threads(
                    matrix_a, matrix_b, num_workers
                )
            else:  # ProcessPoolExecutor
                _, time_parallel = ParallelProcessor.parallel_multiply_executor(
                    matrix_a, matrix_b, num_workers
                )

        results[num_workers] = time_parallel
        progress_bar.progress((idx + 1) / len(workers_list))

    status_text.text("¡Ejecución completada!")
    st.success("✅ Todas las ejecuciones paralelas completadas")

    st.markdown("---")

    # Análisis de resultados
    st.subheader("3️⃣ Análisis de Resultados")

    analysis = PerformanceMetrics.analyze_results(time_seq, results)

    # Tabla de resultados
    st.markdown("**📋 Tabla de Resultados:**")

    df_results = pd.DataFrame({
        'Workers': [1] + list(results.keys()),
        'Tiempo (s)': [time_seq] + [results[w] for w in sorted(results.keys())],
        'Speedup': [1.0] + [analysis['speedups'][w] for w in sorted(results.keys())],
        'Eficiencia (%)': [100.0] + [analysis['efficiencies'][w] * 100 for w in sorted(results.keys())]
    })

    st.dataframe(df_results.style.format({
        'Tiempo (s)': '{:.6f}',
        'Speedup': '{:.3f}',
        'Eficiencia (%)': '{:.2f}'
    }), use_container_width=True)

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        # Gráfico de tiempos
        fig_time = go.Figure()
        fig_time.add_trace(go.Bar(
            x=['Secuencial'] + [f'{w} workers' for w in sorted(results.keys())],
            y=[time_seq] + [results[w] for w in sorted(results.keys())],
            marker_color=['#ff7f0e'] + ['#1f77b4'] * len(results),
            text=[f'{t:.4f}s' for t in [time_seq] + [results[w] for w in sorted(results.keys())]],
            textposition='auto',
        ))
        fig_time.update_layout(
            title="Tiempo de Ejecución",
            xaxis_title="Configuración",
            yaxis_title="Tiempo (segundos)",
            height=400
        )
        st.plotly_chart(fig_time, use_container_width=True)

    with col2:
        # Gráfico de speedup
        fig_speedup = go.Figure()
        speedup_values = [analysis['speedups'][w] for w in sorted(results.keys())]
        fig_speedup.add_trace(go.Scatter(
            x=sorted(results.keys()),
            y=speedup_values,
            mode='lines+markers',
            marker=dict(size=10, color='#2ca02c'),
            line=dict(width=3),
            name='Speedup Real'
        ))
        # Línea ideal (speedup lineal)
        fig_speedup.add_trace(go.Scatter(
            x=sorted(results.keys()),
            y=sorted(results.keys()),
            mode='lines',
            line=dict(dash='dash', color='gray'),
            name='Speedup Ideal'
        ))
        fig_speedup.update_layout(
            title="Speedup (Aceleración)",
            xaxis_title="Número de Workers",
            yaxis_title="Speedup",
            height=400
        )
        st.plotly_chart(fig_speedup, use_container_width=True)

    # Gráfico de eficiencia
    fig_efficiency = go.Figure()
    efficiency_values = [analysis['efficiencies'][w] * 100 for w in sorted(results.keys())]
    fig_efficiency.add_trace(go.Bar(
        x=[f'{w} workers' for w in sorted(results.keys())],
        y=efficiency_values,
        marker_color=['#d62728' if e < 50 else '#ff7f0e' if e < 70 else '#2ca02c'
                      for e in efficiency_values],
        text=[f'{e:.1f}%' for e in efficiency_values],
        textposition='auto',
    ))
    fig_efficiency.update_layout(
        title="Eficiencia de Paralelización",
        xaxis_title="Configuración",
        yaxis_title="Eficiencia (%)",
        height=400
    )
    st.plotly_chart(fig_efficiency, use_container_width=True)

    # Guardar resultados en session state
    st.session_state['last_results'] = {
        'sequential_time': time_seq,
        'parallel_times': results,
        'analysis': analysis
    }


def display_amdahl_analysis(workers_list: list):
    """
    Muestra análisis de la Ley de Amdahl.

    Args:
        workers_list: Lista de números de workers
    """
    st.markdown('<p class="section-header">📈 Análisis de la Ley de Amdahl</p>',
                unsafe_allow_html=True)

    st.markdown("""
    La **Ley de Amdahl** establece el límite teórico de mejora de rendimiento al paralelizar
    un programa, considerando que siempre existe una porción secuencial no paralelizable.
    """)

    # Fórmula
    st.latex(r'''
    Speedup = \frac{1}{(1-P) + \frac{P}{N}}
    ''')

    st.markdown("""
    Donde:
    - **P** = Fracción paralelizable del programa (0 a 1)
    - **N** = Número de procesadores
    - **(1-P)** = Fracción secuencial
    """)

    st.markdown("---")

    # Calculadora interactiva
    st.subheader("🧮 Calculadora de Ley de Amdahl")

    col1, col2 = st.columns(2)

    with col1:
        parallel_fraction = st.slider(
            "Fracción Paralelizable (%)",
            min_value=0,
            max_value=100,
            value=90,
            step=5,
            help="Porcentaje del programa que puede ejecutarse en paralelo"
        ) / 100

    with col2:
        max_processors = st.slider(
            "Número máximo de procesadores",
            min_value=1,
            max_value=32,
            value=16,
            step=1
        )

    # Cálculos
    speedups_amdahl = PerformanceMetrics.calculate_amdahl_for_range(
        parallel_fraction, max_processors
    )

    max_speedup = PerformanceMetrics.calculate_max_theoretical_speedup(parallel_fraction)

    # Información
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Fracción Paralelizable", f"{parallel_fraction * 100:.0f}%")
    with col2:
        st.metric("Fracción Secuencial", f"{(1 - parallel_fraction) * 100:.0f}%")
    with col3:
        st.metric("Speedup Máximo Teórico", f"{max_speedup:.2f}x")

    # Gráfico de Amdahl
    fig_amdahl = go.Figure()

    # Diferentes fracciones paralelas
    fractions = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0]
    colors = px.colors.sequential.Viridis

    for idx, frac in enumerate(fractions):
        speedups = PerformanceMetrics.calculate_amdahl_for_range(frac, max_processors)
        fig_amdahl.add_trace(go.Scatter(
            x=list(speedups.keys()),
            y=list(speedups.values()),
            mode='lines+markers',
            name=f'P = {frac * 100:.0f}%',
            line=dict(width=2),
            marker=dict(size=6)
        ))

    # Línea ideal
    fig_amdahl.add_trace(go.Scatter(
        x=list(range(1, max_processors + 1)),
        y=list(range(1, max_processors + 1)),
        mode='lines',
        line=dict(dash='dash', color='gray', width=2),
        name='Speedup Lineal Ideal'
    ))

    fig_amdahl.update_layout(
        title="Ley de Amdahl: Speedup vs Número de Procesadores",
        xaxis_title="Número de Procesadores",
        yaxis_title="Speedup",
        height=500,
        hovermode='x unified'
    )

    st.plotly_chart(fig_amdahl, use_container_width=True)

    st.markdown("---")

    # Respuestas a preguntas del ejercicio
    st.subheader("📝 Respuestas al Ejercicio")

    st.markdown("#### Pregunta: Según la Ley de Amdahl, ¿cuál es el rendimiento con paralelismo del 60% y 90%?")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🔵 Paralelismo del 60% (P = 0.6)**")
        speedups_60 = PerformanceMetrics.calculate_amdahl_for_range(0.6, 8)
        df_60 = pd.DataFrame({
            'Procesadores': list(speedups_60.keys()),
            'Speedup Teórico': list(speedups_60.values())
        })
        st.dataframe(df_60.style.format({'Speedup Teórico': '{:.3f}x'}),
                     use_container_width=True)

        max_speedup_60 = PerformanceMetrics.calculate_max_theoretical_speedup(0.6)
        st.info(f"**Speedup máximo teórico:** {max_speedup_60:.3f}x (con infinitos procesadores)")

    with col2:
        st.markdown("**🟢 Paralelismo del 90% (P = 0.9)**")
        speedups_90 = PerformanceMetrics.calculate_amdahl_for_range(0.9, 8)
        df_90 = pd.DataFrame({
            'Procesadores': list(speedups_90.keys()),
            'Speedup Teórico': list(speedups_90.values())
        })
        st.dataframe(df_90.style.format({'Speedup Teórico': '{:.3f}x'}),
                     use_container_width=True)

        max_speedup_90 = PerformanceMetrics.calculate_max_theoretical_speedup(0.9)
        st.info(f"**Speedup máximo teórico:** {max_speedup_90:.3f}x (con infinitos procesadores)")

    # Comparación con resultados reales
    if 'last_results' in st.session_state:
        st.markdown("---")
        st.subheader("🔍 Comparación: Teórico vs Real")

        real_speedups = st.session_state['last_results']['analysis']['speedups']

        comparison_data = []
        for num_workers in sorted(real_speedups.keys()):
            comparison_data.append({
                'Workers': num_workers,
                'Speedup Real': real_speedups[num_workers],
                'Amdahl 60%': speedups_60.get(num_workers, 0),
                'Amdahl 90%': speedups_90.get(num_workers, 0)
            })

        df_comparison = pd.DataFrame(comparison_data)

        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Scatter(
            x=df_comparison['Workers'],
            y=df_comparison['Speedup Real'],
            mode='lines+markers',
            name='Speedup Real',
            line=dict(width=3, color='#1f77b4'),
            marker=dict(size=10)
        ))
        fig_comparison.add_trace(go.Scatter(
            x=df_comparison['Workers'],
            y=df_comparison['Amdahl 60%'],
            mode='lines+markers',
            name='Amdahl 60%',
            line=dict(dash='dash', color='#ff7f0e')
        ))
        fig_comparison.add_trace(go.Scatter(
            x=df_comparison['Workers'],
            y=df_comparison['Amdahl 90%'],
            mode='lines+markers',
            name='Amdahl 90%',
            line=dict(dash='dash', color='#2ca02c')
        ))

        fig_comparison.update_layout(
            title="Comparación: Speedup Real vs Predicciones de Amdahl",
            xaxis_title="Número de Workers",
            yaxis_title="Speedup",
            height=500
        )

        st.plotly_chart(fig_comparison, use_container_width=True)

        st.markdown(df_comparison.style.format({
            'Speedup Real': '{:.3f}x',
            'Amdahl 60%': '{:.3f}x',
            'Amdahl 90%': '{:.3f}x'
        }).to_html(), unsafe_allow_html=True)


def display_flynn_taxonomy():
    """Muestra información sobre la Taxonomía de Flynn."""
    st.markdown('<p class="section-header">🏛️ Taxonomía de Flynn</p>',
                unsafe_allow_html=True)

    flynn_info = PerformanceMetrics.get_flynn_taxonomy()

    st.markdown("#### Pregunta: ¿Qué arquitectura de Flynn se utilizó en este ejercicio?")

    # Respuesta destacada
    st.markdown(f"""
    <div class="success-box">
        <h3>✅ Respuesta: {flynn_info['classification']}</h3>
        <p><strong>{flynn_info['full_name']}</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Explicación detallada
    st.subheader("📚 ¿Qué es la Taxonomía de Flynn?")

    st.markdown("""
    La **Taxonomía de Flynn** es una clasificación de arquitecturas de computadoras basada en
    el número de flujos de instrucciones y datos concurrentes:
    """)

    # Tabla de clasificaciones
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **🔵 SISD** (Single Instruction, Single Data)
        - Computadoras secuenciales tradicionales
        - Un procesador ejecuta una instrucción sobre un dato
        - Ejemplo: Procesadores antiguos de un solo núcleo

        **🟢 SIMD** (Single Instruction, Multiple Data)
        - Misma instrucción se aplica a múltiples datos
        - Ejemplo: Procesamiento vectorial, GPUs
        """)

    with col2:
        st.markdown("""
        **🟡 MISD** (Multiple Instruction, Single Data)
        - Múltiples instrucciones sobre el mismo dato
        - Poco común en la práctica
        - Ejemplo: Sistemas tolerantes a fallos

        **🟣 MIMD** (Multiple Instruction, Multiple Data)
        - Múltiples procesadores, instrucciones y datos independientes
        - Ejemplo: Sistemas multiprocesador, clusters
        """)

    st.markdown("---")

    # Justificación para este ejercicio
    st.subheader("🎯 Justificación para Este Ejercicio")

    st.markdown(f"""
    <div class="info-box">
        <h4>¿Por qué este ejercicio es MIMD?</h4>
        <p>{flynn_info['justification']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Ejemplos de arquitecturas MIMD:**")
    for example in flynn_info['examples']:
        st.markdown(f"- {example}")

    # Diagrama visual
    st.markdown("---")
    st.subheader("📊 Diagrama de Funcionamiento")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Ejecución Secuencial (SISD):**
        ```
        CPU única
        ├── Instrucción 1 → Dato A
        ├── Instrucción 2 → Dato B
        ├── Instrucción 3 → Dato C
        └── Instrucción 4 → Dato D
        ```
        Todo se ejecuta secuencialmente en un solo núcleo.
        """)

    with col2:
        st.markdown("""
        **Ejecución Paralela (MIMD):**
        ```
        CPU 1: Instrucción A → Chunk 1
        CPU 2: Instrucción B → Chunk 2
        CPU 3: Instrucción C → Chunk 3
        CPU 4: Instrucción D → Chunk 4
        ```
        Cada CPU ejecuta diferentes instrucciones sobre diferentes datos simultáneamente.
        """)

    st.markdown("---")

    # Características del sistema usado
    st.subheader("💻 Características del Sistema Usado en Este Ejercicio")

    system_info = get_system_info()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Arquitectura", system_info['architecture'])
        st.metric("Núcleos Físicos", system_info['cpu_count_physical'])
    with col2:
        st.metric("Procesador", "Intel i5-10210U")
        st.metric("Núcleos Lógicos", system_info['cpu_count_logical'])
    with col3:
        st.metric("Clasificación Flynn", "MIMD")
        st.metric("Tecnología", "Multicore + Hyper-Threading")

    st.info("""
    **Conclusión:** El Intel Core i5-10210U con 4 núcleos físicos y 8 hilos lógicos
    (gracias a Hyper-Threading) permite ejecutar múltiples instrucciones sobre múltiples
    datos de forma simultánea, clasificándose como arquitectura **MIMD**.
    """)


def display_information():
    """Muestra información general de la aplicación."""
    st.markdown('<p class="section-header">ℹ️ Información de la Aplicación</p>',
                unsafe_allow_html=True)

    st.markdown("""
    ## 📖 Acerca de Esta Aplicación

    Esta aplicación fue desarrollada para el ejercicio de **Programación Paralela** y permite:

    ### ✨ Características Principales

    1. **Multiplicación de Matrices Paralelas**
       - Matrices cuadradas de hasta 2000x2000
       - Soporte para múltiples métodos de paralelización
       - Comparación de rendimiento en tiempo real

    2. **Análisis de Rendimiento**
       - Cálculo de Speedup (aceleración)
       - Medición de eficiencia
       - Comparación con baseline secuencial

    3. **Ley de Amdahl**
       - Cálculos teóricos de speedup máximo
       - Visualización interactiva
       - Comparación con resultados reales

    4. **Taxonomía de Flynn**
       - Clasificación de arquitectura utilizada
       - Justificación técnica
       - Ejemplos y diagramas

    ### 🛠️ Tecnologías Utilizadas

    - **Python 3.11+**
    - **Streamlit** - Framework web interactivo
    - **NumPy** - Operaciones matriciales optimizadas
    - **Multiprocessing** - Paralelización real con múltiples procesos
    - **Plotly** - Visualizaciones interactivas
    - **Pandas** - Manejo de datos tabulares
    - **psutil** - Información del sistema

    ### 📊 Métodos de Paralelización

    #### 1. Multiprocessing (Recomendado)
    - Utiliza múltiples procesos del sistema operativo
    - Verdadero paralelismo (múltiples CPUs)
    - Evita el GIL (Global Interpreter Lock) de Python
    - Mejor rendimiento para operaciones CPU-intensive

    #### 2. Threading
    - Utiliza múltiples hilos dentro de un proceso
    - Limitado por el GIL en Python
    - Incluido para comparación educativa
    - Puede ser útil para operaciones I/O-bound

    #### 3. ProcessPoolExecutor
    - API moderna para manejo de procesos
    - Similar a Multiprocessing pero con interfaz más limpia
    - Parte del módulo concurrent.futures

    ### 🎯 Objetivos del Ejercicio

    ✅ Implementar multiplicación de matrices paralela
    ✅ Variar el número de hilos/procesos
    ✅ Identificar la arquitectura según Flynn (MIMD)
    ✅ Calcular rendimiento según Ley de Amdahl (60% y 90%)
    ✅ Comparar rendimiento teórico vs real

    ### 📚 Referencias

    - **Ley de Amdahl**: Gene Amdahl (1967) - "Validity of the single processor approach
      to achieving large scale computing capabilities"
    - **Taxonomía de Flynn**: Michael J. Flynn (1966) - Clasificación de arquitecturas
      de computadoras paralelas
    - **NumPy Documentation**: https://numpy.org/doc/
    - **Python Multiprocessing**: https://docs.python.org/3/library/multiprocessing.html

    ### 👨‍💻 Autor

    Desarrollado como ejercicio académico de Programación Paralela.

    ### 📝 Notas Importantes

    - Para matrices muy grandes (>1500x1500), el tiempo de ejecución puede ser considerable
    - El speedup real puede variar dependiendo de la carga del sistema
    - Se recomienda cerrar otras aplicaciones para obtener mediciones más precisas
    - Los resultados pueden variar entre ejecuciones debido a factores del sistema operativo

    ### 🚀 Cómo Usar

    1. Ajusta el tamaño de matriz en el panel lateral
    2. Selecciona los números de workers a probar
    3. Elige el método de paralelización
    4. Presiona "Ejecutar Multiplicación"
    5. Revisa los resultados en las diferentes pestañas
    """)


if __name__ == "__main__":
    main()
