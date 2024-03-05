from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from loguru import logger
import os

from api import variables

def load_pdf_document(file_path):
    loader = PyPDFLoader(file_path)
    return loader.load()

def split_documents(pages):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n\n\n\n", "\n\n\n\n", "\n\n\n", "\n\n", "\r\n", "\n"],
        chunk_size=500,
        chunk_overlap=50,
    )
    response = text_splitter.split_documents(pages)
    logger.info(len(response))
    return response

def embeddings(model: str = "text-embedding-ada-002",):
    return OpenAIEmbeddings()

def create_chroma_client(docs, embeddings):
    # Delete any existing collection before creating a new one
    if os.path.exists(variables.persist_directory):
        vectorstore = Chroma.from_documents(
            embedding=embeddings,
            persist_directory=variables.persist_directory
        )
        try:
            vectorstore.delete_collection()
            logger.info("The collection has been deleted")
        except Exception as e:
            logger.warning(f"Error deleting collection: {e}")

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=variables.persist_directory
    )
    logger.info(vectorstore._collection.count())
    return vectorstore

def Load_PDF(file_path: str, model: str = "text-embedding-ada-002"):
    # Upload PDF
    loader = load_pdf_document(file_path)

    # Split PDF
    pages = split_documents(loader)

    # Create Embeddings
    embedding = embeddings(model)

    # Create or overwrite Chroma Client
    vectorstore = create_chroma_client(pages, embedding)

    return vectorstore
