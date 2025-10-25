Proyecto Tarea 1 — Diccionarios (Estructuras de Datos)
======================================================

Requisitos
----------

- Python 3.11 o superior
- Dependencias: `rich`

Instalación
-----------

Si usas uv (recomendado):

1. Instala dependencias del proyecto.
2. Ejecuta la aplicación con:

```
python -m src
```

Ejecución rápida
----------------

En Windows PowerShell (sin instalar nada en el entorno):

```
python -m src
```

Estado actual
-------------

- Disponible: ListaOrdenadaDinámica, ListaOrdenadaEstática (capacidad configurable), TablaHashAbierta, AbbPunteros, ABBVectorHeap, TriePunteros, TrieArreglos
- En progreso: —

Uso
---

1. Selecciona “Menú diccionarios” para manipular las estructuras manualmente, o “Pruebas por etapas” para lanzar los scripts incluidos.
2. Elige la implementación (Listas, Tabla hash, ABB o Tries).
3. Usa las operaciones: Agregar, Borrar, Existencia, Imprimir, Limpiar.
	- Listas, tabla hash y tries permiten duplicados (el tamaño cuenta todas las ocurrencias).
	- En los ABB los duplicados se ignoran para mantener claves únicas.

Pruebas (Primera Entrega)
-------------------------

Se incluye un script de verificación manual para cada estructura. Puedes
ejecutarlo directo desde el menú (`Pruebas por etapas -> Primera entrega`) o
desde la terminal:

```
py scripts/pruebas_primera_entrega.py
```

Solo resultados finales sin pasos intermedios:

```
py scripts/pruebas_primera_entrega.py --sin-detalle
```

Qué valida:

- Inserciones desordenadas producen orden ascendente.
- Duplicados se conservan (listas) o se almacenan como ocurrencias separadas (hash).
- Borrado elimina una ocurrencia existente; no falla con elementos inexistentes.
- Limpieza deja la estructura vacía y permite reinserción.

Notas:
- Los scripts añaden automáticamente la raíz al `sys.path`

Pruebas (Segunda Entrega)
-------------------------

Script que verifica las dos variantes de ABB y ambas versiones de Trie (política “sin duplicados” en ABB y duplicados contados en tries). Disponible desde el menú (`Pruebas por etapas -> Segunda entrega`) o mediante consola:

```
py scripts/pruebas_segunda_entrega.py
```

Resumen compacto:

```
py scripts/pruebas_segunda_entrega.py --sin-detalle
```

Qué valida:

- Inserciones desordenadas conservan el orden in-order.
- Los duplicados se ignoran en ambos ABB.
- Borrados cubren hoja, nodo con un hijo y nodo con dos hijos.
- El `__str__` de los ABB muestra las claves ordenadas y el tamaño final coincide.
- En los tries, los duplicados incrementan el tamaño y se podan ramas cuando quedan sin hijos.
- Al finalizar, tanto ABB como tries quedan consistentes (`[]` cuando se vacían).


