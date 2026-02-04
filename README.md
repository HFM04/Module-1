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
Environments
Cloud Run Function runtime: Python 3.11
Region: us-central1
Memory: 512Mi for both deployments
Dependencies are documented in:
cloud-function/requirements.txt
cloud-run/app/requirements.txt
model/requirements-train.txt
How to Deploy
Deploy Cloud Run Function (Gen 2)
From repo root:
bash deployments/cloud-function-deploy.sh
Deploy Cloud Run Service
From repo root:
bash deployments/cloud-run-deploy.sh
Inference APIs
Cloud Run function request
curl -s \
  -H "Content-Type: application/json" \
  -d '{"instances":[[5.1,3.5,1.4,0.2]]}' \
  https://us-central1-ml-deployment-486403.cloudfunctions.net/iris-predict
Cloud Run service request
Health:
curl -s https://ml-service-2kp22ogzdq-uc.a.run.app
Predict:
curl -s \
  -H "Content-Type: application/json" \
  -d '{"features":[5.1,3.5,1.4,0.2]}' \
  https://ml-service-2kp22ogzdq-uc.a.run.app/predict
Experiment Design
Warm test
Send 10 sequential requests with 1 second delay and record client observed latency via curl:
client_total_s = %{time_total}
Cold test
Allow the service/function to scale to zero by leaving it idle (min instances = 0). After a long idle period, send a single request and measure client observed latency.
Notes:

Cloud Run and Cloud Run functions are both serverless and can scale to zero.
Warm latency reflects steady state request handling.
Cold latency includes additional platform startup overhead.
Results
Cloud Run function (warm)
10 warm requests (client_total_s):
Typical range: ~0.095s to ~0.205s
Median (approx): ~0.12s
p95 (approx): ~0.19 to ~0.20s
Server side metrics from function response:
request_ms (warm): ~0.6ms to ~3.4ms
init_ms (instance init): ~6019ms (measured once per instance)
Cloud Run function (cold)
Example cold response included:
init_ms: ~6019ms
request_ms: ~59ms (first request after init)
This indicates cold start overhead dominated by runtime initialization and dependency loading, not the ML inference itself.
Cloud Run service (warm)
10 warm requests (client_total_s):
Typical range: ~0.086s to ~0.179s
One tail spike observed: ~0.370s
Median (approx): ~0.12s
Cloud Run service (cold)
One cold candidate request observed:
client_total_s: ~0.236s
Estimated cold penalty relative to warm median:
~0.236s - ~0.12s = ~0.116s
Interpretation
Warm performance: Cloud Run service and Cloud Run function showed similar median warm latency (~0.12s). This suggests end to end latency is dominated by network and platform overhead once warm.
Cold starts: The Cloud Run function showed a large cold initialization component (init_ms ~6s). Cloud Run service cold candidate was much smaller (~0.24s total), indicating substantially lower cold start impact in this setup.
ML compute is not the bottleneck: warm inference request_ms in the function was around 1ms, far smaller than end to end latency
