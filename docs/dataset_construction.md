# Dataset Construction (Phase 4)

This document describes how model-ready datasets are constructed from the
feature table, including target attachment, split strategy, leakage controls,
and inference dataset definition.

---

## Inputs

- Feature table (Phase 3 output):
  - `data/features/telco_customer_features.parquet`

- Clean staging table (Phase 2 output, used only for labels):
  - `data/staging/telco_customers_clean.parquet`

---

## Outputs

- Training dataset (features + target):
  - `data/datasets/train.parquet`

- Validation dataset (features + target):
  - `data/datasets/validation.parquet`

- Inference dataset (features only, no target):
  - `data/datasets/inference.parquet`

---

## Target Definition

- Target column: `churn`
- Source: `telco_customers_clean.parquet`
- Encoding: binary integer `{0,1}`

Target values are joined to the feature table by `customer_id` during dataset
construction. No feature logic depends on `churn`.

---

## Split Strategy

### Why a random split?
The Telco dataset used in this project does not include timestamps suitable
for point-in-time training or temporal backtesting. Therefore, a stratified
random split is used.

### Implementation
- Stratified split on `churn`
- Validation size: 20%
- Random seed: 42
- Reproducible outputs

This produces:
- `train.parquet` (80%)
- `validation.parquet` (20%)

---

## Inference Dataset Definition

The inference dataset is defined as:
- **All customers in the feature table**
- **No target column included**

File:
- `data/datasets/inference.parquet`

This dataset is intended to simulate an online scoring population and is not
used for generalization evaluation. Model evaluation is performed using the
validation set.

Note: If an “unseen-only inference” population is desired, an alternative
dataset can be created by excluding customer_ids used in training/validation.
This is optional and not enabled by default in this project.

---

## Leakage Controls

The pipeline enforces the following leakage controls:

1. Features are built without using `churn` (Phase 3).
2. `churn` is joined only during dataset construction (Phase 4).
3. Split logic is applied only after the label join.
4. Inference dataset does not contain `churn`.

---

## Quality Checks

Dataset integrity checks are implemented in `src/datasets/checks.py`:

- `customer_id` uniqueness per dataset
- No overlap of `customer_id` between train and validation
- Train/validation feature columns match exactly
- `churn` exists only in train/validation, never in inference
- No inf/NaN values in numeric features
- Basic churn rate logging for sanity

---

## Limitations

- Random splits may overestimate performance compared to real temporal
  deployment settings.
- Without timestamps, true point-in-time feature correctness cannot be
  backtested on this dataset.

In a production setting, temporal splits and backtesting should be used.
