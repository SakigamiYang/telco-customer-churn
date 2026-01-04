# Data Contracts

| Column Name       | Type    | Description                                                                                           | Notes                         |
|-------------------|---------|-------------------------------------------------------------------------------------------------------|-------------------------------|
| customer_id       | string  | Customer ID                                                                                           |                               |       |
| gender            | string  | Whether the customer is a male or a female                                                            |                               |
| senior_citizen    | boolean | Whether the customer is a senior citizen or not (Yes, No)                                             |                               |
| partner           | boolean | Whether the customer has a partner or not (Yes, No)                                                   |                               |
| dependents        | boolean | Whether the customer has dependents or not (Yes, No)                                                  |                               |
| tenure            | integer | Number of months the customer has stayed with the company                                             |                               |
| phone_service     | string  | Whether the customer has a phone service or not (Yes, No)                                             |                               |
| multiple_lines    | string  | Whether the customer has multiple lines or not (Yes, No, No phone service)                            | depends on `phone_service`    |
| internet_service  | string  | Customer’s internet service provider (DSL, Fiber optic, No)                                           |                               |
| online_security   | string  | Whether the customer has online security or not (Yes, No, No internet service)                        | depends on `internet_service` |
| online_backup     | string  | Whether the customer has online backup or not (Yes, No, No internet service)                          | depends on `internet_service` |
| device_protection | string  | Whether the customer has device protection or not (Yes, No, No internet service)                      | depends on `internet_service` |
| tech_support      | string  | Whether the customer has tech support or not (Yes, No, No internet service)                           | depends on `internet_service` |
| streaming_tv      | string  | Whether the customer has streaming TV or not (Yes, No, No internet service)                           | depends on `internet_service` |
| streaming_movies  | string  | Whether the customer has streaming movies or not (Yes, No, No internet service)                       | depends on `internet_service` |
| contract          | string  | The contract term of the customer (Month-to-month, One year, Two year)                                |                               |
| paperless_billing | string  | Whether the customer has paperless billing or not (Yes, No)                                           |                               |
| payment_method    | string  | The customer’s payment method (Electronic check, Mailed check, Bank transfer (automatic), Credit card |                               |
| monthly_charges   | float   | The amount charged to the customer monthly                                                            |                               |
| total_charges     | float   | The total amount charged to the customer                                                              |                               |
| churn             | boolean | Whether the customer churned or not (1 or 0)                                                          |                               |