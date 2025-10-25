from __future__ import annotations

from .diccionario import Diccionario


class ABBVectorHeap(Diccionario):
    """Árbol binario de búsqueda sin duplicados respaldado por un vector.

    La representación usa un arreglo con índice base 1 donde las posiciones
    ``2*i`` y ``2*i+1`` corresponden a los hijos izquierdo y derecho. Esto
    facilita los cálculos y mantiene buena localidad de referencia, pero
    requiere compactar el arreglo cada vez que se liberan huecos tras un
    borrado.
    """

    permite_duplicados = False

    def __init__(self) -> None:
        """Crea un ABB vacío inicializando el vector con una entrada centinela."""
        self.__vector: list[str | None] = [None]  # índice 0 se deja vacío para facilitar cálculos
        self.__tamaño: int = 0

    def inserte(self, elemento: str) -> None:
        """Inserta ``elemento`` preservando el orden in-order.

        Si la clave ya existe no se realiza ninguna modificación para mantener
        la propiedad de claves únicas del ABB.
        """
        indice = 1
        while True:
            self.__asegure_capacidad(indice)
            valor = self.__vector[indice]
            if valor is None:
                self.__vector[indice] = elemento
                self.__tamaño += 1
                self.__verifique_invariante()
                return
            if elemento < valor:
                indice = self.__hijo_izquierdo(indice)
            elif elemento > valor:
                indice = self.__hijo_derecho(indice)
            else:
                # la clave ya existe, se ignora para evitar duplicados
                return

    def borre(self, elemento: str) -> bool:
        """Elimina ``elemento`` si está presente y devuelve ``True``.

        Gestiona los tres casos clásicos de borrado en ABB (hoja, un hijo,
        dos hijos) mediante sustitución por el sucesor inmediato. Ajusta el
        contador interno y compacta el vector para evitar residuos al final.
        """
        if self.__borre_rec(1, elemento):
            self.__tamaño -= 1
            self.__compacte_vector()
            self.__verifique_invariante()
            return True
        return False

    def limpie(self) -> None:
        """Vacía el árbol dejando únicamente la casilla centinela."""
        self.__vector = [None]
        self.__tamaño = 0

    def miembro(self, elemento: str) -> bool:
        """Devuelve ``True`` si ``elemento`` existe en el árbol."""
        return self.__miembro_rec(1, elemento)

    def imprima(self) -> None:
        """Imprime el recorrido in-order del ABB."""
        print(self)

    def __str__(self) -> str:
        """Genera una representación tipo lista ordenada para depuración."""
        elems: list[str] = []
        self.__recorrido_inorder(1, elems)
        return "[" + ", ".join(elems) + "]"

    def __len__(self) -> int:
        """Retorna la cantidad de claves almacenadas."""
        return self.__tamaño

    def __borre_rec(self, indice: int, elemento: str) -> bool:
        if self.__es_vacio(indice):
            return False
        valor = self.__vector[indice]
        assert valor is not None
        if elemento < valor:
            return self.__borre_rec(self.__hijo_izquierdo(indice), elemento)
        if elemento > valor:
            return self.__borre_rec(self.__hijo_derecho(indice), elemento)
        self.__borre_en_indice(indice)
        return True

    def __borre_en_indice(self, indice: int) -> None:
        izq = self.__hijo_izquierdo(indice)
        der = self.__hijo_derecho(indice)
        if self.__es_vacio(izq) and self.__es_vacio(der):
            self.__vector[indice] = None
            return
        if self.__es_vacio(izq):
            self.__vector[indice] = self.__vector[der]
            self.__borre_en_indice(der)
            return
        if self.__es_vacio(der):
            self.__vector[indice] = self.__vector[izq]
            self.__borre_en_indice(izq)
            return
        sucesor = self.__indice_minimo(der)
        self.__vector[indice] = self.__vector[sucesor]
        self.__borre_en_indice(sucesor)

    def __miembro_rec(self, indice: int, elemento: str) -> bool:
        if self.__es_vacio(indice):
            return False
        valor = self.__vector[indice]
        assert valor is not None
        if elemento < valor:
            return self.__miembro_rec(self.__hijo_izquierdo(indice), elemento)
        if elemento > valor:
            return self.__miembro_rec(self.__hijo_derecho(indice), elemento)
        return True

    def __recorrido_inorder(self, indice: int, salida: list[str]) -> None:
        if self.__es_vacio(indice):
            return
        self.__recorrido_inorder(self.__hijo_izquierdo(indice), salida)
        valor = self.__vector[indice]
        assert valor is not None
        salida.append(valor)
        self.__recorrido_inorder(self.__hijo_derecho(indice), salida)

    def __indice_minimo(self, indice: int) -> int:
        actual = indice
        while not self.__es_vacio(self.__hijo_izquierdo(actual)):
            actual = self.__hijo_izquierdo(actual)
        return actual

    @staticmethod
    def __hijo_izquierdo(indice: int) -> int:
        return indice * 2

    @staticmethod
    def __hijo_derecho(indice: int) -> int:
        return indice * 2 + 1

    def __asegure_capacidad(self, indice: int) -> None:
        if indice >= len(self.__vector):
            self.__vector.extend([None] * (indice - len(self.__vector) + 1))

    def __es_vacio(self, indice: int) -> bool:
        return indice >= len(self.__vector) or self.__vector[indice] is None

    def __compacte_vector(self) -> None:
        ultimo = len(self.__vector) - 1
        while ultimo > 0 and self.__vector[ultimo] is None:
            ultimo -= 1
        if ultimo + 1 != len(self.__vector):
            self.__vector = self.__vector[: ultimo + 1]
        if len(self.__vector) == 0:
            self.__vector = [None]

    def __verifique_invariante(self) -> None:
        elems: list[str] = []
        self.__recorrido_inorder(1, elems)
        for i in range(1, len(elems)):
            assert elems[i - 1] < elems[i], (
                "ABB desordenado o con duplicados: "
                f"{elems[i - 1]} >= {elems[i]}"
            )
        assert len(elems) == self.__tamaño, (
            f"Conteo inconsistente: recorrido={len(elems)} tamaño={self.__tamaño}"
        )

    def __del__(self) -> None:
        self.limpie()
