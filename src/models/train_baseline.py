# coding: utf-8
import numpy as np
import pandas as pd
from joblib import dump
from loguru import logger
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from constants import DATA

TRAIN_FILE = DATA / "datasets" / "train.parquet"
VAL_FILE = DATA / "datasets" / "validation.parquet"
MODEL_FILE = DATA / "models" / "baseline_logreg.joblib"
VAL_PRED_FILE = DATA / "predictions" / "validation_predictions.parquet"

ID_COL = "customer_id"
TARGET_COL = "churn"


def _infer_feature_columns(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """
    Split columns into categorical and numeric based on dtype.
    Assumes Phase 4 datasets already contain: customer_id, features, churn (train/val).
    """
    feature_cols = [c for c in df.columns if c not in {ID_COL, TARGET_COL}]

    cat_cols = df[feature_cols].select_dtypes(include=["object", "string", "category"]).columns.tolist()
    num_cols = df[feature_cols].select_dtypes(include=["number", "bool"]).columns.tolist()

    # Defensive: ensure no missing features
    if not feature_cols:
        raise ValueError("No feature columns found.")

    return cat_cols, num_cols


def _print_top_coefficients(model: Pipeline, cat_cols: list[str], num_cols: list[str], top_k: int = 15) -> None:
    """
    Print top positive/negative coefficients after one-hot expansion.
    Works for binary logistic regression.
    """
    pre: ColumnTransformer = model.named_steps["preprocess"]
    clf: LogisticRegression = model.named_steps["clf"]

    ohe: OneHotEncoder = pre.named_transformers_["cat"]
    ohe_feature_names = ohe.get_feature_names_out(cat_cols).tolist()

    feature_names = ohe_feature_names + num_cols
    coef = clf.coef_.ravel()

    if len(coef) != len(feature_names):
        raise ValueError(f"Coefficient length mismatch: {len(coef)} vs feature_names {len(feature_names)}")

    idx_sorted = np.argsort(coef)
    most_negative = idx_sorted[:top_k]
    most_positive = idx_sorted[-top_k:][::-1]

    logger.info("\nTop positive coefficients (increase churn probability):")
    for i in most_positive:
        logger.info(f"  {feature_names[i]}: {coef[i]:.4f}")

    logger.info("\nTop negative coefficients (decrease churn probability):")
    for i in most_negative:
        logger.info(f"  {feature_names[i]}: {coef[i]:.4f}")


def main() -> None:
    train_df = pd.read_parquet(TRAIN_FILE)
    validation_df = pd.read_parquet(VAL_FILE)

    # Basic sanity
    for name, df in [("train", train_df), ("validation", validation_df)]:
        if TARGET_COL not in df.columns:
            raise ValueError(f"{name}: missing target column `{TARGET_COL}`")
        if ID_COL not in df.columns:
            raise ValueError(f"{name}: missing id column `{ID_COL}`")

    X_train = train_df.drop(columns=[TARGET_COL])
    y_train = train_df[TARGET_COL].astype("int8")

    X_val = validation_df.drop(columns=[TARGET_COL])
    y_val = validation_df[TARGET_COL].astype("int8")

    cat_cols, num_cols = _infer_feature_columns(train_df)

    preprocess = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
            ("num", StandardScaler(), num_cols),
        ],
        remainder="drop",
        sparse_threshold=1.0,
    )

    clf = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        solver="lbfgs",
    )

    model = Pipeline(steps=[
        ("preprocess", preprocess),
        ("clf", clf),
    ])

    model.fit(X_train, y_train)

    # --- Validation metrics ---
    val_proba = model.predict_proba(X_val)[:, 1]
    val_pred = (val_proba >= 0.5).astype(int)

    roc = roc_auc_score(y_val, val_proba)
    ap = average_precision_score(y_val, val_proba)
    cm = confusion_matrix(y_val, val_pred)

    logger.info("Validation Metrics")
    logger.info(f"  ROC-AUC: {roc:.4f}")
    logger.info(f"  PR-AUC (Average Precision): {ap:.4f}")
    logger.info("Confusion Matrix @ threshold=0.5")
    logger.info(cm)
    logger.info("Classification Report @ threshold=0.5")
    logger.info(classification_report(y_val, val_pred, digits=4))

    _print_top_coefficients(model, cat_cols, num_cols, top_k=15)

    # --- Save model ---
    dump(
        {
            "model": model,
            "cat_cols": cat_cols,
            "num_cols": num_cols,
            "id_col": ID_COL,
            "target_col": TARGET_COL,
        },
        MODEL_FILE,
    )
    logger.info(f"\nSaved model to: {MODEL_FILE}")

    # --- Save validation predictions (for analysis / thresholding) ---
    out_val = validation_df[[ID_COL, TARGET_COL]].copy()
    out_val["p_churn"] = val_proba.astype("float64")
    out_val["pred_churn_0p5"] = val_pred.astype("int8")
    out_val.to_parquet(VAL_PRED_FILE, index=False)
    logger.info(f"Saved validation predictions to: {VAL_PRED_FILE}")


if __name__ == "__main__":
    main()
