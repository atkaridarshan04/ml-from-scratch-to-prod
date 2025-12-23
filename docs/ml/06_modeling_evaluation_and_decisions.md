# Modeling & Results Report

## Objective

The objective of this phase was to identify a regression model that:
- Generalizes well on unseen data
- Appropriately balances bias and variance
- Can serve as a strong baseline for further improvement or deployment

This phase focuses specifically on **model selection and evaluation**.
Feature engineering and advanced model families are intentionally deferred
to subsequent phases.

The target variable is `median_house_value`.

---

## Modeling Strategy Overview

The modeling process followed a **progressive complexity approach**:

1. Start with **simple linear models** to establish a baseline and diagnose bias
2. Introduce **regularization** to control variance
3. Move to **non-linear models** when linear assumptions proved limiting
4. Address variance explicitly using **ensemble methods**

Each transition between model families was driven by observed behavior,
not by convention or expected algorithm ranking.

---

## Evaluation Metrics

The following metrics were used consistently across models:

- **RMSE (Root Mean Squared Error)**  
  Primary metric; reflects average prediction error in real-world units.

- **R² Score**  
  Secondary metric; indicates proportion of variance explained by the model.

Train and test metrics were always compared to diagnose:
- Underfitting (high bias)
- Overfitting (high variance)

---

## Baseline Linear Models

### Linear Regression

**Observations:**
- Train and test RMSE were similar
- Error magnitude remained high
- R² indicated reasonable variance explanation but poor precision

**Interpretation:**
- Model generalized well
- However, error plateau suggested **high bias**
- Linear assumptions were insufficient for the data

**Decision:**
- Retain as a diagnostic baseline
- Move to regularization to confirm bias behavior

---

### Ridge Regression

**Observations:**
- Slight stabilization compared to plain linear regression
- Train–test gap remained small
- RMSE improvement was marginal

**Interpretation:**
- Regularization successfully controlled variance
- Persistent error confirmed **model bias**, not overfitting

**Decision:**
- Linear family exhausted
- Non-linear models justified

---

## Decision Tree Regression

### Unconstrained Decision Tree

**Results:**
- Train RMSE = 0
- Test RMSE ≈ 69k

**Interpretation:**
- Perfect memorization of training data
- Severe overfitting
- Extremely high variance

**Decision:**
- Introduce constraints to study bias–variance tradeoff

---

### Constrained Decision Tree

**Constraints Applied:**
- `max_depth`
- `min_samples_leaf`

**Results:**
- Train RMSE ≈ 58k
- Test RMSE ≈ 62k

**Interpretation:**
- Bias intentionally increased
- Variance reduced
- Generalization improved but performance limited

**Decision:**
- Single-tree performance ceiling reached
- Move to ensemble methods designed to reduce variance

---

## Random Forest Regression

### Baseline Random Forest

**Configuration:**
- `n_estimators = 200`
- No aggressive depth or leaf constraints

**Results:**
- Train RMSE ≈ 17.9k
- Test RMSE ≈ 48.8k
- Test R² ≈ 0.82

**Interpretation:**
- Strong reduction in variance compared to single tree
- Non-linear patterns captured effectively
- Best bias–variance tradeoff observed so far

**Decision:**
- Selected as **current baseline model**

---

### Tuned Random Forest

**Additional Constraints Tested:**
- `max_depth`
- `min_samples_leaf`
- `max_features`

**Results:**
- Test RMSE worsened to ≈ 51.7k
- Test R² decreased

**Interpretation:**
- Added bias exceeded remaining variance
- Baseline configuration already near optimal balance

**Decision:**
- Retain baseline Random Forest
- Avoid unnecessary over-regularization

---

### Cross-Validation Conclusion

5-fold cross-validation yielded a mean RMSE of ~49k with a standard deviation
of ~650, which is consistent with hold-out test performance.

This low variance across folds confirms that:
- The model’s performance is stable
- The observed error is not split-dependent
- Further hyperparameter tuning is unlikely to yield material gains

This result serves as a validation gate, after which the Random Forest model
is **locked** as the **current baseline**.


## Final Model Comparison Summary

| Model | Train RMSE | Test RMSE | Bias–Variance Behavior |
|-----|-----------|-----------|-----------------------|
| Linear Regression | High | High | High bias |
| Ridge Regression | High | High | High bias |
| Decision Tree | 0 | Very high | Extreme variance |
| Constrained Tree | Medium | Medium | Balanced but weak |
| Random Forest (Baseline) | Low | **Lowest** | Best tradeoff |
| Random Forest (Tuned) | Medium | Higher | Bias too high |

---

## Final Model Selection

**Selected Baseline Model:**  
👉 **Random Forest Regressor (baseline configuration)**

**Reasons:**
- Lowest test RMSE observed
- Strong generalization
- Robust to feature interactions and non-linearities
- Stable performance without heavy tuning

This model provides a solid foundation for:
- Feature importance analysis
- Feature engineering
- Advanced ensemble methods (e.g., Gradient Boosting)
- MLOps deployment and monitoring

---

## Out of Scope for This Phase

The following were intentionally not pursued during this phase:
- Extensive feature engineering
- Gradient Boosting or external libraries (e.g., XGBoost, LightGBM)
- Target transformation

These steps are deferred to subsequent phases, as the current objective
was to establish a stable and well-understood baseline model.