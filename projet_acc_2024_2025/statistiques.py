class Statistiques:
    def __init__(self, carriere):
        self.carriere = carriere

    def afficher_statistiques(self):
        total_courses = len(self.carriere.courses)
        victoires = sum(1 for course in self.carriere.courses if course.classement == 1)
        podiums = sum(1 for course in self.carriere.courses if course.classement <= 3)
        abandons = sum(1 for course in self.carriere.courses if course.classement == 0)  # Classement 0 = abandon
        meilleurs_temps = [course.meilleur_temps for course in self.carriere.courses if course.meilleur_temps]
        temps_moyen = sum(float(t) for t in meilleurs_temps) / len(meilleurs_temps) if meilleurs_temps else 0

        # Calcul du meilleur temps au tour par circuit
        meilleur_temps_par_circuit = {}
        for course in self.carriere.courses:
            circuit = course.circuit
            temps = float(course.meilleur_temps) if course.meilleur_temps else None
            if circuit not in meilleur_temps_par_circuit or (temps and temps < meilleur_temps_par_circuit[circuit]):
                meilleur_temps_par_circuit[circuit] = temps

        print(f"Statistiques pour {self.carriere.nom_pilote} :")
        print(f"Nombre total de courses : {total_courses}")
        print(f"Victoires : {victoires}")
        print(f"Podiums : {podiums}")
        print(f"Abandons : {abandons}")
        print(f"Temps moyen : {temps_moyen:.2f} secondes")
        print("Meilleur temps au tour par circuit :")
        for circuit, temps in meilleur_temps_par_circuit.items():
            print(f"  - {circuit} : {temps:.2f} secondes" if temps else f"  - {circuit} : Non spécifié")

    def calculer_statistiques_avancees(self):
        total_courses = len(self.carriere.courses)
        victoires = sum(1 for course in self.carriere.courses if course.classement == 1)
        ratio_victoires = victoires / total_courses if total_courses > 0 else 0
        moyenne_classement = sum(course.classement for course in self.carriere.courses if isinstance(course.classement, int)) / total_courses if total_courses > 0 else 0

        return {
            "total_courses": total_courses,
            "victoires": victoires,
            "ratio_victoires": ratio_victoires,
            "moyenne_classement": moyenne_classement
        }