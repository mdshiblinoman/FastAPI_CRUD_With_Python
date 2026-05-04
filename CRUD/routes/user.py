# Import APIRouter and HTTPException from fastapi
from fastapi import APIRouter, HTTPException
# Import database connection function from config module
from config.db import get_connection
# Import users table definition from models module
from models.user import users
# Import User and UserResponse schema models
from schemas.user import User, UserResponse
# Import List type for type hints
from typing import List

# Create an APIRouter instance for user routes
user = APIRouter()

# Define GET endpoint to retrieve all users
@user.get("/", response_model=List[UserResponse])
# Async function to handle get all users request
async def read_all_users():
    """Get all users"""
    # Get database connection context
    with get_connection() as conn:
        # Execute SELECT query to fetch all users
        result = conn.execute(users.select()).fetchall()
        # Return the result to client
        return result

# Define GET endpoint to retrieve a user by ID
@user.get("/{id}", response_model=UserResponse)
# Async function to handle get user by ID request
async def read_user(id: int):
    """Get a user by ID"""
    # Get database connection context
    with get_connection() as conn:
        # Execute SELECT query with WHERE condition to fetch specific user
        result = conn.execute(users.select().where(users.c.id == id)).fetchone()
        # Check if user not found
        if result is None:
            # Raise HTTP 404 exception if user doesn't exist
            raise HTTPException(status_code=404, detail="User not found")
        # Return the found user
        return result

# Define POST endpoint to create a new user
@user.post("/", response_model=UserResponse)
# Async function to handle create user request
async def create_user(user_data: User):
    """Create a new user"""
    # Get database connection context
    with get_connection() as conn:
        # Execute INSERT query with user data values
        result = conn.execute(users.insert().values(
            # Insert user name
            name=user_data.name,
            # Insert user email
            email=user_data.email,
            # Insert user password
            password=user_data.password
        ))
        # Commit the transaction to save changes
        conn.commit()
        # Retrieve the newly created user by its ID
        new_user = conn.execute(users.select().where(users.c.id == result.lastrowid)).fetchone()
        # Return the newly created user
        return new_user

# Define PUT endpoint to update an existing user
@user.put("/{id}", response_model=UserResponse)
# Async function to handle update user request
async def update_user(id: int, user_data: User):
    """Update an existing user"""
    # Get database connection context
    with get_connection() as conn:
        # Execute SELECT query to check if user exists
        existing = conn.execute(users.select().where(users.c.id == id)).fetchone()
        # Check if user not found
        if existing is None:
            # Raise HTTP 404 exception if user doesn't exist
            raise HTTPException(status_code=404, detail="User not found")
        # Execute UPDATE query with new values
        conn.execute(users.update().values(
            # Update user name
            name=user_data.name,
            # Update user email
            email=user_data.email,
            # Update user password
            password=user_data.password
        # Apply WHERE condition to update specific user
        ).where(users.c.id == id))
        # Commit the transaction to save changes
        conn.commit()
        # Retrieve the updated user
        updated_user = conn.execute(users.select().where(users.c.id == id)).fetchone()
        # Return the updated user
        return updated_user

# Define DELETE endpoint to delete a user by ID
@user.delete("/{id}")
# Async function to handle delete user request
async def delete_user(id: int):
    """Delete a user by ID"""
    # Get database connection context
    with get_connection() as conn:
        # Execute SELECT query to check if user exists
        existing = conn.execute(users.select().where(users.c.id == id)).fetchone()
        # Check if user not found
        if existing is None:
            # Raise HTTP 404 exception if user doesn't exist
            raise HTTPException(status_code=404, detail="User not found")
        # Execute DELETE query to remove the user
        conn.execute(users.delete().where(users.c.id == id))
        # Commit the transaction to save changes
        conn.commit()
        # Return success message to client
        return {"message": "User deleted successfully"}