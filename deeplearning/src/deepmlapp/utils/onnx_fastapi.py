import time
import asyncio
import numpy as np
import onnxruntime as ort

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Optional


app = FastAPI(title="ONNX Loan Approval Inference Gateway")


# -----------------------------
# Load ONNX Models
# -----------------------------

model_sessions = {
    "loan_approval": {
        "v1": ort.InferenceSession("loan_approval_pipeline.onnx")
    }
}


# -----------------------------
# Routing Rules
# -----------------------------

tenant_routing = {
    "tenant_a": {
        "loan_approval": "v1"
    },
    "tenant_b": {
        "loan_approval": "v1"
    }
}


def route_model(tenant_id: str, model_name: str, requested_version: Optional[str]):
    if model_name not in model_sessions:
        raise HTTPException(status_code=404, detail="Model not found")

    version = requested_version or tenant_routing.get(
        tenant_id, {}
    ).get(model_name, "v1")

    if version not in model_sessions[model_name]:
        raise HTTPException(status_code=404, detail="Model version not found")

    return model_sessions[model_name][version], version


# -----------------------------
# Quota
# -----------------------------

QUOTA_LIMIT = 5
QUOTA_WINDOW_SECONDS = 60

tenant_usage = {}


def check_quota(tenant_id: str):
    now = time.time()

    if tenant_id not in tenant_usage:
        tenant_usage[tenant_id] = []

    tenant_usage[tenant_id] = [
        t for t in tenant_usage[tenant_id]
        if now - t < QUOTA_WINDOW_SECONDS
    ]

    if len(tenant_usage[tenant_id]) >= QUOTA_LIMIT:
        raise HTTPException(
            status_code=429,
            detail=f"Quota exceeded for {tenant_id}. Try again after some time."
        )

    tenant_usage[tenant_id].append(now)


# -----------------------------
# Backpressure
# -----------------------------

MAX_CONCURRENT_REQUESTS = 3
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)


async def acquire_capacity():
    try:
        await asyncio.wait_for(semaphore.acquire(), timeout=0.2)
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=503,
            detail="Server overloaded. Backpressure activated. Try again later."
        )


# -----------------------------
# Request DTO
# -----------------------------

class LoanRequest(BaseModel):
    salary: float
    credit_score: float
    experience: float
    model_name: str = "loan_approval"
    model_version: Optional[str] = None


# -----------------------------
# ONNX Prediction
# -----------------------------

def predict_onnx(session, request: LoanRequest):
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    input_data = np.array(
        [[request.salary, request.credit_score, request.experience]],
        dtype=np.float32
    )

    output = session.run(
        [output_name],
        {input_name: input_data}
    )

    score = float(output[0][0][0])
    prediction = "Loan Approved" if score > 0.5 else "Loan Rejected"

    return score, prediction


# -----------------------------
# API Endpoint
# -----------------------------

@app.post("/predict")
async def predict(
    request: LoanRequest,
    x_tenant_id: str = Header(...)
):
    tenant_id = x_tenant_id

    check_quota(tenant_id)

    await acquire_capacity()

    try:
        session, routed_version = route_model(
            tenant_id=tenant_id,
            model_name=request.model_name,
            requested_version=request.model_version
        )

        score, prediction = predict_onnx(session, request)

        return {
            "tenant_id": tenant_id,
            "model_name": request.model_name,
            "model_version": routed_version,
            "score": score,
            "prediction": prediction
        }

    finally:
        semaphore.release()


@app.get("/health")
def health():
    return {
        "status": "UP",
        "model": "loan_approval_pipeline.onnx",
        "max_concurrent_requests": MAX_CONCURRENT_REQUESTS,
        "quota_limit_per_minute": QUOTA_LIMIT
    }