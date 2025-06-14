import nbformat
from pathlib import Path

for notebook_path in Path(".").rglob("*.ipynb"):
    try:
        nb = nbformat.read(notebook_path, as_version=4)

        # Fix notebook-level metadata
        if "widgets" in nb.metadata:
            nb.metadata["widgets"].setdefault("state", {})
            nb.metadata["widgets"].setdefault("version", "1.0.0")

        # Fix cell-level metadata (for each code cell)
        for cell in nb.cells:
            if cell.get("cell_type") == "code":
                widgets_meta = cell.get("metadata", {}).get("widgets")
                if widgets_meta:
                    cell["metadata"]["widgets"].setdefault("state", {})
                    cell["metadata"]["widgets"].setdefault("version", "1.0.0")

        nbformat.write(nb, notebook_path)
        print(f"✅ Fixed: {notebook_path}")

    except Exception as e:
        print(f"❌ Failed: {notebook_path}: {e}")
