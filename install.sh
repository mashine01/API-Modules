sudo apt update
sudo apt upgrade
sudo apt install python3
sudo apt install python3-pip
pip install FastAPI nest-asyncio pyngrok uvicorn python-multipart huggingface_hub langchain_community langchain_core numpy --quiet
CMAKE_ARGS="-DLLAMA_CUDA=on" FORCE_CMAKE=1 pip install llama-cpp-python --quiet