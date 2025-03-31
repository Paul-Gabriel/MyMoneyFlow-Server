from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BaseModel):
    nume: str
    prenume: str
    email: EmailStr
    parola: str
    venit: int = Field(ge=0, description="Venitul trebuie să fie pozitiv")
    procent_necesitati: int = Field(ge=0, le=100, description="Procent între 0 și 100")
    procent_dorinte: int = Field(ge=0, le=100, description="Procent între 0 și 100")
    procent_economii: int = Field(ge=0, le=100, description="Procent între 0 și 100")

    def to_dict(self):
        """Convertim obiectul User într-un dicționar pentru Firebase"""
        return self.dict()

    @staticmethod
    def from_dict(data):
        """Reconstruim un obiect User dintr-un dicționar"""
        return User(**data)
