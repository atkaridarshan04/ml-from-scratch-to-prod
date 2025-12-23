from pathlib import Path
from utils import load_joblib

def load_prod_artifacts(artifact_dir: Path) -> dict:
    # Load model and preprocessing artifacts from production directory.
    return {
        "model": load_joblib(artifact_dir / 'model.joblib'),
        "imputer": load_joblib(artifact_dir / 'imputer.joblib'),
        "encoder": load_joblib(artifact_dir / 'encoder.joblib')
    }