# Import FastAPI class for creating the API application
from fastapi import FastAPI
# Import StaticFiles for serving static files from directories
from fastapi.staticfiles import StaticFiles
# Import FileResponse for returning files as responses
from fastapi.responses import FileResponse
# Import user router containing CRUD endpoints
from routes.user import user
# Import SQLAlchemy engine and metadata for database operations
from config.db import engine, meta
# Import users table model
from models.user import users

# Create FastAPI application instance with metadata
app = FastAPI(
    # Set the API title displayed in documentation
    title="User Management API",
    # Set the API description displayed in documentation
    description="A simple CRUD API for managing users",
    # Set the API version number
    version="1.0.0"
)

# Mount static files directory at /static URL path
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define startup event handler to run on application startup
@app.on_event("startup")
# Async function to execute database initialization
async def startup():
    # Create all database tables from metadata definitions
    meta.create_all(engine)

# Define root endpoint to serve the frontend HTML
@app.get("/")
# Async function to handle root path requests
async def root():
    # Return the static index.html file as the response
    return FileResponse("static/index.html")

# Include user router with URL prefix and tags for API documentation
app.include_router(user, prefix="/users", tags=["users"])