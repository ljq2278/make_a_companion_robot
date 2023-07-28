from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


def get_vicuna13b_llm():
    local_path = (
        "E:\models\ggml-vicuna-13b-1.1-q4_2.bin"
    )

    callbacks = [StreamingStdOutCallbackHandler()]

    llm = GPT4All(model=local_path, callbacks=callbacks, backend="gptj", verbose=True)
    return llm
