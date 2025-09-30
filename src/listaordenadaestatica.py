from __future__ import annotations

from .diccionario import Diccionario


class Array:
	def __init__(self, valor_inicial=None, tamaño: int | None = None):
		if not isinstance(tamaño, int) or tamaño < 0:
			raise ValueError("El tamaño debe ser un entero no negativo.")
		if not isinstance(valor_inicial, list):
			self.__lista = [valor_inicial] * tamaño
			self.__tamaño = tamaño
		else:
			self.__lista = valor_inicial
			self.__tamaño = len(valor_inicial)

	def __getitem__(self, indice: int):
		if not (0 <= indice < self.__tamaño):
			raise IndexError("Índice de arreglo fuera de los límites.")
		return self.__lista[indice]

	def __setitem__(self, indice: int, value):
		if not (0 <= indice < self.__tamaño):
			raise IndexError("Índice de arreglo fuera de los límites")
		self.__lista[indice] = value

	def __len__(self) -> int:
		return self.__tamaño

	def __repr__(self) -> str:
		return f"Array({self.__lista})"

	def __str__(self) -> str:
		return str(self.__lista)


class ListaOrdenadaEstática(Diccionario):
	"""Lista ordenada implementada sobre un arreglo de tamaño fijo.

	Características:
	- Orden ascendente permanente.
	- Duplicados permitidos (nuevo va tras los existentes).
	- Capacidad fija: inserciones extra se descartan.
	- Búsqueda por binary search (lower/upper bound).
	"""

	def __init__(self, tamaño: int):
		self.__arreglo: Array = Array(valor_inicial=None, tamaño=tamaño)
		self.__ultimo: int | None = None

	def __len__(self) -> int:
		if self.__ultimo is None:
			return 0
		return self.__ultimo + 1

	def __getitem__(self, indice: int):
		n = len(self)
		if not (0 <= indice < n):
			raise IndexError("Índice fuera de rango")
		return self.__arreglo[indice]

	def inserte(self, elemento: str) -> None:
		capacidad = len(self.__arreglo)
		n = len(self)
		if n >= capacidad:
			return
		pos = self.__upper_bound(elemento, 0, n)
		# correr a la derecha
		i = n - 1
		while i >= pos:
			self.__arreglo[i + 1] = self.__arreglo[i]
			i -= 1
		self.__arreglo[pos] = elemento
		self.__ultimo = 0 if self.__ultimo is None else self.__ultimo + 1
		self.__verifique_invariante()

	def borre(self, elemento: str) -> bool:
		n = len(self)
		if n == 0:
			return False
		idx = self.__lower_bound(elemento, 0, n)
		if idx < n and self.__arreglo[idx] == elemento:
			i = idx
			while i < n - 1:
				self.__arreglo[i] = self.__arreglo[i + 1]
				i += 1
			self.__arreglo[n - 1] = None
			if n - 1 == 0:
				self.__ultimo = None
			else:
				assert self.__ultimo is not None
				self.__ultimo -= 1
			self.__verifique_invariante()
			return True
		return False

	def limpie(self) -> None:
		self.__ultimo = None
		for i in range(len(self.__arreglo)):
			self.__arreglo[i] = None

	def miembro(self, elemento: str) -> bool:
		n = len(self)
		if n == 0:
			return False
		idx = self.__lower_bound(elemento, 0, n)
		return idx < n and self.__arreglo[idx] == elemento

	def imprima(self) -> None:
		print(self)

	def __str__(self) -> str:
		if self.__ultimo is None:
			return "[]"
		visibles = [self.__arreglo[i] for i in range(self.__ultimo + 1)]
		return str(visibles)

	def __del__(self) -> None:
		self.limpie()


	def __verifique_invariante(self) -> None:
		"""Verifica orden ascendente y consistencia de tamaño.
		"""
		n = len(self)
		if n == 0:
			return
		prev = self.__arreglo[0]
		for i in range(1, n):
			curr = self.__arreglo[i]
			if prev is not None and curr is not None and prev > curr:
				raise AssertionError("Invariante roto: arreglo no ordenado")
			prev = curr

	def __lower_bound(self, x: str, lo: int, hi: int) -> int:
		"""Primer índice i en [lo,hi) tal que a[i] >= x."""
		while lo < hi:
			mid = (lo + hi) // 2
			if self.__arreglo[mid] is None:
				hi = mid
			elif self.__arreglo[mid] < x:
				lo = mid + 1
			else:
				hi = mid
		return lo

	def __upper_bound(self, x: str, lo: int, hi: int) -> int:
		"""Primer índice i en [lo,hi) tal que a[i] > x."""
		while lo < hi:
			mid = (lo + hi) // 2
			if self.__arreglo[mid] is None:
				hi = mid
			elif self.__arreglo[mid] <= x:
				lo = mid + 1
			else:
				hi = mid
		return lo