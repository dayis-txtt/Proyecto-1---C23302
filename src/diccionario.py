from __future__ import annotations

from abc import ABC, abstractmethod


class Diccionario(ABC):
	"""
	Clase abstracta Diccionario. Dicta los métodos que deben tener los diccionarios.
	Todas las implementaciones trabajarán con elementos de tipo str.
	"""

	@abstractmethod
	def inserte(self, elemento: str) -> None:
		"""Inserta un elemento (se permiten repetidos)."""
		raise NotImplementedError

	@abstractmethod
	def borre(self, elemento: str) -> bool:
		"""Borra una ocurrencia del elemento y devuelve True si se borró."""
		raise NotImplementedError

	@abstractmethod
	def limpie(self) -> None:
		"""Elimina todos los elementos del diccionario."""
		raise NotImplementedError

	@abstractmethod
	def miembro(self, elemento: str) -> bool:
		"""Retorna True si el elemento pertenece al diccionario."""
		raise NotImplementedError

	@abstractmethod
	def imprima(self) -> None:
		"""Imprime el contenido del diccionario (representación amigable)."""
		raise NotImplementedError

	@abstractmethod
	def __str__(self) -> str:  # pragma: no cover - contrato de representación
		raise NotImplementedError
