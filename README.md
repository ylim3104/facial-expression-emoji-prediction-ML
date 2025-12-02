# Facial Expression Emoji Prediction ML API
## 1. Setup

Download Docker Desktop `https://www.docker.com/products/docker-desktop/` and Google Cloud `https://cloud.google.com/sdk/docs/install`

## 2. Configure Google Cloud in SDK shell

### 2.1 Login to Google Cloud
```gcloud auth login```

### 2.2 Enable cloud run & container registry
   ```
    gcloud services enable run.googleapis.com
    gcloud services enable artifactregistry.googleapis.com
   ```

### 2.3 Set the project
```gcloud config set project [PROJECT ID]```


## 3. Build and Push the Docker Image
### 3.1. Create an artifact registry repo (One time)

```gcloud artifacts repositories create keras-repo --repository-format=docker --location=us-central1```


### 3.2. Build the Docker Image
```
cd [PROJECT_DIRECTORY]
docker build -t ml-api .
```


### 3.3. Tag the image for Artifact Registry

```docker tag ml-api us-central1-docker.pkg.dev/[PROJECT ID]/keras-repo/ml-api```


### 3.4. Authenticate Docker to push to Google

```gcloud auth configure-docker us-central1-docker.pkg.dev```


### 3.5 Push docker image to artifact registry

```docker push us-central1-docker.pkg.dev/[PROJECT ID]/keras-repo/ml-api```


## 4. Deploy to Cloud Run

### 4.1 Deploy the docker image to cloud run
   ```
    gcloud run deploy ml-api 
      --image us-central1-docker.pkg.dev/[PROJECT ID]/keras-repo/ml-api 
      --region us-central1 
      --platform managed 
      --allow-unauthenticated
   ```


## 5. Get API URL

## 5.1. Get url
```gcloud run services describe ml-api --region us-central1 --format "value(status.url)"```


## 6. Testing the website

### 6.1. Testing the status of the model
```curl [URL]/health```

### 6.2. Testing the OPTIONS
```curl -I -X OPTIONS -H "Origin: [URL]" -H "Access-Control-Request-Method: POST" -H "Access-Control-Request-Headers: content-type" [URL]/predict-cnn```

### 6.3. Testing the cnn-predict
```python test_predict.py```

