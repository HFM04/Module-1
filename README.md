# Cold Starts, Warm Instances, and Latency: Cloud Run vs Cloud Run Functions

## Project Overview
This project deploys the same Iris classification model in two serverless configurations on Google Cloud:

1) Cloud Run service (containerized FastAPI inference API)
2) Cloud Run function (Cloud Functions Gen 2, Python HTTP function)

Goal: measure and compare warm vs cold start latency behavior.

## Model
- Dataset: sklearn Iris
- Model: Pipeline(StandardScaler + LogisticRegression)
- Artifact: `model.pkl` (joblib dump containing model, target names, version)

### Generate model artifact
From `model/`:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-train.txt
python train.py

This generates model.pkl.

Deployment URLs
Cloud Run service:
  https://ml-service-2kp22ogzdq-uc.a.run.app
Cloud Run function (Gen 2):
  https://us-central1-ml-deployment-486403.cloudfunctions.net/iris-predict
```
Environments
  Cloud Run Function runtime: Python 3.11
  Region: us-central1
  Memory: 512Mi for both deployments

Dependencies are documented in:
  cloud-function/requirements.txt
  cloud-run/app/requirements.txt
  model/requirements-train.txt
