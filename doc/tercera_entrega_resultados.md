# Tercera Entrega — Resultados y Análisis

> Proyecto: Modelo Diccionario — Comparación de E.D. (Listas, Hash, ABB, Tries)
> Fecha: (completa aquí)

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
Para incluir el tiempo de print en el tamaño grande (bajo tu propia responsabilidad):
```
py scripts/analisis_tercera_entrega.py --print-large
```

Los resultados se guardan en `resultados/` como JSON y Markdown (`bench_YYYYMMDD_HHMMSS.*`).

## 2. Tablas de resultados (empíricos)

Pega aquí las tablas del Markdown generado automáticamente (`resultados/bench_*.md`).

- ListaOrdenadaDinámica
- ListaOrdenadaEstática
- TablaHashAbierta
- AbbPunteros
- ABBVectorHeap
- TriePunteros
- TrieArreglos

(Alternativamente, enlaza el archivo generado y referencia sus secciones.)

### 2.1 Gráficos

Una vez generado el JSON con los resultados, puedes producir gráficos PNG por operación y memoria con:

```
py scripts/graficas_tercera_entrega.py --json resultados/bench_YYYYMMDD_HHMMSS.json
```

Esto creará una carpeta `resultados/bench_YYYYMMDD_HHMMSS_plots/` con imágenes y un `graficos.md` que las referencia. Inserta aquí las figuras más representativas.

## 3. Comparación con órdenes teóricas

Resume si los tiempos empíricos siguen la tendencia esperada:
- Listas: inserte/borre/miembro ≈ O(n) (líneas crecientes con N).
- Hash abierta: ≈ O(1) amortizado (prácticamente constante con N; picos por rehash).
- ABB (promedio): ≈ O(log n); peor caso ≈ O(n) si se desbalancea.
- Tries: ≈ O(m) con m = longitud de palabra (constante en este proyecto), por lo que el tiempo debe ser casi independiente de N.

Comenta también el impacto de la longitud de palabra (20) sobre tries.

## 4. Rangos sugeridos para N

El analizador genera una heurística de “rangos” basados en qué estructura resulta más rápida para cada tamaño. Pega aquí esa sección y, si es necesario, ajusta la interpretación para reflejar tus observaciones.

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
