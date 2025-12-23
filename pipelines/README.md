# Pipelines — Execution Entry Points

This directory contains **executable entry points** that orchestrate
training and batch inference using reusable logic from `src/`.

Pipelines are responsible for:
- wiring components together
- managing data flow
- producing artifacts and outputs



## 🚀 Available Pipelines

### Training Pipeline

```bash
python -m pipelines.train
````

**What it does**

* Loads raw dataset
* Applies preprocessing and feature engineering
* Trains the selected model
* Evaluates performance
* Saves production artifacts

**Outputs**

```
artifacts/production/
```

---

### Batch Inference Pipeline

```bash
python -m pipelines.inference
```

**What it does**

* Loads production artifacts
* Reads inference input data
* Applies identical preprocessing
* Runs predictions
* Writes outputs

**Outputs**

```
outputs/predictions.json
```


## 🧠 Notes

* Pipelines do not contain ML logic themselves
* All reusable logic lives in `src/`
* Pipelines are deterministic and CI-friendly
