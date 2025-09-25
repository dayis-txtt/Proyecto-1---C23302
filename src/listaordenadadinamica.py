from __future__ import annotations

from .diccionario import Diccionario


class Nodo:
	def __init__(self, elemento: str = ""):
		self.elemento: str = elemento
		self.siguiente: Nodo | None = None


class ListaOrdenadaDinámica(Diccionario):
	"""Lista simplemente enlazada que mantiene sus elementos en orden ascendente.

	- Permite elementos repetidos.
	- Las operaciones recorren secuencialmente la lista (O(n)).
	"""

	def __init__(self) -> None:
		self.__cabeza: Nodo = Nodo()  # centinela (no almacena dato real)
		self.__tamaño: int = 0

	def __len__(self) -> int:
		return self.__tamaño

	def __getitem__(self, indice: int) -> str:
		if not (0 <= indice < self.__tamaño):
			raise IndexError("Índice fuera de rango")
		actual = self.__cabeza.siguiente
		i = 0
		while i < indice and actual is not None:
			actual = actual.siguiente
			i += 1
		assert actual is not None
		return actual.elemento

	def inserte(self, elemento: str) -> None:
		"""Inserta manteniendo orden ascendente (permite duplicados)."""
		nuevo = Nodo(elemento)
		ant = self.__cabeza
		act = ant.siguiente
		while act is not None and act.elemento <= elemento:
			# con <= colocamos nuevos duplicados después de existentes
			ant = act
			act = act.siguiente
		nuevo.siguiente = act
		ant.siguiente = nuevo
		self.__tamaño += 1

	def borre(self, elemento: str) -> bool:
		ant = self.__cabeza
		act = ant.siguiente
		while act is not None and act.elemento < elemento:
			ant = act
			act = act.siguiente
		if act is not None and act.elemento == elemento:
			ant.siguiente = act.siguiente
			self.__tamaño -= 1
			return True
		return False

	def limpie(self) -> None:
		self.__cabeza.siguiente = None
		self.__tamaño = 0

	def miembro(self, elemento: str) -> bool:
		act = self.__cabeza.siguiente
		while act is not None and act.elemento < elemento:
			act = act.siguiente
		return act is not None and act.elemento == elemento

	def imprima(self) -> None:
		print(self)

	def __str__(self) -> str:
		elems: list[str] = []
		act = self.__cabeza.siguiente
		while act is not None:
			elems.append(act.elemento)
			act = act.siguiente
		return "[" + ", ".join(elems) + "]"

	def __del__(self) -> None:  # liberar por claridad (GC lo maneja normalmente)
		self.limpie()