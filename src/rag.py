import os
import tempfile

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
load_dotenv(dotenv_path=".env")

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    streaming = True
)

def build_db(uploaded_file):
    with tempfile.NamedTemporaryFile(delete = False,suffix = ".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()



    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size= 1000,
        chunk_overlap = 200
    )

    docs = text_splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(
        docs,
        embeddings
    )
    return db

def build_db_from_path(pdf_path):
     loader = PyPDFLoader(pdf_path)
     documents = loader.load()



     text_splitter = RecursiveCharacterTextSplitter(
        chunk_size= 1000,
        chunk_overlap = 200
    )

     docs = text_splitter.split_documents(documents)
     embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )

     db = FAISS.from_documents(
        docs,
        embeddings
    )
     return db,docs

def get_answer_stream(question,db):
    """generator - yields chunks as produced"""
    results = db.similarity_search(
        question,
        k=5
    )

    context = "\n".join(
        [doc.page_content for doc in results]
    )

    prompt = f"""
    Context:
    {context}
    Question:
    {question}
    
    Answer in a concise and clear manner using only the provided context.
    """
    for chunk in llm.stream(prompt):
        yield chunk.content

def get_answer(question, db):
    """Keep the original non-streaming version too — useful for quick scripts/tests."""
    results = db.similarity_search(question, k=5)
    context = "\n".join([doc.page_content for doc in results])

    prompt = f"""
    Context:
    {context}
    Question:
    {question}
    
    Answer in a concise and clear manner using only the provided context.
    """

    response = llm.invoke(prompt)
    return response.content