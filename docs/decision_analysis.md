# Decision Analysis – From Prediction to Action (Phase 6)

## Objective

The objective of this phase is to translate churn probability predictions
into **concrete business decisions** under realistic cost and resource
constraints.

Rather than evaluating model quality in isolation, this phase focuses on:
- identifying who should be targeted
- quantifying the value of model-based targeting
- comparing model-driven decisions with naive baselines

---

## Setup and Assumptions

We simulate a customer retention intervention with the following assumptions:

- Each contacted customer incurs a fixed cost.
- Only customers who would churn can generate benefit if successfully retained.
- Resources are limited: only the top-K customers can be contacted.

The analysis is conducted offline using the validation dataset.

---

## Decision Policies Evaluated

Two decision policies are compared:

### 1. Top-K Risk-Based Targeting

Customers are ranked by predicted churn probability (`p_churn`), and the top-K
customers are selected for intervention.

### 2. Random Targeting Baseline

K customers are selected uniformly at random, ignoring model predictions.

This baseline represents a naive strategy with no predictive signal.

---

## Results: Top-K Targeting

| K | True Churners | Total Cost | Total Benefit | Net Gain |
|---|---------------|------------|---------------|----------|
| 20  | 17  | 20  | 51  | 31  |
| 50  | 41  | 50  | 123 | 73  |
| 100 | 78  | 100 | 234 | 134 |
| 200 | 141 | 200 | 423 | 223 |
| 300 | 197 | 300 | 591 | 291 |
| 500 | 277 | 500 | 831 | 331 |
| 800 | 345 | 800 | 1035 | 235 |

**Observations:**
- Net gain increases rapidly for small K and peaks around K ≈ 500.
- For very large K, marginal returns diminish as lower-risk customers are included.
- The model concentrates true churners effectively in the head of the ranking.

---

## Results: Random Targeting Baseline

| K | Net Gain |
|---|----------|
| 20  | −5  |
| 50  | −8  |
| 100 | −22 |
| 200 | −29 |
| 300 | −54 |
| 500 | −86 |
| 800 | −152 |

**Observations:**
- Random targeting produces negative net gain for all K.
- Contacting customers without predictive ranking destroys value under the
  current cost–benefit assumptions.

---

## Comparative Analysis

Key differences between the two policies:

- **Sign of returns**  
  - Top-K targeting yields positive net gain across a wide range of K.
  - Random targeting is consistently loss-making.

- **Efficiency**  
  - Top-K targeting achieves positive returns with small K (e.g. K = 20, 50).
  - Random targeting fails even when scaling outreach.

- **Resource sensitivity**  
  - Model-based targeting is effective under strict capacity constraints.
  - Random targeting cannot be justified under any realistic budget.

---

## Interpretation

These results demonstrate that:

1. **Prediction quality alone is insufficient**  
   High AUC or accuracy does not automatically translate into business value.

2. **Decision value depends on ranking quality at the head**  
   The model’s ability to concentrate true churners in the top of the score
   distribution enables profitable decisions.

3. **Cost and capacity constraints are decisive**  
   Under realistic assumptions, only selective targeting creates value.

4. **Risk-based targeting already encodes uplift intuition**  
   While no explicit treatment effect is modeled, prioritizing high-risk
   customers approximates an incremental value strategy under simplifying
   assumptions.

---

## Limitations

- The analysis assumes all contacted churners can be successfully retained.
- Negative effects of contacting non-churners are not explicitly modeled.
- The dataset does not include treatment or exposure information, preventing
  true causal uplift modeling.

---

## Conclusion

Under realistic cost and resource constraints, **model-based top-K targeting
clearly dominates random outreach**, converting churn predictions into
measurable business value.

This phase completes the transition from:
> *“Can we predict churn?”*  
to  
> *“Who should we act on, and why?”*

The resulting decision framework provides a strong foundation for future
extensions such as uplift modeling or policy optimization.

---

## Suggested Next Steps

- Formalize the decision policy as a reusable module.
- Optimize K based on budget or operational constraints.
- Extend the framework with treatment data to enable causal uplift modeling.
