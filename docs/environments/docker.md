# 🚀 Building and Running the API Using Docker

This guide shows you how to run the online inference (api) using docker by packaging your model into a Docker image, building container and pushing it to the GitHub Container Registry (GHCR).

## 🏗️ How it Works

* **Download First:** We download the model files from MLflow to local first. For details on how to set up MLflow and download these files, please refer to [docs/environments/local.md](./local.md).
* **Put Model in Docker:** The Docker build process copies these local files into the image.



## Step 1: Get the Model & Build

Before building, ensure you have followed the steps in `local.md` to download the model into the `./serving/models` folder.

```bash
docker build -t california-housing-api .
```


## Step 2: Run the API

You can now run the API anywhere using Docker.

```bash
docker run -d \
  --name housing-api \
  -p 8000:8000 \
  california-housing-api
```

## 🌐 Step 3: Test the API

Once the container is running, you can check these links:

* **Check if it's alive:** [http://localhost:8000/health](http://localhost:8000/health)
* **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Example Test (using terminal)

Run this command to send a single house's data and get a price prediction back:

```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": [
    {
      "households": 126,
      "housing_median_age": 41,
      "latitude": 37.88,
      "longitude": -122.23,
      "median_income": 8.3252,
      "ocean_proximity": "NEAR BAY",
      "population": 322,
      "total_bedrooms": 129,
      "total_rooms": 880
    }
  ]
}'
```


## Step 4: Save to GitHub Registry (GHCR)

Replace `[USERNAME]` with your GitHub username.

```bash
# 1. Tag your image so GitHub knows where it belongs
docker tag california-housing-api ghcr.io/[USERNAME]/california-housing-api:v1.0.0

# 2. Log in to GitHub's registry
echo $CR_PAT | docker login ghcr.io -u [USERNAME] --password-stdin

# 3. Upload (push) the image
docker push ghcr.io/[USERNAME]/california-housing-api:v1.0.0
```

---