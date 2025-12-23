## Dataset Overview

### Dataset Name

California Housing Dataset  
**Source**: [Kaggle Link](https://www.kaggle.com/datasets/camnugent/california-housing-prices)

---

### Dataset Shape

| Property | Value             |
| -------- | ----------------- |
| Rows     | ~20,640           |
| Features | 8                 |
| Target   | 1 (`MedHouseVal`) |

---

### Feature Types

| Type        | Count                                       |
| ----------- | ------------------------------------------- |
| Numerical   | 8                                           |
| Categorical | 1 (`ocean_proximity`, if using CSV version) |

---

### High-Level Feature Themes

* Demographics (income, population)
* Housing density
* Room statistics
* Geographic location (latitude, longitude)
* Proximity to ocean (categorical)

---

### Target Variable Characteristics

* Moderately right-skewed
* Upper bound exists (capped in dataset)
* Represents aggregated values, not individual prices

---

### Known Dataset Characteristics

* Strong correlation between income and house value
* Geographic location plays a major role
* Features are highly correlated with each other
* Dataset contains noise and aggregation effects

---
