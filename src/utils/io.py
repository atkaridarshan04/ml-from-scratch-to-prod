import joblib
from pathlib import Path
import json
from typing import Any, Dict

def save_joblib(obj: Any, path: Path) -> None:
    # Save any Python object using joblib.
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(obj, path)

def load_joblib(path: Path) -> Any:
    # Load a joblib-saved object.
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Artifact not found: {path}")
    return joblib.load(path)

# --------------------------------------------------------------

def save_json(data: Dict, path: Path) -> None:
    """
    Save dictionary as JSON.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def load_json(path: Path) -> Dict:
    """
    Load JSON file into dictionary.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")

    with open(path, "r") as f:
        return json.load(f)
