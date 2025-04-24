import tkinter as tk
from tkinter import ttk  # Pour le widget Notebook (onglets)
import customtkinter as ctk
from carriere import Carriere
from reglage import Reglage
from course import Course
from statistiques import Statistiques
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuration du thème et des couleurs
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Configuration de la fenêtre
        self.title("Gestionnaire de Carrière - ACC")
        self.geometry("1000x800")
        
        # Styles personnalisés
        self.configure(fg_color="#1a1a1a")
        
        # Configuration des onglets
        self.tabview = ctk.CTkTabview(self)
        self.tabview.configure(
            fg_color="#2b2b2b",
            segmented_button_fg_color="#1f6aa5",
            segmented_button_selected_color="#144870",
            segmented_button_unselected_color="#1f6aa5"
        )
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Charger la carrière existante ou en créer une nouvelle
        self.carriere = Carriere.charger() or Carriere("Nom par défaut", "Équipe par défaut", "Voiture par défaut")

        # Création du Tabview (onglets)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Ajout des onglets
        self.reglages_tab = self.tabview.add("Réglages")
        self.carriere_tab = self.tabview.add("Carrière")
        self.courses_tab = self.tabview.add("Courses")
        self.stats_tab = self.tabview.add("Statistiques")

        # Création du contenu des onglets
        self.creer_onglet_reglages()
        self.creer_onglet_carriere()
        self.creer_onglet_courses()
        self.creer_onglet_statistiques()

    def creer_onglet_reglages(self):
        """Crée le contenu de l'onglet Réglages."""
        ctk.CTkLabel(self.reglages_tab, text="Réglages :", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.voiture_label = ctk.CTkLabel(self.reglages_tab, text="Voiture :", font=("Arial", 14))
        self.voiture_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.voiture_entry = ctk.CTkEntry(self.reglages_tab, width=200)
        self.voiture_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.circuit_label = ctk.CTkLabel(self.reglages_tab, text="Circuit :", font=("Arial", 14))
        self.circuit_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.circuit_entry = ctk.CTkEntry(self.reglages_tab, width=200)
        self.circuit_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.aileron_avant_label = ctk.CTkLabel(self.reglages_tab, text="Aileron Avant :", font=("Arial", 14))
        self.aileron_avant_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.aileron_avant_entry = ctk.CTkEntry(self.reglages_tab, width=200)
        self.aileron_avant_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.aileron_arriere_label = ctk.CTkLabel(self.reglages_tab, text="Aileron Arrière :", font=("Arial", 14))
        self.aileron_arriere_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.aileron_arriere_entry = ctk.CTkEntry(self.reglages_tab, width=200)
        self.aileron_arriere_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.pression_av_gauche_label = ctk.CTkLabel(self.reglages_tab, text="Pression Pneu Avant Gauche :", font=("Arial", 14))
        self.pression_av_gauche_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.pression_av_gauche_entry = ctk.CTkEntry(self.reglages_tab, width=200)
        self.pression_av_gauche_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        self.pression_av_droit_label = ctk.CTkLabel(self.reglages_tab, text="Pression Pneu Avant Droit :", font=("Arial", 14))
        self.pression_av_droit_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.pression_av_droit_entry = ctk.CTkEntry(self.reglages_tab, width=200)
        self.pression_av_droit_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        self.pression_ar_gauche_label = ctk.CTkLabel(self.reglages_tab, text="Pression Pneu Arrière Gauche :", font=("Arial", 14))
        self.pression_ar_gauche_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.pression_ar_gauche_entry = ctk.CTkEntry(self.reglages_tab, width=200)
        self.pression_ar_gauche_entry.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

        self.pression_ar_droit_label = ctk.CTkLabel(self.reglages_tab, text="Pression Pneu Arrière Droit :", font=("Arial", 14))
        self.pression_ar_droit_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")
        self.pression_ar_droit_entry = ctk.CTkEntry(self.reglages_tab, width=200)
        self.pression_ar_droit_entry.grid(row=8, column=1, padx=10, pady=5, sticky="ew")

        self.suspension_avant_label = ctk.CTkLabel(self.reglages_tab, text="Suspension Avant :", font=("Arial", 14))
        self.suspension_avant_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.suspension_avant_entry = ctk.CTkEntry(self.reglages_tab, width=200)
        self.suspension_avant_entry.grid(row=9, column=1, padx=10, pady=5, sticky="ew")

        self.suspension_arriere_label = ctk.CTkLabel(self.reglages_tab, text="Suspension Arrière :", font=("Arial", 14))
        self.suspension_arriere_label.grid(row=10, column=0, padx=10, pady=5, sticky="w")
        self.suspension_arriere_entry = ctk.CTkEntry(self.reglages_tab, width=200)
        self.suspension_arriere_entry.grid(row=10, column=1, padx=10, pady=5, sticky="ew")

        self.hauteur_caisse_label = ctk.CTkLabel(self.reglages_tab, text="Hauteur de Caisse :", font=("Arial", 14))
        self.hauteur_caisse_label.grid(row=11, column=0, padx=10, pady=5, sticky="w")
        self.hauteur_caisse_entry = ctk.CTkEntry(self.reglages_tab, width=200)
        self.hauteur_caisse_entry.grid(row=11, column=1, padx=10, pady=5, sticky="ew")

        button_style = {
            "fg_color": "#1f6aa5",
            "hover_color": "#144870",
            "border_width": 2,
            "border_color": "#2b2b2b",
            "corner_radius": 8,
            "font": ("Arial", 12)
        }

        # Exemple d'utilisation
        self.add_reglage_button = ctk.CTkButton(
            self.reglages_tab,
            text="Ajouter Réglage",
            command=self.ajouter_reglage,
            **button_style
        )
        self.add_reglage_button.grid(row=12, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.reglages_textbox = tk.Text(self.reglages_tab, height=10, wrap="word", bg="#2b2b2b", fg="white", font=("Arial", 12))
        self.reglages_textbox.grid(row=13, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.afficher_reglages_existants()

    def creer_onglet_carriere(self):
        """Crée le contenu de l'onglet Carrière."""
        ctk.CTkLabel(self.carriere_tab, text="Carrière :", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.nom_pilote_label = ctk.CTkLabel(self.carriere_tab, text="Nom du Pilote :", font=("Arial", 14))
        self.nom_pilote_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.nom_pilote_entry = ctk.CTkEntry(self.carriere_tab, width=200)
        self.nom_pilote_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.equipe_label = ctk.CTkLabel(self.carriere_tab, text="Équipe :", font=("Arial", 14))
        self.equipe_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.equipe_entry = ctk.CTkEntry(self.carriere_tab, width=200)
        self.equipe_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.voiture_label = ctk.CTkLabel(self.carriere_tab, text="Voiture Préférée :", font=("Arial", 14))
        self.voiture_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.voiture_entry = ctk.CTkEntry(self.carriere_tab, width=200)
        self.voiture_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.save_button = ctk.CTkButton(self.carriere_tab, text="Sauvegarder Carrière", command=self.sauvegarder_carriere, fg_color="#1f6aa5", hover_color="#144870")
        self.save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def creer_onglet_courses(self):
        """Crée le contenu de l'onglet Courses."""
        ctk.CTkLabel(self.courses_tab, text="Courses :", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.circuit_label = ctk.CTkLabel(self.courses_tab, text="Circuit:")
        self.circuit_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.circuit_entry = ctk.CTkEntry(self.courses_tab)
        self.circuit_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.classement_label = ctk.CTkLabel(self.courses_tab, text="Classement:")
        self.classement_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.classement_entry = ctk.CTkEntry(self.courses_tab)
        self.classement_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.duree_label = ctk.CTkLabel(self.courses_tab, text="Durée ou Tours:")
        self.duree_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.duree_entry = ctk.CTkEntry(self.courses_tab)
        self.duree_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.meilleur_temps_label = ctk.CTkLabel(self.courses_tab, text="Meilleur Temps (mm:ss.ms):")
        self.meilleur_temps_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.meilleur_temps_entry = ctk.CTkEntry(self.courses_tab)
        self.meilleur_temps_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        self.date_label = ctk.CTkLabel(self.courses_tab, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.date_entry = ctk.CTkEntry(self.courses_tab)
        self.date_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

        self.meteo_label = ctk.CTkLabel(self.courses_tab, text="Météo:")
        self.meteo_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.meteo_entry = ctk.CTkEntry(self.courses_tab)
        self.meteo_entry.grid(row=6, column=1, padx=10, pady=5, sticky="ew")

        self.strategie_label = ctk.CTkLabel(self.courses_tab, text="Stratégie:")
        self.strategie_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.strategie_entry = ctk.CTkEntry(self.courses_tab)
        self.strategie_entry.grid(row=7, column=1, padx=10, pady=5, sticky="ew")

        self.add_course_button = ctk.CTkButton(self.courses_tab, text="Ajouter Course", command=self.ajouter_course)
        self.add_course_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.courses_textbox = tk.Text(self.courses_tab, height=10, wrap="word", bg="#2b2b2b", fg="white", font=("Arial", 12))
        self.courses_textbox.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.afficher_courses_existantes()

    def creer_onglet_statistiques(self):
        """Crée le contenu de l'onglet Statistiques."""
        ctk.CTkLabel(self.stats_tab, text="Statistiques :", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Configuration du cadre sombre pour afficher les statistiques
        self.stats_textbox = tk.Text(self.stats_tab, height=15, wrap="word", state="disabled", bg="#2b2b2b", fg="white", font=("Arial", 12))
        self.stats_textbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.update_stats_button = ctk.CTkButton(self.stats_tab, text="Mettre à jour les statistiques", command=self.afficher_statistiques)
        self.update_stats_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.graph_button = ctk.CTkButton(self.stats_tab, text="Afficher le graphique de progression", command=self.afficher_graphique)
        self.graph_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def ajouter_reglage(self):
        """Ajoute un réglage pour une voiture sur un circuit donné."""
        voiture = self.voiture_entry.get()
        circuit = self.circuit_entry.get()
        try:
            aileron_avant = float(self.aileron_avant_entry.get())
            aileron_arriere = float(self.aileron_arriere_entry.get())
        except ValueError:
            print("⚠️ Veuillez entrer des valeurs numériques pour les ailerons.")
            return

        # Valeurs par défaut pour les autres paramètres
        pression_pneus = 25  
        suspension = "Moyenne"  
        diff = 1  
        rapports_rapides = 4  

        reglage = Reglage(voiture, circuit, aileron_avant, aileron_arriere, pression_pneus, suspension, diff, rapports_rapides)

        # Vérification que la carrière est bien définie
        if not self.carriere:
            self.carriere = Carriere("Nom par défaut", "Équipe par défaut", "Voiture par défaut")

        self.carriere.ajouter_reglage(reglage)
        self.afficher_reglages_existants()
        print(f"✅ Réglage ajouté pour {voiture} sur {circuit}")

    def sauvegarder_carriere(self):
        """Sauvegarde la carrière actuelle avec les informations saisies."""
        nom_pilote = self.nom_pilote_entry.get()
        equipe = self.equipe_entry.get()
        voiture = self.voiture_entry.get()

        # Vérifier que self.carriere existe
        if not self.carriere:
            self.carriere = Carriere(nom_pilote, equipe, voiture)
        else:
            self.carriere.nom_pilote = nom_pilote
            self.carriere.equipe = equipe
            self.carriere.voiture_preferee = voiture

        self.carriere.enregistrer()
        print("✅ Carrière sauvegardée avec succès !")

    def afficher_reglages_existants(self):
        """Affiche les réglages existants dans un format plus lisible."""
        self.reglages_textbox.delete("1.0", tk.END)
        self.reglages_textbox.tag_configure("title", font=("Arial", 12, "bold"))
        self.reglages_textbox.tag_configure("value", font=("Arial", 11))
        
        for reglage in self.carriere.reglages:
            # Titre du réglage
            self.reglages_textbox.insert(tk.END, f"\n📝 Réglage pour {reglage.voiture} sur {reglage.circuit}\n", "title")
            self.reglages_textbox.insert(tk.END, "━" * 50 + "\n", "value")
            
            # Aérodynamique
            self.reglages_textbox.insert(tk.END, "🛩️ Aérodynamique:\n", "title")
            self.reglages_textbox.insert(tk.END, f"  • Aileron avant : {reglage.aileron_avant}\n", "value")
            self.reglages_textbox.insert(tk.END, f"  • Aileron arrière : {reglage.aileron_arriere}\n", "value")
            
            # Pressions des pneus
            self.reglages_textbox.insert(tk.END, "🚗 Pressions des pneus:\n", "title")
            self.reglages_textbox.insert(tk.END, f"  • Avant gauche : {reglage.pression_pneus_av_gauche} PSI\n", "value")
            self.reglages_textbox.insert(tk.END, f"  • Avant droit : {reglage.pression_pneus_av_droit} PSI\n", "value")
            self.reglages_textbox.insert(tk.END, f"  • Arrière gauche : {reglage.pression_pneus_ar_gauche} PSI\n", "value")
            self.reglages_textbox.insert(tk.END, f"  • Arrière droit : {reglage.pression_pneus_ar_droit} PSI\n", "value")
            
            # Suspensions
            self.reglages_textbox.insert(tk.END, "🔧 Suspensions:\n", "title")
            self.reglages_textbox.insert(tk.END, f"  • Avant : {reglage.suspension_avant}\n", "value")
            self.reglages_textbox.insert(tk.END, f"  • Arrière : {reglage.suspension_arriere}\n", "value")
            self.reglages_textbox.insert(tk.END, f"  • Hauteur de caisse : {reglage.hauteur_caisse}mm\n", "value")
            
            self.reglages_textbox.insert(tk.END, "\n" + "═" * 50 + "\n", "value")

    def afficher_courses_existantes(self):
        """Affiche les courses existantes avec un meilleur formatage."""
        self.courses_textbox.delete("1.0", tk.END)
        self.courses_textbox.tag_configure("title", font=("Arial", 12, "bold"))
        self.courses_textbox.tag_configure("value", font=("Arial", 11))
        self.courses_textbox.tag_configure("separator", font=("Arial", 11), foreground="#666666")
        
        for course in self.carriere.courses:
            # En-tête de la course
            self.courses_textbox.insert(tk.END, f"\n🏁 Course sur {course.circuit}\n", "title")
            self.courses_textbox.insert(tk.END, "━" * 50 + "\n", "separator")
            
            # Informations principales
            self.courses_textbox.insert(tk.END, "📊 Résultats:\n", "title")
            self.courses_textbox.insert(tk.END, f"  • Classement : {course.classement}ème\n", "value")
            self.courses_textbox.insert(tk.END, f"  • Meilleur temps : {course.meilleur_temps}\n", "value")
            
            # Détails de la course
            self.courses_textbox.insert(tk.END, "🏎️ Détails:\n", "title")
            self.courses_textbox.insert(tk.END, f"  • Type : {course.type_course}\n", "value")
            self.courses_textbox.insert(tk.END, f"  • Durée/Tours : {course.duree_ou_tours}\n", "value")
            self.courses_textbox.insert(tk.END, f"  • Voiture : {course.voiture_utilisee}\n", "value")
            
            # Conditions
            if course.date or course.meteo:
                self.courses_textbox.insert(tk.END, "🌤️ Conditions:\n", "title")
                if course.date:
                    self.courses_textbox.insert(tk.END, f"  • Date : {course.date}\n", "value")
                if course.meteo:
                    self.courses_textbox.insert(tk.END, f"  • Météo : {course.meteo}\n", "value")
            
            self.courses_textbox.insert(tk.END, "\n" + "═" * 50 + "\n", "separator")

    def ajouter_course(self):
        """Ajoute une course avec les informations saisies."""
        circuit = self.circuit_entry.get()
        classement = self.classement_entry.get()
        meilleur_temps = self.meilleur_temps_entry.get()
        type_course = self.voiture_entry.get()  # Exemple : type de course
        duree_ou_tours = self.duree_entry.get()
        voiture_utilisee = self.voiture_entry.get()

        # Créer une instance de Course
        course = Course(circuit, classement, meilleur_temps, type_course, duree_ou_tours, voiture_utilisee)

        # Vérification que la carrière est bien définie
        if not self.carriere:
            self.carriere = Carriere("Nom par défaut", "Équipe par défaut", "Voiture par défaut")

        self.carriere.ajouter_course(course)
        self.afficher_courses_existantes()  # Met à jour l'affichage des courses
        print(f"✅ Course ajoutée : {circuit} - {classement} - {meilleur_temps} - {duree_ou_tours} - {voiture_utilisee}")

    def afficher_statistiques(self):
        """Affiche les statistiques avec un meilleur formatage."""
        if not self.carriere:
            self.stats_textbox.config(state="normal")
            self.stats_textbox.delete("1.0", tk.END)
            self.stats_textbox.insert(tk.END, "❌ Aucune carrière chargée.")
            self.stats_textbox.config(state="disabled")
            return

        self.stats_textbox.config(state="normal")
        self.stats_textbox.delete("1.0", tk.END)
        
        # Configuration des styles
        self.stats_textbox.tag_configure("header", font=("Arial", 14, "bold"))
        self.stats_textbox.tag_configure("section", font=("Arial", 12, "bold"))
        self.stats_textbox.tag_configure("data", font=("Arial", 11))
        
        # En-tête
        self.stats_textbox.insert(tk.END, f"📊 Statistiques de {self.carriere.nom_pilote}\n", "header")
        self.stats_textbox.insert(tk.END, "━" * 50 + "\n\n")
        
        # Statistiques générales
        self.stats_textbox.insert(tk.END, "🏆 Résultats généraux:\n", "section")
        victoires = sum(1 for course in self.carriere.courses if self._convertir_classement(course.classement) == 1)
        podiums = sum(1 for course in self.carriere.courses if self._convertir_classement(course.classement) <= 3)
        courses_total = len(self.carriere.courses)
        
        self.stats_textbox.insert(tk.END, f"  • Courses disputées : {courses_total}\n", "data")
        self.stats_textbox.insert(tk.END, f"  • Victoires : {victoires} ({(victoires/courses_total*100):.1f}%)\n", "data")
        self.stats_textbox.insert(tk.END, f"  • Podiums : {podiums} ({(podiums/courses_total*100):.1f}%)\n\n", "data")
        
        # Meilleurs temps par circuit
        self.stats_textbox.insert(tk.END, "⏱️ Meilleurs temps par circuit:\n", "section")
        meilleurs_temps = {}
        for course in self.carriere.courses:
            temps = self._convertir_temps(course.meilleur_temps)
            if temps and (course.circuit not in meilleurs_temps or temps < meilleurs_temps[course.circuit]):
                meilleurs_temps[course.circuit] = temps
        
        for circuit, temps in meilleurs_temps.items():
            self.stats_textbox.insert(tk.END, f"  • {circuit}: {temps:.3f}s\n", "data")
        
        self.stats_textbox.config(state="disabled")

    def afficher_graphique(self):
        """Affiche un graphique montrant l'évolution des performances."""
        if not self.carriere or not self.carriere.courses:
            print("⚠️ Aucune donnée disponible pour afficher le graphique.")
            return

        # Préparer les données pour le graphique
        circuits = [course.circuit for course in self.carriere.courses]
        temps_au_tour = [self._convertir_temps(course.meilleur_temps) for course in self.carriere.courses]
        classements = [self._convertir_classement(course.classement) for course in self.carriere.courses]

        # Créer le graphique
        fig, ax1 = plt.subplots()

        # Graphique des temps au tour
        ax1.set_xlabel("Courses (par circuit)")
        ax1.set_ylabel("Temps au tour (secondes)", color="tab:blue")
        ax1.plot(circuits, temps_au_tour, label="Temps au tour", color="tab:blue", marker="o")
        ax1.tick_params(axis="y", labelcolor="tab:blue")

        # Ajouter un second axe pour les classements
        ax2 = ax1.twinx()
        ax2.set_ylabel("Classement", color="tab:red")
        ax2.plot(circuits, classements, label="Classement", color="tab:red", marker="x")
        ax2.tick_params(axis="y", labelcolor="tab:red")

        # Ajouter un titre et une légende
        fig.suptitle("Évolution des performances")
        fig.tight_layout()

        # Afficher le graphique dans une nouvelle fenêtre Tkinter
        graph_window = tk.Toplevel(self)
        graph_window.title("Graphique de progression")
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _convertir_classement(self, classement):
        """Convertit le classement en entier, ou retourne une valeur par défaut."""
        try:
            return int(classement)
        except (ValueError, TypeError):
            return -1  # Valeur par défaut pour les classements invalides

    def _convertir_temps(self, temps):
        """Convertit le temps en float, ou retourne None si invalide."""
        try:
            return float(temps)
        except (ValueError, TypeError):
            return None  # Retourne None si le temps n'est pas convertible

# Lancer l'application
if __name__ == "__main__":
    app = Application()  # Plus besoin de root
    app.mainloop()  # Lancement de l'UI
