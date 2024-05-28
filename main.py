import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pyngrok import ngrok
from routes import router
from config import NGROK_AUTH_TOKEN

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

# Set the authtoken
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Connect to ngrok
ngrok_tunnel = ngrok.connect(8000)

# Print the public URL
print('Public URL:', ngrok_tunnel.public_url)

# Apply nest_asyncio
nest_asyncio.apply()

# Run the uvicorn server
uvicorn.run(app, port=8000)