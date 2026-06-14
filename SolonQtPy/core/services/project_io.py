from __future__ import annotations

import json
from pathlib import Path

from core.models.project_model import ProjectModel


def save_project(file_path: str, project: ProjectModel) -> None:
    path = Path(file_path)
    data = project.to_dict()
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def load_project(file_path: str) -> ProjectModel:
    path = Path(file_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    return ProjectModel.from_dict(data)
