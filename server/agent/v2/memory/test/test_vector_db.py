from langchain.embeddings import LlamaCppEmbeddings

llama = LlamaCppEmbeddings(model_path="E:\\models\\llama\\llama13b\\ggml-model-q8_0.bin")

text = "This is a test document."

query_result = llama.embed_query(text)

doc_result = llama.embed_documents([text])

tt = 1