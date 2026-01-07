# Feature Definitions (Telco Customer Churn) (Stage 3)

This document defines the feature table produced in Phase 3:
`data/features/telco_customer_features.parquet`.

The feature layer is built from `telco_customers_clean.parquet` and does not
use the target variable (`churn`) to construct any features.

---

## Entity Key

- `customer_id` (string)  
  Unique customer identifier. Primary key for feature tables.

---

## Customer Profile Features

- `is_senior` (int8, 0/1)  
  1 if the customer is a senior citizen, else 0.  
  Source: `senior_citizen`.

- `has_partner` (int8, 0/1)  
  1 if the customer has a partner, else 0.  
  Source: `partner`.

- `has_dependents` (int8, 0/1)  
  1 if the customer has dependents, else 0.  
  Source: `dependents`.

---

## Contract & Service Features

- `is_month_to_month` (int8, 0/1)  
  1 if the customer is on a month-to-month contract, else 0.  
  Source: `contract`.

- `contract_type` (category)  
  Contract category: `Month-to-month`, `One year`, `Two year`.  
  Source: `contract`.

- `has_phone_service` (int8, 0/1)  
  1 if the customer has phone service, else 0.  
  Source: `phone_service` (canonical: `Yes/No`).

- `has_multiple_lines` (int8, 0/1)
  1 if the customer has phone service and has multiple lines, else 0.
  Source: `multiple_lines` (canonical: `Yes/No/NoPhone`).

- `has_internet_service` (int8, 0/1)  
  1 if the customer has an internet service (DSL or Fiber optic), else 0.  
  Source: `internet_service`.

- `num_internet_addons` (int16)  
  Count of internet add-on services enabled (`Yes`) among:  
  `online_security`, `online_backup`, `device_protection`, `tech_support`,
  `streaming_tv`, `streaming_movies`.  
  Range: 0–6.

---

## Tenure & Billing Features

- `tenure` (int32)  
  Number of months the customer has stayed with the company.  
  Source: `tenure`.

- `tenure_bucket` (category)  
  Coarse customer lifecycle bucket based on tenure:
    - `tenure_new`: 0–5 months
    - `tenure_early`: 6–11 months
    - `tenure_stable`: 12–23 months
    - `tenure_loyal`: 24+ months

- `monthly_charges` (float64)  
  Current monthly fee.  
  Source: `monthly_charges`.

- `total_charges` (float64)  
  Lifetime cumulative charges. In the source data, `total_charges` is missing
  for some customers with `tenure == 0`; in the feature table it is filled with 0.0.  
  Source: `total_charges` (with conditional fill).

- `avg_monthly_charges` (float64)  
  Average monthly charges computed as `total_charges / tenure` for `tenure > 0`,
  else 0.0.  
  Rationale: proxy for customer value and billing intensity.