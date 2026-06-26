import os
import time
import pandas as pd
from dotenv import load_dotenv

from ragapp.utils.rag_engine import receive_prompt
#pip install --upgrade "click==8.4.1" "typer==0.25.1"
env_path = os.path.join(os.path.dirname(__file__),'..', ".env")

load_dotenv(env_path)

eval_df = pd.read_csv(os.getenv("qa_source_file_path"))
results = []

for _, row in eval_df.iterrows():
    question = row["question"]
    expected = row["expected_answer"]

    start_time = time.time()

    response = receive_prompt(question)

    actual_answer = response.get("answer", "")
    retrieved_context = str(response.get("sources", ""))

    latency = time.time() - start_time

    accuracy_score = 1 if expected.lower() in actual_answer.lower() else 0

    hallucination_score = 0 if accuracy_score == 1 else 1

    results.append({
        "question": question,
        "expected_answer": expected,
        "actual_answer": actual_answer,
        "retrieved_context": retrieved_context,
        "accuracy_score": accuracy_score,
        "hallucination_score": hallucination_score,
        "latency_seconds": round(latency, 2)
    })


# -----------------------------
# 11. Save Report
# -----------------------------
result_df = pd.DataFrame(results)
result_df.to_csv("food_delivery_rag_evaluation_report.csv", index=False)


# -----------------------------
# 12. Final Metrics
# -----------------------------
accuracy = result_df["accuracy_score"].mean() * 100
hallucination_rate = result_df["hallucination_score"].mean() * 100
avg_latency = result_df["latency_seconds"].mean()


print("\nFood Delivery RAG Evaluation Report")
print("=" * 50)

print(result_df[[
    "question",
    "expected_answer",
    "actual_answer",
    "accuracy_score",
    "hallucination_score",
    "latency_seconds"
]])

print("\nFinal Metrics")
print("-" * 50)
print(f"Accuracy           : {accuracy:.2f}%")
print(f"Hallucination Rate : {hallucination_rate:.2f}%")
print(f"Average Latency    : {avg_latency:.2f} seconds")

print("\nReport saved as food_delivery_rag_evaluation_report.csv")