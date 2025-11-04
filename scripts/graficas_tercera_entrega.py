"""Generador de gráficos (Tercera Entrega)

Lee un archivo JSON producido por scripts/analisis_tercera_entrega.py y
produce gráficos PNG por operación y memoria.

Uso:
  py scripts/graficas_tercera_entrega.py --json resultados/bench_YYYYMMDD_HHMMSS.json
  # Salida por defecto: resultados/bench_YYYYMMDD_HHMMSS_plots/

Requisitos opcionales:
  - matplotlib (si no está instalado, el script lo indicará y saldrá)
"""
from __future__ import annotations

import argparse
import json
import math
import os
from dataclasses import dataclass
from typing import Any

try:
    import matplotlib.pyplot as plt  
except Exception as e:
    plt = None  


def load_results(json_path: str) -> dict[str, Any]:
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_matplotlib():
    if plt is None:
        raise SystemExit(
            "matplotlib no está disponible. Instala con: py -3 -m pip install matplotlib"
        )


def to_ms(ns: float) -> float:
    return ns / 1e6


def plot_lines_by_operation(results: dict[str, Any], out_dir: str) -> list[str]:
    ensure_matplotlib()
    os.makedirs(out_dir, exist_ok=True)

    structures = results["results"]
    # Eje X (Ns) en conjunto ordenado
    Ns = sorted({ss["n"] for r in structures for ss in r["sizes"]})

    ops = [
        ("insert", "Inserción (ms)"),
        ("delete", "Borrado (ms)"),
        ("search", "Búsqueda (ms)"),
        ("done_ns", "Done/Limpie (ms)"),
    ]

    generated: list[str] = []

    for op_key, ylabel in ops:
        fig, ax = plt.subplots(figsize=(9, 5))  # type: ignore
        for r in structures:
            ys: list[float] = []
            for n in Ns:
                sstat = next((ss for ss in r["sizes"] if ss["n"] == n), None)
                if not sstat:
                    ys.append(float("nan"))
                    continue
                if op_key == "done_ns":
                    val = sstat["done_ns"]
                else:
                    val = sstat[op_key]["mean_ns"]
                ys.append(to_ms(val))
            ax.plot(Ns, ys, marker="o", label=r["name"])  # type: ignore
        ax.set_xscale("log")
        ax.set_xlabel("N (log)")
        ax.set_ylabel(ylabel)
        ax.set_title(ylabel + " por estructura")
        ax.grid(True, which="both", ls=":", alpha=0.5)
        ax.legend(loc="best", fontsize=8)
        fname = f"{op_key}_lines.png"
        out_path = os.path.join(out_dir, fname)
        fig.tight_layout()
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        generated.append(out_path)



    has_print = any(any(ss.get("print_ns") is not None for ss in r["sizes"]) for r in structures)
    if has_print:
        fig, ax = plt.subplots(figsize=(9, 5)) 
        for r in structures:
            ys: list[float] = []
            for n in Ns:
                sstat = next((ss for ss in r["sizes"] if ss["n"] == n), None)
                if not sstat:
                    ys.append(float("nan"))
                    continue
                p = sstat.get("print_ns")
                ys.append(to_ms(p) if p is not None else float("nan"))
            ax.plot(Ns, ys, marker="o", label=r["name"])
        ax.set_xscale("log")
        ax.set_xlabel("N (log)")
        ax.set_ylabel("Print (ms)")
        ax.set_title("Tiempo de print (ms) por estructura")
        ax.grid(True, which="both", ls=":", alpha=0.5)
        ax.legend(loc="best", fontsize=8)
        fname = "print_lines.png"
        out_path = os.path.join(out_dir, fname)
        fig.tight_layout()
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        generated.append(out_path)

    fig, ax = plt.subplots(figsize=(9, 5))
    for r in structures:
        ys: list[float] = []
        for n in Ns:
            sstat = next((ss for ss in r["sizes"] if ss["n"] == n), None)
            if not sstat:
                ys.append(float("nan"))
                continue
            ys.append(sstat["memory_peak_bytes"] / 1024 / 1024)
        ax.plot(Ns, ys, marker="o", label=r["name"])  # type: ignore
    ax.set_xscale("log")
    ax.set_xlabel("N (log)")
    ax.set_ylabel("Memoria pico (MiB)")
    ax.set_title("Memoria pico (MiB) por estructura")
    ax.grid(True, which="both", ls=":", alpha=0.5)
    ax.legend(loc="best", fontsize=8)
    fname = "memory_lines.png"
    out_path = os.path.join(out_dir, fname)
    fig.tight_layout()  # type: ignore
    fig.savefig(out_path, dpi=150)  # type: ignore
    plt.close(fig)  # type: ignore
    generated.append(out_path)

    return generated


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description="Genera gráficos a partir del JSON de benchmarks")
    ap.add_argument("--json", required=True, help="Ruta al JSON generado por analisis_tercera_entrega.py")
    ap.add_argument("--out", help="Carpeta de salida; por defecto junto al JSON con sufijo _plots")
    args = ap.parse_args(argv)

    json_path = os.path.abspath(args.json)
    if not os.path.exists(json_path):
        raise SystemExit(f"No existe el archivo: {json_path}")

    base, _ = os.path.splitext(json_path)
    out_dir = args.out or (base + "_plots")

    data = load_results(json_path)
    generated = plot_lines_by_operation(data, out_dir)

    # Crear un markdown simple con enlaces a los PNG
    md_path = os.path.join(out_dir, "graficos.md")
    rels = [os.path.basename(p) for p in generated]
    md_lines = ["# Gráficos de rendimiento\n"]
    for r in rels:
        md_lines.append(f"![]({r})\n")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    print("Gráficos generados en:", out_dir)
    print("Markdown con enlaces:", md_path)


if __name__ == "__main__":
    main()
