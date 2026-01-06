# Staging Data Quality Report

## Scope
This document summarizes the data quality checks and invariants enforced
in the **staging layer (Phase 2)** for the Telco Customer Churn dataset.

Input dataset:
- `data/staging/telco_customers_staging.parquet`

Output dataset:
- `data/staging/telco_customers_clean.parquet`

All checks described below are enforced programmatically in
`src/staging/checks.py`.

---

## Row Count & Uniqueness

- Number of rows: 7,043
- Unit of observation: customer
- Primary key: `customer_id`

**Checks**
- `customer_id` is unique  
- No duplicate rows detected

**Status**: ✅ Pass

---

## Missing Value Policy

The following missing value rules are enforced:

| Column           | Allowed Missing     | Rule                              |
|------------------|---------------------|-----------------------------------|
| total_charges    | Yes (conditional)   | Missing only when `tenure == 0`   |
| tenure           | No                  | Must be non-null and ≥ 0          |
| monthly_charges  | No                  | Must be non-null and ≥ 0          |
| All other fields | No                  | Missing values not allowed        |

**Status**: ✅ Pass

---

## Categorical Domain Validation

All categorical columns are validated against canonical domains
after normalization.

Examples:

- `phone_service`: `{Yes, No}`
- `multiple_lines`: `{Yes, No, NoPhone}`
- `internet_service`: `{DSL, Fiber optic, No}`
- Internet add-on services: `{Yes, No, NoInternet}`
- `contract`: `{Month-to-month, One year, Two year}`
- `payment_method`: `{Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic)}`

No unexpected categories or casing/whitespace variants were found.

**Status**: ✅ Pass

---

## Cross-Field Invariants

The following business invariants are enforced:

### Phone Service vs Multiple Lines
- If `phone_service == "No"` then `multiple_lines == "NoPhone"`
- If `phone_service == "Yes"` then `multiple_lines in {"Yes","No"}`

### Internet Service vs Add-on Services
If `internet_service == "No"`, then all of the following must equal `"NoInternet"`:
- `online_security`
- `online_backup`
- `device_protection`
- `tech_support`
- `streaming_tv`
- `streaming_movies`

### Billing Consistency
- `total_charges` may be missing **only** when `tenure == 0`

All invariants were satisfied for the entire dataset.

**Status**: ✅ Pass

---

## Known Data Characteristics

- Customers with `tenure == 0` have missing `total_charges`
  due to no completed billing cycle.
- This condition is treated as valid and explicitly allowed.

No other systematic data quality issues were observed.

---

## Conclusion

The staging dataset `telco_customers_clean.parquet` is:
- clean
- internally consistent
- invariant-safe
- suitable as input for feature engineering (Phase 3)

Any downstream data issues should be treated as feature or modeling
concerns rather than data quality defects.

