from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes.user import user
from config.db import engine, meta
from models.user import users

app = FastAPI(
    title="User Management API",
    description="A simple CRUD API for managing users",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create tables on startup
@app.on_event("startup")
async def startup():
    meta.create_all(engine)

# Serve frontend
@app.get("/")
async def root():
    return FileResponse("static/index.html")

app.include_router(user, prefix="/users", tags=["users"])