#create streaming inference
from time import sleep
import time
import random
def stream_inf(prompt):
    #stimulate ttft
    ttft=0.248

    response="""
    The Supreme Court, on Monday (May 25, 2026), 
    squarely blamed the National Testing 
    Agency (NTA) for the National Eligibility 
    cum Entrance Test Undergraduate (NEET-UG) 
    2026 paper leak, saying the exam body sadly 
    did not learn its lesson even two 
    years after the last security breach in 2024.
    
    """
    tokens=response.split()
    start_time=time.time()
    for token in tokens:
        print(token,end=" ",flush=True)
        delay=random.uniform(0.05,0.15) #simulate token generation time
        sleep(delay)
    end_time=time.time()
    total_time = end_time - start_time
    token_count = len(tokens)
    tokens_per_second = token_count / total_time
     
    print("\n\n--- Streaming Metrics ---")
    print(f"TTFT              : {int(ttft * 1000)} ms")
    print(f"Total Time        : {round(total_time * 1000)} ms")
    print(f"Tokens Generated  : {token_count}")
    print(f"Throughput        : {round(tokens_per_second, 2)} tokens/sec")

if __name__=="__main__":
    prompt="What is the latest news on NEET-UG 2026 paper leak?"
    stream_inf(prompt)
