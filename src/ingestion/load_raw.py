# coding: utf-8
import pandas as pd
from loguru import logger

from constants import DATA
from ingestion.schemas import staging_schema
from log_utils import log_dataframe

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

RAW_FILE = DATA / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"


def apply_schema(df: pd.DataFrame, schema) -> pd.DataFrame:
    rename_map = {k: v["name"] for k, v in schema.items()}
    df = df.rename(columns=rename_map)

    bool_mapping = {
        'Yes': True, 'No': False,
        'yes': True, 'no': False,
        '1': True, '0': False,
        1: True, 0: False
    }

    for old_name, config in schema.items():
        new_name = config["name"]
        dtype = config["type"]

        logger.info(f"handling {new_name} ...")
        if dtype == "string":
            df[new_name] = df[new_name].astype("string")

        elif dtype == "integer":
            df[new_name] = pd.to_numeric(df[new_name]).astype("Int64")

        elif dtype == "float":
            raw = df[new_name].astype("string")
            clean = raw.str.strip()
            clean = clean.mask(clean.eq(""), pd.NA)
            s = pd.to_numeric(clean, errors="coerce")

            if s.isna().any():
                bad_idx = s.isna()
                sample = pd.DataFrame({
                    "customer_id": df.loc[bad_idx, "customer_id"].astype("string"),
                    "tenure": df.loc[bad_idx, "tenure"],
                    f"raw_{new_name}": raw.loc[bad_idx],
                    f"clean_{new_name}": clean.loc[bad_idx],
                })

                log_dataframe(sample, "Float parse produced NaNs", level=logger.warning)

                top_raw = raw.loc[bad_idx].value_counts(dropna=False)
                log_dataframe(top_raw, "Top raw values that failed parsing", level=logger.warning)

            df[new_name] = s.astype("float64")

        elif dtype == "boolean":
            mapped = df[new_name].map(bool_mapping)
            if mapped.isna().any():
                bad = df.loc[mapped.isna(), new_name].astype(str).value_counts().head(5)
                raise ValueError(f"{new_name}: unmapped boolean values:\n{bad}")
            df[new_name] = mapped.astype("boolean")

    return df


df = pd.read_csv(RAW_FILE)
df = apply_schema(df, staging_schema)
log_dataframe(df, "loaded raw:", level=logger.warning)
df.to_parquet(DATA / "staging" / "telco_customers_staging.parquet")
