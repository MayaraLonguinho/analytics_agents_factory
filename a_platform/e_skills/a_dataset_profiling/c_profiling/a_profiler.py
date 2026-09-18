"""
DatasetProfilingSkill — physical dataset profiler.

Computes dataset statistics directly from disk using pandas.
Does NOT use LLM for profiling. No mock, no fake data.
"""
from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

SUPPORTED_FORMATS = {"csv", "json"}


@dataclass
class ColumnProfile:
    name: str
    inferred_type: str
    null_count: int
    null_percentage: float
    unique_count: int


@dataclass
class DatasetProfile:
    dataset_path: str
    format: str
    row_count: int
    column_count: int
    columns: List[ColumnProfile] = field(default_factory=list)
    duplicate_rows: int = 0
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_path": self.dataset_path,
            "format": self.format,
            "row_count": self.row_count,
            "column_count": self.column_count,
            "columns": [
                {
                    "name": c.name,
                    "inferred_type": c.inferred_type,
                    "null_count": c.null_count,
                    "null_percentage": c.null_percentage,
                    "unique_count": c.unique_count,
                }
                for c in self.columns
            ],
            "duplicate_rows": self.duplicate_rows,
            "warnings": self.warnings,
        }


from a_platform.b_contracts import BaseSkill, ParameterDefinition


class DatasetProfilingSkill(BaseSkill):
    """
    Physical profiler. Reads the dataset from disk and returns a DatasetProfile.
    Supports CSV and JSON. Does NOT call the LLM.
    """

    def __init__(self, **data: Any):
        super().__init__(
            skill_id="dataset_profiling",
            name="Dataset Profiling Skill",
            input_schema=[
                ParameterDefinition(name="dataset_path", data_type="string", required=True),
            ],
            **data
        )

    def validate_input(self, context: Dict[str, Any]) -> None:
        super().validate_input(context)
        path = context.get("dataset_path")
        if not os.path.exists(path):
            raise FileNotFoundError(f"[DatasetProfilingSkill] Dataset not found: {path}")
        if not os.path.isfile(path):
            raise ValueError(f"[DatasetProfilingSkill] Path is not a regular file: {path}")
        ext = os.path.splitext(path)[-1].lstrip(".").lower()
        if ext not in SUPPORTED_FORMATS:
            raise ValueError(
                f"[DatasetProfilingSkill] Unsupported format '{ext}'. Supported: {SUPPORTED_FORMATS}"
            )

    def validate_output(self, result: Dict[str, Any]) -> None:
        super().validate_output(result)
        if "dataset_profile" not in result:
            raise ValueError("[DatasetProfilingSkill] Output must contain 'dataset_profile'.")
        dp = result["dataset_profile"]
        if not isinstance(dp, dict):
            raise ValueError("[DatasetProfilingSkill] 'dataset_profile' must be a dict.")
        if "row_count" not in dp or "column_count" not in dp:
            raise ValueError("[DatasetProfilingSkill] 'dataset_profile' missing row_count or column_count.")

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Returns a dict with key 'dataset_profile' containing the DatasetProfile as dict.
        Synchronous — no LLM, no coroutines.
        """
        self.validate_input(context)

        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "[DatasetProfilingSkill] pandas is required for profiling. "
                "Install it with: pip install pandas"
            ) from exc

        path: str = context["dataset_path"]
        ext = os.path.splitext(path)[-1].lstrip(".").lower()
        warnings: List[str] = []

        logger.info(f"[DatasetProfilingSkill] Profiling dataset: {path} (format={ext})")

        try:
            if ext == "csv":
                df = pd.read_csv(path)
            elif ext == "json":
                # Try records orient first; fall back to lines format
                try:
                    df = pd.read_json(path)
                except ValueError:
                    df = pd.read_json(path, lines=True)
        except Exception as exc:
            raise RuntimeError(
                f"[DatasetProfilingSkill] Failed to read dataset '{path}': {exc}"
            ) from exc

        if df.empty:
            raise ValueError(f"[DatasetProfilingSkill] Dataset is empty: {path}")

        row_count = len(df)
        column_count = len(df.columns)
        duplicate_rows = int(df.duplicated().sum())

        if duplicate_rows > 0:
            warnings.append(f"{duplicate_rows} duplicate rows detected.")

        columns: List[ColumnProfile] = []
        for col in df.columns:
            null_count = int(df[col].isna().sum())
            null_pct = round(null_count / row_count * 100, 2) if row_count > 0 else 0.0
            unique_count = int(df[col].nunique(dropna=True))
            inferred_type = str(df[col].dtype)
            columns.append(
                ColumnProfile(
                    name=col,
                    inferred_type=inferred_type,
                    null_count=null_count,
                    null_percentage=null_pct,
                    unique_count=unique_count,
                )
            )
            if null_pct > 50:
                warnings.append(f"Column '{col}' has {null_pct}% null values.")

        profile = DatasetProfile(
            dataset_path=path,
            format=ext,
            row_count=row_count,
            column_count=column_count,
            columns=columns,
            duplicate_rows=duplicate_rows,
            warnings=warnings,
        )

        logger.info(
            f"[DatasetProfilingSkill] Profile complete: {row_count} rows, "
            f"{column_count} columns, {duplicate_rows} duplicates."
        )

        res = {"dataset_profile": profile.to_dict()}
        self.validate_output(res)
        return res
