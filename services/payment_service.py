from services.firebase_service import get_collection
from models.plata import Plata

payments_collection = get_collection("payments")

def add_payment(payment: Plata):
    """Adaugă o plată în Firestore"""
    payment_dict = payment.model_dump()  # Pentru Pydantic v2
    payments_collection.add(payment_dict)

def get_payments_by_user(user_id: str):
    """Obține toate plățile unui utilizator"""
    payments = payments_collection.where("user_id", "==", user_id).stream()
    return [{"plata_id": p.id, **p.to_dict()} for p in payments]

def delete_payment(payment_id: str):
    """Șterge o plată din Firestore"""
    payments_collection.document(payment_id).delete()
