# Import create_engine and MetaData from SQLAlchemy library
from sqlalchemy import create_engine, MetaData
# Import os module for environment variable access
import os

# Get DATABASE_URL from environment variable or use default SQLite database path
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Create SQLAlchemy engine with database URL and optional connection arguments
engine = create_engine(
    # Use the database URL for connection
    DATABASE_URL, 
    # Add connection arguments: disable thread check for SQLite, empty dict for other databases
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
# Create MetaData instance for table definitions and schema management
meta = MetaData()

# Define function to get a database connection
def get_connection():
    # Return a new database connection from the engine
    return engine.connect()

