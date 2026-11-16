from dataclasses import dataclass, field
from pathlib import Path
import json

@dataclass(frozen=True)
class ProjectConfig:
    root: Path
    random_seed: int = 42
    offline_mode: bool = True
    risk_thresholds: dict[str, float] = field(default_factory=lambda: {"low": .3, "medium": .6, "high": .8})
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:3b"

    @classmethod
    def from_json(cls, path: str | Path) -> "ProjectConfig":
        source = Path(path)
        data = json.loads(source.read_text(encoding="utf-8"))
        return cls(source.parent.parent.resolve(), int(data.get("random_seed", 42)),
                   bool(data.get("offline_mode", True)))

    def path(self, *parts: str) -> Path:
        return self.root.joinpath(*parts)
