# coding: utf-8
import numpy as np
import pandas as pd
from loguru import logger

from constants import DATA

IN_FILE = DATA / "features" / "telco_customer_features.parquet"

REQUIRED_COLS = [
    "customer_id",
    "is_senior",
    "has_partner",
    "has_dependents",
    "is_month_to_month",
    "contract_type",
    "has_phone_service",
    "has_multiple_lines",
    "has_internet_service",
    "num_internet_addons",
    "tenure",
    "tenure_bucket",
    "monthly_charges",
    "total_charges",
    "avg_monthly_charges",
]


def main():
    df = pd.read_parquet(IN_FILE)

    # 1) Column presence
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required feature columns: {missing}")

    # 2) Uniqueness
    if df["customer_id"].isna().any():
        raise ValueError("customer_id contains NULLs")

    if df["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer_id found in feature table")

    # 3) Null checks (Phase 3 policy: features should be non-null)
    null_counts = df[REQUIRED_COLS].isna().sum()
    if (null_counts > 0).any():
        bad = null_counts[null_counts > 0].sort_values(ascending=False)
        raise ValueError(f"Unexpected NULLs in feature table:\n{bad}")

    # 4) Numeric sanity
    if (df["tenure"] < 0).any():
        raise ValueError("tenure has negative values")

    if (df["monthly_charges"] < 0).any():
        raise ValueError("monthly_charges has negative values")

    # avg_monthly_charges must be finite
    if not np.isfinite(df["avg_monthly_charges"].to_numpy()).all():
        raise ValueError("avg_monthly_charges contains inf or NaN")

    # num_internet_addons should be within [0, 6]
    if ((df["num_internet_addons"] < 0) | (df["num_internet_addons"] > 6)).any():
        raise ValueError("num_internet_addons out of expected range [0, 6]")

    logger.info("Feature checks passed.")


if __name__ == '__main__':
    main()
