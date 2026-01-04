# Decision-Aware Customer Churn Platform

***An end-to-end Data Engineering + Data Science project***

## Overview

This project demonstrates how to build a **decision-oriented data platform** using a real-world open dataset. <br />
Rather than focusing solely on predictive modeling, the project emphasizes the **full lifecycle** from raw data ingestion 
to **actionable business decisions** under resource constraints.

The use case is **customer churn prevention** in a subscription-based telecom business.

---

## Business Problem

Customer churn directly impacts recurring revenue. <br />
While predictive models can estimate churn probability, **business value is only realized when predictions are 
translated into decisions.**

Constraints:

- Retention actions (e.g. offers, calls) have **limited budget**
- Not all high-risk customers are worth intervening
- Data must be reliable, reproducible, and explainable

**Goal** <br />
Design a system that:

1. Produces stable, well-defined datasets
2. Trains a churn prediction model
3. Converts predictions into a **resource-constrained intervention policy**
4. Evaluates expected business impact offline

---

## Dataset

- **Telco Customer Churn Dataset** (open-source)
- Source: Kaggle / OpenML
- Granularity: one row per customer (snapshot)

---

## Project Structure

```powershell
Telco-Customer-Churn/
├── data/
│   ├── raw/            # Original dataset (immutable)
│   ├── staging/        # Cleaned, typed data
│   ├── features/       # Business features
│   └── artifacts/      # Models, scores, decisions
│
├── src/
│   ├── ingestion/      # Raw → staging
│   ├── features/       # Feature construction
│   ├── datasets/       # Train / inference datasets
│   ├── models/         # Prediction models
│   ├── decision/       # Decision policies
│   └── evaluation/     # Offline evaluation
│
├── docs/
│   ├── data_contracts.md
│   ├── feature_definitions.md
│   ├── decision_policy.md
│   └── evaluation.md
│
├── pipelines/
│   └── run_all.sh
│
└── README.md

```

---

## Methodology

1. **Data Engineering**
   - Schema definition and validation
   - Separation of raw, staging, and feature layers
   - Reproducible dataset construction
2. **Data Science**
   - Baseline churn prediction model
   - Transparent evaluation (ROC-AUC, Precision@K)
3. **Decision Science**
   - Budget-constrained intervention policy
   - Ranking-based decision making
   - Offline value estimation

---

## Key Concepts Demonstrated

- Prediction vs Decision
- Data contracts and schema stability
- Feature engineering with business meaning
- Resource-constrained decision policies
- Offline evaluation of strategies

--- 

## Disclaimer

This project is designed for **learning and demonstration purposes.** <br />
The dataset is a static snapshot and does not include real intervention outcomes; therefore, 
causal impact is approximated rather than identified.