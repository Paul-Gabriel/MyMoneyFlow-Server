from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Plata(BaseModel):
    # id: Optional[int] = None  # Poate fi generat automat
    user_id: str  # ID-ul utilizatorului care face plata
    suma: float = Field(gt=0, description="Suma trebuie să fie mai mare decât 0")
    categorie: str
    descriere: str
    data: datetime = Field(default_factory=datetime.utcnow)  # Data implicită = momentul curent

    def to_dict(self):
        """Convertim obiectul Plata într-un dicționar pentru Firebase"""
        return {
            # "id": self.id,
            "user_id": self.user_id,
            "suma": self.suma,
            "categorie": self.categorie,
            "descriere": self.descriere,
            "data": self.data.isoformat()  # Stocăm data ca string ISO 8601
        }

    @staticmethod
    def from_dict(data):
        """Reconstruim un obiect Plata dintr-un dicționar"""
        data["data"] = datetime.fromisoformat(data["data"])  # Convertim string-ul ISO în datetime
        return Plata(**data)
