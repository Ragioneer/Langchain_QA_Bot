from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from loguru import logger
import os

from api import variables


def load_pdf_document(file_path):
    """Loads a PDF document from a given file path."""

    try:
        loader = PyPDFLoader(file_path)
        return loader.load()
    except Exception as e:
        logger.error(f"Error loading PDF: {e}")
        raise


def split_documents(pages):
    """Splits PDF pages into smaller text chunks for embedding."""

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n\n\n\n", "\n\n\n\n", "\n\n\n", "\n\n", "\r\n", "\n"],
        chunk_size=500,
        chunk_overlap=50,
    )
    response = text_splitter.split_documents(pages)
    logger.info(f"Split documents into {len(response)} chunks")
    return response


def embeddings(model: str = "text-embedding-ada-002"):
    """Returns an OpenAI embedding model instance."""

    try:
        return OpenAIEmbeddings()
    except Exception as e:
        logger.error(f"Error creating embedding model: {e}")
        raise


def create_chroma_client(docs, embeddings):
    """
    Creates a Chroma vectorstore, optionally deleting any existing collection first.

    Args:
        docs: List of documents to embed.
        embeddings: Embedding model instance.

    Returns:
        Chroma vectorstore instance.
    """

    if os.path.exists("chroma.sqlite3"):
        try:
            delete = os.path.join(variables.persist_directory, "chroma.sqlite3")
            os.remove(delete)
            logger.info("Existing Chroma collection deleted")
        except Exception as e:
            logger.warning(f"Error deleting collection: {e}")

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=variables.persist_directory
    )
    logger.info(f"Chroma vectorstore created with {vectorstore._collection.count()} documents")
    return vectorstore


def delete_file(file_path, identifier):
    """Deletes a file based on its path and identifier.

    Args:
        file_path: Path to the file.
        identifier: Unique identifier for the file (optional).

    Raises:
        FileNotFoundError: If the file is not found.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        os.remove(file_path)
        logger.info(f"File deleted: {identifier}")
    except Exception as e:
        logger.error(f"Error deleting file: {e}")
        raise


def Load_PDF(file_path: str, model: str = "text-embedding-ada-002", delete_flag=False, identifier=None):
    """
    Main function to load a PDF, split it, create embeddings, and potentially delete files.

    Args:
        file_path: Path to the PDF file.
        model: Embedding model name (default: "text-embedding-ada-002").
        delete_flag: Flag indicating whether to delete the file after processing (default: False).
        identifier: Unique identifier for the file (optional).

    Returns:
        Chroma vectorstore instance containing the embeddings.

    Raises:
        Exception: If any error occurs during processing.
    """

    try:
        # Load the PDF
        loader = load_pdf_document(file_path)

        # Split the PDF into text chunks
        pages = split_documents(loader)

        # Create embedding model
        embedding = embeddings(model)

        # Accumulate all documents
        all_documents = []

        # Generate identifier if not provided (assuming unique file names)
        if not identifier:
            identifier = os.path.basename(file_path)

        # Handle file deletion based on flag
        if delete_flag:
            delete_file(file_path, identifier)

        # Add current file's documents to the list
        all_documents.extend(pages)

        # Create or overwrite Chroma Client with combined documents
        vectorstore = create_chroma_client(all_documents, embedding)

        return vectorstore
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        raise