from sqlalchemy import create_engine, MetaData
import os

# Use environment variable or default to SQLite for easy local testing
# For MySQL: "mysql+pymysql://username:password@localhost:3306/database_name"
# For SQLite: "sqlite:///./test.db"
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
meta = MetaData()

def get_connection():
    return engine.connect()

