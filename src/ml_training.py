"""
Entrenamiento ML.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from src.features import FEATURE_COLUMNS, validate_training_dataframe


def train_models_from_csv(df: pd.DataFrame, output_dir: str = "models") -> dict[str, Any]:
    """
    Entrena modelos de calidad, energía y anomalías.

    Args:
        df: Dataset.
        output_dir: Carpeta de salida.

    Returns:
        Reporte de entrenamiento.
    """
    validate_training_dataframe(df)

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    clean = df.dropna(subset=FEATURE_COLUMNS + ["energy_kwh", "product_quality_pct"]).copy()

    X = clean[FEATURE_COLUMNS]
    y_quality = clean["product_quality_pct"]
    y_energy = clean["energy_kwh"]

    X_train, X_test, yq_train, yq_test = train_test_split(
        X,
        y_quality,
        test_size=0.2,
        random_state=42,
    )

    _, _, ye_train, ye_test = train_test_split(
        X,
        y_energy,
        test_size=0.2,
        random_state=42,
    )

    quality_model = RandomForestRegressor(n_estimators=120, random_state=42, min_samples_leaf=2)
    energy_model = RandomForestRegressor(n_estimators=120, random_state=42, min_samples_leaf=2)
    anomaly_model = IsolationForest(n_estimators=100, contamination=0.08, random_state=42)

    quality_model.fit(X_train, yq_train)
    energy_model.fit(X_train, ye_train)
    anomaly_model.fit(X)

    q_pred = quality_model.predict(X_test)
    e_pred = energy_model.predict(X_test)

    report = {
        "samples": int(len(clean)),
        "features": FEATURE_COLUMNS,
        "quality_model": {
            "mae": float(mean_absolute_error(yq_test, q_pred)),
            "mse": float(mean_squared_error(yq_test, q_pred)),
            "r2": float(r2_score(yq_test, q_pred)),
        },
        "energy_model": {
            "mae": float(mean_absolute_error(ye_test, e_pred)),
            "mse": float(mean_squared_error(ye_test, e_pred)),
            "r2": float(r2_score(ye_test, e_pred)),
        },
    }

    joblib.dump(quality_model, out / "quality_model.joblib")
    joblib.dump(energy_model, out / "energy_model.joblib")
    joblib.dump(anomaly_model, out / "anomaly_model.joblib")
    (out / "training_report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return report
