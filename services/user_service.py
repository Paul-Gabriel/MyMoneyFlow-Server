from fastapi import HTTPException
from services.firebase_service import get_collection
from models.user import User

users_collection = get_collection("users")

def add_user(user: User):
    """Adaugă un utilizator în Firestore"""

    # Verifică dacă există deja un utilizator cu același email
    if get_user_by_email(user.email):
        raise ValueError("Un utilizator cu acest email există deja.")
    
    # Verifică dacă procentajele insumeazază 100%
    if (user.procentNecesitati + user.procentDorinte + user.procentEconomii != 100):
        raise ValueError("Suma procentelor trebuie să fie 100%.")

    # Verifică dacă venitul este pozitiv
    if user.venit <= 0:
        raise ValueError("Venitul trebuie să fie pozitiv.")
    
    user_dict = user.model_dump()
    users_collection.add(user_dict)

def get_user_by_id(user_id: str):
    """Obține un utilizator după ID și returnează conținutul documentului împreună cu ID-ul"""
    user_doc = users_collection.document(user_id).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        user_data['user_id'] = user_doc.id
        return user_data
    else:
        raise HTTPException(status_code=404, detail="User not found")

def get_all_users():
    """Obține și afișează toți utilizatorii din baza de date, inclusiv ID-urile documentelor"""
    all_users = users_collection.get()
    users_list = []
    for user_doc in all_users:
        user_data = user_doc.to_dict()
        user_data['user_id'] = user_doc.id
        users_list.append(user_data)
    return users_list

def get_user_by_email(email: str):
    """Obține un utilizator după email și returnează conținutul documentului împreună cu ID-ul"""
    query = users_collection.where("email", "==", email).get()
    for user_doc in query:
        user_data = user_doc.to_dict()
        user_data['user_id'] = user_doc.id
        return user_data
    return None

def update_user_by_id(user_id: str, user: User):
    """Actualizează datele unui utilizator"""
    
    # Verifică dacă procentajele insumeazază 100%
    if (user.procentNecesitati + user.procentDorinte + user.procentEconomii != 100):
        raise ValueError("Suma procentelor trebuie să fie 100%.")

    user_doc = users_collection.document(user_id).get()
    if user_doc.exists:
        # Verifică dacă există deja un utilizator cu același email și nu este utilizatorul curent
        existing_user = get_user_by_email(user.email)
        if existing_user and existing_user['user_id'] != user_id:
            raise ValueError("Un alt utilizator cu acest email există deja.")
        users_collection.document(user_id).update(user.model_dump())
    else:
        raise HTTPException(status_code=404, detail="User not found")

def delete_user_by_id(user_id: str):
    """Șterge un utilizator din Firestore"""

    # Import local pentru a evita importul circular
    from services.payment_service import get_payments_by_user, delete_payment_by_id

    # Verifică dacă utilizatorul are plăți asociate și le șterge
    user_payments = get_payments_by_user(user_id)
    for payment_doc in user_payments:
        delete_payment_by_id(payment_doc['plata_id'])

    user_doc = users_collection.document(user_id).get()
    if user_doc.exists:
        users_collection.document(user_id).delete()
    else:
        raise HTTPException(status_code=404, detail="User not found")
