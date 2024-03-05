from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from api.parameters import prompt
from api import variables

def vector_call(directory):
    persist_directory = directory

    embedding = OpenAIEmbeddings()

    vectordb = Chroma(
        persist_directory=variables.persist_directory,
        embedding_function=embedding
    )

    return vectordb

def llm_selector(model,temperature):
    llm = ChatOpenAI(model = model, temperature = temperature)
    return llm

# Stuff Chain
def qa_chain(llm, vector_db):
    chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vector_db.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt.QA_CHAIN_PROMPT}
    )   
    return chain


vectorstore = vector_call("./chroma")

print (vectorstore._collection.count())

# QA Retiever
llm = llm_selector( "gpt-3.5-turbo-0125",0 )
qa = qa_chain(llm, vectorstore)


# # Example question:
# question = str("What is the introduction of Saqlain Mushtaque")
# result = qa .invoke({'query': question})
# print(result["result"])


