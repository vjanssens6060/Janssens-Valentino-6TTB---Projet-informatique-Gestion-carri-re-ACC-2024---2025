class Reglage:
    def __init__(self, voiture, circuit, aileron_avant=0, aileron_arriere=0, 
                 pression_pneus_av_gauche=0, pression_pneus_av_droit=0,
                 pression_pneus_ar_gauche=0, pression_pneus_ar_droit=0,
                 suspension_avant=0, suspension_arriere=0, hauteur_caisse=0,
                 diff=0, rapports_rapides=0):
        self.voiture = voiture  # Nom de la voiture (par exemple, "Ferrari 488")
        self.circuit = circuit  # Nom du circuit (par exemple, "Monza")
        self.aileron_avant = aileron_avant  # Réglage de l'aileron avant
        self.aileron_arriere = aileron_arriere  # Réglage de l'aileron arrière
        self.pression_pneus_av_gauche = pression_pneus_av_gauche  # Pression pneu avant gauche
        self.pression_pneus_av_droit = pression_pneus_av_droit  # Pression pneu avant droit
        self.pression_pneus_ar_gauche = pression_pneus_ar_gauche  # Pression pneu arrière gauche
        self.pression_pneus_ar_droit = pression_pneus_ar_droit  # Pression pneu arrière droit
        self.suspension_avant = suspension_avant  # Réglage de la suspension avant
        self.suspension_arriere = suspension_arriere  # Réglage de la suspension arrière
        self.hauteur_caisse = hauteur_caisse  # Hauteur de caisse
        self.diff = diff  # Différentiel
        self.rapports_rapides = rapports_rapides  # Réglage des rapports de boîte

    def to_dict(self):
        return {
            "voiture": self.voiture,
            "circuit": self.circuit,
            "aileron_avant": self.aileron_avant,
            "aileron_arriere": self.aileron_arriere,
            "pression_pneus_av_gauche": self.pression_pneus_av_gauche,
            "pression_pneus_av_droit": self.pression_pneus_av_droit,
            "pression_pneus_ar_gauche": self.pression_pneus_ar_gauche,
            "pression_pneus_ar_droit": self.pression_pneus_ar_droit,
            "suspension_avant": self.suspension_avant,
            "suspension_arriere": self.suspension_arriere,
            "hauteur_caisse": self.hauteur_caisse,
            "diff": self.diff,
            "rapports_rapides": self.rapports_rapides
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            voiture=data.get('voiture', "Voiture inconnue"),
            circuit=data.get('circuit', "Circuit inconnu"),
            aileron_avant=data.get('aileron_avant', 0),
            aileron_arriere=data.get('aileron_arriere', 0),
            pression_pneus_av_gauche=data.get('pression_pneus_av_gauche', 0),
            pression_pneus_av_droit=data.get('pression_pneus_av_droit', 0),
            pression_pneus_ar_gauche=data.get('pression_pneus_ar_gauche', 0),
            pression_pneus_ar_droit=data.get('pression_pneus_ar_droit', 0),
            suspension_avant=data.get('suspension_avant', 0),
            suspension_arriere=data.get('suspension_arriere', 0),
            hauteur_caisse=data.get('hauteur_caisse', 0),
            diff=data.get('diff', 0),
            rapports_rapides=data.get('rapports_rapides', 0)
        )

    def afficher_reglages(self):
        print(f"Réglages pour la voiture {self.voiture} sur le circuit {self.circuit} :")
        print(f"Aileron avant : {self.aileron_avant}")
        print(f"Aileron arrière : {self.aileron_arriere}")
        print(f"Pression des pneus avant gauche : {self.pression_pneus_av_gauche}")
        print(f"Pression des pneus avant droit : {self.pression_pneus_av_droit}")
        print(f"Pression des pneus arrière gauche : {self.pression_pneus_ar_gauche}")
        print(f"Pression des pneus arrière droit : {self.pression_pneus_ar_droit}")
        print(f"Suspension avant : {self.suspension_avant}")
        print(f"Suspension arrière : {self.suspension_arriere}")
        print(f"Hauteur de caisse : {self.hauteur_caisse}")
        print(f"Différentiel : {self.diff}")
        print(f"Rapports rapides : {self.rapports_rapides}")
