from fastapi import HTTPException, status
from typing import List
import enum

class UserRole(str, enum.Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"

def require_role(user_role: UserRole, allowed_roles: List[UserRole]):
    """Check if user has required role"""
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return True
