# Telco Customer Churn

## Dataset Descripiton

This dataset represents a snapshot of customers from a subscription-based telecom company. <br />
Each row corresponds to a single customer and describes their demographic attricutes, service subscriptions, 
contract details, and billing information.

The target variable `Churn` indicates whether the customer left the company after the observed snapshot period.

---

## Unit of Observation

- One row = one customer
- Granularity: customer-level
- Temporal nature: static snapshot (no event-level timestamps)

---

## Columns Classification

### Identifiers

- customerID: unique identifier of a customer

### Customer Attributes

- gender
- SeniorCitizen
- Partner
- Dependents

These attributes are relatively stable and describe the customer rather than usage behavior.

---

### Service and Contract Characteristics

- PhoneService
- MultipleLines
- InternetService
- OnlineSecurity
- OnlineBackup
- DeviceProtection
- TechSupport
- StreamingTV
- StreamingMovies
- Contract
- PaperlessBilling
- PaymentMethod

These variables describe the services the customer subscribes to and how they are billed.

---

### Billing and Tenure Information

- tenure: number of months the customer has stayed with the company
- MonthlyCharges: current monthly fee
- TotalCharges: cumulative charges over the customer’s lifetime

These variables act as proxies for usage intensity and customer value.

---

### Outcome Variables

- Churn: binary indicator of whether the customer churned

This variable must not be used for feature construction or decision logic prior to modeling.

---

## Business Interpretation

The dataset can be used to estimate churn risk at the customer level and to rank customers
for retention actions under budget constraints.

Due to the snapshot nature of the data, causal effects of interventions cannot be identified,
and any evaluation of retention strategies must be treated as offline approximation.
