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
'''text
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
