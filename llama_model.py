from huggingface_hub import hf_hub_download
from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
from config import MODEL, MODEL_BASENAME

model_path = hf_hub_download(repo_id=MODEL, filename=MODEL_BASENAME)

lcpp_llm = LlamaCpp(
    model_path=model_path,
    n_threads=4,
    n_batch=64,
    n_ctx=4096,
    n_gpu_layers=32,
)
