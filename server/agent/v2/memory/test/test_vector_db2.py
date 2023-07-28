from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.embeddings.llamacpp import LlamaCppEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader

# load the document and split it into chunks
# loader = TextLoader("state_of_the_union_simple.txt", encoding='utf-8')
# documents = loader.load()
#
# # split it into chunks
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)
query = "What is the current situation of Russian"
# create the open-source embedding function
# embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
embedding_function = LlamaCppEmbeddings(model_path="E:\\models\\llama\\llama13b\\ggml-model-q8_0.bin")
######################################################################
# load from disk
db3 = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
docs_result = db3.similarity_search(query)
print("search db3: ", docs_result[0].page_content)
