# Feature Engineering and Gradient Boosting

## Context and Motivation

The Random Forest model was previously selected as the baseline after demonstrating:
- Strong generalization performance
- Stable cross-validation results
- A well-balanced bias–variance tradeoff

However, test RMSE plateaued around ~49k, indicating a potential **bias ceiling**
given the current feature representation.

This phase explores whether:
1. Feature engineering can expose additional predictive signal, and
2. A bias-reducing model family (Gradient Boosting) can leverage that signal.

---

## Feature Engineering Strategy

### Rationale

The dataset contains several **count-based features**:
- `total_rooms`
- `total_bedrooms`
- `population`
- `households`

Absolute counts are heavily influenced by census block size and therefore
do not directly represent housing quality or density.

To address this,  `ratio-based` features were introduced to normalize these
counts into **per-unit signals**, which are more closely aligned with how
housing prices are determined.

---

### Engineered Features

The following features were created:

1. **Rooms per Household**

    ```bash
    rooms_per_household = total_rooms / households
    ```
    Captures average house size.

2. **Bedrooms per Room**

    ```bash
    bedrooms_per_room = total_bedrooms / total_rooms
    ```

3. **Population per Household**

    ```bash
    population_per_household = population / households
    ```
    Measures household density and socio-economic pressure.

These features were selected due to their clear domain interpretation and
minimal risk of introducing noise or leakage.

---

## Impact of Feature Engineering on Random Forest

The engineered features were first evaluated using the existing Random Forest
baseline configuration to isolate the effect of feature representation alone.

### Observed Results

- Train RMSE remained largely unchanged
- Test RMSE increased slightly compared to the baseline
- No improvement in generalization performance was observed

### Interpretation

Random Forest models are capable of learning non-linear interactions and
threshold-based relationships directly from raw count features.
As a result, the ratio-based engineered features were largely **redundant**
for this model family.

### Decision

- Engineered features were **not retained** for the Random Forest baseline
- The Random Forest model remains unchanged

This outcome is expected and does not invalidate the feature engineering
approach.

---

## Transition to Gradient Boosting

### Why Gradient Boosting?

Random Forest performance plateaued, indicating a bias limitation.
Gradient Boosting models reduce bias by:
- Training trees sequentially
- Correcting residual errors from previous iterations
- Exploiting cleaner feature representations more effectively

---

## Model Selection: HistGradientBoostingRegressor

`HistGradientBoostingRegressor` was selected due to:
- High efficiency on tabular data
- Built-in regularization

## Gradient Boosting Results (with Engineered Features)

### Hold-out Performance

- **Train RMSE:** ~35k  
- **Test RMSE:** ~45.5k  
- **Train R²:** ~0.91  
- **Test R²:** ~0.84  

This represents a **meaningful improvement** over the Random Forest baseline.

---

### Cross-Validation Results

5-fold cross-validation was performed on the training set:

- **Mean CV RMSE:** ~46.5k  
- **Standard Deviation:** ~574  

### Interpretation

- Performance is stable across folds
- Improvement over Random Forest is consistent
- No evidence of overfitting or instability

Cross-validation confirms that the observed improvement is not due to a
favorable data split.

<!-- --- -->
<!-- 
## Feature Selection Considerations

Explicit forward or backward feature selection techniques were not applied.

Reasons:
- Tree-based and boosting models perform implicit feature selection during training
- Feature interactions violate assumptions of sequential selection methods
- Model performance provides a more reliable signal of feature usefulness

Feature relevance is instead evaluated through:
- Model performance comparison
- Validation metrics
- Feature importance analysis (future work) -->

---

## Final Model Comparison (Post Feature Engineering)

| Model | Test RMSE | CV RMSE (mean) | Notes |
|-----|----------|---------------|------|
| Random Forest (Baseline) | ~48.8k | ~49.2k | Stable, variance-controlled |
| Gradient Boosting (HGBR) | **~45.5k** | **~46.5k** | Lower bias, improved accuracy |

---

## Final Conclusion

- Feature engineering did not improve Random Forest performance but revealed
additional signal exploitable by Gradient Boosting.
- Gradient Boosting achieved a consistent and meaningful reduction in RMSE.
- Cross-validation confirmed stability and generalization.

👉 **HistGradientBoostingRegressor with engineered features is selected as the
new baseline model.**

---
