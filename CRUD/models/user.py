# Import Table, Column, Integer, String from SQLAlchemy for defining database tables
from sqlalchemy import Table, Column, Integer, String
# Import metadata instance from database configuration module
from config.db import meta

# Define users table with metadata and columns
users = Table(
    # Table name in the database
    'users', meta,
    # Define id column as Integer primary key with auto-increment
    Column('id', Integer, primary_key=True, autoincrement=True),
    # Define name column as String with max 255 characters, required field
    Column('name', String(255), nullable=False),
    # Define email column as String with max 255 characters, unique and required
    Column('email', String(255), nullable=False, unique=True),
    # Define password column as String with max 255 characters, required field
    Column('password', String(255), nullable=False),
)

