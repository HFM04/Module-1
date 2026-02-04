import time
import joblib
from pathlib import Path
from flask import Request, jsonify

# Global initialization (runs once per instance)
INIT_T0 = time.perf_counter()

ARTIFACT_PATH = Path(__file__).resolve().parent / "model.pkl"
artifact = joblib.load(ARTIFACT_PATH)

model = artifact["model"]
target_names = artifact["target_names"]
model_version = artifact.get("model_version", "v1")

INIT_T1 = time.perf_counter()
INIT_MS = (INIT_T1 - INIT_T0) * 1000


def predict(request: Request):
    req_t0 = time.perf_counter()

    payload = request.get_json(silent=True) or {}
    instances = payload.get("instances")

    if not instances:
        return jsonify({
            "error": "Expected JSON body with key 'instances'",
            "example": {"instances": [[5.1, 3.5, 1.4, 0.2]]}
        }), 400

    preds = model.predict(instances)
    labels = [target_names[int(i)] for i in preds]

    req_t1 = time.perf_counter()
    req_ms = (req_t1 - req_t0) * 1000

    return jsonify({
        "predictions": labels,
        "model_version": model_version,
        "init_ms": INIT_MS,
        "request_ms": req_ms
    })
