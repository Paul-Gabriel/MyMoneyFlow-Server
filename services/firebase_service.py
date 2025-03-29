from api.dependencies import get_firestore

db = get_firestore()

def get_collection(collection_name: str):
    """Returnează referința către o colecție din Firestore"""
    return db.collection(collection_name)
