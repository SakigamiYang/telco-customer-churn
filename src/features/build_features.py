# coding: utf-8
import pandas as pd

from constants import DATA
from feature_views import (
    build_customer_profile_features,
    build_contract_service_features,
    build_tenure_billing_features
)

IN_FILE = DATA / "staging" / "telco_customers_clean.parquet"
OUT_FILE = DATA / "features" / "telco_customer_features.parquet"


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    base = df[["customer_id"]].copy()

    df_profile = build_customer_profile_features(df)
    df_contract = build_contract_service_features(df)
    df_billing = build_tenure_billing_features(df)

    out = (
        base
        .merge(df_profile, on="customer_id", how="left", validate="one_to_one")
        .merge(df_contract, on="customer_id", how="left", validate="one_to_one")
        .merge(df_billing, on="customer_id", how="left", validate="one_to_one")
    )

    return out


def main():
    df = pd.read_parquet(IN_FILE)
    out = build_features(df)

    if len(out) != len(df):
        raise ValueError(f"Row count mismatch: staging={len(df)} vs features={len(out)}")

    if out["customer_id"].duplicated().any():
        raise ValueError("Duplicate customer_id found in feature output")

    out.to_parquet(OUT_FILE, index=False)


if __name__ == '__main__':
    main()
