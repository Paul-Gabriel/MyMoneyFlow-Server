from fastapi import APIRouter, HTTPException
from models.plata import Plata
from services.payment_service import *

router = APIRouter()

@router.post("/")
async def create_payment(payment: Plata):
    """Adaugă o plată în Firestore"""
    try:
        add_payment(payment)
        return {"message": "Payment added successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def list_payments():
    """Obține toate plățile"""
    try:
        payments = get_all_payments()
        return payments
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_ref}")
async def list_payments(user_ref: str):
    """Obține toate plățile unui utilizator"""
    try:
        payments = get_payments_by_user(user_ref)
        return payments
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/payment/{payment_id}")
async def get_payment(payment_id: str):
    """Obține o plată după ID"""
    try:
        payment = get_payment_by_id(payment_id)
        return payment
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{payment_id}")
async def update_payment(payment_id: str, payment: Plata):
    """Actualizează o plată în Firestore"""
    try:
        update_payment_by_id(payment_id, payment)
        return {"message": "Payment updated successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{payment_id}")
async def remove_payment(payment_id: str):
    """Șterge o plată după ID"""
    try:
        delete_payment_by_id(payment_id)
        return {"message": "Payment deleted successfully"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
