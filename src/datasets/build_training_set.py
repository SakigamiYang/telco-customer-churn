# coding: utf-8
import pandas as pd
from loguru import logger

from constants import DATA
from datasets.splits import stratified_split

FEATURE_FILE = DATA / "features" / "telco_customer_features.parquet"
CLEAN_FILE = DATA / "staging" / "telco_customers_clean.parquet"
TRAIN_FILE = DATA / "datasets" / "train.parquet"
VALIDATION_FILE = DATA / "datasets" / "validation.parquet"
INFERENCE_FILE = DATA / "datasets" / "inference.parquet"


def _log_class_balance(df: pd.DataFrame, name: str) -> None:
    """
    Print row count and churn rate for sanity check.
    """
    n = len(df)
    churn_rate = df["churn"].mean()
    logger.info(f"[{name}] rows={n}, churn_rate={churn_rate:.4f}")


def main():
    feature_df = pd.read_parquet(FEATURE_FILE)
    clean_df = pd.read_parquet(CLEAN_FILE)

    # Build labels (target)
    label_df = clean_df[["customer_id", "churn"]].copy()
    label_df["churn"] = label_df["churn"].astype("int8")

    # Join labels to features for supervised training
    feature_label_df = feature_df.merge(label_df, on="customer_id", how="inner", validate="one_to_one")

    # --- Sanity check: join should not drop rows ---
    if len(feature_label_df) != len(feature_df):
        dropped = len(feature_df) - len(feature_label_df)
        raise ValueError(
            f"Feature–label join dropped {dropped} rows. "
            f"Check customer_id consistency between features and staging."
        )

    # Train/Validation split (stratified)
    train_df, validation_df = stratified_split(feature_label_df, target="churn", test_size=0.2, random_state=42)

    # --- Log class balance ---
    _log_class_balance(train_df, "train")
    _log_class_balance(validation_df, "validation")

    # Inference dataset: features only (no churn)
    inference_df = feature_df.copy()

    train_df.to_parquet(TRAIN_FILE, index=False)
    validation_df.to_parquet(VALIDATION_FILE, index=False)
    inference_df.to_parquet(INFERENCE_FILE, index=False)


if __name__ == '__main__':
    main()
