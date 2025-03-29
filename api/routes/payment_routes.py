from fastapi import APIRouter, HTTPException
from models.plata import Plata
from services.payment_service import add_payment, get_payments_by_user, delete_payment

router = APIRouter()

@router.post("/")
async def create_payment(payment: Plata):
    """Adaugă o plată în Firestore"""
    try:
        add_payment(payment)
        return {"message": "Payment added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
async def list_payments(user_id: str):
    """Obține toate plățile unui utilizator"""
    payments = get_payments_by_user(user_id)
    if not payments:
        raise HTTPException(status_code=404, detail="No payments found for this user")
    return payments

@router.delete("/{payment_id}")
async def remove_payment(payment_id: str):
    """Șterge o plată după ID"""
    try:
        delete_payment(payment_id)
        return {"message": "Payment deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
