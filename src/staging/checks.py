# coding: utf-8
import pandas as pd
from loguru import logger

from constants import DATA
from log_utils import log_dataframe
from staging.transform import INTERNET_ADDON_COLS

IN_FILE = DATA / "staging" / "telco_customers_clean.parquet"

# --- Domain definitions (canonical values expected after transform) ---
DOMAIN_VALUES = {
    "gender": {"Male", "Female"},
    "phone_service": {"Yes", "No"},
    "multiple_lines": {"Yes", "No", "NoPhone"},
    "internet_service": {"DSL", "Fiber optic", "No"},
    "online_security": {"Yes", "No", "NoInternet"},
    "online_backup": {"Yes", "No", "NoInternet"},
    "device_protection": {"Yes", "No", "NoInternet"},
    "tech_support": {"Yes", "No", "NoInternet"},
    "streaming_tv": {"Yes", "No", "NoInternet"},
    "streaming_movies": {"Yes", "No", "NoInternet"},
    "contract": {"Month-to-month", "One year", "Two year"},
    "payment_method": {
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)",
    },
}

# Some columns may legitimately contain missing values in staging/clean.
# We keep this explicit to avoid accidental "string 'nan'" problems.
NULL_POLICY = {
    # total_charges can be NA only when tenure == 0 (validated in invariant checks)
    "total_charges": "conditional",
    # everything else below is expected non-null after cleaning
    "gender": "no_null",
    "phone_service": "no_null",
    "multiple_lines": "no_null",
    "internet_service": "no_null",
    "contract": "no_null",
    "payment_method": "no_null",
}


def domain_check(df) -> None:
    """
    Validate that categorical columns contain only canonical values
    after Phase 2 transformations.

    Fail-fast: raise if any invalid value exists.
    """

    for col, values in DOMAIN_VALUES.items():
        # Null handling: require non-null for all domain columns in this phase
        if df[col].isna().any():
            bad = df.loc[df[col].isna(), ["customer_id", col]]
            log_dataframe(
                bad,
                f"Domain check `{col}`: NULL values found (unexpected)",
                max_rows=20,
                level=logger.error,
            )
            raise ValueError(f"Domain check `{col}` failed: NULL values present")

        invalid_mask = ~df[col].isin(values)
        if invalid_mask.any():
            bad = df.loc[invalid_mask, ["customer_id", col]]
            log_dataframe(
                bad,
                f"Domain check `{col}` failed: values must be in {values!r}",
                max_rows=50,
                level=logger.error,
            )
            raise ValueError(f"Domain check `{col}` failed: invalid values present")

        logger.info(f"Domain check `{col}` OK")


def invariant_check(df):
    """
    Validate cross-field invariants and numeric constraints.

    Invariants are intentionally implemented as explicit checks.
    This keeps the logic auditable and easy to maintain.
    """

    # --- Invariant 0: customer_id uniqueness ---
    dup_mask = df["customer_id"].duplicated(keep=False)
    if dup_mask.any():
        bad = df.loc[dup_mask, ["customer_id"]]
        log_dataframe(bad, "Invariant failed: customer_id must be unique", max_rows=50, level=logger.error)
        raise ValueError("Invariant failed: customer_id duplicates found")
    logger.info("Invariant OK: customer_id is unique")

    # --- Invariant 1: tenure is non-negative and non-null ---
    if df["tenure"].isna().any():
        bad = df.loc[df["tenure"].isna(), ["customer_id", "tenure"]]
        log_dataframe(bad, "Invariant failed: tenure is NULL", max_rows=20, level=logger.error)
        raise ValueError("Invariant failed: tenure NULL")

    if (df["tenure"] < 0).any():
        bad = df.loc[df["tenure"] < 0, ["customer_id", "tenure"]]
        log_dataframe(bad, "Invariant failed: tenure must be >= 0", max_rows=20, level=logger.error)
        raise ValueError("Invariant failed: tenure < 0")
    logger.info("Invariant OK: tenure >= 0 and non-null")

    # --- Invariant 2: total_charges null policy ---
    # Allowed: total_charges is NA only when tenure == 0
    null_total = df["total_charges"].isna()
    invalid_null_total = null_total & (df["tenure"] > 0)
    if invalid_null_total.any():
        bad = df.loc[invalid_null_total, ["customer_id", "tenure", "total_charges"]]
        log_dataframe(
            bad,
            "Invariant failed: total_charges can be NULL only when tenure == 0",
            max_rows=50,
            level=logger.error,
        )
        raise ValueError("Invariant failed: unexpected NULL total_charges for tenure > 0")
    logger.info("Invariant OK: total_charges NULL policy")

    # --- Invariant 3: PhoneService <-> MultipleLines ---
    # If phone_service == "No" then multiple_lines must be "NoPhone"
    mask_no_phone = df["phone_service"].eq("No")
    bad_no_phone = mask_no_phone & ~df["multiple_lines"].eq("NoPhone")
    if bad_no_phone.any():
        bad = df.loc[bad_no_phone, ["customer_id", "phone_service", "multiple_lines"]]
        log_dataframe(bad, "Invariant failed: phone_service='No' => multiple_lines='NoPhone'",
                      max_rows=50, level=logger.error)
        raise ValueError("Invariant failed: phone_service='No' but multiple_lines not 'NoPhone'")

    # If phone_service == "Yes" then multiple_lines must be Yes/No
    mask_yes_phone = df["phone_service"].eq("Yes")
    bad_yes_phone = mask_yes_phone & ~df["multiple_lines"].isin({"Yes", "No"})
    if bad_yes_phone.any():
        bad = df.loc[bad_yes_phone, ["customer_id", "phone_service", "multiple_lines"]]
        log_dataframe(bad, "Invariant failed: phone_service='Yes' => multiple_lines in {'Yes','No'}",
                      max_rows=50, level=logger.error)
        raise ValueError("Invariant failed: phone_service='Yes' but multiple_lines not in {'Yes','No'}")

    logger.info("Invariant OK: phone_service <-> multiple_lines")

    # --- Invariant 4: InternetService <-> Add-on service columns ---
    # If internet_service == "No" then all add-ons must be "NoInternet"
    mask_no_internet = df["internet_service"].eq("No")
    for c in INTERNET_ADDON_COLS:
        bad_addon = mask_no_internet & ~df[c].eq("NoInternet")
        if bad_addon.any():
            bad = df.loc[bad_addon, ["customer_id", "internet_service", c]]
            log_dataframe(
                bad,
                f"Invariant failed: internet_service='No' => {c}='NoInternet'",
                max_rows=50,
                level=logger.error,
            )
            raise ValueError(f"Invariant failed: internet_service='No' but {c} not 'NoInternet'")

    logger.info("Invariant OK: internet_service <-> add-ons")


def main():
    df = pd.read_parquet(IN_FILE)
    domain_check(df)
    invariant_check(df)
    logger.info("All Phase 2 checks passed.")


if __name__ == '__main__':
    main()
