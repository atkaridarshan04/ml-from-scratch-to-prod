# Artifacts

This directory stores all **model artifacts and metrics** produced during
experimentation and production pipeline execution.

## 📁 Directory Structure

### `experiments/`

Contains artifacts generated during **notebook-based experimentation**.

Typical contents:
- Multiple model versions
- Metrics from exploratory runs
- Intermediate results used for comparison

---

### `production/`

Contains the **final, validated artifacts** produced by the training pipeline
and used by inference systems.

Typical contents:
- Trained model
- Preprocessing objects (imputer, encoder, etc.)
- Evaluation metrics for the selected model

---