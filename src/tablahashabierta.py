from __future__ import annotations

from .diccionario import Diccionario


class TablaHashAbierta(Diccionario):
    """Tabla hash con hashing abierto (encadenamiento).

    - Guarda elementos de tipo str.
    - Permite duplicados.
    - Borrado elimina solo una ocurrencia.
    - Imprime una vista ordenada alfabéticamente para mejor legibilidad.
    """

    __slots__ = ("__buckets", "__n", "__capacidad_inicial")

    def __init__(self, capacidad: int = 101) -> None:
        if capacidad < 4:
            capacidad = 4
        self.__capacidad_inicial = self.___siguiente_primo(capacidad)
        self.__buckets: list[list[str]] = [[] for _ in range(self.__capacidad_inicial)]
        self.__n: int = 0

    # =====================
    # API Diccionario
    # =====================
    def inserte(self, elemento: str) -> None:
        idx = self.__indice(elemento)
        self.__buckets[idx].append(elemento)
        self.__n += 1
        # rehash si el factor de carga supera 0.75
        if self.__n > (len(self.__buckets) * 3) // 4:
            self.__rehash(len(self.__buckets) * 2)

    def borre(self, elemento: str) -> bool:
        idx = self.__indice(elemento)
        bucket = self.__buckets[idx]
        for i, v in enumerate(bucket):
            if v == elemento:
                del bucket[i]
                self.__n -= 1
                return True
        return False

    def limpie(self) -> None:
        cap = len(self.__buckets)
        self.__buckets = [[] for _ in range(cap)]
        self.__n = 0

    def miembro(self, elemento: str) -> bool:
        idx = self.__indice(elemento)
        bucket = self.__buckets[idx]
        for v in bucket:
            if v == elemento:
                return True
        return False

    def imprima(self) -> None:
        print(self)

    def __str__(self) -> str:  # representación amigable, ordenada
        if self.__n == 0:
            return "[]"
        elems: list[str] = []
        for bucket in self.__buckets:
            if bucket:
                elems.extend(bucket)
        elems.sort()
        return "[" + ", ".join(elems) + "]"

    # =====================
    # Internos
    # =====================
    def __indice(self, s: str) -> int:
        # hash determinístico sencillo (evita randomización de hash() de Python)
        h = 0
        for ch in s:
            h = (h * 257 + ord(ch)) & 0xFFFFFFFF
        return h % len(self.__buckets)

    def __rehash(self, nueva_capacidad: int) -> None:
        nueva_cap = self.___siguiente_primo(max(nueva_capacidad, 2 * len(self.__buckets)))
        nuevos: list[list[str]] = [[] for _ in range(nueva_cap)]
        for bucket in self.__buckets:
            for v in bucket:
                # re-calcular índice en la nueva tabla
                h = 0
                for ch in v:
                    h = (h * 257 + ord(ch)) & 0xFFFFFFFF
                nuevos[h % nueva_cap].append(v)
        self.__buckets = nuevos

    @staticmethod
    def ___siguiente_primo(n: int) -> int:
        def es_primo(x: int) -> bool:
            if x <= 3:
                return x >= 2
            if x % 2 == 0 or x % 3 == 0:
                return False
            f = 5
            while f * f <= x:
                if x % f == 0 or x % (f + 2) == 0:
                    return False
                f += 6
            return True

        p = n if n % 2 else n + 1
        while not es_primo(p):
            p += 2
        return p