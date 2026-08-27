import logging
import json
import os
from typing import Dict, Any
from a_platform.e_skills.skill_contract import BaseSkill, CORE_SKILL_CONTRACTS

logger = logging.getLogger(__name__)

class DatasetProfilingSkill(BaseSkill):
    def __init__(self):
        super().__init__(contract=CORE_SKILL_CONTRACTS["dataset_profiling"])

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.validate_input(context)
        
        path = context["dataset_path"]
        logger.info(f"[DatasetProfilingSkill] Executando profiling real em {path}")
        
        profile = {
            "schema": [],
            "row_count": 0,
            "nulls": 0,
            "metrics": {},
            "quality_score": 0.0
        }
        
        if not os.path.exists(path):
            error_msg = f"Arquivo {path} não encontrado."
            logger.error(f"[DatasetProfilingSkill] {error_msg}")
            raise FileNotFoundError(error_msg)
            
        try:
            import pandas as pd
            if path.endswith('.csv'):
                df = pd.read_csv(path)
            elif path.endswith('.parquet'):
                df = pd.read_parquet(path)
            elif path.endswith('.json'):
                df = pd.read_json(path)
            else:
                df = pd.DataFrame()
            
            if not df.empty:
                profile["schema"] = list(df.columns)
                profile["row_count"] = int(len(df))
                profile["nulls"] = int(df.isnull().sum().sum())
                profile["quality_score"] = max(0.0, 1.0 - (profile["nulls"] / (profile["row_count"] * len(df.columns))))
                
                # Compute basic metrics for numeric columns
                desc = df.describe()
                for col in desc.columns:
                    profile["metrics"][col] = {
                        "min": float(desc[col]["min"]) if not pd.isna(desc[col]["min"]) else 0.0,
                        "max": float(desc[col]["max"]) if not pd.isna(desc[col]["max"]) else 0.0,
                        "mean": float(desc[col]["mean"]) if not pd.isna(desc[col]["mean"]) else 0.0
                    }
        except Exception as e:
            error_msg = f"Falha ao processar {path}: {e}"
            logger.error(f"[DatasetProfilingSkill] {error_msg}")
            raise ValueError(error_msg)

        result = {
            "dataset_profile.json": json.dumps(profile, indent=2)
        }
        
        self.validate_output(result)
        return result
