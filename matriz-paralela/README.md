# Multiplicación de Matrices Paralelas

Aplicación web interactiva para el análisis de rendimiento de multiplicación de matrices usando paralelización con Python y Streamlit.

## Descripción

Este proyecto implementa la multiplicación de matrices de forma paralela utilizando diferentes métodos de paralelización en Python (Multiprocessing, Threading, ProcessPoolExecutor). Incluye análisis completo de rendimiento, cálculos de la Ley de Amdahl y clasificación según la Taxonomía de Flynn.

## Características Principales

- **Multiplicación de Matrices Paralelas**: Matrices cuadradas de hasta 2000x2000
- **Múltiples Métodos de Paralelización**:
  - Multiprocessing (múltiples procesos)
  - Threading (múltiples hilos)
  - ProcessPoolExecutor (API moderna)
- **Análisis de Rendimiento**:
  - Cálculo de Speedup (aceleración)
  - Medición de Eficiencia
  - Comparación con baseline secuencial
- **Ley de Amdahl**:
  - Cálculos teóricos de speedup máximo
  - Visualización interactiva
  - Comparación con resultados reales (60% y 90% paralelismo)
- **Taxonomía de Flynn**: Identificación y justificación de arquitectura MIMD
- **Visualizaciones Interactivas**: Gráficos en tiempo real con Plotly

## Requisitos del Sistema

- **Python**: 3.11 o superior
- **Sistema Operativo**: Linux, macOS o Windows
- **Procesador**: Intel Core i5-10210U (4 núcleos, 8 hilos) o equivalente
- **RAM**: Mínimo 4GB recomendado

## Instalación

### 1. Clonar o descargar el proyecto

```bash
cd matriz-paralela
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Activar en Linux/Mac:
source venv/bin/activate

# Activar en Windows:
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso

### Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Configuración

1. **Tamaño de Matriz**: Ajusta el slider para elegir el tamaño (100 a 2000)
2. **Número de Workers**: Selecciona los números de workers a probar (1, 2, 4, 8)
3. **Método de Paralelización**: Elige entre Multiprocessing, Threading o ProcessPoolExecutor
4. **Semilla Aleatoria**: Activa para resultados reproducibles

### Pestañas de la Aplicación

- **Resultados**: Ejecución de multiplicación y análisis de rendimiento
- **Análisis de Amdahl**: Cálculos teóricos y comparaciones
- **Taxonomía de Flynn**: Clasificación de arquitectura utilizada
- **Información**: Documentación y referencias

## Estructura del Proyecto

```
matriz-paralela/
├── app.py                    # Aplicación Streamlit principal
├── core/
│   ├── matrix_operations.py  # Operaciones de matrices con NumPy
│   ├── parallel_processor.py # Lógica de paralelización
│   └── performance_metrics.py # Métricas y Ley de Amdahl
├── utils/
│   └── helpers.py            # Funciones auxiliares
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
```

## Tecnologías Utilizadas

- **Python 3.11+**: Lenguaje de programación
- **Streamlit**: Framework web para aplicaciones de datos
- **NumPy**: Biblioteca para operaciones matriciales optimizadas
- **Multiprocessing**: Paralelización con múltiples procesos
- **Plotly**: Visualizaciones interactivas
- **Pandas**: Manejo de datos tabulares
- **psutil**: Información del sistema

## Respuestas a las Preguntas del Ejercicio

### a. Taxonomía de Flynn

**Respuesta: MIMD (Multiple Instruction, Multiple Data)**

**Justificación:**
En este ejercicio utilizamos arquitectura MIMD porque:
- Empleamos múltiples procesos (multiprocessing) donde cada proceso ejecuta instrucciones de forma independiente
- Cada proceso trabaja sobre diferentes chunks (porciones) de datos de forma simultánea
- El procesador Intel i5-10210U con 4 núcleos y 8 hilos permite ejecutar múltiples instrucciones sobre múltiples datos de manera concurrente
- No hay sincronización de instrucciones entre procesos (cada uno ejecuta su propia secuencia)

### b. Ley de Amdahl

**Pregunta: ¿Cuál es el rendimiento o aceleración asumiendo que el paralelismo es del 60% y 90%?**

La Ley de Amdahl establece:

```
Speedup = 1 / ((1-P) + P/N)
```

Donde:
- P = fracción paralelizable
- N = número de procesadores

**Para P = 0.6 (60% paralelizable):**

| Procesadores | Speedup Teórico |
|--------------|-----------------|
| 1            | 1.000x          |
| 2            | 1.429x          |
| 4            | 2.105x          |
| 8            | 2.759x          |

Speedup máximo teórico (∞ procesadores): **2.500x**

**Para P = 0.9 (90% paralelizable):**

| Procesadores | Speedup Teórico |
|--------------|-----------------|
| 1            | 1.000x          |
| 2            | 1.818x          |
| 4            | 3.077x          |
| 8            | 4.706x          |

Speedup máximo teórico (∞ procesadores): **10.000x**

**Conclusión:**
La porción secuencial (no paralelizable) limita significativamente el speedup máximo alcanzable. Con 60% de paralelismo, el speedup máximo es solo 2.5x, mientras que con 90% puede llegar a 10x, demostrando la importancia de minimizar la porción secuencial del código.

## Ejemplos de Resultados

### Configuración Típica
- **Matriz**: 1000x1000
- **Método**: Multiprocessing
- **Sistema**: Intel i5-10210U (4 cores, 8 threads)

### Resultados Esperados
- **Secuencial**: ~2.5 segundos
- **2 workers**: ~1.4 segundos (speedup: 1.8x)
- **4 workers**: ~0.9 segundos (speedup: 2.8x)
- **8 workers**: ~0.7 segundos (speedup: 3.5x)

*Nota: Los resultados varían según la carga del sistema y otras aplicaciones en ejecución*

## Notas Importantes

1. **Tamaño de Matrices**: Para matrices muy grandes (>1500x1500), el tiempo de ejecución puede ser considerable
2. **Variabilidad de Resultados**: El speedup real puede variar dependiendo de la carga del sistema
3. **Cierre de Aplicaciones**: Se recomienda cerrar otras aplicaciones para obtener mediciones más precisas
4. **Threading vs Multiprocessing**: Threading no muestra speedup real en Python debido al GIL (Global Interpreter Lock)
5. **Memoria**: Asegúrate de tener suficiente RAM para matrices grandes (2000x2000 usa ~45MB)

## Optimizaciones Aplicadas

1. **NumPy Optimizado**: Uso de `np.matmul()` que está altamente optimizado con BLAS/LAPACK
2. **División de Trabajo**: Las matrices se dividen en chunks horizontales para distribución equitativa
3. **Process Pooling**: Reutilización de procesos para evitar overhead de creación
4. **Medición Precisa**: Uso de `time.perf_counter()` para alta precisión temporal

## Troubleshooting

### Error: "ModuleNotFoundError"
```bash
# Asegúrate de instalar todas las dependencias
pip install -r requirements.txt
```

### Error: "Port 8501 already in use"
```bash
# Usa un puerto diferente
streamlit run app.py --server.port 8502
```

### Aplicación muy lenta
- Reduce el tamaño de matriz
- Cierra otras aplicaciones
- Verifica que estés usando Multiprocessing (no Threading)

### Errores de memoria
- Reduce el tamaño de matriz
- Cierra otras aplicaciones que consuman RAM

## Referencias

- **Ley de Amdahl**: Gene Amdahl (1967) - "Validity of the single processor approach to achieving large scale computing capabilities"
- **Taxonomía de Flynn**: Michael J. Flynn (1966) - Clasificación de arquitecturas paralelas
- **NumPy Documentation**: https://numpy.org/doc/
- **Python Multiprocessing**: https://docs.python.org/3/library/multiprocessing.html
- **Streamlit Documentation**: https://docs.streamlit.io/

## Autor

Desarrollado como ejercicio académico de Programación Paralela.

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo.
