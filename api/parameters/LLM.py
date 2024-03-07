from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from api.parameters import prompt
from langchain.memory import ConversationBufferMemory
from api import variables

def vector_call():

    embedding = OpenAIEmbeddings()

    vectordb = Chroma(
        persist_directory=variables.persist_directory,
        embedding_function=embedding
    )

    return vectordb

def llm_selector(model, temperature):
    llm = ChatOpenAI(model=model, temperature=temperature)
    return llm

# Stuff Chain
def qa_chain(llm, vectorstore, memory):

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt": prompt.QA_CHAIN_PROMPT},
    )

    return chain


vectorstore = vector_call()

print(vectorstore._collection.count())

# QA Retiever
llm = llm_selector("gpt-3.5-turbo-0125", 0)

# Initialize conversation memory
conversation_memory = ConversationBufferMemory()

# Create the QA chain with memory
qa = qa_chain(llm, vectorstore, conversation_memory)

# Example question:
question = str("What is the introduction of Saqlain Mushtaque")

result = qa.invoke({'query': question})

# Append query and response to memory
conversation_memory.append(question, result["result"])

print(result["result"])
