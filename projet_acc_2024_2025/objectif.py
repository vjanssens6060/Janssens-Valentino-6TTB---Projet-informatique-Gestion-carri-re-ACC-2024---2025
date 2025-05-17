from datetime import datetime

class Objectif:
    def __init__(self, description, type_objectif, valeur_cible, saison, statut="En cours"):
        self.description = description
        self.type_objectif = type_objectif  # "victoires", "podiums", "classement", "temps"
        self.valeur_cible = valeur_cible
        self.saison = saison
        self.statut = statut  # "En cours", "Réussi", "Échoué"
        self.date_creation = datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "description": self.description,
            "type_objectif": self.type_objectif,
            "valeur_cible": self.valeur_cible,
            "saison": self.saison,
            "statut": self.statut,
            "date_creation": self.date_creation
        }

    @classmethod
    def from_dict(cls, data):
        objectif = cls(
            data.get("description"),
            data.get("type_objectif"),
            data.get("valeur_cible"),
            data.get("saison"),
            data.get("statut", "En cours")
        )
        objectif.date_creation = data.get("date_creation", datetime.now().strftime("%Y-%m-%d"))
        return objectif