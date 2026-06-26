#create prompt input using post operation

from fastapi import FastAPI
import fastapi
from ragapp.api.prompt_request import PromptRequest
from ragapp.utils.rag_engine import receive_prompt
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
import time

app=FastAPI(
    title="RAG pipeline API",
    description="API for RAG pipeline",
    version="1.0.0"
    
)
prediction_counter = Counter(
    "prediction_requests_total",
    "Total prediction requests"
)

prediction_latency = Histogram(
    "prediction_latency_seconds",
    "Prediction latency"
)

@app.post("/prompt")
def create_prompt_input(prompt_request: PromptRequest):
    prediction_counter.inc()

    start = time.time()
    
    result = receive_prompt(prompt_request.prompt)
    prediction_latency.observe(time.time() - start)

    return result

@app.get("/metrics")
def metrics():
    return Response(generate_latest(),
                    media_type="text/plain")