from services.firebase_service import get_collection
from models.user import User

users_collection = get_collection("users")

def add_user(user: User):
    """Adaugă un utilizator în Firestore"""
    # Verifică dacă există deja un utilizator cu același email
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise ValueError("Un utilizator cu acest email există deja.")
    
    # Verifică dacă procentajele insumeazază 100%
    if user.procentNecesitati + user.procentDorinte + user.procentEconomii != 100:
        raise ValueError("Suma procentelor trebuie să fie 100%.")

    # # Obține toate documentele pentru a determina următorul ID
    # all_users = users_collection.get()
    # next_id = 0
    # if all_users:
    #     existing_ids = sorted(int(user.id) for user in all_users)
    #     for i, user_id in enumerate(existing_ids):
    #         if i != user_id:
    #             next_id = i
    #             break
    #     else:
    #         next_id = len(existing_ids)
    # user.id = next_id

    user_dict = user.model_dump()  # Pentru Pydantic v2
    users_collection.add(user_dict)

def get_user_by_id(user_id: str):
    """Obține un utilizator după ID și returnează conținutul documentului împreună cu ID-ul"""
    user_doc = users_collection.document(user_id).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        user_data['user_id'] = user_doc.id
        return user_data
    return None

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
    user_doc = users_collection.document(user_id).get()
    if user_doc.exists:
        users_collection.document(user_id).update(user.model_dump())
        return True
    return False

def delete_user_by_id(user_id: str):
    """Șterge un utilizator din Firestore"""
    user_doc = users_collection.document(user_id).get()
    if user_doc.exists:
        users_collection.document(user_id).delete()
        return True
    return False
