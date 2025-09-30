# Tarea 1 

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
## Resumen de operaciones por estructura
| Estructura | inserte | borre | miembro | limpie | Nota |
|-----------|---------|-------|---------|--------|------|
| Lista dinámica | O(n) | O(n) | O(n) | O(1) | Sin índice directo |
| Lista estática | O(n) | O(n) | O(log n) | O(1) | Capacidad fija |
| Tabla hash | O(1)* | O(1)* | O(1)* | O(m) | *Promedio; peor O(n) |

Duplicados: sí en todas. Borrado: una sola ocurrencia.







