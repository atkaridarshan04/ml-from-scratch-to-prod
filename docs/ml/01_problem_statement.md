## Problem Statement

### Business Objective

Estimate the **median house value** of a residential district in California based on aggregated census and geographic features.

This type of problem is relevant for:

* Real estate valuation
* Market analysis
* Policy and urban planning simulations

---

### Machine Learning Objective

Build a **regression model** that predicts `MedHouseVal` using available district-level features while:

* Maintaining interpretability
* Avoiding overfitting
* Providing a reliable performance baseline for further modeling

---

### Target Variable

* **Name:** `MedHouseVal`
* **Type:** Continuous
* **Meaning:** Median house value for a district
* **Unit:** Hundreds of thousands of dollars
  (e.g., value = 2.5 → $250,000)

---

### Evaluation Metric

* **RMSE (Root Mean Squared Error)**

**Rationale:**

* Penalizes large prediction errors
* Interpretable in monetary units
* Standard metric for regression problems involving prices

---

