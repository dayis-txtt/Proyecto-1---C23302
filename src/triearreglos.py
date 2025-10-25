from __future__ import annotations

from .diccionario import Diccionario


class TrieArreglos(Diccionario):
    """Trie respaldado por arreglos paralelos de transiciones y contadores.

    Los nodos se identifican por índices enteros. Cada posición del arreglo
    ``__hijos`` guarda un diccionario de transiciones hacia otros índices y el
    arreglo ``__finales`` almacena cuántas palabras terminan en ese nodo. Se
    permiten duplicados sumando en ``__finales`` y se realiza poda explícita
    cuando los nodos dejan de ser necesarios.
    """

    permite_duplicados = True

    def __init__(self) -> None:
        """Inicializa el trie vacío con solo la raíz (índice 0)."""
        self.__hijos: list[dict[str, int]] = [{}]
        self.__finales: list[int] = [0]
        self.__total: int = 0

    def inserte(self, elemento: str) -> None:
        """Agrega ``elemento`` y aumenta el contador en su nodo terminal."""
        indice = 0
        for ch in elemento:
            siguiente = self.__hijos[indice].get(ch)
            if siguiente is None:
                siguiente = self.__nuevo_nodo()
                self.__hijos[indice][ch] = siguiente
            indice = siguiente
        self.__finales[indice] += 1
        self.__total += 1
        self.__verifique_invariante()

    def borre(self, elemento: str) -> bool:
        """Elimina una ocurrencia de ``elemento`` si está presente."""
        pila: list[tuple[int, str]] = []
        indice = 0
        for ch in elemento:
            siguiente = self.__hijos[indice].get(ch)
            if siguiente is None:
                return False
            pila.append((indice, ch))
            indice = siguiente
        if self.__finales[indice] == 0:
            return False
        self.__finales[indice] -= 1
        self.__total -= 1
        if self.__finales[indice] == 0 and not self.__hijos[indice]:
            self.__podar(pila)
        self.__verifique_invariante()
        return True

    def limpie(self) -> None:
        """Reinicia la estructura dejando solo el nodo raíz."""
        self.__hijos = [{}]
        self.__finales = [0]
        self.__total = 0

    def miembro(self, elemento: str) -> bool:
        """Devuelve ``True`` cuando ``elemento`` posee al menos una copia."""
        indice = 0
        for ch in elemento:
            indice = self.__hijos[indice].get(ch, -1)
            if indice == -1:
                return False
        return self.__finales[indice] > 0

    def imprima(self) -> None:
        """Imprime el recorrido lexicográfico de las palabras almacenadas."""
        print(self)

    def __str__(self) -> str:
        """Retorna el contenido ordenado como lista para depuración."""
        palabras: list[str] = []
        self.__dfs(0, [], palabras)
        return "[" + ", ".join(palabras) + "]"

    def __len__(self) -> int:
        """Entrega el total de palabras del trie (contando duplicados)."""
        return self.__total

    def __dfs(self, indice: int, prefijo: list[str], salida: list[str]) -> None:
        for _ in range(self.__finales[indice]):
            salida.append("".join(prefijo))
        for ch in sorted(self.__hijos[indice].keys()):
            prefijo.append(ch)
            self.__dfs(self.__hijos[indice][ch], prefijo, salida)
            prefijo.pop()

    def __podar(self, pila: list[tuple[int, str]]) -> None:
        while pila:
            padre, ch = pila.pop()
            del self.__hijos[padre][ch]
            if self.__finales[padre] > 0 or self.__hijos[padre]:
                break

    def __nuevo_nodo(self) -> int:
        self.__hijos.append({})
        self.__finales.append(0)
        return len(self.__hijos) - 1

    def __verifique_invariante(self) -> None:
        conteo = 0
        visitados = {0}
        pila = [0]
        while pila:
            indice = pila.pop()
            fin = self.__finales[indice]
            assert fin >= 0, "Conteo negativo en nodo"
            conteo += fin
            for ch, hijo in self.__hijos[indice].items():
                assert isinstance(ch, str) and len(ch) == 1, "Clave inválida en trie"
                if hijo not in visitados:
                    visitados.add(hijo)
                    pila.append(hijo)
        assert conteo == self.__total, "Conteo inconsistente en trie"

    def __del__(self) -> None:
        self.limpie()
