# coding: utf-8
import pandas as pd
from joblib import load
from loguru import logger

from constants import DATA

INFERENCE_FILE = DATA / "datasets" / "inference.parquet"
MODEL_FILE = DATA / "models" / "baseline_logreg.joblib"
OUT_FILE = DATA / "predictions" / "inference_predictions.parquet"

ID_COL = "customer_id"


def main() -> None:
    (DATA / "predictions").mkdir(parents=True, exist_ok=True)

    bundle = load(MODEL_FILE)
    model = bundle["model"]
    id_col = bundle.get("id_col", ID_COL)

    df = pd.read_parquet(INFERENCE_FILE)

    if id_col not in df.columns:
        raise ValueError(f"Inference dataset missing `{id_col}`")

    proba = model.predict_proba(df)[:, 1]

    out = pd.DataFrame({
        id_col: df[id_col].astype("string"),
        "p_churn": proba.astype("float64"),
    })

    out.to_parquet(OUT_FILE, index=False)
    logger.info(f"Saved inference predictions to: {OUT_FILE}")


if __name__ == "__main__":
    main()
