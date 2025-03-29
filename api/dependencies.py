import firebase_admin
from firebase_admin import credentials, firestore
import os

def initialize_firebase():
    """Configurează Firebase la pornirea serverului"""
    if not firebase_admin._apps:  # Evită inițializări multiple
        project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        cred = credentials.Certificate(os.path.join(project_path, 'de-testat-firebase-adminsdk-fbsvc-62679032fd.json'))#my-money-flow-4fd41-firebase-adminsdk-fbsvc-ea9a5a5f5c.json
        firebase_admin.initialize_app(cred)

def get_firestore():
    """Returnează clientul Firestore"""
    initialize_firebase()
    return firestore.client()

