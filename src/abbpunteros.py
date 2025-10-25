from __future__ import annotations

from dataclasses import dataclass

from .diccionario import Diccionario


@dataclass
class _NodoAbb:
    clave: str
    izquierdo: _NodoAbb | None = None
    derecho: _NodoAbb | None = None


class AbbPunteros(Diccionario):
    """Árbol binario de búsqueda sin duplicados usando nodos enlazados.

    Cada nodo mantiene referencias explícitas a sus hijos izquierdo y derecho.
    Las operaciones estándar (insertar, borrar, buscar) preservan la propiedad
    de orden y garantizan que solo exista una ocurrencia por clave.
    """

    permite_duplicados = False

    def __init__(self) -> None:
        """Crea un ABB vacío sin nodos iniciales."""
        self.__raiz: _NodoAbb | None = None
        self.__tamaño: int = 0

    def inserte(self, elemento: str) -> None:
        """Agrega ``elemento`` si no existe ya en el árbol.

        Recorre recursivamente comparando con cada nodo y lo inserta en la
        posición correspondiente. Al detectar un duplicado, no modifica la
        estructura para mantener claves únicas.
        """
        self.__raiz, insertado = self.__inserte_rec(self.__raiz, elemento)
        if insertado:
            self.__tamaño += 1
            self.__verifique_invariante()

    def borre(self, elemento: str) -> bool:
        """Elimina ``elemento`` si está presente y retorna ``True``.

        Maneja los casos de borrado sin hijos, con un hijo o con dos hijos
        (reemplazo por el sucesor in-order) y actualiza el tamaño en
        consecuencia.
        """
        self.__raiz, borrado = self.__borre_rec(self.__raiz, elemento)
        if borrado:
            self.__tamaño -= 1
            self.__verifique_invariante()
        return borrado

    def limpie(self) -> None:
        """Vacía por completo el ABB removiendo todos los nodos."""
        self.__raiz = None
        self.__tamaño = 0

    def miembro(self, elemento: str) -> bool:
        """Devuelve ``True`` si ``elemento`` existe en el árbol."""
        return self.__miembro_rec(self.__raiz, elemento)

    def imprima(self) -> None:
        """Imprime el recorrido in-order del árbol."""
        print(self)

    def __len__(self) -> int:
        """Entrega la cantidad de claves almacenadas."""
        return self.__tamaño

    def __str__(self) -> str:
        """Construye una representación legible con las claves ordenadas."""
        elementos: list[str] = []
        self.__recorrido_inorder(self.__raiz, elementos)
        return "[" + ", ".join(elementos) + "]"

    def __inserte_rec(self, raiz: _NodoAbb | None, elemento: str) -> tuple[_NodoAbb, bool]:
        if raiz is None:
            return _NodoAbb(elemento), True
        if elemento < raiz.clave:
            raiz.izquierdo, insertado = self.__inserte_rec(raiz.izquierdo, elemento)
            return raiz, insertado
        if elemento > raiz.clave:
            raiz.derecho, insertado = self.__inserte_rec(raiz.derecho, elemento)
            return raiz, insertado
        return raiz, False

    def __borre_rec(self, raiz: _NodoAbb | None, elemento: str) -> tuple[_NodoAbb | None, bool]:
        if raiz is None:
            return None, False
        if elemento < raiz.clave:
            raiz.izquierdo, borrado = self.__borre_rec(raiz.izquierdo, elemento)
            return raiz, borrado
        if elemento > raiz.clave:
            raiz.derecho, borrado = self.__borre_rec(raiz.derecho, elemento)
            return raiz, borrado
        if raiz.izquierdo is None:
            return raiz.derecho, True
        if raiz.derecho is None:
            return raiz.izquierdo, True
        sucesor = self.__minimo(raiz.derecho)
        raiz.clave = sucesor.clave
        raiz.derecho, _ = self.__borre_rec(raiz.derecho, sucesor.clave)
        return raiz, True

    def __miembro_rec(self, raiz: _NodoAbb | None, elemento: str) -> bool:
        if raiz is None:
            return False
        if elemento < raiz.clave:
            return self.__miembro_rec(raiz.izquierdo, elemento)
        if elemento > raiz.clave:
            return self.__miembro_rec(raiz.derecho, elemento)
        return True

    def __recorrido_inorder(self, raiz: _NodoAbb | None, salida: list[str]) -> None:
        if raiz is None:
            return
        self.__recorrido_inorder(raiz.izquierdo, salida)
        salida.append(raiz.clave)
        self.__recorrido_inorder(raiz.derecho, salida)

    def __minimo(self, raiz: _NodoAbb) -> _NodoAbb:
        actual = raiz
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    def __verifique_invariante(self) -> None:
        elementos: list[str] = []
        self.__recorrido_inorder(self.__raiz, elementos)
        for i in range(1, len(elementos)):
            assert elementos[i - 1] < elementos[i], (
                "ABB desordenado o con duplicados: "
                f"{elementos[i - 1]} >= {elementos[i]}"
            )
        assert len(elementos) == self.__tamaño, (
            f"Conteo inconsistente: recorrido={len(elementos)} tamaño={self.__tamaño}"
        )

    def __del__(self) -> None:
        self.limpie()
