"""Armador de reporte (Tercera Entrega)

Combina el template de doc/tercera_entrega_resultados.md con los resultados
más recientes en resultados/ (bench_*.json/.md) y, si existen, los gráficos
(bench_*_plots/), para generar un reporte final listo para entregar.

Uso:
  py scripts/armar_reporte_tercera_entrega.py
  # genera doc/tercera_entrega_resultados_completo.md

Requisitos: haber corrido antes el análisis y, opcionalmente, las gráficas.
"""
from __future__ import annotations

import os
import re
from datetime import datetime
from typing import Optional

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOC = os.path.join(ROOT, "doc")
RESULTS = os.path.join(ROOT, "resultados")
TEMPLATE = os.path.join(DOC, "tercera_entrega_resultados.md")
OUTPUT = os.path.join(DOC, "tercera_entrega_resultados_completo.md")


def find_latest_bench(prefix: str = "bench_") -> Optional[str]:
    if not os.path.isdir(RESULTS):
        return None
    cands = [f for f in os.listdir(RESULTS) if f.startswith(prefix) and f.endswith(".json")]
    if not cands:
        return None
    # ordenar por mtime descendente
    cands.sort(key=lambda f: os.path.getmtime(os.path.join(RESULTS, f)), reverse=True)
    return os.path.join(RESULTS, cands[0])


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def maybe_read(path: str) -> Optional[str]:
    try:
        return read_text(path)
    except Exception:
        return None


def extract_section(markdown: str, heading: str) -> Optional[str]:
    """Extrae una sección a partir de un encabezado '## heading' hasta el próximo '## ' o fin."""
    # Buscar el encabezado exacto de segundo nivel
    patt = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.M)
    m = patt.search(markdown)
    if not m:
        return None
    start = m.end()
    # Encontrar el siguiente encabezado de nivel 2
    m2 = re.search(r"^##\s+.+$", markdown[start:], re.M)
    end = start + m2.start() if m2 else len(markdown)
    return markdown[m.start():end].strip()


def main() -> None:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    latest_json = find_latest_bench()
    if not latest_json:
        raise SystemExit("No se encontraron resultados en 'resultados/'. Ejecuta primero el análisis.")

    base = latest_json[:-5]  # sin .json
    latest_md = base + ".md"
    bench_md = maybe_read(latest_md)

    plots_dir = base + "_plots"
    plots_md_path = os.path.join(plots_dir, "graficos.md")
    plots_md = maybe_read(plots_md_path)

    # Cargar template base
    template = read_text(TEMPLATE)

    # Construir salida
    out_lines: list[str] = []
    out_lines.append(f"# Tercera Entrega — Resultados y Análisis (auto)\n")
    out_lines.append(f"> Generado: {ts}\n")

    # 1. Metodología: copiar del template (sección 1)
    sec1 = extract_section(template, "1. Metodología de medición")
    if sec1:
        out_lines.append(sec1)
        out_lines.append("")

    # 2. Tablas: si tenemos el markdown del benchmark, incrustarlo
    out_lines.append("## 2. Tablas de resultados (empíricos)\n")
    if bench_md:
        out_lines.append("> Extracto del resumen automático generado por el benchmark.\n")
        # Insertar el contenido completo del bench md
        out_lines.append(bench_md)
    else:
        out_lines.append("(No se encontró el Markdown del benchmark. Asegúrate de correr el análisis.)\n")

    # 2.1 Gráficos: si existen, incrustar el graficos.md
    if plots_md:
        out_lines.append("\n### 2.1 Gráficos\n")
        out_lines.append("> Figuras generadas automáticamente desde el JSON.\n")
        # Ajustar rutas relativas: graficos.md asume estar en la carpeta de plots
        # Aquí convertimos a rutas relativas desde doc/
        rel_dir_from_doc = os.path.relpath(plots_dir, DOC).replace('\\', '/')
        fixed = plots_md
        fixed = re.sub(r"!\[]\(([^)]+)\)", lambda m: f"![]({rel_dir_from_doc}/{m.group(1)})", fixed)
        out_lines.append(fixed)

    # 3. Comparación teórica: copiar estructura del template y dejar lugar a comentarios
    sec3 = extract_section(template, "3. Comparación con órdenes teóricas")
    if sec3:
        out_lines.append("")
        out_lines.append(sec3)

    # 4. Rangos sugeridos: extraer del bench si está
    out_lines.append("\n## 4. Rangos sugeridos para N\n")
    extracted = None
    if bench_md:
        extracted = extract_section(bench_md, "Rangos sugeridos (heurística)")
    if extracted:
        out_lines.append(extracted)
    else:
        out_lines.append("(No se pudo extraer la sección de rangos; revisa el resumen del benchmark.)\n")

    # 5. Memoria utilizada: copiar estructura del template
    sec5 = extract_section(template, "5. Memoria utilizada")
    if sec5:
        out_lines.append("")
        out_lines.append(sec5)

    # 6. Limitaciones
    sec6 = extract_section(template, "6. Limitaciones")
    if sec6:
        out_lines.append("")
        out_lines.append(sec6)

    # 7. Conclusiones
    sec7 = extract_section(template, "7. Conclusiones")
    if sec7:
        out_lines.append("")
        out_lines.append(sec7)

    # Escribir salida
    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines).rstrip() + "\n")

    print("Reporte generado en:", OUTPUT)
    if not plots_md:
        print("Nota: no se encontraron gráficos; puedes generarlos con scripts/graficas_tercera_entrega.py")


if __name__ == "__main__":
    main()
