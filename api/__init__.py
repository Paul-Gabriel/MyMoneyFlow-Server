from fastapi import FastAPI
from api.routes import user_routes, payment_routes
from api.dependencies import get_firestore

# Inițializăm aplicația FastAPI
app = FastAPI(title="MyMoneyFlow API", version="1.0")

# Configurăm Firebase (dacă e necesar)
get_firestore()

# Adăugăm rutele API
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(payment_routes.router, prefix="/payments", tags=["Payments"])
