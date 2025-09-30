Proyecto Tarea 1 — Diccionarios (Estructuras de Datos)
======================================================

Requisitos
----------

- Python 3.13 o superior
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

- Disponible: ListaOrdenadaDinámica, ListaOrdenadaEstática (capacidad configurable), TablaHashAbierta
- En progreso: ABBPunteros, ABBVectorHeap, TriePunteros, TrieArreglos

Uso
---

1. Selecciona “Menú diccionarios”.
2. Elige la implementación (ListaOrdenadaDinámica, ListaOrdenadaEstática o TablaHashAbierta).
3. Usa las operaciones: Agregar, Borrar, Existencia, Imprimir, Limpiar.

Pruebas (Primera Entrega)
-------------------------

Se incluye un script de verificación manual para cada estructura.
El script ejecuta los tres escenarios con aserciones y muestra el estado final de cada estructura:

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


