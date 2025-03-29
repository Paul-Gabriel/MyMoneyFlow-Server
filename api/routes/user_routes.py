from fastapi import APIRouter
from models.user import User
from services.user_service import *

router = APIRouter()

@router.post("/")
async def create_user(user: User):
    """Endpoint pentru adăugarea unui utilizator"""
    add_user(user)
    return {"message": "User added successfully"}

@router.get("/")
async def read_all_users():
    """Endpoint pentru obținerea tuturor utilizatorilor"""
    users = get_all_users()
    return users

@router.get("/{user_id}")
async def read_user(user_id: str):
    """Endpoint pentru obținerea unui utilizator după ID"""
    user = get_user_by_id(user_id)
    if user:
        return user
    return {"error": "User not found"}

@router.get("/email/{email}")
async def read_user_by_email(email: str):
    """Endpoint pentru obținerea unui utilizator după email"""
    user = get_user_by_email(email)
    if user:
        return user
    return {"error": "User not found"}

@router.put("/{user_id}")
async def update_user(user_id: str, user: User):
    """Endpoint pentru actualizarea unui utilizator"""
    updated = update_user_by_id(user_id, user)
    if updated:
        return {"message": "User updated successfully"}
    return {"error": "User not found"}

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """Endpoint pentru ștergerea unui utilizator"""
    deleted = delete_user_by_id(user_id)
    if deleted:
        return {"message": "User deleted successfully"}
    return {"error": "User not found"}
