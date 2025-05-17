import uuid  # Pour générer des identifiants uniques

class Course:
    def __init__(self, circuit, classement, meilleur_temps, type_course, duree_ou_tours=None, voiture_utilisee=None, date=None, meteo=None, strategie=None):
        self.id = str(uuid.uuid4())  # Identifiant unique pour chaque course
        self.circuit = circuit
        self.classement = classement  # Classement final
        self.meilleur_temps = meilleur_temps  # Meilleur tour (temps au tour)
        self.type_course = type_course  # 'qualif', 'sprint', 'endurance'
        self.duree_ou_tours = duree_ou_tours  # Durée ou nombre de tours
        self.voiture_utilisee = voiture_utilisee  # Voiture utilisée
        self.date = date  # Date de la course
        self.meteo = meteo  # Conditions météo
        self.strategie = strategie  # Stratégie utilisée (ex : arrêts, pneus)

    def to_dict(self):
        return {
            "id": self.id,
            "circuit": self.circuit,
            "classement": self.classement,
            "meilleur_temps": self.meilleur_temps,
            "type_course": self.type_course,
            "duree_ou_tours": self.duree_ou_tours,
            "voiture_utilisee": self.voiture_utilisee,
            "date": self.date,
            "meteo": self.meteo,
            "strategie": self.strategie
        }

    @classmethod
    def from_dict(cls, data):
        course = cls(
            data.get('circuit'),
            data.get('classement'),
            data.get('meilleur_temps'),
            data.get('type_course'),
            data.get('duree_ou_tours'),
            data.get('voiture_utilisee'),
            data.get('date'),
            data.get('meteo'),
            data.get('strategie')
        )
        course.id = data.get('id', str(uuid.uuid4()))  # Récupérer l'ID ou en générer un nouveau
        return course
