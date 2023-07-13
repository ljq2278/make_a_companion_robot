from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

path_0 = "E:\\models\\llama\\llama7b\\ggml-model-f16.bin"
path_1 = "E:\\models\\llama\\llama13b\\ggml-model-q8_0.bin"
path_2 = "E:\\models\\llama\\llama13b\\ggml-model-q4_0.bin"
path_3 = "E:\models\gpt4all\GPT4All-13B-snoozy.ggmlv3.q4_0.bin"
path_4 = "E:\\models\\llama\\llama30b\\ggml-model-q4_1.bin"
path_5 = "E:\\models\\llama\\llama30b\\ggml-model-q5_0.bin"
def get_llama_llm():
    # Callbacks support token-wise streaming
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    # Verbose is required to pass to the callback manager

    n_gpu_layers = 61  # Change this value based on your model and your GPU VRAM pool.
    n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.

    # Make sure the model path is correct for your system!
    llm = LlamaCpp(
        model_path=path_1,
        n_gpu_layers=n_gpu_layers,
        n_batch=n_batch,
        n_ctx=5000,
        callback_manager=callback_manager,
        # verbose=True,
    )
    return llm
