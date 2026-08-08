"""Export the executed notebooks to Obsidian-readable Markdown.

The .ipynb files are the source of truth (they run in Colab). This produces a
plain-Markdown copy of each — code, prose, tables, and the rendered plots as
extracted PNGs — under `notebooks/obsidian/`, so the full session reads and
searches like any other note in the vault. Re-run after changing a notebook:

    python3 notebooks/export_obsidian.py

This is a one-way, read-only view. Do not edit the Markdown expecting it to
flow back into the notebook; edit `build_session1.py` and rebuild instead.
"""

from pathlib import Path

from nbconvert import MarkdownExporter
from nbconvert.writers import FilesWriter
import nbformat

HERE = Path(__file__).resolve().parent
OUT = HERE / "obsidian"
OUT.mkdir(exist_ok=True)

for name in ["01_complete", "01_live"]:
    src = HERE / f"{name}.ipynb"
    if not src.exists():
        continue
    nb = nbformat.read(src, as_version=4)
    body, resources = MarkdownExporter().from_notebook_node(nb)
    resources["output_extension"] = ".md"
    writer = FilesWriter(build_directory=str(OUT))
    writer.write(body, resources, notebook_name=name)
    print(f"exported {name} -> notebooks/obsidian/{name}.md")
