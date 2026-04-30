from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Header
from .database import SessionLocal
from typing import List, Optional
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user(authorization: Optional[str] = Header(None)) -> User:
    """
    Verifies the JWT from the frontend and returns user data + role.
    If no authorization header is provided, returns a mock user for development.
    """
    if not authorization:
        # Mock user for development/testing
        return User(id=1, roles=["faculty", "admin", "hod", "director"])
    
    try:
        token = authorization.split(" ")[1]
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        
        # In Supabase, roles are often in app_metadata
        # Defaulting to ["faculty"] if no role is set
        role = user.app_metadata.get("role", "faculty")
        # Ensure role is a list for consistency with current code
        roles = [role] if isinstance(role, str) else role
        
        return User(id=user.id, roles=roles)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}",
        )
