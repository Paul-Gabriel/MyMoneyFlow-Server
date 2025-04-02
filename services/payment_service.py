from fastapi import HTTPException
from services.firebase_service import get_collection
from models.plata import Plata
from services.user_service import get_user_by_id

payments_collection = get_collection("payments")

def add_payment(payment: Plata):
    """Adaugă o plată în Firestore"""
    payment_dict = payment.model_dump()

    # Verifică dacă utilizatorul există
    if get_user_by_id(payment_dict.get("user_ref")) is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verifică dacă suma este pozitivă
    if payment_dict.get("suma") <= 0:
        raise ValueError("Suma trebuie să fie pozitivă.")
    
    payments_collection.add(payment_dict)

def get_all_payments():
    """Obține toate plățile"""
    payments = payments_collection.stream()
    if payments:
        return [{"plata_id": p.id, **p.to_dict()} for p in payments]
    else:
        raise HTTPException(status_code=404, detail="No payments found")

def get_payments_by_user(user_ref: str):
    """Obține toate plățile unui utilizator"""
    payments = payments_collection.where("user_ref", "==", user_ref).stream()
    if payments:
        return [{"plata_id": p.id, **p.to_dict()} for p in payments]
    else:
        raise HTTPException(status_code=404, detail="No payments found for this user")

def get_payment_by_id(payment_id: str):
    """Obține o plată după ID"""
    payment = payments_collection.document(payment_id).get()
    if payment.exists:
        return {"plata_id": payment.id, **payment.to_dict()}
    else:
        raise HTTPException(status_code=404, detail="Payment not found")
    
def update_payment_by_id(payment_id: str, payment: Plata):
    """Actualizează o plată în Firestore"""
    payment_doc = payments_collection.document(payment_id).get()
    if payment_doc.exists:
        payment_dict = payment.model_dump()
        payments_collection.document(payment_id).update(payment_dict)
    else:
        raise HTTPException(status_code=404, detail="Payment not found")
    
def delete_payment_by_id(payment_id: str):
    """Șterge o plată din Firestore"""
    payment_doc = payments_collection.document(payment_id).get()
    if payment_doc.exists:
        payments_collection.document(payment_id).delete()
    else:
        raise HTTPException(status_code=404, detail="Payment not found")
