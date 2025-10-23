"""Pruebas de la *Segunda Entrega*.

Ejecuta:
    - AbbPunteros
    - ABBVectorHeap
    - TriePunteros
    - TrieArreglos

Produce un resumen final con métricas simples.

Uso (desde la raíz del repositorio):
    py scripts/pruebas_segunda_entrega.py
Opciones:
    --sin-detalle    Muestra solo el resumen final.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.abbpunteros import AbbPunteros
from src.abbvectorheap import ABBVectorHeap
from src.triearreglos import TrieArreglos
from src.triepunteros import TriePunteros


@dataclass
class ResultadoEstructura:
    nombre: str
    ok: bool = True
    mensajes: list[str] = None
    final_repr: str = ""
    tamaño: int = 0

    def __post_init__(self) -> None:
        if self.mensajes is None:
            self.mensajes = []

    def agrega(self, msg: str) -> None:
        self.mensajes.append(msg)

    def fallo(self, msg: str) -> None:
        self.ok = False
        self.mensajes.append("ERROR: " + msg)


def probar_abb_punteros(verbose: bool = True) -> ResultadoEstructura:
    r = ResultadoEstructura("AbbPunteros")
    try:
        abb = AbbPunteros()
        for palabra in ["mango", "aguacate", "pera", "banano", "kiwi"]:
            abb.inserte(palabra)
        abb.inserte("mango")  # duplicado ignorado
        if verbose:
            r.agrega(f"Tras inserciones (sin duplicados): {abb}")
        assert str(abb) == "[aguacate, banano, kiwi, mango, pera]", "Orden inesperado"
        assert len(abb) == 5, "El ABB debería ignorar duplicados"
        assert abb.miembro("mango") and not abb.miembro("sandía"), "Fallo en miembro()"

        abb.borre("kiwi")   # hoja
        abb.borre("banano")  # un hijo
        abb.inserte("ciruela")
        abb.inserte("durazno")
        abb.borre("mango")  # dos hijos
        if verbose:
            r.agrega(f"Tras borrados y reinserciones: {abb}")

        esperado = "[aguacate, ciruela, durazno, pera]"
        assert str(abb) == esperado, "Resultado final inesperado"
        r.final_repr = str(abb)
        r.tamaño = len(abb)
    except AssertionError as e:
        r.fallo(str(e))
    except Exception as e:  # pragma: no cover - seguridad adicional
        r.fallo(f"Excepción inesperada: {e.__class__.__name__}: {e}")
    return r


def probar_abb_vector(verbose: bool = True) -> ResultadoEstructura:
    r = ResultadoEstructura("ABBVectorHeap")
    try:
        abb = ABBVectorHeap()
        for palabra in ["mango", "aguacate", "pera", "banano", "kiwi"]:
            abb.inserte(palabra)
        abb.inserte("pera")  # duplicado ignorado
        if verbose:
            r.agrega(f"Tras inserciones (sin duplicados): {abb}")
        assert str(abb) == "[aguacate, banano, kiwi, mango, pera]", "Orden inesperado"
        assert len(abb) == 5, "El ABB debería ignorar duplicados"
        assert abb.miembro("aguacate") and not abb.miembro("sandía"), "Fallo en miembro()"

        abb.borre("kiwi")
        abb.borre("banano")
        abb.inserte("ciruela")
        abb.inserte("durazno")
        abb.borre("mango")
        if verbose:
            r.agrega(f"Tras borrados y reinserciones: {abb}")

        esperado = "[aguacate, ciruela, durazno, pera]"
        assert str(abb) == esperado, "Resultado final inesperado"
        r.final_repr = str(abb)
        r.tamaño = len(abb)
    except AssertionError as e:
        r.fallo(str(e))
    except Exception as e:  # pragma: no cover - seguridad adicional
        r.fallo(f"Excepción inesperada: {e.__class__.__name__}: {e}")
    return r


def _ejecutar_casos_trie(trie, verbose: bool, nombre: str) -> ResultadoEstructura:
    r = ResultadoEstructura(nombre)
    try:
        palabras = ["gato", "gallina", "gallo", "gato", "gal"]
        for palabra in palabras:
            trie.inserte(palabra)
        if verbose:
            r.agrega(f"Tras inserciones (con duplicados): {trie}")
        assert len(trie) == len(palabras), "El tamaño debe contabilizar duplicados"
        assert trie.miembro("gato") and trie.miembro("gallo"), "Fallo en miembro existente"
        assert not trie.miembro("perro"), "Miembro reporta palabra inexistente"

        assert trie.borre("gato"), "No se pudo borrar 'gato'"
        if verbose:
            r.agrega(f"Tras borrar 'gato': {trie}")
        assert len(trie) == len(palabras) - 1, "El tamaño debe decrementar"
        assert trie.miembro("gato"), "Debe quedar una ocurrencia de 'gato'"

        for palabra in ["gato", "gallo", "gallina", "gal"]:
            assert trie.borre(palabra), f"No se pudo borrar {palabra}"
        assert not trie.miembro("gal"), "La palabra 'gal' debería haberse eliminado"
        assert len(trie) == 0, "El trie debe quedar vacío"
        assert str(trie) == "[]", "Representación inesperada tras limpiar"

        if verbose:
            r.agrega("Trie vacío tras borrados: []")
        r.final_repr = str(trie)
        r.tamaño = len(trie)
    except AssertionError as e:
        r.fallo(str(e))
    except Exception as e:  # pragma: no cover - seguridad adicional
        r.fallo(f"Excepción inesperada: {e.__class__.__name__}: {e}")
    return r


def probar_trie_punteros(verbose: bool = True) -> ResultadoEstructura:
    return _ejecutar_casos_trie(TriePunteros(), verbose, "TriePunteros")


def probar_trie_arreglos(verbose: bool = True) -> ResultadoEstructura:
    return _ejecutar_casos_trie(TrieArreglos(), verbose, "TrieArreglos")


def imprimir_resultado(r: ResultadoEstructura) -> None:
    estado = "OK" if r.ok else "FALLO"
    print(f"\n=== {r.nombre} -> {estado} ===")
    for m in r.mensajes:
        print(" -", m)
    print(f" Final: {r.final_repr}  (tamaño={r.tamaño})")


def main(argv: list[str]) -> None:
    verbose = "--sin-detalle" not in argv
    if verbose:
        print("Iniciando pruebas de la Segunda Entrega (ABB + Tries)...\n")
    resultados: list[ResultadoEstructura] = []
    resultados.append(probar_abb_punteros(verbose))
    resultados.append(probar_abb_vector(verbose))
    resultados.append(probar_trie_punteros(verbose))
    resultados.append(probar_trie_arreglos(verbose))
    if verbose:
        for r in resultados:
            imprimir_resultado(r)
    else:
        print("\nResumen compacto:")
        for r in resultados:
            estado = "OK" if r.ok else "FALLO"
            print(f" - {r.nombre}: {estado} (tamaño={r.tamaño})")


if __name__ == "__main__":
    main(sys.argv[1:])
