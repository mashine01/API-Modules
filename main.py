import nest_asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pyngrok import ngrok
from routes import router

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Include router
app.include_router(router)

auth_token = "2fM2RPGQACidFDDZgaEmMTQnbSQ_7E7sSafjHSGnFgQH6rERF"
ngrok.set_auth_token(auth_token)
ngrok_tunnel = ngrok.connect(8000)
print('Public URL:', ngrok_tunnel.public_url)

nest_asyncio.apply()
uvicorn.run(app, host="0.0.0.0", port=8000)
