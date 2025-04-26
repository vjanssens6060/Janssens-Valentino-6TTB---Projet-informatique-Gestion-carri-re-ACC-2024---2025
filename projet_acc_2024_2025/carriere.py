import json
import os  # Ajout de l'importation du module os
from reglage import Reglage
from course import Course

class Carriere:
    def __init__(self, nom_pilote, equipe, voiture_preferee):
        self.nom_pilote = nom_pilote
        self.equipe = equipe
        self.voiture_preferee = voiture_preferee
        self.courses = []  # Liste des courses auxquelles le pilote a participé
        self.reglages = []  # Liste des réglages des voitures

    def ajouter_course(self, course):
        """Ajoute une course à la liste des courses."""
        self.courses.append(course)

    def ajouter_reglage(self, reglage):
        """Ajoute un réglage à la liste des réglages."""
        if not hasattr(self, 'reglages'):
            self.reglages = []
        self.reglages.append(reglage)

    def enregistrer(self):
        data = {
            "nom_pilote": self.nom_pilote,
            "equipe": self.equipe,
            "voiture_preferee": self.voiture_preferee,
            "courses": [course.to_dict() for course in self.courses],
            "reglages": [reglage.to_dict() for reglage in self.reglages]
        }
        os.makedirs('data', exist_ok=True)
        with open('data/carriere_data.json', 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def charger(cls):
        """Charge les données depuis le fichier JSON."""
        try:
            with open('data/carriere_data.json', 'r') as f:
                data = json.load(f)
                carriere = cls(
                    data.get("nom_pilote", "Pilote inconnu"),
                    data.get("equipe", "Équipe inconnue"),
                    data.get("voiture_preferee", "Voiture inconnue")
                )
                
                # Initialisation des listes
                carriere.courses = []
                carriere.reglages = []
                
                # Chargement des courses
                for course_data in data.get("courses", []):
                    course = Course.from_dict(course_data)
                    carriere.courses.append(course)
                
                # Chargement des réglages
                for reglage_data in data.get("reglages", []):
                    reglage = Reglage.from_dict(reglage_data)
                    carriere.reglages.append(reglage)
                
                return carriere
        except FileNotFoundError:
            return None

    def modifier_course(self, course_id, nouvelles_donnees):
        """Modifie une course existante."""
        for course in self.courses:
            if course.id == course_id:
                for key, value in nouvelles_donnees.items():
                    if hasattr(course, key):
                        setattr(course, key, value)
                return True
        return False

    def supprimer_reglage(self, index):
        """Supprime un réglage à partir de son index."""
        if 0 <= index < len(self.reglages):
            del self.reglages[index]
            self.enregistrer()
            return True
        return False
    
    def supprimer_course(self, course_id):
        """Supprime une course existante."""
        self.courses = [course for course in self.courses if course.id != course_id]
        self.enregistrer()