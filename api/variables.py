import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
dataset = "datasets/" + os.getenv("FILE_PATH")
persist_directory = os.getenv("PERSIST_DIRECTORY")
collection_name = os.getenv("COLLECTION_NAME")