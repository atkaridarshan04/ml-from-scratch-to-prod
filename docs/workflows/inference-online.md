
# Online Inference (API) Workflow

This document describes how **online (real-time) inference** is performed
using the FastAPI service. It focuses on **request flow, model loading strategy, and design decisions**, not on environment-specific commands.


## 🎯 Purpose of Online Inference

Online inference serves real-time predictions for user or application
requests.

Key goals:
- Low latency
- Predictable behavior
- Safe deployment
- Clear separation from training logic



## 🧠 High-Level Flow

1. API service starts
2. Unified model is loaded from MLflow
3. API waits for requests
4. Incoming requests are validated
5. Raw input is passed to the model
6. Predictions are returned


## 🔄 Request Lifecycle

### 1️⃣ Application Startup

At application startup, the model is loaded **once** using FastAPI’s
`lifespan` mechanism:

- The model is fetched from MLflow Model Registry
- The `Production` alias is resolved
- The model is stored in application state

This avoids loading the model per request.



### 2️⃣ Request Handling

For each `/predict` request:

1. Request body is validated using Pydantic schemas
2. Input data is converted to a Pandas DataFrame
3. The unified model’s `predict()` method is called
4. Predictions are returned to the client

No preprocessing logic exists in the API layer.



## 🧱 Model Access via Application State

The model is accessed using FastAPI’s application state:

```python
request.app.state.model
```