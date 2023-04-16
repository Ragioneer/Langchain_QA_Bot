import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPAPI_API_KEY"] = os.getenv("SERPAPI_API_KEY")
bucket_name = os.getenv("AWS_BUCKET_NAME")
object_name = os.getenv("OBJECT_NAME")
file_name = os.getenv("FILE_NAME")
file_path = "https://www.git-tower.com/learn/assets/files/ebook-learn_version_control_with_git-SAMPLE.pdf"
access_key = os.getenv('AWS_ACCESS_KEY')
secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
