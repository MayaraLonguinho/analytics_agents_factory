import pandas as pd
import json
import os
from typing import Dict, Any

class DatasetProfiler:
    def __init__(self):
        pass

    def profile_dataset(self, file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
            
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext == '.csv':
                df = pd.read_csv(file_path)
            elif ext == '.json':
                df = pd.read_json(file_path)
            elif ext in ['.parquet', '.pq']:
                df = pd.read_parquet(file_path)
            else:
                raise ValueError(f"Formato não suportado: {ext}")
        except Exception as e:
            return {"error": str(e), "status": "failed"}

        profile = {
            "status": "success",
            "file_name": os.path.basename(file_path),
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": {}
        }
        
        for col in df.columns:
            null_count = df[col].isnull().sum()
            profile["columns"][col] = {
                "type": str(df[col].dtype),
                "null_count": int(null_count),
                "null_percentage": float(null_count / len(df) * 100) if len(df) > 0 else 0.0
            }
            
        return profile
