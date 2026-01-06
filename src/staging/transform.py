# coding: utf-8
import pandas as pd

from constants import DATA

IN_FILE = DATA / "staging" / "telco_customers_staging.parquet"
OUT_FILE = DATA / "staging" / "telco_customers_clean.parquet"

NO_PHONE_MAP = {"No phone service": "NoPhone"}
NO_INTERNET_MAP = {"No internet service": "NoInternet"}

INTERNET_ADDON_COLS = [
    "online_security",
    "online_backup",
    "device_protection",
    "tech_support",
    "streaming_tv",
    "streaming_movies",
]


def strip_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip whitespace on all string columns

    :param df:
    :return:
    """

    string_cols = df.select_dtypes(include=["object", "string"]).columns
    for c in string_cols:
        df[c] = df[c].astype("string").str.strip()
    return df


def canonicalize_vocabulary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Canonicalize “No internet service” / “No phone service”
    No internet service -> NoInternet
    No phone service -> NoPhone

    :param df:
    :return:
    """

    df["multiple_lines"] = df["multiple_lines"].replace(NO_PHONE_MAP)

    for col in INTERNET_ADDON_COLS:
        df[col] = df[col].replace(NO_INTERNET_MAP)

    return df


def normalize_phone_service(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize binary categorical tokens (for phone_service)

    :param df:
    :return:
    """

    df["phone_service"] = df["phone_service"].replace({"yes": "Yes", "no": "No"})
    return df


def main():
    df = pd.read_parquet(IN_FILE)
    df = strip_string_columns(df)
    df = canonicalize_vocabulary(df)
    df = normalize_phone_service(df)
    df.to_parquet(OUT_FILE, index=False)


if __name__ == '__main__':
    main()
