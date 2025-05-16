from datetime import datetime

class HistoriqueCarriere:
    def __init__(self):
        self.changements = []

    def ajouter_changement(self, type_changement, ancienne_valeur, nouvelle_valeur):
        changement = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'type': type_changement,
            'ancienne_valeur': ancienne_valeur,
            'nouvelle_valeur': nouvelle_valeur
        }
        self.changements.append(changement)

    def to_dict(self):
        return {'changements': self.changements}

    @classmethod
    def from_dict(cls, data):
        historique = cls()
        historique.changements = data.get('changements', [])
        return historique