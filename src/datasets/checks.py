# coding: utf-8
import numpy as np
import pandas as pd
from loguru import logger

from constants import DATA

TRAIN_FILE = DATA / "datasets" / "train.parquet"
VALIDATION_FILE = DATA / "datasets" / "validation.parquet"
INFERENCE_FILE = DATA / "datasets" / "inference.parquet"

TARGET_COL = "churn"
ID_COL = "customer_id"


def _require_columns(df: pd.DataFrame, cols: list[str], name: str) -> None:
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"[{name}] Missing required columns: {missing}")


def _log_basic_stats(df: pd.DataFrame, name: str, has_target: bool) -> None:
    n = len(df)
    logger.info(f"[{name}] rows={n}")

    if df[ID_COL].duplicated().any():
        raise ValueError(f"[{name}] Duplicate {ID_COL} found")

    if df[ID_COL].isna().any():
        raise ValueError(f"[{name}] {ID_COL} contains NULLs")

    if has_target:
        if df[TARGET_COL].isna().any():
            raise ValueError(f"[{name}] {TARGET_COL} contains NULLs")

        churn_rate = float(df[TARGET_COL].mean())
        logger.info(f"[{name}] churn_rate={churn_rate:.4f}")


def _check_no_inf_nan_numeric(df: pd.DataFrame, name: str) -> None:
    # Only check numeric columns
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if not num_cols:
        return

    arr = df[num_cols].to_numpy()
    if not np.isfinite(arr).all():
        # Find first few problematic cells for debugging
        bad_mask = ~np.isfinite(arr)
        bad_locs = np.argwhere(bad_mask)
        sample = bad_locs[:10]
        details = []
        for r, c in sample:
            details.append((df.index[r], num_cols[c], df.iloc[r][num_cols[c]]))
        raise ValueError(f"[{name}] Numeric columns contain inf/NaN. Sample: {details}")


def main() -> None:
    train_df = pd.read_parquet(TRAIN_FILE)
    val_df = pd.read_parquet(VALIDATION_FILE)
    inf_df = pd.read_parquet(INFERENCE_FILE)

    # --- Target presence rules ---
    _require_columns(train_df, [ID_COL, TARGET_COL], "train")
    _require_columns(val_df, [ID_COL, TARGET_COL], "validation")
    _require_columns(inf_df, [ID_COL], "inference")

    if TARGET_COL in inf_df.columns:
        raise ValueError("[inference] Target column churn must NOT exist in inference dataset")

    # --- Feature columns must match between train and validation (excluding target) ---
    train_feat_cols = [c for c in train_df.columns if c != TARGET_COL]
    val_feat_cols = [c for c in val_df.columns if c != TARGET_COL]

    if set(train_feat_cols) != set(val_feat_cols):
        only_in_train = sorted(set(train_feat_cols) - set(val_feat_cols))
        only_in_val = sorted(set(val_feat_cols) - set(train_feat_cols))
        raise ValueError(
            "Train/Validation feature columns mismatch.\n"
            f"Only in train: {only_in_train}\n"
            f"Only in validation: {only_in_val}"
        )

    # --- No overlap of customer_id between train and validation ---
    overlap = set(train_df[ID_COL]) & set(val_df[ID_COL])
    if overlap:
        # Print a small sample for debugging
        sample = list(overlap)[:10]
        raise ValueError(f"Train/Validation overlap detected in {ID_COL}. Sample: {sample}")

    # --- Basic stats & sanity ---
    _log_basic_stats(train_df, "train", has_target=True)
    _log_basic_stats(val_df, "validation", has_target=True)
    _log_basic_stats(inf_df, "inference", has_target=False)

    # --- Numeric inf/NaN checks (very common failure: avg_monthly_charges) ---
    _check_no_inf_nan_numeric(train_df, "train")
    _check_no_inf_nan_numeric(val_df, "validation")
    _check_no_inf_nan_numeric(inf_df, "inference")

    # --- Optional: churn domain check ---
    if not set(train_df[TARGET_COL].unique()).issubset({0, 1}):
        raise ValueError("[train] churn must be in {0,1}")
    if not set(val_df[TARGET_COL].unique()).issubset({0, 1}):
        raise ValueError("[validation] churn must be in {0,1}")

    logger.info("Dataset checks passed.")


if __name__ == "__main__":
    main()
