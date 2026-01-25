from fastapi import APIRouter, HTTPException
from config.db import get_connection
from models.user import users
from schemas.user import User, UserResponse
from typing import List

user = APIRouter()

@user.get("/", response_model=List[UserResponse])
async def read_all_users():
    """Get all users"""
    with get_connection() as conn:
        result = conn.execute(users.select()).fetchall()
        return result

@user.get("/{id}", response_model=UserResponse)
async def read_user(id: int):
    """Get a user by ID"""
    with get_connection() as conn:
        result = conn.execute(users.select().where(users.c.id == id)).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return result

@user.post("/", response_model=UserResponse)
async def create_user(user_data: User):
    """Create a new user"""
    with get_connection() as conn:
        result = conn.execute(users.insert().values(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        ))
        conn.commit()
        new_user = conn.execute(users.select().where(users.c.id == result.lastrowid)).fetchone()
        return new_user

@user.put("/{id}", response_model=UserResponse)
async def update_user(id: int, user_data: User):
    """Update an existing user"""
    with get_connection() as conn:
        # Check if user exists
        existing = conn.execute(users.select().where(users.c.id == id)).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        conn.execute(users.update().values(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password
        ).where(users.c.id == id))
        conn.commit()
        
        updated_user = conn.execute(users.select().where(users.c.id == id)).fetchone()
        return updated_user

@user.delete("/{id}")
async def delete_user(id: int):
    """Delete a user by ID"""
    with get_connection() as conn:
        # Check if user exists
        existing = conn.execute(users.select().where(users.c.id == id)).fetchone()
        if existing is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        conn.execute(users.delete().where(users.c.id == id))
        conn.commit()
        return {"message": "User deleted successfully"}