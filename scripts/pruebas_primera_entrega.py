"""Pruebas de la *Primera Entrega*.

Ejecuta:
  - ListaOrdenadaDinámica
  - ListaOrdenadaEstática
  - TablaHashAbierta

Produce un resumen final con métricas simples.

Uso (desde la raíz del repositorio):
    py scripts/pruebas_primera_entrega.py
Opciones:
    --sin-detalle    Muestra solo el resumen final.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.listaordenadadinamica import ListaOrdenadaDinámica  
from src.listaordenadaestatica import ListaOrdenadaEstática  
from src.tablahashabierta import TablaHashAbierta  


class ResultadoEstructura:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.ok = True
        self.mensajes: list[str] = []
        self.final_repr: str = ""
        self.tamaño: int = 0
        # Hash extras
        self.factor_carga: float | None = None
        self.bucket_min: int | None = None
        self.bucket_max: int | None = None
        self.bucket_promedio_no_vacios: float | None = None

    def agrega(self, msg: str):
        self.mensajes.append(msg)

    def fallo(self, msg: str):
        self.ok = False
        self.mensajes.append("ERROR: " + msg)


def probar_lista_dinamica(verbose: bool = True) -> ResultadoEstructura:
    r = ResultadoEstructura("ListaOrdenadaDinámica")
    try:
        l = ListaOrdenadaDinámica()
        for x in ["b", "a", "c", "b"]:
            l.inserte(x)
        if verbose:
            r.agrega(f"Tras inserciones: {l}")
        assert str(l) == "[a, b, b, c]", "Orden / duplicados inesperados"
        assert l.miembro("a") and not l.miembro("z"), "Fallo en miembro()"
        l.borre("b")
        if verbose:
            r.agrega(f"Tras borrar 'b': {l}")
        l.borre("x")  
        l.limpie()
        assert str(l) == "[]", "Limpieza falló"
        for x in ["d", "d", "c"]:
            l.inserte(x)
        if verbose:
            r.agrega(f"Reinserciones: {l}")
        r.final_repr = str(l)
        r.tamaño = len(l)
    except AssertionError as e:
        r.fallo(str(e))
    except Exception as e:
        r.fallo(f"Excepción inesperada: {e.__class__.__name__}: {e}")
    return r


def probar_lista_estatica(verbose: bool = True) -> ResultadoEstructura:
    r = ResultadoEstructura("ListaOrdenadaEstática")
    try:
        l = ListaOrdenadaEstática(5)
        for x in ["b", "a", "c", "b"]:
            l.inserte(x)
        if verbose:
            r.agrega(f"Tras inserciones: {l}")
        assert str(l) == "['a', 'b', 'b', 'c']", "Orden / duplicados inesperados"
        assert l.miembro("c") and not l.miembro("z"), "Fallo en miembro()"
        l.borre("b")
        if verbose:
            r.agrega(f"Tras borrar 'b': {l}")
        l.borre("x")
        l.inserte("d")
        l.inserte("e")
        llenado = str(l)
        l.inserte("f")  
        if verbose:
            r.agrega(f"Capacidad llena: {llenado} -> tras intentar extra: {l}")
        l.limpie()
        assert str(l) == "[]", "Limpieza falló"
        for x in ["d", "d", "c"]:
            l.inserte(x)
        if verbose:
            r.agrega(f"Reinserciones: {l}")
        r.final_repr = str(l)
        r.tamaño = len(l)
    except AssertionError as e:
        r.fallo(str(e))
    except Exception as e:  
        r.fallo(f"Excepción inesperada: {e.__class__.__name__}: {e}")
    return r


def probar_hash_abierta(verbose: bool = True) -> ResultadoEstructura:
    r = ResultadoEstructura("TablaHashAbierta")
    try:
        t = TablaHashAbierta(11)
        for x in ["b", "a", "c", "b"]:
            t.inserte(x)
        if verbose:
            r.agrega(f"Tras inserciones: {t}")
        assert t.miembro("a") and not t.miembro("z"), "Fallo en miembro()"
        t.borre("b")
        if verbose:
            r.agrega(f"Tras borrar 'b': {t}")
        for i in range(60):
            t.inserte(f"x{i}")
        if verbose:
            r.agrega("Rehash forzado (si correspondía)")
        t.limpie()
        assert str(t) == "[]", "Limpieza falló"
        t.inserte("q")
        t.inserte("q")
        if verbose:
            r.agrega(f"Duplicados: {t}")
        r.final_repr = str(t)
        r.tamaño = len(t)
    except AssertionError as e:
        r.fallo(str(e))
    except Exception as e:  
        r.fallo(f"Excepción inesperada: {e.__class__.__name__}: {e}")
    return r


def imprimir_resultado(r: ResultadoEstructura):
    estado = "OK" if r.ok else "FALLO"
    print(f"\n=== {r.nombre} -> {estado} ===")
    for m in r.mensajes:
        print(" -", m)
    print(f" Final: {r.final_repr}  (tamaño={r.tamaño})")

def main(argv: list[str]):
    verbose = "--sin-detalle" not in argv
    if verbose:
        print("Iniciando pruebas de la Primera Entrega...\n")
    resultados: list[ResultadoEstructura] = []
    resultados.append(probar_lista_dinamica(verbose))
    resultados.append(probar_lista_estatica(verbose))
    resultados.append(probar_hash_abierta(verbose))
    if verbose:
        for r in resultados:
            imprimir_resultado(r)


if __name__ == "__main__": 
    main(sys.argv[1:])
