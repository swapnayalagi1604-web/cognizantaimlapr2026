#read the food delivery policy from data folder create embeddings
import os
from dotenv import load_dotenv
from langchain_classic.document_loaders import Docx2txtLoader, TextLoader,PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
   # Assuming you have an embedding model and vector store initialized
from langchain_classic.embeddings import OpenAIEmbeddings
from langchain_classic.vectorstores import Chroma
import warnings
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning
)
env_path = os.path.join(os.path.dirname(__file__),'..', '.env')
load_dotenv(env_path)

def load_documents(dir_path):
    documents=[]

    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if filename.endswith('.txt'):            
            loader=TextLoader(file_path, encoding='utf-8')
            documents.extend(loader.load())
        elif filename.endswith('.pdf'):            
            loader=PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif filename.endswith('.docx'):
            loader=Docx2txtLoader(file_path)
            documents.extend(loader.load())
    return documents

def create_chunks(documents, chunk_size=1000, chunk_overlap=10):
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(documents)
    return chunks

def create_embeddings(chunks, embedding_model):
    embeddings = embedding_model.embed_documents([chunk.page_content for chunk in chunks])
    return embeddings



if __name__ == "__main__":
    data_dir = os.getenv('data_dir')
    documents = load_documents(data_dir)
    chunks = create_chunks(documents)   

    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    #chroma store
    persist_directory = os.getenv('persist_directory')   

    embeddings = create_embeddings(chunks, embedding_model)
    vector_store = Chroma.from_documents(chunks, embedding_model, persist_directory=persist_directory)  
    
    vector_store.persist()
    #check data stored
    print("Data stored successfully in Chroma vector store.")
    print(f"Documents ingested and stored in vector database at {persist_directory}")
    print(f"Total number of chunks: {len(chunks)}")

