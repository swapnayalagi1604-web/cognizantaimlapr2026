import streamlit as st
#from ragapp.utils.rag_engine import receive_prompt
import requests
import os
import redis
import hashlib
from dotenv import load_dotenv
from ragapp.agents.delivery_support_agent import ask_food_delivery_agent
#to run this app,
#streamlit run src/ragapp/views/app.py
#Create an order for Parameswari, product id 128, product name TV, Quantity 1, Price 50000
env_path=os.path.join(os.path.dirname(__file__), '..','.env')
load_dotenv(env_path)

REDIS_HOST = os.getenv("redis_host")
REDIS_PORT = int(os.getenv("redis_port"))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)
def get_cache_key(question):
    normalized_question = question.lower().strip()
    return "food_agent:" + hashlib.md5(normalized_question.encode()).hexdigest()

API_URL = os.getenv("api_url")
print(f"API_URL: {API_URL}")
st.set_page_config(
    page_title="Food Delivery Policy Assistant",
    page_icon="🍔",
    layout="wide",
)

st.markdown("""
<style>
[data-testid="stHeader"] {
    background: transparent;
    height: 0rem;
}

[data-testid="stToolbar"] {
    display: none;
}

.stApp {
    background: linear-gradient(
        120deg,
        #ff9a9e 0%,
        #fad0c4 25%,
        #a8e6a1 60%,
        #dcedc1 100%
    );
    min-height: 100vh;
}

.block-container {
    padding-top: 1rem;
}

.stTitle {
    background: radial-gradient(circle, blue, red, orange, yellow, green);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 48px;
    font-weight: bold;
    text-align: center;
}

.stWelcome {
    background: radial-gradient(circle, lightblue, darkblue);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 46px;
    font-weight: bold;
    text-align: center;
}

.answer-box {
    width: 75%;
    margin: 20px auto;
    background: rgba(255,255,255,0.9);
    padding: 25px;
    border-radius: 20px;
    font-size: 22px;
    line-height: 1.8;
    color: #1f2937;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    text-align: left;
}

div[data-testid="stTextInput"] input {
    border-radius: 12px;
    padding: 14px;
    font-size: 16px;
    height: 55px;
}

/* Button styling only */
div[data-testid="stButton"] button {
    background-color: #003cff;
    color: white;
    border-radius: 12px;
    height: 55px;
    font-size: 24px;
    font-weight: bold;
    border: none;
}

div[data-testid="stButton"] button:hover {
    background-color: #002bcc;
    color: white;
    font-size: 24px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<h1 class="stTitle">Food Delivery Policy Assistant</h1>',
    unsafe_allow_html=True
)

st.markdown(
    '<h2 class="stWelcome">Welcome to the Food Delivery Policy Assistant!</h2>',
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Center textbox and button together
left, center, right = st.columns([2, 5, 2])

with center:
    question = st.text_input(
        label="Food delivery Agent - Ask a question about the Food Delivery Policy, Placing an Order",
        placeholder="Ask a question about the Food Delivery Policy or place an order...",
        key="question_input",
        label_visibility="collapsed"
    )

    # Center button below textbox
    b_left, b_center, b_right = st.columns([2, 1, 2])
    #apply css styling to the button
    with b_center:
        ask_clicked = st.button("Ask", use_container_width=True)

if ask_clicked:
    if question.strip() == "":
        st.warning("Please enter a question")
    else:
        cache_key = get_cache_key(question)

        #st.write("Cache Key:", cache_key)

        cached_answer = redis_client.get(cache_key)
        if cached_answer:
            answer = cached_answer
            st.success("✅ Redis Cache Hit - Answer returned from cache")
        else:
            with st.spinner("Calling Food Delivery Agent..."):
                response = ask_food_delivery_agent(question)

            if isinstance(response, dict):
                answer = response.get("answer", "")
            else:
                with st.spinner("Calling Food Delivery Agent..."):
                    response = ask_food_delivery_agent(question)

                    if isinstance(response, dict):
                        answer = response.get("answer", "")
                    else:
                        answer = str(response)

                    # Store answer in Redis for 1 hour
                    redis_client.setex(cache_key, 3600, answer)

                    st.warning("⚠️ Redis Cache Miss - Agent called and answer cached")

        st.markdown(
            """
            <h2 style='text-align:center;color:#15803d;'>
                ✅ Answer
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="answer-box">
                {answer}
            </div>
            """,
            unsafe_allow_html=True
        )