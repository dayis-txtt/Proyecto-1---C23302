# -*- coding: utf-8 -*-
"""
Programa principal para utilizar el modelo Diccionario.

Programado por Braulio José Solano Rojas.
"""

from __future__ import annotations

import sys

from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from .diccionario import Diccionario
from .listaordenadadinamica import ListaOrdenadaDinámica
from .listaordenadaestatica import ListaOrdenadaEstática
from .tablahashabierta import TablaHashAbierta

console = Console()




def panel_contenido(
	texto: str, *, titulo: str = "Diccionario", width: int | None = None
) -> None:
	"""Imprime un Panel con doble línea y fondo azul."""
	console.clear()
	if width is None:
		width = min(80, max(40, console.size.width - 4))
	panel = Panel(
		Align.left(texto),
		title=titulo,
		title_align="center",
		padding=(1, 4),
		box=box.DOUBLE,
		width=width,
		style="white on blue",
	)
	console.print(panel, justify="left")


def pausa(msg: str = "Pulse [bold]Enter[/] para continuar…") -> None:
	Prompt.ask(msg, default="", show_default=False)


def leer_hilera(pregunta: str) -> str:
	"""Lee una hilera similar a TDato (máx. 20 chars)."""
	s = Prompt.ask(pregunta).strip()
	return s[:20]



def leer_tecla(validos: str) -> str:
	"""Lee una sola tecla y la devuelve sin requerir Enter.
	"""
	try:
		import msvcrt  
	except Exception:
		msvcrt = None  

	if msvcrt is not None:  
		while True:
			ch = msvcrt.getwch()

			if ch in ("\x00", "\xe0"):
				_ = msvcrt.getwch()
				continue
			if ch in validos:
				console.print(ch, end="")  
				return ch
	else:  
		import termios
		import tty

		fd = sys.stdin.fileno()
		old = termios.tcgetattr(fd)
		try:
			tty.setraw(fd)
			while True:
				ch = sys.stdin.read(1)
				if ch in validos:
					console.print(ch, end="")
					return ch
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old)



def agregar(diccionario: Diccionario) -> None:
	texto = "Digite la hilera que desea agregar:"
	panel_contenido(texto)
	h = leer_hilera("")
	if diccionario.miembro(h):
		console.print("[yellow]El elemento YA existe (se permiten repetidos).[/]")
	diccionario.inserte(h)
	console.print("[green]Elemento insertado.[/]")
	pausa()


def borrar(diccionario: Diccionario) -> None:
	texto = "Digite la hilera que desea borrar:"
	panel_contenido(texto)
	h = leer_hilera("")
	if diccionario.borre(h):
		console.print("[green]Elemento borrado.[/]")
	else:
		console.print("[red]El elemento NO existe.[/]")
	pausa()


def existencia(diccionario: Diccionario) -> None:
	texto = "Digite la hilera que desea verificar:"
	panel_contenido(texto)
	h = leer_hilera("")
	if diccionario.miembro(h):
		console.print("[green]El elemento existe.[/]")
	else:
		console.print("[red]El elemento NO existe.[/]")
	pausa()


def imprimir(diccionario: Diccionario) -> None:
	panel_contenido("Imprimir el diccionario")
	diccionario.imprima()
	pausa()


def limpiar(diccionario: Diccionario) -> None:
	diccionario.limpie()
	panel_contenido("Diccionario limpio.")
	pausa()




def render_menu_etapa() -> None:
	cuerpo = (
		"\n" 
		"            Etapa\n\n"
		"[1] Menú diccionarios \n"
		"[2] Pruebas de rendimiento (no disponible)\n\n"
		"Digite una opción [_]"
	)
	panel_contenido(cuerpo)


def render_menu_clase() -> None:
	cuerpo = (
		"\n"  
		"            Clase Diccionario\n\n"
			"[1] ListaOrdenadaDinámica\n"
		"[2] ListaOrdenadaEstática\n"
			"[3] TablaHashAbierta\n"
		"[4] ABBPunteros (no disponible)\n"
		"[5] ABBVectorHeap (no disponible)\n"
		"[6] TriePunteros (no disponible)\n"
		"[7] TrieArreglos (no disponible)\n\n"
		"Digite una opción [_]"
	)
	panel_contenido(cuerpo)


def render_menu_diccionario() -> None:
	cuerpo = (
		"\n"  
		"            Diccionario\n\n"
		"[1] Agregar un elemento al diccionario\n"
		"[2] Borrar un elemento del diccionario\n"
		"[3] Existencia de un elemento en el diccionario\n"
		"[4] Imprimir el diccionario\n"
		"[5] Limpiar el diccionario\n"
		"[6] Ver estadísticas\n"
		"[7] Salir\n\n"
		"Digite una opción [_]"
	)
	panel_contenido(cuerpo)


def menu_etapa() -> str:
	try:
		render_menu_etapa()
		return leer_tecla("12")
	except BaseException:
		raise ValueError("No se pudo devolver una opción.")


def menu_clase() -> Diccionario:
	try:
		while True:
			render_menu_clase()
			opcion = leer_tecla("1234567")
			match opcion:
				case "1":
					return ListaOrdenadaDinámica()
				case "2":
					try:
						panel_contenido(
							"Capacidad de ListaOrdenadaEstática (entero > 0).\nDeje vacío para usar 100 por defecto.",
							titulo="Configuración",
						)
						s = leer_hilera("")
						cap = int(s) if s.strip() else 100
						if cap <= 0:
							cap = 100
					except Exception:
						cap = 100
					return ListaOrdenadaEstática(cap)
				case "3":
					return TablaHashAbierta(101)
				case "4" | "5" | "6" | "7":
					pausa("Opción no disponible todavía. Presione Enter…")
	except BaseException:
		raise ValueError("No se pudo instanciar una clase diccionario.")


def menu_diccionario(diccionario: Diccionario) -> None:
	try:
		while True:
			render_menu_diccionario()
			opcion = leer_tecla("1234567")
			match opcion:
				case "1":
					agregar(diccionario)
				case "2":
					borrar(diccionario)
				case "3":
					existencia(diccionario)
				case "4":
					imprimir(diccionario)
				case "5":
					limpiar(diccionario)
				case "6":  
					panel_contenido("Estadísticas de la estructura")
					info: list[str] = []
					info.append(f"Tipo: {diccionario.__class__.__name__}")
					try:
						info.append(f"Tamaño: {len(diccionario)}")  
					except Exception:
						pass
					info.append("Duplicados: permitidos")
					info.append("Borrado: elimina UNA ocurrencia")
					if hasattr(diccionario, "factor_carga"):
						try:
							fc = diccionario.factor_carga()  
							info.append(f"Factor de carga: {fc:.3f}")
						except Exception:
							pass
					console.print("\n".join(info))
					pausa()
				case "7":
					console.clear()
					break
	finally:
		del diccionario


def main() -> None:
	opcion = menu_etapa()
	match opcion:
		case "1":
			diccionario = menu_clase()
			menu_diccionario(diccionario)
		case "2":
			pausa("Benchmark no implementado aún. Presione Enter…")
