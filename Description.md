<h2> :floppy_disk: Project Description</h2>

This project, to a great extent is credited to the insurgance of Large language models and generative AI. The aim is to create an application which will take external docs/pdf as input from the user, load the data parse it in such a way thay the LLMs can understand and use that data along with their strong NLP capabilities, answer the queries of the user which is related to the context with precision and consistency.
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<h2> 🧰: Resources </h2>

* Langchain
* OpenAI
* Unstructured.io
* FAISS
* SERP API     - Not implemented yet
* Pinecone     - to be used in replacement of FAISS
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.png)

<img src = "https://github.com/mudassiraqeel2022skipq/Lanchain_QA_Bot/blob/main/static/QA_Bot.png">

<h2> :clipboard: Execution Instruction</h2>

### Loading files
For loading the docs from the user we are using **Langchain** library's extension `UnstructuredPDFLoader` which internally user **Unstructured.io**.
The `unstructured` library provides open-source components for pre-processing text documents
such as **PDFs**, **HTML** and **Word** Documents. These components are packaged as *bricks* 🧱, which provide
users the building blocks they need to build pipelines targeted at the documents they care
about. Bricks in the library fall into three categories:

- :jigsaw: ***Partitioning bricks*** that break raw documents down into standard, structured
  elements.
- :broom: ***Cleaning bricks*** that remove unwanted text from documents, such as boilerplate and
  sentence
  fragments.
- :performing_arts: ***Staging bricks*** that format data for downstream tasks, such as ML inference
  and data labeling.
  
### Splitting The Document
Since OpenAI for a free subscription has a token limit of **2049** tokens per request we can not exceed this therefore we need to split the documents using **Langchain** library's extension `RecursiveCharacterTextSplitter`
This text splitter is the recommended one for generic text. It is parameterized by a list of characters. It tries to split on them in order until the chunks are small enough. The default list is ["\n\n", "\n", " ", ""]. This has the effect of trying to keep all paragraphs (and then sentences, and then words) together as long as possible, as those would generically seem to be the strongest semantically related pieces of text.

### Creating the vectorstore database
The project uses **Langchain** library's extension `OpenAIEmbeddings`.
OpenAI’s text embeddings measure the relatedness of text strings. Embeddings are commonly used for:

* Search (where results are ranked by relevance to a query string)
* Clustering (where text strings are grouped by similarity)
* Recommendations (where items with related text strings are recommended)
* Anomaly detection (where outliers with little relatedness are identified)
* Diversity measurement (where similarity distributions are analyzed)
* Classification (where text strings are classified by their most similar label)

An embedding is a vector (list) of floating point numbers. The distance between two vectors measures their relatedness. Small distances suggest high relatedness and large distances suggest low relatedness.

The project uses **Langchain** library's extension `FAISS` which is a wrapper around FAISS vector database, and the VectorStore initialized from documents after splitting and embeddings.
**Faiss** is a library — developed by Facebook AI — that enables efficient similarity search.

### Querying the data

So, given a set of vectors, we can index them using Faiss — then using another vector (the query vector), we search for the most similar vectors within the index.
Now, Faiss not only allows us to build an index and search — but it also speeds up search times to ludicrous performance levels, for instance;

Faiss allows us to add multiple steps that can optimize our search using many different methods. A popular approach is to partition the index into <a href="https://www.baeldung.com/cs/voronoi-diagram">Voronoi cells.</a>

Using this method, we would take a query vector xq, identify the cell it belongs to, and then use our IndexFlatL2 (or another metric) to search between the query vector and all other vectors belonging to that specific cell.

So, we are reducing the scope of our search, producing an approximate answer, rather than exact (as produced through exhaustive search).

The project uses **Langchain** library's extension `VectorDBQA` from **chain** the chain type is **Refine** as the block diagram above depicts, the query is passed to the VectorDBQA which serves as a retriever for similar context by first converting the query to a vector and calculates the cosine similarity with the vectors in the vectorstore and fetches the texts with the highest cosine similarity and then combine/summarize them in a refining fashion as shown in the diagram and finally submits the output.

If asked about something which doesn't relates to the subject of the pdf/docs uploaded, the bot reply with an appropriate answer telling the user that the question is out of context
