from fastapi import APIRouter, HTTPException
from models.user import User
from services.firebase_service import get_collection
from services.user_service import add_user, confirm_user_email, delete_user_by_id, get_all_users, get_user_by_email, get_user_by_id, update_user_by_id

users_collection = get_collection("users")

router = APIRouter()

@router.post("/")
async def create_user(user: User):
    """Endpoint pentru adăugarea unui utilizator"""
    try:
        add_user(user)
        return {"message": "User added successfully"}
    except ValueError as ve:
        raise HTTPException(status_code=500, detail=str(ve))
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/confirm/{token}")
def confirm_user(token: str):
    """Confirmă un utilizator pe baza token-ului"""
    try:
        confirm_user_email(token)
        return {"message": "Contul a fost confirmat cu succes!"}
    except HTTPException as http_exc:
        raise HTTPException(status_code=404, detail="Token invalid sau expirat.")

@router.get("/")
async def read_all_users():
    """Endpoint pentru obținerea tuturor utilizatorilor"""
    try:
        users = get_all_users()
        return users
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def read_user(user_id: str):
    """Endpoint pentru obținerea unui utilizator după ID"""
    try:
        user = get_user_by_id(user_id)
        return user
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/email/{email}")
async def read_user_by_email(email: str):
    """Endpoint pentru obținerea unui utilizator după email"""
    try:
        user = get_user_by_email(email)
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}")
async def update_user(user_id: str, user: User):
    """Endpoint pentru actualizarea unui utilizator"""
    try:
        update_user_by_id(user_id, user)
        return {"message": "User updated successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    """Endpoint pentru ștergerea unui utilizator"""
    try:
        delete_user_by_id(user_id)
        return {"message": "User deleted successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
