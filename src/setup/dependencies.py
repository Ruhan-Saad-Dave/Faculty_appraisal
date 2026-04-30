from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, Header
from .database import SessionLocal
from typing import List, Optional, Annotated
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User:
    def __init__(self, id: str, roles: List[str], department: Optional[str] = None):
        self.id = id
        self.roles = roles
        self.department = department

    def has_authority_over(self, subordinate_id: str, subordinate_role: str, subordinate_dept: Optional[str] = None) -> bool:
        """
        Returns True if this user has authority to view/manage the subordinate's data.
        Hierarchy: Faculty (0) < HoD (1) < Director (2) < Dean (3) < VC (4)
        """
        role_weights = {
            "faculty": 0,
            "hod": 1,
            "director": 2,
            "dean": 3,
            "vc": 4,
            "admin": 5
        }
        
        # Admin has authority over everyone
        if "admin" in self.roles:
            return True
            
        # Get highest role weight for current user
        user_weight = max([role_weights.get(r.lower(), 0) for r in self.roles])
        sub_weight = role_weights.get(subordinate_role.lower(), 0)
        
        # Higher authority check
        if user_weight > sub_weight:
            # Special case for HoD: only if in same department
            if "hod" in self.roles and user_weight == 1:
                return self.department == subordinate_dept
            return True
            
        # Same user check
        if str(self.id) == str(subordinate_id):
            return True
            
        return False

def get_current_user(authorization: Annotated[Optional[str], Header()] = None) -> User:
    """
    Verifies the JWT from the frontend and returns user data + role.
    If no authorization header is provided, returns a mock user for development.
    """
    if not authorization:
        # Mock user for development/testing
        # In a real scenario, we'd mock specific roles as needed for testing
        return User(id=1, roles=["faculty"], department="Computer Science")
    
    try:
        token = authorization.split(" ")[1]
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        
        # In Supabase, roles and department are often in app_metadata or user_metadata
        role = user.app_metadata.get("role", "faculty")
        dept = user.user_metadata.get("department")
        
        roles = [role] if isinstance(role, str) else role
        
        return User(id=user.id, roles=roles, department=dept)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}",
        )

CurrentUser = Annotated[User, Depends(get_current_user)]
