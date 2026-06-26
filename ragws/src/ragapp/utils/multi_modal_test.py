# app.py
import streamlit as st
import os
import base64
import tempfile
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from gtts import gTTS
from dotenv import load_dotenv

env_path = os.path.join(os.path.dirname(__file__), '..', ".env")
load_dotenv(env_path)

# streamlit run src/ragapp/utils/multi_modal_test.py

st.set_page_config(page_title="Medical Multimodal Assistant", page_icon="🩺")

# Azure OpenAI setup
deployment_name = "gpt-4.1-mini"
transcribe_deployment = "gpt-4o-mini-transcribe"

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url=os.getenv("azure_openai_project_endpoint"),
    api_key=token_provider
)

st.title("🩺 Medical Image + Audio Support Assistant")

uploaded_file = st.file_uploader(
    "Upload medical image",
    type=["jpg", "jpeg", "png"]
)

audio_input = st.file_uploader(
    "Upload audio question",
    type=["mp3", "wav", "m4a"]
)

question = st.text_area(
    "Your typed question",
    "Analyze this medical image and suggest next safe step."
)

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded image", width=300)

transcribed_text = ""

if audio_input:
    st.audio(audio_input)

    with st.spinner("Transcribing audio..."):
        suffix = os.path.splitext(audio_input.name)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(audio_input.read())
            audio_path = tmp.name

        with open(audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model=transcribe_deployment,
                file=audio_file
            )

        transcribed_text = transcript.text

        os.remove(audio_path)

    st.write("### Audio Transcript")
    st.write(transcribed_text)

if st.button("Analyze Image"):
    if uploaded_file is None:
        st.warning("Please upload a medical image.")
    else:
        image_bytes = uploaded_file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        mime_type = uploaded_file.type

        combined_question = f"""
User typed question:
{question}

User audio question:
{transcribed_text}

Analyze the uploaded medical image and explain:
1. What is visible in the image
2. Possible observations
3. Safe next steps
4. When the user should consult a doctor

Give safe, non-diagnostic guidance only.
Do not claim a final diagnosis.
"""

        with st.spinner("Analyzing image and question..."):
            response = client.chat.completions.create(
                model=deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": """
You are a medical support assistant.
Give safe, non-diagnostic guidance.
Do not provide a final diagnosis.
Do not prescribe medicines.
Ask the user to consult a qualified healthcare professional for diagnosis or treatment.
Mention urgent red-flag symptoms when appropriate.
"""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": combined_question
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=700
            )

        answer = response.choices[0].message.content

        st.success("Analysis completed")
        st.write(answer)

        with st.spinner("Generating audio response..."):
            audio_output_path = "response.mp3"
            tts = gTTS(text=answer, lang="en")
            tts.save(audio_output_path)

            with open(audio_output_path, "rb") as audio_file:
                audio_bytes = audio_file.read()

            st.audio(audio_bytes, format="audio/mp3")

            os.remove(audio_output_path)