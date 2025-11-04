# Tercera Entrega — Resultados y Análisis (auto)

> Generado: 2025-11-03 13:20

## 1. Metodología de medición

- Palabras: longitud fija 20, alfabeto `a..z`.
- Operaciones medidas: inserte, borre, miembro, print (opcional), done (limpie).
- Tamaños N: 100 (pequeño), 50 000 (mediano), 1 000 000 (grande; puede requerir mucha memoria).
- Corridas: 10 por tamaño (usar `--runs 10`). Para pruebas rápidas puede usarse `--quick`.
- Ensayos por operación: 100 (promedio por corrida; configurable con `--trials`).
- Memoria: pico de asignaciones rastreadas con `tracemalloc` durante la construcción de cada estructura.

Ejecución recomendada (rápida):
```
py scripts/analisis_tercera_entrega.py --quick
```
Ejecución completa:
```
py scripts/analisis_tercera_entrega.py
```
Para incluir el tiempo de print en el tamaño grande:
```
py scripts/analisis_tercera_entrega.py --print-large
```

Los resultados se guardan en `resultados/` como JSON y Markdown (`bench_YYYYMMDD_HHMMSS.*`).

## 2. Tablas de resultados (empíricos)

> Extracto del resumen automático generado por el benchmark.

# Resultados de rendimiento (20251103_120635)

Notas: tiempos en nanosegundos promedio por operación (media de corridas).

## ListaOrdenadaDinámica

| N | insert (ns) | delete (ns) | search (ns) | print (ns) | done (ns) | mem pico (MiB) |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | 6930 ± 0 | 6480 ± 0 | 1990 ± 0 | 17200 | 2700 | 0.01 |
| 10000 | 1002560 ± 0 | 1014790 ± 0 | 240550 ± 0 | 1281200 | 339100 | 0.84 |

## ListaOrdenadaEstática

| N | insert (ns) | delete (ns) | search (ns) | print (ns) | done (ns) | mem pico (MiB) |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | 19260 ± 0 | 17150 ± 0 | 1890 ± 0 | 34200 | 17500 | 0.00 |
| 10000 | 1894040 ± 0 | 2092130 ± 0 | 3240 ± 0 | 1885300 | 1655100 | 0.15 |

## TablaHashAbierta

| N | insert (ns) | delete (ns) | search (ns) | print (ns) | done (ns) | mem pico (MiB) |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | 11240 ± 0 | 10860 ± 0 | 2210 ± 0 | 27900 | 11000 | 0.02 |
| 10000 | 881330 ± 0 | 898210 ± 0 | 3160 ± 0 | 2623900 | 1088700 | 1.53 |

## AbbPunteros

| N | insert (ns) | delete (ns) | search (ns) | print (ns) | done (ns) | mem pico (MiB) |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | 16370 ± 0 | 15780 ± 0 | 1350 ± 0 | 24800 | 3600 | 0.01 |
| 10000 | 1748220 ± 0 | 1751470 ± 0 | 3320 ± 0 | 2032000 | 433800 | 1.00 |

## ABBVectorHeap

| N | insert (ns) | delete (ns) | search (ns) | print (ns) | done (ns) | mem pico (MiB) |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | 39760 ± 0 | 112550 ± 0 | 1830 ± 0 | 40800 | 1200 | 0.64 |

## TriePunteros

| N | insert (ns) | delete (ns) | search (ns) | print (ns) | done (ns) | mem pico (MiB) |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | 225290 ± 0 | 221680 ± 0 | 1360 ± 0 | 2344000 | 66700 | 13626.68 |
| 10000 | 28417910 ± 0 | 28006500 ± 0 | 2330 ± 0 | 70401700 | 18363900 | 45.24 |

## TrieArreglos

| N | insert (ns) | delete (ns) | search (ns) | print (ns) | done (ns) | mem pico (MiB) |
|---:|---:|---:|---:|---:|---:|---:|
| 100 | 437100 ± 0 | 430800 ± 0 | 1950 ± 0 | 759900 | 386700 | 0.55 |
| 10000 | 53418770 ± 0 | 52478690 ± 0 | 2390 ± 0 | 75935500 | 6684500 | 50.44 |


## Rangos sugeridos (heurística)

Recomendaciones por rangos de N (heurística):
- ListaOrdenadaDinámica: competitivo en diccionarios pequeños (≈100).
- ListaOrdenadaEstática: competitivo en diccionarios pequeños (≈100).
- TablaHashAbierta: competitivo en diccionarios pequeños (≈100).
- AbbPunteros: competitivo en diccionarios pequeños (≈100).
- ABBVectorHeap: competitivo en diccionarios pequeños (≈100).
- TriePunteros: competitivo en diccionarios pequeños (≈100).
- TrieArreglos: competitivo en diccionarios pequeños (≈100).

### 2.1 Gráficos

> Figuras generadas automáticamente desde el JSON.

# Gráficos de rendimiento

![](../resultados/bench_20251103_120635_plots/insert_lines.png)

![](../resultados/bench_20251103_120635_plots/delete_lines.png)

![](../resultados/bench_20251103_120635_plots/search_lines.png)

![](../resultados/bench_20251103_120635_plots/done_ns_lines.png)

![](../resultados/bench_20251103_120635_plots/print_lines.png)

![](../resultados/bench_20251103_120635_plots/memory_lines.png)


## 3. Comparación con órdenes teóricas

Resume si los tiempos empíricos siguen la tendencia esperada:
- Listas: inserte/borre/miembro ≈ O(n) (líneas crecientes con N).
- Hash abierta: ≈ O(1) amortizado (prácticamente constante con N; picos por rehash).
- ABB (promedio): ≈ O(log n); peor caso ≈ O(n) si se desbalancea.
- Tries: ≈ O(m) con m = longitud de palabra (constante en este proyecto), por lo que el tiempo debe ser casi independiente de N.

Comenta también el impacto de la longitud de palabra (20) sobre tries.

## 4. Rangos sugeridos para N

## Rangos sugeridos (heurística)

Recomendaciones por rangos de N (heurística):
- ListaOrdenadaDinámica: competitivo en diccionarios pequeños (≈100).
- ListaOrdenadaEstática: competitivo en diccionarios pequeños (≈100).
- TablaHashAbierta: competitivo en diccionarios pequeños (≈100).
- AbbPunteros: competitivo en diccionarios pequeños (≈100).
- ABBVectorHeap: competitivo en diccionarios pequeños (≈100).
- TriePunteros: competitivo en diccionarios pequeños (≈100).
- TrieArreglos: competitivo en diccionarios pequeños (≈100).

## 5. Memoria utilizada

Incluye y comenta los picos de memoria por estructura en N = 100, 50 000 y 1 000 000.

- ¿Qué estructuras crecen más en memoria?
- ¿Cómo se comparan tries vs ABB vs hash?

## 6. Limitaciones

- Python y su GC pueden introducir ruido (pausas, asignaciones temporales).
- `tracemalloc` mide asignaciones de Python, no la RSS total del proceso.
- Ruido del sistema operativo y de otros procesos.
- Resolución del reloj (`perf_counter_ns`) y variabilidad entre corridas.
- Para `print` en N grandes, el costo puede estar dominado por la construcción de la cadena y la memoria necesaria.
- Hardware disponible (CPU, RAM) condiciona la viabilidad de N = 1 000 000.

## 7. Conclusiones

- Resume qué estructuras recomendarías por rango de N y por tipo de operación predominante.
- Señala sorpresas o divergencias respecto a la teoría.
- Propón trabajo futuro (por ejemplo, medir prefijos compartidos para tries o árboles balanceados como AVL/Red-Black para ABB).
