"""Análisis de rendimiento (Tercera Entrega)

Mide tiempos promedio y desviación estándar para:
- inserte
- borre
- miembro
- print
- done (limpie)

en las 7 implementaciones del Modelo Diccionario para tamaños:
- pequeño (100)
- mediano (50 000)
- grande (1 000 000) 

Además, estima el uso de memoria por estructura (via tracemalloc) y genera
un resumen en consola y archivos JSON/Markdown.

Uso rápido en consola:
  py scripts/analisis_tercera_entrega.py --quick     # 100 y 50k, 3 corridas
  py scripts/analisis_tercera_entrega.py             # 100, 50k, y 1e6 (si no se desactiva), 10 corridas

Parámetros:
  --sizes 100,50000,1000000   Lista de tamaños N
  --runs 10                   Cantidad de corridas por tamaño
  --trials 100                Operaciones por corrida para promediar
  --no-large                  Omite el tamaño grande
  --quick                     Alias de: --sizes 100,50000 --runs 3 --trials 50 --no-large
    --out resultados            Carpeta donde guardar JSON/MD
    --print-large               Permite medir print() también en tamaño grande 
"""
from __future__ import annotations

import argparse
import io
import json
import math
import os
import random
import statistics as stats
import sys
import time
import tracemalloc
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Callable, Iterable


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.listaordenadadinamica import ListaOrdenadaDinámica
from src.listaordenadaestatica import ListaOrdenadaEstática
from src.tablahashabierta import TablaHashAbierta
from src.abbpunteros import AbbPunteros
from src.abbvectorheap import ABBVectorHeap
from src.triepunteros import TriePunteros
from src.triearreglos import TrieArreglos


ABC = "abcdefghijklmnopqrstuvwxyz"


def rand_word(rng: random.Random, length: int = 20) -> str:
    return "".join(rng.choice(ABC) for _ in range(length))


def gen_words_unique(n: int, seed: int) -> list[str]:
    rng = random.Random(seed)
    s: set[str] = set()
    while len(s) < n:
        s.add(rand_word(rng, 20))
    return list(s)


@dataclass
class OpStats:
    mean_ns: float
    stdev_ns: float


@dataclass
class SizeStats:
    n: int
    insert: OpStats
    delete: OpStats
    search: OpStats
    print_ns: float | None
    done_ns: float
    memory_peak_bytes: int


@dataclass
class StructureResult:
    name: str
    sizes: list[SizeStats]


def time_ns(fn: Callable[[], None]) -> int:
    t0 = time.perf_counter_ns()
    fn()
    return time.perf_counter_ns() - t0


def benchmark_one_size(
    name: str,
    factory: Callable[[int], object],
    n: int,
    runs: int,
    trials: int,
    seed: int,
    enable_print_large: bool,
) -> SizeStats:
    insert_avgs: list[float] = []
    delete_avgs: list[float] = []
    search_avgs: list[float] = []
    print_times: list[int] = []
    done_times: list[int] = []
    memory_peaks: list[int] = []

    for r in range(runs):
        rng = random.Random(seed * 9176 + r * 101 + hash(name) % 10_000)
        base_words = gen_words_unique(n, rng.randrange(1_000_000_000))
        extra_words = gen_words_unique(trials * 2, rng.randrange(1_000_000_000))
        base_set = set(base_words)
        extra_words = [w for w in extra_words if w not in base_set][:trials]
        if len(extra_words) < trials:
        
            while len(extra_words) < trials:
                w = rand_word(rng)
                if w not in base_set:
                    extra_words.append(w)

       
        tracemalloc.start()
        d = factory(n)
        for w in base_words:
            d.inserte(w)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memory_peaks.append(peak)

        
        del_words = [base_words[rng.randrange(0, n)] for _ in range(trials)]
        # Asegurar que las palabras a borrar estén en la base
        del_words = [w for w in del_words if w in base_set]
        miss_words = gen_words_unique(trials, rng.randrange(1_000_000_000))
        miss_words = [w for w in miss_words if w not in base_set][:trials]
        while len(miss_words) < trials:
            w = rand_word(rng)
            if w not in base_set:
                miss_words.append(w)
        search_pool = [base_words[rng.randrange(0, n)] for _ in range(trials)]

        def bench_insert_once(word: str) -> int:
            t = time_ns(lambda: d.inserte(word))
            d.borre(word)
            return t

        insert_times = [bench_insert_once(w) for w in extra_words]
        insert_avgs.append(sum(insert_times) / len(insert_times))

        def bench_delete_once(word: str) -> int:
            t = time_ns(lambda: d.borre(word))
            d.inserte(word)
            return t

        delete_times = [bench_delete_once(w) for w in del_words]
        delete_avgs.append(sum(delete_times) / len(delete_times))


        def bench_search_once(word: str) -> int:
            return time_ns(lambda: d.miembro(word))


        search_times: list[int] = []
        for i in range(trials):
            if i % 2 == 0:
                search_times.append(bench_search_once(search_pool[i]))
            else:
                search_times.append(bench_search_once(miss_words[i]))
        search_avgs.append(sum(search_times) / len(search_times))

        pt: int | None = None
        if enable_print_large or n <= 100_000:
            buf = io.StringIO()
            def do_print():
                s = str(d)  
                buf.write(s)
                buf.seek(0)
                buf.truncate(0)
            pt = time_ns(do_print)
            print_times.append(pt)

        dt = time_ns(lambda: d.limpie())
        done_times.append(dt)
        del d

    def to_stats(values: list[float]) -> OpStats:
        if len(values) == 1:
            return OpStats(mean_ns=float(values[0]), stdev_ns=0.0)
        return OpStats(mean_ns=float(stats.mean(values)), stdev_ns=float(stats.stdev(values)))

    print_ns = float(stats.mean(print_times)) if print_times else None
    done_ns = float(stats.mean(done_times)) if done_times else 0.0
    memory_peak = int(stats.mean(memory_peaks)) if memory_peaks else 0

    return SizeStats(
        n=n,
        insert=to_stats(insert_avgs),
        delete=to_stats(delete_avgs),
        search=to_stats(search_avgs),
        print_ns=print_ns,
        done_ns=done_ns,
        memory_peak_bytes=memory_peak,
    )


def build_factory(name: str) -> Callable[[int], object]:
    def factory_lo_dinamica(_: int) -> object:
        return ListaOrdenadaDinámica()

    def factory_lo_estatica(n: int) -> object:
        cap = max(100, n * 2)
        return ListaOrdenadaEstática(cap)

    def factory_hash(_: int) -> object:
        return TablaHashAbierta(101)

    def factory_abb_ptr(_: int) -> object:
        return AbbPunteros()

    def factory_abb_vec(_: int) -> object:
        return ABBVectorHeap()

    def factory_trie_ptr(_: int) -> object:
        return TriePunteros()

    def factory_trie_arr(_: int) -> object:
        return TrieArreglos()

    mapping = {
        "ListaOrdenadaDinámica": factory_lo_dinamica,
        "ListaOrdenadaEstática": factory_lo_estatica,
        "TablaHashAbierta": factory_hash,
        "AbbPunteros": factory_abb_ptr,
        "ABBVectorHeap": factory_abb_vec,
        "TriePunteros": factory_trie_ptr,
        "TrieArreglos": factory_trie_arr,
    }
    return mapping[name]


def analyze_ranges(results: list[StructureResult]) -> str:
    """Heurística simple que propone rangos de N basados en comparaciones.

    Compara promedios de búsqueda e inserción en N pequeños/medianos/grandes
    y sugiere dónde cada estructura es más conveniente.
    """
    by_name = {r.name: r for r in results}

    def get_time(name: str, n: int, op: str) -> float:
        # Si falta un tamaño para una estructura (por error o memoria), usar infinito para que no gane ese rango
        s = next((ss for ss in by_name[name].sizes if ss.n == n), None)
        if s is None:
            return math.inf
        return getattr(s, op).mean_ns

    lines: list[str] = []
    lines.append("Recomendaciones por rangos de N (heurística):")
    try:
        Ns = sorted({ss.n for r in results for ss in r.sizes})
        for name in by_name:
            times = [(n, get_time(name, n, "search")) for n in Ns]
            best_at = min(times, key=lambda t: t[1])[0]
            if best_at == Ns[0]:
                lines.append(f"- {name}: competitivo en diccionarios pequeños (≈{Ns[0]}).")
            elif best_at == Ns[-1]:
                lines.append(f"- {name}: ventajoso hacia diccionarios grandes (≈{Ns[-1]}).")
            else:
                lines.append(f"- {name}: desempeño intermedio (mejor cerca de N≈{best_at}).")
    except Exception:
        lines.append("- No fue posible derivar recomendaciones (faltan datos).")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Análisis de rendimiento de diccionarios")
    parser.add_argument("--sizes", type=str, default="100,50000,1000000")
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--trials", type=int, default=100)
    parser.add_argument("--no-large", action="store_true")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--out", type=str, default="resultados")
    parser.add_argument("--print-large", action="store_true")
    args = parser.parse_args(argv)

    if args.quick:
        args.sizes = "100,50000"
        args.runs = min(args.runs, 3) if args.runs else 3
        args.trials = min(args.trials, 50) if args.trials else 50
        args.no_large = True

    sizes = [int(x) for x in args.sizes.split(",") if x.strip()]
    if args.no_large:
        sizes = [n for n in sizes if n < 1_000_000]

    os.makedirs(args.out, exist_ok=True)

    structures = [
        "ListaOrdenadaDinámica",
        "ListaOrdenadaEstática",
        "TablaHashAbierta",
        "AbbPunteros",
        "ABBVectorHeap",
        "TriePunteros",
        "TrieArreglos",
    ]

    print("Iniciando análisis de rendimiento...\n")
    results: list[StructureResult] = []
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    for name in structures:
        print(f"==> {name}")
        factory = build_factory(name)
        sizes_stats: list[SizeStats] = []
        for n in sizes:
            print(f"  - N={n} (runs={args.runs}, trials={args.trials})...")
            try:
                ss = benchmark_one_size(
                    name,
                    factory,
                    n=n,
                    runs=args.runs,
                    trials=args.trials,
                    seed=12345,
                    enable_print_large=bool(args.print_large), 
                )
                sizes_stats.append(ss)
                print(
                    f"    insert≈{ss.insert.mean_ns/1e6:.3f}ms, delete≈{ss.delete.mean_ns/1e6:.3f}ms, "
                    f"search≈{ss.search.mean_ns/1e6:.3f}ms, mem≈{ss.memory_peak_bytes/1024/1024:.2f} MiB"
                )
            except MemoryError:
                print("    [omitido por falta de memoria en este tamaño]")
                continue
            except Exception as e:
                print(f"    [omitido por error: {type(e).__name__}]")
                continue
        results.append(StructureResult(name=name, sizes=sizes_stats))

    json_path = os.path.join(args.out, f"bench_{ts}.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"results": [
            {"name": r.name, "sizes": [asdict(s) for s in r.sizes]} for r in results
        ]}, f, ensure_ascii=False, indent=2)
    print(f"\nResultados JSON: {json_path}")

    md_lines: list[str] = []
    md_lines.append(f"# Resultados de rendimiento ({ts})\n")
    md_lines.append("Notas: tiempos en nanosegundos promedio por operación (media de corridas).\n")

    for r in results:
        md_lines.append(f"## {r.name}\n")
        md_lines.append("| N | insert (ns) | delete (ns) | search (ns) | print (ns) | done (ns) | mem pico (MiB) |")
        md_lines.append("|---:|---:|---:|---:|---:|---:|---:|")
        for s in r.sizes:
            md_lines.append(
                f"| {s.n} | {int(s.insert.mean_ns)} ± {int(s.insert.stdev_ns)} | "
                f"{int(s.delete.mean_ns)} ± {int(s.delete.stdev_ns)} | {int(s.search.mean_ns)} ± {int(s.search.stdev_ns)} | "
                f"{int(s.print_ns) if s.print_ns is not None else '-'} | {int(s.done_ns)} | {s.memory_peak_bytes/1024/1024:.2f} |"
            )
        md_lines.append("")

    md_lines.append("\n## Rangos sugeridos (heurística)\n")
    md_lines.append(analyze_ranges(results))
    md_path = os.path.join(args.out, f"bench_{ts}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"Resumen Markdown: {md_path}")

    print("\nListo. Puedes abrir el Markdown para el informe preliminar y completar el análisis comparando con órdenes teóricas y limitaciones.")


if __name__ == "__main__":
    main(sys.argv[1:])
