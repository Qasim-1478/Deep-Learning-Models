import nbformat
from pathlib import Path

root_dir = Path(".")

for notebook_path in root_dir.rglob("*.ipynb"):
    try:
        nb = nbformat.read(notebook_path, as_version=4)
        metadata = nb.get("metadata", {})

        if "widgets" in metadata:
            widgets = metadata["widgets"]
            widgets.setdefault("state", {})
            widgets.setdefault("version", "1.0.0")
            nb["metadata"]["widgets"] = widgets

        nbformat.write(nb, notebook_path)
        print(f"✅ Fixed: {notebook_path}")

    except Exception as e:
        print(f"❌ Failed to process {notebook_path}: {e}")
