#rag engine will load data from vector database
#send prompt to llm
#llm will query the vector database and return relevant information

import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import RetrievalQA

from ragapp.filters.gaurdrails import mask_pii, validate_input, validate_output
from ragapp.filters.safety_filter import input_safety_check, output_safety_check
env_path= os.path.join(os.path.dirname(__file__), '..','.env')
load_dotenv(env_path)

def load_data_from_vector_db():
    persistent_directory = os.getenv("persist_directory")
    if not persistent_directory:
        raise ValueError("persist_directory is not set in the environment variables.")
    #read embeddings from persistent directory
    embeddings= HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    #read from vector database
    vector_db = Chroma(persist_directory=persistent_directory, embedding_function=embeddings)
    retriever = vector_db.as_retriever(
        search_kwargs={"k": 3}
    )
    return retriever

def load_llm(retriever):
    #define open ai llm
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are a Food Delivery Support Assistant.

    Answer only from the Food Delivery Policy.

    Rules:
    - Use only the provided context.
    - If not found say:
    "I am sorry, I could not find any information regarding your query in the Food Delivery Policy."

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    )
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    return rag_chain

def receive_prompt(question:str):
   #safety check for input question

    status, message = input_safety_check(question)
    if not status:
        return {"answer": message}
    
    status,message= validate_input(question)
    if not status:
        return {"answer": message}
    #read the prompt
    retriever = load_data_from_vector_db()
    ragchain= load_llm(retriever)
    answer= ragchain.invoke({
        "query": question
    })

    answer_text = output_safety_check(answer['result'])
    answer_text=validate_output(answer_text)
    return {
        "answer": mask_pii(answer_text)
        
       
    }
#"source_documents": answer['source_documents']