from pathlib import Path
from typing import Any, Dict, Optional
import pandas as pd

class DatasetProfiler:
    """Agentic capability to profile datasets and extract structural metadata."""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        
    def profile(self, dataset_source: Optional[str]) -> Dict[str, Any]:
        """Detect source, infer schema, and calculate basic quality statistics."""
        if not dataset_source:
            return {}
            
        dataset_path = Path(dataset_source).expanduser()
        if not dataset_path.is_absolute():
            dataset_path = (self.project_root / dataset_path).resolve()
            
        if not dataset_path.exists() or dataset_path.suffix.lower() not in {".csv", ".xlsx"}:
            return {"error": "Dataset not found or unsupported format"}

        try:
            if dataset_path.suffix.lower() == ".csv":
                frame = pd.read_csv(dataset_path)
            else:
                frame = pd.read_excel(dataset_path)
                
            total_cells = frame.size
            null_cells = frame.isna().sum().sum()
            quality_score = 100 - (null_cells / total_cells * 100) if total_cells > 0 else 0

            profile = {
                "source": str(dataset_path),
                "source_type": dataset_path.suffix.lower()[1:],
                "rows": int(len(frame)),
                "columns": list(frame.columns),
                "column_count": int(frame.shape[1]),
                "dtypes": {str(key): str(value) for key, value in frame.dtypes.items()},
                "null_counts": {str(key): int(value) for key, value in frame.isna().sum().items()},
                "numeric_columns": [str(c) for c in frame.select_dtypes(include=['number']).columns],
                "categorical_columns": [str(c) for c in frame.select_dtypes(exclude=['number']).columns],
                "statistics": {
                    "quality_score": float(round(quality_score, 2)),
                    "memory_usage_mb": float(round(frame.memory_usage(deep=True).sum() / (1024 * 1024), 2))
                }
            }
            return profile
        except Exception as e:
            return {"error": f"Failed to profile dataset: {str(e)}"}
