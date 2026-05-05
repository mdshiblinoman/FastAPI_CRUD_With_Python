# Import BaseModel from Pydantic for creating request/response schemas
from pydantic import BaseModel
# Import Optional type for optional fields in schemas
from typing import Optional

# Define User schema for request body validation
class User(BaseModel):
    # Optional user ID (not provided in create/update requests)
    id: Optional[int] = None
    # Required user name field
    name: str
    # Required user email field
    email: str
    # Required user password field
    password: str

# Define UserResponse schema for API responses
class UserResponse(BaseModel):
    # Required user ID in response
    id: int
    # Required user name in response
    name: str
    # Required user email in response
    email: str
    # Configuration class for schema settings
    class Config:
        # Use attribute names instead of alias when converting database models
        from_attributes = True

