
## Feature Understanding (Phase 0)

This document captures **initial understanding and hypotheses** about the dataset features based on:

Implementation: [01_feature_exploration.ipynb](../notebooks/01_feature_exploration.ipynb)

---

## Feature List & Initial Interpretation

### Feature: `longitude`

**Type:** Numerical

**Quick observations:**

* Strong geographic signal
* Non-linear relationship with `median_house_value`
* Interacts heavily with `latitude`

**Decision:**

* Retain as a key spatial feature
* Tree-based models expected to perform better
* Linear models capture limited signal

---

### Feature: `latitude`

**Type:** Numerical

**Quick observations:**

* Strong non-linear relationship with target
* Clear regional pricing patterns
* Complements `longitude` for spatial effects

**Decision:**

* Retain as a core feature
* Trees and ensembles preferred
* Linear models limited without interactions

---

### Feature: `total_rooms`

**Type:** Numerical

**Quick observations:**

* Strongly right-skewed distribution
* Weak standalone relationship with `median_house_value`
* Highly correlated with `total_bedrooms` and `households`

**Decision:**

* Retain for baseline modeling
* Acts as a structural proxy
* Monitor redundancy with related features

---

### Feature: `total_bedrooms`

**Type:** Numerical

**Quick observations:**

* Similar distribution to `total_rooms`
* Contains missing values (in original dataset)
* Weak direct relationship with target

**Decision:**

* Retain initially
* Imputation required
* Likely redundant in linear models

---

### Feature: `households`

**Type:** Numerical

**Quick observations:**

* Right-skewed distribution
* Closely related to `population` and room counts
* Weak standalone signal

**Decision:**

* Retain as a contextual feature
* Scaling required
* Interaction-based usefulness

---

### Feature: `population`

**Type:** Numerical

**Quick observations:**

* Highly right-skewed with extreme values
* No clear monotonic relationship with target
* Large variance across districts

**Decision:**

* Retain as a contextual feature
* Scaling required
* Tree-based models may utilize it better

---

### Feature: `housing_median_age`

**Type:** Numerical

**Quick observations:**

* Bounded and plausible values
* Skewed toward older housing districts
* Weak standalone relationship with target

**Decision:**

* Retain for interaction effects
* Scaling required
* More informative when combined with location and income

---

### Feature: `median_income`

**Type:** Numerical

**Quick observations:**

* Right-skewed distribution
* Strong positive relationship with target
* Shows diminishing returns at higher values

**Decision:**

* Retain as primary predictor
* Scaling required
* Non-linear models may capture saturation better

---

### Feature: `ocean_proximity`

**Type:** Categorical (Nominal)

**Quick observations:**

* Clear separation between coastal and inland districts
* Strong impact on `median_house_value`
* No natural ordering

**Decision:**

* Retain
* Encode using one-hot encoding
* Important across all model types

---