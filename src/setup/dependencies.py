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
    def __init__(self, id: str, roles: List[str], department: Optional[str] = None, school_id: Optional[str] = None, division: Optional[str] = None):
        self.id = id
        self.roles = [r.lower() for r in roles]
        self.department = department
        self.school_id = school_id
        self.division = division

    def has_authority_over(self, subordinate_id: str, subordinate_role: str, subordinate_dept: Optional[str] = None, subordinate_school_id: Optional[str] = None, subordinate_division: Optional[str] = None) -> bool:
        """
        Implements Hierarchical Access Control:
        1. VC: All schools.
        2. Dean: All schools within their division (Engineering/Non-Engineering).
        3. Director: All departments within their school.
        4. HOD: Only their specific department (Horizontal Isolation).
        """
        role_weights = {
            "faculty": 0,
            "hod": 1,
            "director": 2,
            "dean": 3,
            "vc": 4,
            "admin": 5
        }
        
        if "admin" in self.roles:
            return True
            
        user_weight = max([role_weights.get(r, 0) for r in self.roles])
        sub_weight = role_weights.get(subordinate_role.lower(), 0)
        
        # Self-access
        if str(self.id) == str(subordinate_id):
            return True
            
        # Hierarchy check
        if user_weight > sub_weight:
            # VC Access
            if "vc" in self.roles:
                return True
            
            # Dean Access (Division Isolation)
            if "dean" in self.roles:
                return self.division == subordinate_division
            
            # Director Access (School Isolation)
            if "director" in self.roles:
                return str(self.school_id) == str(subordinate_school_id)
            
            # HOD Access (Departmental/Horizontal Isolation)
            if "hod" in self.roles:
                # Must be in the same school AND same department
                return str(self.school_id) == str(subordinate_school_id) and self.department == subordinate_dept
                
        return False

def get_current_user(authorization: Annotated[Optional[str], Header()] = None) -> User:
    """
    Verifies the JWT from the frontend and returns user data + role.
    If no authorization header is provided, returns a mock user for development.
    """
    if not authorization:
        # Mock user for development/testing
        # Faculty in CS Department, SO-CS School, Engineering Division
        return User(
            id="00000000-0000-0000-0000-000000000001", 
            roles=["faculty"], 
            department="Computer Science",
            school_id="00000000-0000-0000-0000-000000000000", # Mock School ID
            division="Engineering"
        )
    
    try:
        token = authorization.split(" ")[1]
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        user_response = supabase.auth.get_user(token)
        user = user_response.user
        
        # In Supabase, roles, department, school_id, and division are in app_metadata/user_metadata
        role = user.app_metadata.get("role", "faculty")
        dept = user.user_metadata.get("department")
        school_id = user.user_metadata.get("school_id")
        division = user.user_metadata.get("division")
        
        roles = [role] if isinstance(role, str) else role
        
        return User(
            id=user.id, 
            roles=roles, 
            department=dept, 
            school_id=school_id, 
            division=division
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}",
        )

CurrentUser = Annotated[User, Depends(get_current_user)]
