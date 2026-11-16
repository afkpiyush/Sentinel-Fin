from pathlib import Path
import json
def test_all_notebooks_are_valid():
    notebooks = sorted((Path(__file__).parents[1] / "notebooks").glob("*.ipynb"))
    assert len(notebooks) == 15
    for path in notebooks:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["nbformat"] == 4 and isinstance(data["cells"], list)
