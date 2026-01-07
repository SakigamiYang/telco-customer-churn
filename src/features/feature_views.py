# coding: utf-8
import pandas as pd

INTERNET_ADDON_COLS = [
    "online_security",
    "online_backup",
    "device_protection",
    "tech_support",
    "streaming_tv",
    "streaming_movies",
]


def build_customer_profile_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Customer profile features.
    Output columns:
      - customer_id
      - is_senior
      - has_partner
      - has_dependents
    """
    out = pd.DataFrame({
        "customer_id": df["customer_id"].astype("string"),
        "is_senior": df["senior_citizen"].astype("int8"),
        "has_partner": df["partner"].astype("int8"),
        "has_dependents": df["dependents"].astype("int8"),
    })
    return out


def build_contract_service_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Contract & Services features
    Output columns:
    - customer_id
    - is_month_to_month
    - contract_type
    - has_phone_service
    - has_multiple_lines
    - has_internet_service
    - num_internet_addons
    """

    out = pd.DataFrame({
        "customer_id": df["customer_id"].astype("string"),
        "is_month_to_month": df["contract"].eq("Month-to-month").astype("int8"),
        "contract_type": df["contract"].astype("category"),
        "has_phone_service": df["phone_service"].eq("Yes").astype("int8"),
        "has_multiple_lines": df["multiple_lines"].eq("Yes").astype("int8"),
        "has_internet_service": df["internet_service"].ne("No").astype("int8"),
        "num_internet_addons": (df[INTERNET_ADDON_COLS].eq("Yes")).sum(axis=1).astype("int16"),
    })
    return out


def build_tenure_billing_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tenure & Billing Proxies features
    Output columns:
    - customer_id
    - tenure
    - tenure_bucket
    - monthly_charges
    - total_charges
    - avg_monthly_charges
    """

    tenure_int = df["tenure"].astype("int32")
    tenure_float = tenure_int.astype("float64")
    total = df["total_charges"].fillna(0.0).astype("float64")
    avg = (total / tenure_float).where(tenure_int > 0, 0.0)

    out = pd.DataFrame({
        "customer_id": df["customer_id"].astype("string"),
        "tenure": tenure_int,
        "tenure_bucket": pd.cut(
            tenure_int,
            bins=[0, 6, 12, 24, 10_000],
            labels=[
                "tenure_new",
                "tenure_early",
                "tenure_stable",
                "tenure_loyal",
            ],
            right=False,
            include_lowest=True,
        ).astype("category"),
        "monthly_charges": df["monthly_charges"].astype("float64"),
        "total_charges": total,
        "avg_monthly_charges": avg.astype("float64"),
    })
    return out
