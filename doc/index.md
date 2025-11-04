# Tarea 1 

> Requiere Python 3.11 o superior y la dependencia `rich`.

## 1. Modelo Diccionario
El “Diccionario” es una idea general: una colección de palabras donde se puede:
- agregar (`inserte`)
- quitar (`borre`)
- preguntar si existe (`miembro`)
- vaciar todo (`limpie`)
- imprimir su contenido (`imprima` / `__str__`)

Estas operaciones se implementan con diferentes estructuras internas (listas u hash) pero la interfaz es la misma.

Funciones (métodos abstractos definidos en `diccionario.py`):
- `inserte(elem)`: guarda el elemento.
- `borre(elem)`: intenta borrar una sola copia.
- `miembro(elem)`: True si está, False si no.
- `limpie()`: deja el diccionario vacío.
- `imprima()`: muestra el contenido en pantalla.
- `__str__()`: devuelve el contenido como texto.

---
## 2. Lista Ordenada (idea genérica)
Es una secuencia que siempre está ORDENADA de menor a mayor (orden alfabético en nuestro caso). Cuando insertas algo, se coloca en el lugar correcto para mantener el orden. Se permiten duplicados (los iguales quedan juntos).

Operaciones típicas:
- Insertar: buscar dónde va y ponerlo ahí.
- Borrar: encontrar la primera copia y quitarla.
- Miembro: recorrer hasta encontrarlo (o saber que no está).
- Imprimir: mostrar todos en orden.

Desventaja: insertar o borrar en el medio puede ser lento porque hay que recorrer o mover cosas.

---
## 3. Lista Ordenada Dinámica (por punteros)
Cómo está hecha: es una lista simplemente enlazada. Cada nodo guarda:
- el dato (una hilera)
- un “puntero” (referencia) al siguiente nodo


Flujo de las funciones principales (`listaordenadadinamica.py`):
- `inserte(x)`: recorre desde el inicio hasta encontrar el primer elemento MAYOR que `x`. Inserta antes de ese. Si hay iguales, el nuevo va después de los existentes.
- `borre(x)`: recorre hasta pasar donde debería estar; si lo encuentra, ajusta el puntero para “saltar” ese nodo.
- `miembro(x)`: similar al borrado pero solo devuelve True/False.
- `limpie()`: hace que el centinela deje de apuntar a la lista (se descartan los nodos).
- `imprima() / __str__()`: recorre y arma una lista `[a, b, c]`.

Características:
- Inserción y borrado no mueven bloques grandes de memoria (solo re-enlazan nodos).
- Acceder al elemento n requiere recorrer (no hay índices directos).

---
## 4. Lista Ordenada Estática (por arreglo)
Cómo está hecha: un arreglo (lista Python) de tamaño fijo elegido al crearla. Lleva un contador de cuántos elementos reales hay.

Funciones principales (`listaordenadaestatica.py`):
- `inserte(x)`: usa búsqueda binaria para encontrar dónde debe ir (posición después de duplicados). Luego mueve a la derecha los que siguen y coloca `x` (si hay espacio). Si está llena, la inserción se ignora.
- `borre(x)`: búsqueda binaria para localizar la primera copia, la elimina y corre a la izquierda lo que estaba después.
- `miembro(x)`: búsqueda binaria, retorna True si está.
- `limpie()`: pone el contador en 0.
- `imprima()/__str__()`: muestra los primeros n elementos en orden.

Características:
- Buscar es rápido (búsqueda binaria).
- Insertar y borrar pueden ser costosos porque hay que mover elementos.
- Tiene capacidad limitada (no crece sola).

---
## 5. Tabla Hash (idea genérica)
Objetivo: acceder (insertar, buscar, borrar) muy rápido en promedio. Para eso:
- Se calcula un número (hash) a partir del texto.
- Ese número indica un “bucket” (una posición) donde se guarda.
- Si dos palabras caen en el mismo bucket → “colisión”.

Necesitamos:
- Buena función hash (distribuya parejo).
- Controlar el factor de carga (que no haya demasiados en cada bucket).
- Redistribuir (rehash) cuando crece mucho.

---
## 6. Tabla Hash Abierta (nuestra implementación)
Cómo está hecha (`tablahashabierta.py`):
- Arreglo de buckets; cada bucket es una lista Python.
- Duplicados: se agregan al final de su bucket.
- Factor de carga = elementos_totales / número_de_buckets.
- Si factor de carga > 0.75 → se crea un arreglo más grande y se reubican todos (rehash).

Funciones:
- `inserte(x)`: calcula índice, mete `x` al bucket, y revisa si necesita rehash.
- `borre(x)`: busca en su bucket y elimina la primera coincidencia.
- `miembro(x)`: revisa el bucket por esa palabra.
- `limpie()`: reinicia todos los buckets a listas vacías (mantiene capacidad actual).
- `imprima()/__str__()`: junta todos los elementos, los ordena y los muestra (para que la salida sea legible).

Características:
- Muy rápido en promedio (O(1)).
- Peor caso: si todos caen en el mismo bucket → se vuelve una lista (O(n)).

---
## 7. Función Hash (evaluación de su aleatoriedad)
Función usada (idea):
```
h = 0
por cada caracter ch en la hilera:
	h = h * 257 + código_ASCII(ch)
	(se mantiene en 32 bits)
indice = h % tamaño_tabla
```
Por qué así:
- Multiplicar por 257 y sumar mezcla bien las letras.
- 257 > 256 (número de valores byte) ayuda a distribuir.
- Es determinística (mismo texto → mismo índice siempre).

Aleatoriedad básica:
- Para muchas cadenas distintas se reparte “bastante” uniforme.
- Si se necesitara medir: contar elementos por bucket y ver que no haya buckets gigantes frente a otros vacíos.

---
## 8. Proceso de redistribución y evaluación del tiempo
Cuándo se hace: si `carga > 0.75`.
Pasos:
1. Se duplica (aprox.) el número de buckets y se busca el siguiente número primo.
2. Se crea una nueva lista de buckets vacíos.
3. Se recalcula el índice de cada elemento y se vuelve a insertar.

Costo:
- Un rehash cuesta O(n) porque todos se reubican.
- Pero no pasa todo el tiempo, así que la *inserción promedio* sigue siendo rápida (O(1) amortizado).

Si se quisiera medir el tiempo: tomar la hora antes y después del rehash y dividir entre los elementos reinsertados.

---
## 9. Árbol Binario de Búsqueda (ABB)
Un ABB mantiene la propiedad de orden: para cada nodo, toda rama del subárbol izquierdo es menor y toda rama del subárbol derecho es mayor. Esto permite búsquedas, inserciones y borrados eficientes mientras el árbol esté balanceado.

Operaciones típicas:
- `inserte`: compara desde la raíz y baja a izquierda/derecha hasta encontrar un lugar vacío (`None`); ahí crea el nuevo nodo. Si la clave ya existe se ignora para evitar duplicados.
- `miembro`: mismo recorrido que inserte, devolviendo `True` si encuentra la clave.
- `borre`: al localizar el nodo puede tener (a) 0 hijos → se elimina directo; (b) 1 hijo → se reemplaza por el hijo; (c) 2 hijos → se reemplaza por el sucesor in-order (el menor del subárbol derecho).

Complejidad aproximada:
- Promedio: O(log n) para inserción/borrado/búsqueda (asumiendo árbol razonablemente balanceado).
- Peor caso: O(n) si se desbalancea (por ejemplo, claves insertadas en orden ascendente).

Recorridos importantes:
- **In-order** (izquierdo → nodo → derecho) entrega las claves en orden ascendente.
- **Pre-order** y **post-order** ayudan a clonar o liberar el árbol.

### 9.1 ABB por punteros (`AbbPunteros`)
- Implementación con nodos enlazados (`_NodoAbb`) que almacenan `clave`, `izquierdo` y `derecho`.
- `inserte` y `borre` re-enlazan referencias manteniendo la propiedad del ABB.
- `__str__/imprima` usan un recorrido in-order para mostrar `[a, b, c]`.
- Ventajas: estructura flexible, no necesita un arreglo predeterminado.
- Desventajas: puede desbalancearse fácilmente y cada nodo requiere memoria extra para las referencias.

### 9.2 ABB por vector (*heap*) (`ABBVectorHeap`)
- Representa el árbol dentro de un arreglo, similar a la representación de un heap binario.
- Para índice base 0: los hijos de `i` están en `2*i + 1` y `2*i + 2` (si existen); con base 1 serían `2*i` y `2*i + 1`.
- Permite acceso por índice y favorece la localidad de referencia, pero complica el manejo de huecos al borrar y exige ampliar el arreglo cuando crece.

---
## 10. Tries (árboles de prefijos)
Un trie almacena palabras descomponiéndolas carácter por carácter. Cada arista representa una letra y cada nodo puede marcar el final de alguna palabra. Esta estructura permite búsquedas por prefijo en tiempo proporcional a la longitud de la palabra, independientemente del número total de palabras guardadas.

Operaciones básicas:
- `inserte`: recorre/crea los nodos correspondientes a cada carácter y aumenta el contador de final.
- `miembro`: recorre las letras y verifica que el nodo final tenga un contador > 0.
- `borre`: disminuye el contador; si llega a cero y el nodo no tiene hijos, se podan las ramas sobrantes.

Complejidad aproximada (con `m = len(palabra)`):
- Inserción / búsqueda / borrado: O(m)
- Impresión (`__str__`): O(n · L) donde `n` es el número de palabras y `L` la longitud promedio.

### 10.1 Trie por punteros (`TriePunteros`)
- Cada nodo es un objeto con un diccionario `hijos` y un contador `fin` de cuántas palabras terminan ahí.
- Permite duplicados almacenando el conteo en `fin`.
- Borrar incluye un paso de poda para eliminar nodos que queden sin hijos.
- Ventaja: flexibilidad total sobre el alfabeto. Desventaja: mayor sobrecarga por objetos pequeños.

### 10.2 Trie por arreglos (`TrieArreglos`)
- Mantiene arreglos paralelos: uno con diccionarios de transiciones y otro con contadores finales.
- Cada nodo se identifica por un índice entero, lo que reduce la cantidad de objetos creados.
- Permite duplicados igual que la versión por punteros.
- Ventaja: buena localidad de referencia; desventaja: requiere manejar índices y cuidar la poda manual.

---
## Resumen de operaciones por estructura
| Estructura | inserte | borre | miembro | limpie | Nota |
|-----------|---------|-------|---------|--------|------|
| Lista dinámica | O(n) | O(n) | O(n) | O(1) | Sin índice directo |
| Lista estática | O(n) | O(n) | O(log n) | O(1) | Capacidad fija |
| Tabla hash | O(1)* | O(1)* | O(1)* | O(m) | *Promedio; peor O(n) |
| ABB por punteros | O(log n) | O(log n) | O(log n) | O(1) | Puede desbalancearse |
| ABB por vector | O(log n) | O(log n) | O(log n) | O(1) | Manejo especial al borrar |
| Trie por punteros | O(m) | O(m) | O(m) | O(1) | Poda de ramas sin uso |
| Trie por arreglos | O(m) | O(m) | O(m) | O(1) | Índices enteros + diccionarios |

Duplicados: permitidos en listas, hash y tries (se lleva un contador); en los ABB se ignoran (claves únicas). Borrado: una sola ocurrencia por llamada.


## 11. Scripts de prueba manual

- `scripts/pruebas_primera_entrega.py`: verifica las estructuras de la primera etapa (listas ordenadas y tabla hash), mostrando el paso a paso u opción compacta. Puede invocarse desde el menú principal (`Pruebas por etapas -> Primera entrega`) o ejecutarse manualmente.
- `scripts/pruebas_segunda_entrega.py`: prueba ambas variantes de ABB y las dos implementaciones de trie; valida duplicados (ignorados en ABB, contados en tries), casos de borrado (hoja, 1 hijo, 2 hijos) y poda de ramas sobrantes. Disponible también desde el menú (`Pruebas por etapas -> Segunda entrega`) o por consola.

## 12. Análisis de rendimiento (Tercera Entrega)

El programa incluye un analizador de rendimiento que:

- mide tiempos promedio y desviación estándar de inserción, borrado y búsqueda;
- estima el uso de memoria por estructura; y
- genera resultados en JSON y un resumen Markdown.

Puedes ejecutarlo desde el menú principal con “Pruebas de rendimiento”, 
seleccionando modo rápido (100 y 50 000; 3 corridas) o completo (100, 50 000 y 1 000 000; 10 corridas).

Por consola:

```
py scripts/analisis_tercera_entrega.py --quick
# o completo
py scripts/analisis_tercera_entrega.py
```

Los resultados se guardan en `resultados/` con tablas por estructura y una heurística de rangos para N.







