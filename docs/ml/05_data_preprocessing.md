# Data Preprocessing Strategy

## Purpose

This document describes the preprocessing decisions applied during model development.
The goal of preprocessing is to:
- Prepare raw data for model consumption
- Prevent data leakage
- Ensure reproducibility
- Apply only the transformations required by each model family

Preprocessing is treated as **model-specific**, not as a one-time global data transformation.

---

## General Preprocessing Principles

The following principles guided all preprocessing decisions:

- Raw data is never permanently modified
- Train–test split is performed before any statistical preprocessing
- All statistics (median, mean, frequency) are computed using **training data only**
- Preprocessing steps are applied conditionally based on model requirements

---

## Missing Value Handling

### Identified Missing Data
- `total_bedrooms` contains missing values

### Strategy
- Numerical features: **Median imputation**

### Rationale
- Median is robust to outliers
- Simple and stable baseline
- Avoids dropping rows and reducing data size

### Applied To
- Linear Regression
- Ridge Regression
- Decision Tree
- Random Forest

---

## Categorical Encoding

### Affected Feature
- `ocean_proximity`

### Strategy
- One-Hot Encoding

### Rationale
- Feature is nominal (no ordinal relationship)
- Required by all sklearn models
- Avoids introducing artificial ordering

### Applied To
- Linear Regression
- Ridge Regression
- Decision Tree
- Random Forest

---

## Feature Scaling

### Strategy
- Standard Scaling (mean = 0, std = 1)

### Rationale
- Linear and regularized models are sensitive to feature scale
- Coefficient magnitude and regularization penalties depend on scaling
- Improves numerical stability and interpretability

### Applied To
- Linear Regression
- Ridge Regression

### Not Applied To
- Decision Tree
- Random Forest

**Reason:**
Tree-based models split on thresholds and are invariant to feature scale.

---

## Duplicate Handling

### Strategy
- No duplicate removal performed

### Rationale
- Dataset represents aggregated census districts
- Duplicate rows are not inherently erroneous
- Removal could distort data distribution

---

## Outlier Handling

### Strategy
- No outlier removal performed during preprocessing

### Rationale
- Outliers are meaningful in housing data
- Tree-based models are robust to extreme values
- Premature removal may discard important signals

---

## Model-wise Preprocessing Summary

| Preprocessing Step | Linear / Ridge | Decision Tree | Random Forest |
|-------------------|---------------|---------------|---------------|
| Train–test split first | ✅ | ✅ | ✅ |
| Missing value imputation | ✅ | ✅ | ✅ |
| One-hot encoding | ✅ | ✅ | ✅ |
| Feature scaling | ✅ | ❌ | ❌ |
| Outlier removal | ❌ | ❌ | ❌ |

---