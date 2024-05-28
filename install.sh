sudo apt update
sudo apt upgrade
sudo apt install python3
sudo apt install python3-pip
pip install FastAPI nest-asyncio pyngrok uvicorn python-multipart huggingface_hub numpy nest_asyncio --quiet
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python --quiet