# Baseline Modeling – Logistic Regression (Phase 5)

## Objective

The goal of this phase is to establish a **simple, interpretable baseline**
for customer churn prediction using the features constructed in Phase 3 and
the datasets built in Phase 4.

The baseline is intended to:

- provide a performance reference point
- enable direct interpretation of feature effects
- support downstream decision analysis (e.g., threshold or top-K selection)

---

## Model Choice

**Model:** Logistic Regression  
**Implementation:** scikit-learn (`LogisticRegression`)

Rationale:

- interpretable coefficients
- well-understood behavior
- strong baseline for binary classification
- suitable for small-to-medium tabular datasets

Categorical features are one-hot encoded.
Numeric features are standardized.

Class imbalance is handled using:

- `class_weight="balanced"`

---

## Input Data

- Training set: `data/datasets/train.parquet`
- Validation set: `data/datasets/validation.parquet`

Target:

- `churn` ∈ {0, 1}

No feature is constructed using the target variable.

---

## Evaluation Metrics

The model is evaluated on the validation set using:

- ROC-AUC (ranking ability)
- PR-AUC / Average Precision (performance under class imbalance)
- Confusion matrix and classification report at threshold = 0.5

Predicted churn probabilities (`p_churn`) are saved for further analysis.

---

## Results (Validation)

Key observations:

- The model provides meaningful separation between churn and non-churn users.
- Contract-related and tenure-related features show strong effects.
- The baseline significantly outperforms a naive predictor based on churn rate alone.

(Exact metric values are printed during training and can be reproduced.)

---

## Model Interpretation

Coefficient analysis indicates:

- Month-to-month contracts and short tenure increase churn risk.
- Longer tenure and fixed-term contracts reduce churn risk.
- Service complexity and billing characteristics contribute additional signal.

These effects are directionally consistent with domain expectations.

---

## Limitations

- Random split is used due to lack of temporal information.
- The baseline does not capture non-linear feature interactions.
- Threshold = 0.5 is not optimized for business objectives.
