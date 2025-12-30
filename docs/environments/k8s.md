# 🚀 KServe Demonstration (Model Serving on Kubernetes)

This document demonstrates a **basic KServe setup** for serving a trained
machine learning model on Kubernetes.

This is a **standalone demonstration** meant to showcase how a model can be
served using **KServe InferenceService**, independent of the FastAPI-based
serving approach used elsewhere in this repository.

> **Note:** Make sure you have a working Kubernetes cluster and `kubectl` configured.


## 📦 Install Cert Manager

KServe depends on cert-manager for webhook certificates.

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/latest/download/cert-manager.yaml
````

Verify installation:

```bash
kubectl get pods -n cert-manager
```



## ☸️ Install KServe

### 1️⃣ Install KServe CRDs

```bash
kubectl create namespace kserve

helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd \
  --version v0.16.0 \
  -n kserve \
  --wait
```

---

### 2️⃣ Install KServe Controller

```bash
helm install kserve oci://ghcr.io/kserve/charts/kserve \
  --version v0.16.0 \
  -n kserve \
  --set kserve.controller.deploymentMode=RawDeployment \
  --wait
```

Verify installation:

```bash
kubectl get pods -n kserve
```



## 🏗️ Deploy the Housing Model with KServe

### 1️⃣ Create a namespace for the model

```bash
kubectl create namespace housing-ns
```

---

### 2️⃣ Create an InferenceService

```yaml
cat <<EOF | kubectl apply -n housing-ns -f -
apiVersion: serving.kserve.io/v1beta1
kind: InferenceService
metadata:
  name: housing-model
spec:
  predictor:
    containers:
      - name: housing-api
        image: ghcr.io/atkaridarshan04/california-housing-api:v1.0.0
        imagePullPolicy: IfNotPresent
        ports:
          - containerPort: 8000
        resources:
          requests:
            cpu: "100m"
            memory: "512Mi"
          limits:
            cpu: "1"
            memory: "1Gi"
EOF
```

### Verify the Resources

```bash
kubectl get deployment -n housing-ns
kubectl get svc -n housing-ns
kubectl get hpa -n housing-ns
```

![k-get-all](../__assets/k-get-all.png)

---

### 3️⃣ Verify the InferenceService

```bash
kubectl get inferenceservice housing-model -n housing-ns
```

Wait until the service status is `Ready=True`.



## 🌐 Accessing the Model

For local clusters, use port-forwarding.

```bash
kubectl -n housing-ns port-forward svc/housing-model-predictor 8000:80
```

Now access:

* API: [http://localhost:8000/health](http://localhost:8000/health)    
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

