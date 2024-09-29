from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.config import Config
from .routes import router as api_router
from .frontend_routes import frontend_router

app = FastAPI()

# Load environment variables
config = Config('.env')

# Set up session middleware
app.add_middleware(SessionMiddleware, secret_key=config('SECRET_KEY'))

# Set up static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include API routes
app.include_router(api_router, prefix="/api")

# Include frontend routes
app.include_router(frontend_router)

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
