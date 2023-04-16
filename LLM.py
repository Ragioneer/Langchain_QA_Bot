import variables
import pickle
from langchain import OpenAI, VectorDBQA

with open("vectorstore.pkl", "rb") as f:
        docsearch = pickle.load(f)

llm = OpenAI(temperature=0, model_name="text-davinci-003")

qa = VectorDBQA.from_chain_type(llm = llm, chain_type="refine", vectorstore=docsearch)

