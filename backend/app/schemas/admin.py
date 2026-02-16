from pydantic import BaseModel
from typing import List

class AdminStats(BaseModel):
    total_users: int
    total_modules: int
    total_completions: int
    average_rating: float
    users_growth: int
    completions_rate: float

class RegistrationData(BaseModel):
    date: str
    count: int

class PopularModule(BaseModel):
    module_id: str
    title: str
    views: int

class UserRoleCount(BaseModel):
    role: str
    count: int

class RecentActivity(BaseModel):
    user: str
    action: str
    timestamp: str

class Analytics(BaseModel):
    registrations_per_day: List[RegistrationData]
    popular_modules: List[PopularModule]
    user_roles: List[UserRoleCount]
    recent_activity: List[RecentActivity]
