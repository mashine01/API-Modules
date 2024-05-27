from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from config import MODEL, MODEL_BASENAME

model_path = hf_hub_download(repo_id=MODEL, filename=MODEL_BASENAME)

lcpp_llm = Llama(
    model_path=model_path,
    n_threads=4,
    n_batch=64,
    n_ctx=4096,
    n_gpu_layers=64,
    f16_kv=True
)
