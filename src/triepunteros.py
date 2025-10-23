from __future__ import annotations

from dataclasses import dataclass, field

from .diccionario import Diccionario


@dataclass
class _NodoTrie:
    fin: int = 0
    hijos: dict[str, _NodoTrie] = field(default_factory=dict)


class TriePunteros(Diccionario):
    """Trie (árbol prefijo) con nodos enlazados.

    Mantiene conteo total de palabras (con duplicados) y permite limpiar
    pruning de nodos al borrar para no dejar ramas inútiles.
    """

    permite_duplicados = True

    def __init__(self) -> None:
        self.__raiz = _NodoTrie()
        self.__total = 0

    def inserte(self, elemento: str) -> None:
        nodo = self.__raiz
        for ch in elemento:
            nodo = nodo.hijos.setdefault(ch, _NodoTrie())
        nodo.fin += 1
        self.__total += 1
        self.__verifique_invariante()

    def borre(self, elemento: str) -> bool:
        pila: list[tuple[_NodoTrie, str]] = []
        nodo = self.__raiz
        for ch in elemento:
            if ch not in nodo.hijos:
                return False
            pila.append((nodo, ch))
            nodo = nodo.hijos[ch]
        if nodo.fin == 0:
            return False
        nodo.fin -= 1
        self.__total -= 1
        if nodo.fin == 0 and not nodo.hijos:
            self.__podar(pila)
        self.__verifique_invariante()
        return True

    def limpie(self) -> None:
        self.__raiz = _NodoTrie()
        self.__total = 0

    def miembro(self, elemento: str) -> bool:
        nodo = self.__raiz
        for ch in elemento:
            nodo = nodo.hijos.get(ch)
            if nodo is None:
                return False
        return nodo.fin > 0

    def imprima(self) -> None:
        print(self)

    def __str__(self) -> str:
        palabras: list[str] = []
        self.__dfs(self.__raiz, [], palabras)
        return "[" + ", ".join(palabras) + "]"

    def __len__(self) -> int:
        return self.__total

    def __dfs(self, nodo: _NodoTrie, prefijo: list[str], salida: list[str]) -> None:
        for _ in range(nodo.fin):
            salida.append("".join(prefijo))
        for ch in sorted(nodo.hijos.keys()):
            prefijo.append(ch)
            self.__dfs(nodo.hijos[ch], prefijo, salida)
            prefijo.pop()

    def __podar(self, pila: list[tuple[_NodoTrie, str]]) -> None:
        while pila:
            nodo, ch = pila.pop()
            hijo = nodo.hijos[ch]
            if hijo.fin == 0 and not hijo.hijos:
                del nodo.hijos[ch]
            else:
                break

    def __verifique_invariante(self) -> None:
        conteo = 0
        pila: list[_NodoTrie] = [self.__raiz]
        while pila:
            nodo = pila.pop()
            assert nodo.fin >= 0, "Conteo negativo en nodo"
            conteo += nodo.fin
            for hijo in nodo.hijos.values():
                pila.append(hijo)
        assert conteo == self.__total, "Conteo inconsistente en el trie"

    def __del__(self) -> None:
        self.limpie()
