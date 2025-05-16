import os
import json
import uuid
from datetime import datetime
from reglage import Reglage
from course import Course
from historique import HistoriqueCarriere
from objectif import Objectif

class Carriere:
    def __init__(self, nom_pilote, equipe, voiture_preferee):
        self.id = str(uuid.uuid4())
        self.nom_pilote = nom_pilote
        self.equipe = equipe
        self._voiture_preferee = voiture_preferee
        self.courses = []
        self.reglages = []
        self.objectifs = []
        self.historique = HistoriqueCarriere()

    @property
    def voiture_preferee(self):
        return self._voiture_preferee

    @voiture_preferee.setter
    def voiture_preferee(self, nouvelle_voiture):
        if hasattr(self, '_voiture_preferee'):
            self.historique.ajouter_changement(
                'voiture',
                self._voiture_preferee,
                nouvelle_voiture
            )
        self._voiture_preferee = nouvelle_voiture

    def ajouter_course(self, course):
        """Ajoute une course à la liste des courses."""
        self.courses.append(course)

    def ajouter_reglage(self, reglage):
        """Ajoute un réglage à la liste des réglages."""
        if not hasattr(self, 'reglages'):
            self.reglages = []
        self.reglages.append(reglage)

    def ajouter_objectif(self, objectif):
        """Ajoute un objectif à la carrière."""
        self.objectifs.append(objectif)

    def enregistrer(self):
        """Enregistre les données de la carrière dans un fichier JSON."""
        data = {
            "nom_pilote": self.nom_pilote,
            "equipe": self.equipe,
            "voiture_preferee": self.voiture_preferee,
            "courses": [course.to_dict() for course in self.courses],
            "reglages": [reglage.to_dict() for reglage in self.reglages],
            "historique": self.historique.to_dict() if hasattr(self, 'historique') else {},
            "objectifs": [objectif.to_dict() for objectif in self.objectifs]
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
                carriere.objectifs = []
                
                # Chargement des courses
                for course_data in data.get("courses", []):
                    course = Course.from_dict(course_data)
                    carriere.courses.append(course)
                
                # Chargement des réglages
                for reglage_data in data.get("reglages", []):
                    reglage = Reglage.from_dict(reglage_data)
                    carriere.reglages.append(reglage)
                
                # Chargement des objectifs
                for objectif_data in data.get("objectifs", []):
                    objectif = Objectif.from_dict(objectif_data)
                    carriere.objectifs.append(objectif)
                
                return carriere
        except FileNotFoundError:
            return None

    def modifier_course(self, course_id, nouvelles_donnees):
        """Modifie une course existante."""
        for i, course in enumerate(self.courses):
            if course.id == course_id:
                # Mise à jour des attributs de la course
                course.circuit = nouvelles_donnees['circuit']
                course.classement = nouvelles_donnees['classement']
                course.meilleur_temps = nouvelles_donnees['meilleur_temps']
                course.date = nouvelles_donnees['date']
                course.meteo = nouvelles_donnees['meteo']
                course.strategie = nouvelles_donnees['strategie']
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

    def supprimer_objectif(self, index):
        """Supprime un objectif de la carrière."""
        if 0 <= index < len(self.objectifs):
            del self.objectifs[index]
            return True
        return False

    def verifier_objectifs(self):
        """Vérifie le statut des objectifs."""
        for objectif in self.objectifs:
            if objectif.statut != "En cours":
                continue

            valeur_actuelle = 0
            if objectif.type_objectif == "victoires":
                valeur_actuelle = sum(1 for course in self.courses 
                    if course.classement == "1" and course.date.startswith(objectif.saison))
            elif objectif.type_objectif == "podiums":
                valeur_actuelle = sum(1 for course in self.courses 
                    if int(course.classement) <= 3 and course.date.startswith(objectif.saison))

            if valeur_actuelle >= int(objectif.valeur_cible):
                objectif.statut = "Réussi"
            elif datetime.now().year > int(objectif.saison):
                objectif.statut = "Échoué"

    def to_dict(self):
        return {
            "id": self.id,
            "nom_pilote": self.nom_pilote,
            "equipe": self.equipe,
            "voiture_preferee": self.voiture_preferee,
            "courses": [course.to_dict() for course in self.courses],
            "reglages": [reglage.to_dict() for reglage in self.reglages],
            "objectifs": [obj.to_dict() for obj in self.objectifs],
            "historique": self.historique.to_dict() if hasattr(self, 'historique') else {}
        }

    @classmethod
    def from_dict(cls, data):
        carriere = cls(
            data.get("nom_pilote", "Pilote inconnu"),
            data.get("equipe", "Équipe inconnue"),
            data.get("voiture_preferee", "Voiture inconnue")
        )
        carriere.id = data.get("id", str(uuid.uuid4()))
        
        # Chargement des courses
        for course_data in data.get("courses", []):
            course = Course.from_dict(course_data)
            carriere.courses.append(course)
        
        # Chargement des réglages
        for reglage_data in data.get("reglages", []):
            reglage = Reglage.from_dict(reglage_data)
            carriere.reglages.append(reglage)

        # Chargement des objectifs
        for objectif_data in data.get("objectifs", []):
            objectif = Objectif.from_dict(objectif_data)
            carriere.objectifs.append(objectif)

        # Chargement de l'historique
        if "historique" in data:
            carriere.historique = HistoriqueCarriere.from_dict(data["historique"])
        
        return carriere

    @classmethod
    def charger_carrieres(cls):
        """Charge toutes les carrières depuis le fichier JSON."""
        try:
            with open('data/carrieres_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                carrieres = []
                for carriere_data in data.get("carrieres", []):
                    carriere = cls.from_dict(carriere_data)
                    carrieres.append(carriere)
                return carrieres, data.get("carriere_active")
        except FileNotFoundError:
            return [], None

    @classmethod
    def sauvegarder_carrieres(cls, carrieres, carriere_active=None):
        """Sauvegarde toutes les carrières dans le fichier JSON."""
        data = {
            "carrieres": [carriere.to_dict() for carriere in carrieres],
            "carriere_active": carriere_active.id if carriere_active else None
        }
        with open('data/carrieres_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)