# Respuestas al Ejercicio de Programación Paralela

## Ejercicio de Matrices: Multiplicación Paralela

### Implementación Realizada

Se desarrolló una aplicación completa de multiplicación de matrices paralelas con las siguientes características:

- **Lenguaje**: Python 3.11+
- **Framework Web**: Streamlit
- **Paralelización**: Multiprocessing, Threading, ProcessPoolExecutor
- **Tamaño de matrices**: Variable de 100x100 hasta 2000x2000
- **Número de hilos/procesos**: Configurable (1, 2, 4, 8, 16)

### Configuración del Sistema Usado

```
Procesador: Intel(R) Core(TM) i5-10210U CPU @ 1.60GHz
Arquitectura: x86_64
Núcleos físicos: 4
Núcleos lógicos: 8 (con Hyper-Threading)
CPU MHz máx.: 4200.0000
CPU MHz mín.: 400.0000
Familia de CPU: 6
Modelo: 142
```

---

## Pregunta a: Taxonomía de Flynn

### ¿Qué arquitectura según la taxonomía de Flynn se utilizó en este ejercicio?

**Respuesta: MIMD (Multiple Instruction, Multiple Data)**

### Clasificación Completa

La **Taxonomía de Flynn** clasifica las arquitecturas de computadoras según el número de flujos de instrucciones y datos concurrentes:

| Clasificación | Nombre Completo | Descripción |
|---------------|-----------------|-------------|
| **SISD** | Single Instruction, Single Data | Una instrucción, un dato (secuencial tradicional) |
| **SIMD** | Single Instruction, Multiple Data | Una instrucción sobre múltiples datos (vectorización) |
| **MISD** | Multiple Instruction, Single Data | Múltiples instrucciones sobre un dato (poco común) |
| **MIMD** | Multiple Instruction, Multiple Data | Múltiples instrucciones sobre múltiples datos (paralelo) |

### Justificación Técnica

Este ejercicio utiliza arquitectura **MIMD** por las siguientes razones:

1. **Múltiples Procesos Independientes**
   - Se utilizó `multiprocessing.Pool` de Python que crea múltiples procesos del sistema operativo
   - Cada proceso tiene su propio espacio de memoria y ejecuta código de forma independiente

2. **Diferentes Instrucciones**
   - Cada proceso ejecuta su propia secuencia de instrucciones
   - No hay sincronización de instrucciones entre procesos
   - Cada worker puede estar en diferentes puntos de ejecución simultáneamente

3. **Diferentes Datos**
   - La matriz A se divide en chunks (porciones) horizontales
   - Cada proceso trabaja sobre un chunk diferente de datos
   - Proceso 1 trabaja con filas 0-250, Proceso 2 con 251-500, etc.

4. **Hardware Multicore**
   - El Intel i5-10210U tiene 4 núcleos físicos y 8 hilos lógicos
   - Cada núcleo puede ejecutar diferentes instrucciones de forma simultánea
   - El sistema operativo distribuye los procesos entre los núcleos disponibles

### Ejemplo Práctico

```
Matriz A (1000x1000) dividida en 4 chunks:

┌─────────────────┐
│ Chunk 1 (0-250) │ → Proceso 1 en CPU 0: Ejecuta multiplicación con instrucciones propias
├─────────────────┤
│ Chunk 2(251-500)│ → Proceso 2 en CPU 1: Ejecuta multiplicación con instrucciones propias
├─────────────────┤
│ Chunk 3(501-750)│ → Proceso 3 en CPU 2: Ejecuta multiplicación con instrucciones propias
├─────────────────┤
│ Chunk 4(751-1000)│ → Proceso 4 en CPU 3: Ejecuta multiplicación con instrucciones propias
└─────────────────┘
```

Cada CPU ejecuta:
- **Diferentes instrucciones**: Cada proceso está en diferente punto de su código
- **Diferentes datos**: Cada proceso opera sobre diferentes filas de la matriz
- **Simultáneamente**: Todos los CPUs trabajan al mismo tiempo

### Comparación con Otras Arquitecturas

**¿Por qué NO es SIMD?**
- En SIMD, una misma instrucción se aplica a múltiples datos simultáneamente
- Ejemplo: Instrucción vectorial `ADD` que suma 8 números al mismo tiempo
- En nuestro caso, cada proceso ejecuta su propia secuencia de instrucciones

**¿Por qué NO es SISD?**
- SISD es ejecución secuencial (un solo procesador)
- No hay paralelismo real
- Todo se ejecuta uno después del otro

**¿Por qué NO es MISD?**
- MISD ejecuta múltiples instrucciones sobre el MISMO dato
- Es muy poco común en la práctica
- Nuestro ejercicio usa datos diferentes para cada proceso

### Conclusión

El ejercicio implementado utiliza **arquitectura MIMD** ya que emplea múltiples procesos que ejecutan diferentes instrucciones sobre diferentes porciones de datos de forma simultánea en un procesador multicore. Esta es la arquitectura más común en sistemas paralelos modernos.

---

## Pregunta b: Ley de Amdahl

### ¿Cuál es el rendimiento o aceleración asumiendo que el paralelismo es del 60% y 90%?

### Fórmula de la Ley de Amdahl

```
Speedup = 1 / ((1-P) + P/N)
```

Donde:
- **P** = Fracción del programa que es paralelizable (0 a 1)
- **N** = Número de procesadores
- **(1-P)** = Fracción secuencial del programa

### Speedup Máximo Teórico

Con infinitos procesadores:
```
Speedup_máx = 1 / (1-P)
```

---

### Caso 1: Paralelismo del 60% (P = 0.6)

**Fracción paralelizable**: 60%
**Fracción secuencial**: 40%

#### Tabla de Resultados

| Número de Procesadores | Speedup Teórico | Cálculo Detallado |
|-------------------------|-----------------|-------------------|
| **1** | 1.000x | 1 / ((1-0.6) + 0.6/1) = 1 / 1 = 1.000 |
| **2** | 1.429x | 1 / ((1-0.6) + 0.6/2) = 1 / 0.7 = 1.429 |
| **4** | 2.105x | 1 / ((1-0.6) + 0.6/4) = 1 / 0.55 = 2.105 |
| **8** | 2.759x | 1 / ((1-0.6) + 0.6/8) = 1 / 0.475 = 2.759 |
| **16** | 3.200x | 1 / ((1-0.6) + 0.6/16) = 1 / 0.4375 = 3.200 |
| **∞** | **2.500x** | 1 / (1-0.6) = 1 / 0.4 = **2.500** |

#### Análisis

- Con 2 procesadores: Aceleración de **1.43x** (43% más rápido)
- Con 4 procesadores: Aceleración de **2.11x** (2.11 veces más rápido)
- Con 8 procesadores: Aceleración de **2.76x** (cercano al límite)
- **Límite máximo**: **2.5x** (incluso con infinitos procesadores)

**Conclusión**: Con 60% de paralelismo, el speedup máximo alcanzable es solo **2.5x**, sin importar cuántos procesadores se agreguen. La porción secuencial del 40% limita severamente el rendimiento.

---

### Caso 2: Paralelismo del 90% (P = 0.9)

**Fracción paralelizable**: 90%
**Fracción secuencial**: 10%

#### Tabla de Resultados

| Número de Procesadores | Speedup Teórico | Cálculo Detallado |
|-------------------------|-----------------|-------------------|
| **1** | 1.000x | 1 / ((1-0.9) + 0.9/1) = 1 / 1 = 1.000 |
| **2** | 1.818x | 1 / ((1-0.9) + 0.9/2) = 1 / 0.55 = 1.818 |
| **4** | 3.077x | 1 / ((1-0.9) + 0.9/4) = 1 / 0.325 = 3.077 |
| **8** | 4.706x | 1 / ((1-0.9) + 0.9/8) = 1 / 0.2125 = 4.706 |
| **16** | 6.400x | 1 / ((1-0.9) + 0.9/16) = 1 / 0.15625 = 6.400 |
| **∞** | **10.000x** | 1 / (1-0.9) = 1 / 0.1 = **10.000** |

#### Análisis

- Con 2 procesadores: Aceleración de **1.82x** (82% más rápido)
- Con 4 procesadores: Aceleración de **3.08x** (3 veces más rápido)
- Con 8 procesadores: Aceleración de **4.71x** (casi 5 veces más rápido)
- **Límite máximo**: **10.0x** (con infinitos procesadores)

**Conclusión**: Con 90% de paralelismo, se puede lograr un speedup mucho mejor. Con 8 procesadores se alcanza **4.71x**, y el límite máximo teórico es **10x**.

---

### Comparación: 60% vs 90% de Paralelismo

| Procesadores | Speedup 60% | Speedup 90% | Diferencia |
|--------------|-------------|-------------|------------|
| 2 | 1.429x | 1.818x | +27% |
| 4 | 2.105x | 3.077x | +46% |
| 8 | 2.759x | 4.706x | +71% |
| ∞ (máximo) | 2.500x | 10.000x | +300% |

### Gráfica Conceptual

```
Speedup vs Número de Procesadores

10 ┤                                              ╭─────── P=90%
   │                                          ╭───╯
 8 ┤                                     ╭────╯
   │                                 ╭───╯
 6 ┤                            ╭────╯
   │                       ╭────╯
 4 ┤                  ╭────╯
   │             ╭────╯
 2 ┤        ╭────╯..................╭─────────── P=60%
   │   ╭────╯                  ╭───╯
 0 ┼───┴────────┴────────┴────────┴────────┴────
   0   2        4        8        16       ∞
              Número de Procesadores
```

---

### Resultados Reales del Sistema (Intel i5-10210U)

#### Configuración de Prueba
- **Matriz**: 1000x1000
- **Método**: Multiprocessing
- **Sistema**: Intel i5-10210U (4 cores físicos, 8 threads lógicos)

#### Resultados Típicos Esperados

| Workers | Tiempo Esperado | Speedup Real | Eficiencia |
|---------|-----------------|--------------|------------|
| 1 (seq) | ~2.5s | 1.00x | 100% |
| 2 | ~1.4s | ~1.8x | 90% |
| 4 | ~0.9s | ~2.8x | 70% |
| 8 | ~0.7s | ~3.5x | 44% |

#### Comparación con Amdahl

Los resultados reales típicamente están entre las predicciones de 60% y 90% de paralelismo, porque:

1. **Overhead de paralelización**:
   - Creación de procesos
   - Comunicación entre procesos
   - División y combinación de datos

2. **Contención de recursos**:
   - Cache compartido
   - Ancho de banda de memoria
   - Hyper-Threading no duplica rendimiento

3. **Porción secuencial real**:
   - Generación de matrices
   - División de datos
   - Combinación de resultados

---

### Implicaciones Prácticas

#### Lección 1: La Porción Secuencial Es Crítica

Reducir la porción secuencial del 40% al 10% (60%→90% paralelismo) aumenta el speedup máximo de **2.5x** a **10x** - ¡un incremento del 300%!

#### Lección 2: Límite de Rendimiento

No importa cuántos procesadores agreguemos, **nunca** superaremos:
- **2.5x** con 60% paralelismo
- **10x** con 90% paralelismo

#### Lección 3: Rendimientos Decrecientes

Después de 8 procesadores con 60% paralelismo, agregar más procesadores da muy poco beneficio adicional (ya se está cerca del límite de 2.5x).

#### Lección 4: Optimización del Código Secuencial

Es más efectivo **reducir la porción secuencial** que agregar más procesadores. Optimizar el código secuencial del 40% al 10% da más beneficio que multiplicar por 10 el número de procesadores.

---

### Fórmulas de Referencia

#### Speedup
```
S(N) = 1 / ((1-P) + P/N)
```

#### Eficiencia
```
E(N) = S(N) / N
```

#### Speedup Máximo
```
S_max = 1 / (1-P)
```

#### Tiempo Paralelo
```
T_parallel = T_serial * ((1-P) + P/N)
```

---

### Conclusión Final

**Para el sistema Intel i5-10210U con 8 hilos lógicos:**

1. **Con paralelismo del 60%**:
   - Speedup máximo teórico: **2.76x** con 8 procesadores
   - Speedup absoluto máximo: **2.5x** (límite de Amdahl)
   - La porción secuencial (40%) limita severamente el rendimiento

2. **Con paralelismo del 90%**:
   - Speedup máximo teórico: **4.71x** con 8 procesadores
   - Speedup absoluto máximo: **10x** (límite de Amdahl)
   - Rendimiento mucho mejor gracias a menor porción secuencial (10%)

3. **Recomendación práctica**:
   - Con 4 núcleos físicos: Usar 4 procesos (uno por núcleo)
   - Con 8 hilos lógicos: Usar hasta 8 procesos con rendimientos decrecientes
   - Optimizar código secuencial es más efectivo que agregar procesadores

La **Ley de Amdahl** demuestra que el speedup está fundamentalmente limitado por la porción secuencial del código, haciendo que la optimización del código secuencial sea tan importante como la paralelización.

---

## Referencias

- Amdahl, Gene M. (1967). "Validity of the single processor approach to achieving large scale computing capabilities". AFIPS Conference Proceedings (30): 483-485.
- Flynn, Michael J. (1972). "Some Computer Organizations and Their Effectiveness". IEEE Transactions on Computers. C-21 (9): 948-960.
- Intel® Core™ i5-10210U Processor Specifications
- Python multiprocessing documentation: https://docs.python.org/3/library/multiprocessing.html
