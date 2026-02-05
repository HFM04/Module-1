## ML Model Deployment and Serverless Performance Comparison on Google Cloud
This project demonstrates an end-to-end machine learning deployment workflow on Google Cloud, along with a performance comparison between Cloud Run and Cloud Functions focusing on cold start vs warm start behavior.
The project emphasizes reproducibility, portability, and serverless performance trade-offs when serving ML models via HTTP APIs.

## Project Overview
The workflow consists of two parallel deployment paths:
  1. Container-based deployment using Cloud Run
  2. Function-based deployment using Cloud Functions
Both deployments serve the same trained ML model and expose HTTP endpoints for inference. Their performance is then evaluated under cold and warm start conditions.

## End-to-End Workflow
1. Train, test, and evaluate a machine learning model locally or in a notebook environment
2. Serialize the trained model as a reusable artifact (model.pkl)
3. Build an API layer (FastAPI) that exposes prediction endpoints
4. Package the application and model into a container image
5. Push the image to Google Artifact Registry
6. Deploy the container image to Cloud Run
7. Separately deploy the same model logic as a Cloud Function
8. Measure and compare cold start and warm start latency for both services

## Repository Structure
'''python
.
├── main.py               # FastAPI application (Cloud Run)
├── model.pkl             # Trained ML model artifact
├── model.py              # Training / preprocessing logic
├── requirements.txt      # Runtime dependencies
├── Dockerfile            # Container build instructions
├── README.md
'''

## Cloud Run Deployment (Container-Based)
### Design
Packages the full runtime, dependencies, and model into an immutable container image.
Scales horizontally based on incoming request volume.
Supports configurable concurrency per instance.
Exhibits higher cold start latency but better sustained performance.

### Build the Container Image
'''bash
docker build -t iris-classifier:v1 .
'''

### Run Locally
'''bash
docker run -p 8080:8080 iris-classifier:v1
'''

### Push Image to Artifact Registry
'''bash
docker tag iris-classifier:v1 \
  us-central1-docker.pkg.dev/PROJECT_ID/REPO_NAME/iris-classifier:v1

docker push us-central1-docker.pkg.dev/PROJECT_ID/REPO_NAME/iris-classifier:v1
'''
Artifact Registry stores the image as an immutable deployment artifact.

### Deploy to Cloud Run
'''bash
gcloud run deploy iris-classifier \
  --image us-central1-docker.pkg.dev/PROJECT_ID/REPO_NAME/iris-classifier:v1 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080
'''

### Retrieve the service URL:
'''bash
SERVICE_URL=$(gcloud run services describe iris-classifier \
  --region us-central1 \
  --format 'value(status.url)')
'''

## Cloud Functions Deployment (Function-Based)
### Design
  Deploys only the function logic and dependencies
  Faster cold start for lightweight workloads
  Limited runtime control compared to containers
  Less suitable for larger ML models
The Cloud Function exposes an HTTP-triggered endpoint using the same prediction logic.

## API Endpoints
### Health Check
'''bash
curl ${SERVICE_URL}/health
'''bash

### Prediction
'''bash
curl -X POST ${SERVICE_URL}/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
'''

## Cold Start vs Warm Start Analysis
The project compares:
Cold start latency: first request after scale-to-zero
Warm start latency: subsequent requests to an already running instance

### Observations
Cloud Functions exhibit faster cold starts for small workloads
Cloud Run cold starts are higher due to container initialization
Cloud Run warm performance is more stable under sustained load
Cloud Run provides greater flexibility for production ML systems

### Key Engineering Takeaways
Containers provide stronger reproducibility guarantees
Serverless platforms require stateless application design
Cold start behavior matters for latency-sensitive ML APIs
Cloud Run is better suited for scalable, long-running inference services
Cloud Functions are appropriate for lightweight, event-driven inference


























