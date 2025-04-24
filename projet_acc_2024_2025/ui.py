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
        self.geometry("1200x900")  # Augmentez la largeur et la hauteur
        
        # Création d'un Canvas pour le défilement
        self.main_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main_frame, bg="#1a1a1a", highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self.main_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="#1a1a1a")

        # Configuration du Canvas et de la Scrollbar
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Placement du Canvas et de la Scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Charger la carrière existante ou en créer une nouvelle
        self.carriere = Carriere.charger() or Carriere("Nom par défaut", "Équipe par défaut", "Voiture par défaut")
        
        # Styles personnalisés
        self.configure(fg_color="#1a1a1a")
        
        # Définition des styles
        self.label_style = {
            "font": ("Helvetica", 14, "bold"),  # Augmentez la taille de la police
            "text_color": "#ffffff"
        }
        self.entry_style = {
            "font": ("Helvetica", 14),  # Augmentez la taille de la police
            "corner_radius": 6,
            "border_width": 2,
            "border_color": "#2b2b2b",
            "width": 300,  # Augmentez la largeur des champs
            "height": 40   # Augmentez la hauteur des champs
        }
        self.button_style = {
            "font": ("Helvetica", 14, "bold"),  # Augmentez la taille de la police
            "corner_radius": 8,
            "border_width": 2,
            "border_color": "#2b2b2b",
            "fg_color": "#1f6aa5",
            "hover_color": "#144870",
            "height": 50  # Augmentez la hauteur des boutons
        }
        
        # Configuration des onglets (un seul tabview)
        self.tabview = ctk.CTkTabview(self.scrollable_frame)
        self.tabview.configure(
            fg_color="#2b2b2b",
            segmented_button_fg_color="#1f6aa5",
            segmented_button_selected_color="#144870",
            segmented_button_unselected_color="#1f6aa5"
        )
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        # Ajout des onglets
        self.reglages_tab = self.tabview.add("⚙️ Réglages")
        self.carriere_tab = self.tabview.add("👤 Carrière")
        self.courses_tab = self.tabview.add("🏁 Courses")
        self.stats_tab = self.tabview.add("📊 Statistiques")

        # Création des frames pour chaque section
        self.frames = {}
        for tab in [self.reglages_tab, self.carriere_tab, self.courses_tab, self.stats_tab]:
            frame = ctk.CTkFrame(tab, fg_color="#232323", corner_radius=10)
            frame.pack(fill="both", expand=True, padx=15, pady=15)
            self.frames[tab] = frame

        # Configuration du style des textboxes
        self.textbox_style = {
            "wrap": "word",
            "fg_color": "#2b2b2b",
            "text_color": "white",
            "font": ("Helvetica", 12),
            "corner_radius": 8,
            "border_width": 2,
            "border_color": "#1f6aa5"
        }

        # Création du contenu des onglets
        self.creer_onglet_reglages()
        self.creer_onglet_carriere()
        self.creer_onglet_courses()
        self.creer_onglet_statistiques()

    def creer_onglet_reglages(self):
        """Crée le contenu de l'onglet Réglages."""
        frame = self.frames[self.reglages_tab]
        
        # Titre de la section
        title = ctk.CTkLabel(
            frame, 
            text="⚙️ Configuration des réglages",
            font=("Helvetica", 20, "bold"),
            text_color="#ffffff"
        )
        title.pack(pady=30)  # Augmentez l'espacement vertical
        
        # Frame pour les entrées
        input_frame = ctk.CTkFrame(frame, fg_color="transparent")
        input_frame.pack(fill="both", padx=30, pady=20)  # Augmentez les marges autour du frame
        
        # Création des champs de saisie avec une meilleure organisation
        fields = [
            ("🏎️ Voiture", "voiture"),
            ("🏁 Circuit", "circuit"),
            ("📏 Aileron Avant", "aileron_avant"),
            ("📏 Aileron Arrière", "aileron_arriere"),
            ("🔧 Pression Pneu AV-G", "pression_av_gauche"),
            ("🔧 Pression Pneu AV-D", "pression_av_droit"),
            ("🔧 Pression Pneu AR-G", "pression_ar_gauche"),
            ("🔧 Pression Pneu AR-D", "pression_ar_droit"),
            ("⚖️ Suspension Avant", "suspension_avant"),
            ("⚖️ Suspension Arrière", "suspension_arriere"),
            ("📊 Hauteur de Caisse", "hauteur_caisse")
        ]
        
        for i, (label_text, field_name) in enumerate(fields):
            row = i // 2
            col = i % 2
            
            # Container pour chaque paire label/entrée
            container = ctk.CTkFrame(input_frame, fg_color="transparent")
            container.grid(row=row, column=col, padx=20, pady=10, sticky="ew")  # Augmentez les paddings
            
            # Label
            label = ctk.CTkLabel(
                container,
                text=label_text,
                **self.label_style
            )
            label.pack(anchor="w")
            
            # Champ de saisie
            entry = ctk.CTkEntry(
                container,
                **self.entry_style
            )
            entry.pack(fill="x", pady=(0, 10))
            setattr(self, f"{field_name}_entry", entry)
        
        # Bouton pour ajouter un réglage
        self.add_reglage_button = ctk.CTkButton(
            frame, 
            text="➕ Ajouter Réglage", 
            command=self.ajouter_reglage, 
            **self.button_style
        )
        self.add_reglage_button.pack(fill="x", padx=20, pady=10)

        # Zone d'affichage des réglages existants
        self.reglages_textbox = ctk.CTkTextbox(
            frame,
            height=300,
            **self.textbox_style
        )
        self.reglages_textbox.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Afficher les réglages existants
        self.afficher_reglages_existants()

    def creer_onglet_carriere(self):
        """Crée le contenu de l'onglet Carrière."""
        frame = self.frames[self.carriere_tab]
        
        # Titre de la section
        title = ctk.CTkLabel(
            frame, 
            text="👤 Informations de carrière",
            font=("Helvetica", 20, "bold"),
            text_color="#ffffff"
        )
        title.pack(pady=20)
        
        # Frame pour les entrées
        input_frame = ctk.CTkFrame(frame, fg_color="transparent")
        input_frame.pack(fill="both", padx=20, pady=10)
        
        # Création des champs avec pack
        # Nom du pilote
        self.nom_pilote_label = ctk.CTkLabel(
            input_frame, 
            text="🏎️ Nom du Pilote :", 
            **self.label_style
        )
        self.nom_pilote_label.pack(anchor="w", padx=10, pady=5)
        
        self.nom_pilote_entry = ctk.CTkEntry(
            input_frame, 
            **self.entry_style
        )
        self.nom_pilote_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Équipe
        self.equipe_label = ctk.CTkLabel(
            input_frame, 
            text="🏢 Équipe :", 
            **self.label_style
        )
        self.equipe_label.pack(anchor="w", padx=10, pady=5)
        
        self.equipe_entry = ctk.CTkEntry(
            input_frame, 
            **self.entry_style
        )
        self.equipe_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Voiture préférée
        self.voiture_label = ctk.CTkLabel(
            input_frame, 
            text="🚗 Voiture Préférée :", 
            **self.label_style
        )
        self.voiture_label.pack(anchor="w", padx=10, pady=5)
        
        self.voiture_entry = ctk.CTkEntry(
            input_frame, 
            **self.entry_style
        )
        self.voiture_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Bouton de sauvegarde
        self.save_button = ctk.CTkButton(
            input_frame, 
            text="💾 Sauvegarder Carrière", 
            command=self.sauvegarder_carriere, 
            **self.button_style
        )
        self.save_button.pack(fill="x", padx=10, pady=20)

        # Zone d'affichage des informations de carrière
        self.carriere_textbox = ctk.CTkTextbox(
            frame,
            height=200,
            **self.textbox_style
        )
        self.carriere_textbox.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Afficher les informations actuelles
        if hasattr(self, 'carriere') and self.carriere:
            info_carriere = (
                f"🏎️ Informations de carrière :\n\n"
                f"Pilote : {self.carriere.nom_pilote}\n"
                f"Équipe : {self.carriere.equipe}\n"
                f"Voiture préférée : {self.carriere.voiture_preferee}\n"
            )
            self.carriere_textbox.insert("1.0", info_carriere)

        # Si la carrière existe, pré-remplir les champs
        if hasattr(self, 'carriere') and self.carriere:
            self.nom_pilote_entry.insert(0, self.carriere.nom_pilote)
            self.equipe_entry.insert(0, self.carriere.equipe)
            self.voiture_entry.insert(0, self.carriere.voiture_preferee)

    def creer_onglet_courses(self):
        """Crée le contenu de l'onglet Courses."""
        frame = self.frames[self.courses_tab]
        
        # Titre de la section
        title = ctk.CTkLabel(
            frame, 
            text="🏁 Gestion des courses",
            font=("Helvetica", 20, "bold"),
            text_color="#ffffff"
        )
        title.pack(pady=20)
        
        # Frame pour les entrées
        input_frame = ctk.CTkFrame(frame, fg_color="transparent")
        input_frame.pack(fill="both", padx=20, pady=10)
        
        # Circuit
        self.circuit_label = ctk.CTkLabel(
            input_frame, 
            text="🏎️ Circuit :", 
            **self.label_style
        )
        self.circuit_label.pack(anchor="w", padx=10, pady=5)
        
        self.circuit_entry = ctk.CTkEntry(
            input_frame, 
            **self.entry_style
        )
        self.circuit_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Classement
        self.classement_label = ctk.CTkLabel(
            input_frame, 
            text="🏆 Classement :", 
            **self.label_style
        )
        self.classement_label.pack(anchor="w", padx=10, pady=5)
        
        self.classement_entry = ctk.CTkEntry(
            input_frame, 
            **self.entry_style
        )
        self.classement_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Meilleur temps
        self.meilleur_temps_label = ctk.CTkLabel(
            input_frame, 
            text="⏱️ Meilleur Temps (mm:ss.ms) :", 
            **self.label_style
        )
        self.meilleur_temps_label.pack(anchor="w", padx=10, pady=5)
        
        self.meilleur_temps_entry = ctk.CTkEntry(
            input_frame, 
            **self.entry_style
        )
        self.meilleur_temps_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Date
        self.date_label = ctk.CTkLabel(
            input_frame, 
            text="📅 Date (YYYY-MM-DD) :", 
            **self.label_style
        )
        self.date_label.pack(anchor="w", padx=10, pady=5)
        
        self.date_entry = ctk.CTkEntry(
            input_frame, 
            **self.entry_style
        )
        self.date_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Météo
        self.meteo_label = ctk.CTkLabel(
            input_frame, 
            text="🌤️ Météo :", 
            **self.label_style
        )
        self.meteo_label.pack(anchor="w", padx=10, pady=5)
        
        self.meteo_entry = ctk.CTkEntry(
            input_frame, 
            **self.entry_style
        )
        self.meteo_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Stratégie
        self.strategie_label = ctk.CTkLabel(
            input_frame, 
            text="📋 Stratégie :", 
            **self.label_style
        )
        self.strategie_label.pack(anchor="w", padx=10, pady=5)
        
        self.strategie_entry = ctk.CTkEntry(
            input_frame, 
            **self.entry_style
        )
        self.strategie_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Bouton d'ajout
        self.add_course_button = ctk.CTkButton(
            input_frame, 
            text="➕ Ajouter Course", 
            command=self.ajouter_course, 
            **self.button_style
        )
        self.add_course_button.pack(fill="x", padx=30, pady=20)  # Augmentez les paddings pour le bouton
        
        # Zone d'affichage des courses
        self.courses_textbox = ctk.CTkTextbox(
            frame,
            height=300,  # Augmentez la hauteur
            **self.textbox_style
        )
        self.courses_textbox.pack(fill="both", expand=True, padx=30, pady=20)  # Augmentez les paddings
        
        # Afficher les courses existantes
        self.afficher_courses_existantes()

    def creer_onglet_statistiques(self):
        """Crée le contenu de l'onglet Statistiques."""
        frame = self.frames[self.stats_tab]
        
        # Titre de la section
        title = ctk.CTkLabel(
            frame, 
            text="📊 Statistiques",
            font=("Helvetica", 20, "bold"),
            text_color="#ffffff"
        )
        title.pack(pady=20)
        
        # Zone d'affichage des statistiques
        self.stats_textbox = ctk.CTkTextbox(
            frame,
            height=400,  # Augmentez la hauteur
            **self.textbox_style
        )
        self.stats_textbox.pack(fill="both", expand=True, padx=30, pady=20)  # Augmentez les paddings
        
        # Bouton pour mettre à jour les statistiques
        self.update_stats_button = ctk.CTkButton(
            frame, 
            text="🔄 Mettre à jour les statistiques", 
            command=self.afficher_statistiques, 
            **self.button_style
        )
        self.update_stats_button.pack(fill="x", padx=20, pady=10)
        
        # Bouton pour afficher le graphique
        self.graph_button = ctk.CTkButton(
            frame, 
            text="📈 Afficher le graphique de progression", 
            command=self.afficher_graphique, 
            **self.button_style
        )
        self.graph_button.pack(fill="x", padx=20, pady=10)

        # Afficher les statistiques actuelles
        self.afficher_statistiques()

    def ajouter_reglage(self):
        """Ajoute un réglage à la carrière et met à jour l'affichage."""
        try:
            # Récupération des valeurs des champs
            voiture = getattr(self, 'voiture_entry', None)
            circuit = getattr(self, 'circuit_entry', None)
            
            # Vérification que les champs existent
            if not voiture or not circuit:
                print("⚠️ Erreur: Champs manquants dans l'interface")
                return
            
            # Récupération des valeurs
            nouveau_reglage = Reglage(
                voiture=self.voiture_entry.get(),
                circuit=self.circuit_entry.get(),
                aileron_avant=float(self.aileron_avant_entry.get() or 0),
                aileron_arriere=float(self.aileron_arriere_entry.get() or 0),
                pression_pneus_av_gauche=float(self.pression_av_gauche_entry.get() or 0),
                pression_pneus_av_droit=float(self.pression_av_droit_entry.get() or 0),
                pression_pneus_ar_gauche=float(self.pression_ar_gauche_entry.get() or 0),
                pression_pneus_ar_droit=float(self.pression_ar_droit_entry.get() or 0),
                suspension_avant=float(self.suspension_avant_entry.get() or 0),
                suspension_arriere=float(self.suspension_arriere_entry.get() or 0),
                hauteur_caisse=float(self.hauteur_caisse_entry.get() or 0)
            )

            # Ajout à la carrière
            if not hasattr(self.carriere, 'reglages'):
                self.carriere.reglages = []
            self.carriere.ajouter_reglage(nouveau_reglage)
            
            # Sauvegarde dans le JSON
            self.carriere.enregistrer()

            # Effacement des champs
            for field in ['voiture', 'circuit', 'aileron_avant', 'aileron_arriere',
                         'pression_av_gauche', 'pression_av_droit',
                         'pression_ar_gauche', 'pression_ar_droit',
                         'suspension_avant', 'suspension_arriere', 'hauteur_caisse']:
                entry = getattr(self, f'{field}_entry', None)
                if entry:
                    entry.delete(0, 'end')

            # Mise à jour de l'affichage
            self.afficher_reglages_existants()
            print("✅ Réglage ajouté avec succès!")

        except ValueError as e:
            print(f"⚠️ Erreur de conversion: {str(e)}")
        except Exception as e:
            print(f"⚠️ Erreur lors de l'ajout du réglage: {str(e)}")

    def ajouter_course(self):
        """Ajoute une course à la carrière et l'enregistre."""
        circuit = self.circuit_entry.get()
        classement = self.classement_entry.get()
        meilleur_temps = self.meilleur_temps_entry.get()
        date = self.date_entry.get()
        meteo = self.meteo_entry.get()
        strategie = self.strategie_entry.get()
        
        course = Course(circuit, classement, meilleur_temps, "Course", 
                       voiture_utilisee=self.carriere.voiture_preferee,
                       date=date, meteo=meteo, strategie=strategie)

        self.carriere.ajouter_course(course)
        self.carriere.enregistrer()

        # Effacer les champs
        for entry in [self.circuit_entry, self.classement_entry, 
                     self.meilleur_temps_entry, self.date_entry,
                     self.meteo_entry, self.strategie_entry]:
            entry.delete(0, 'end')

        # Mettre à jour l'affichage des courses
        self.afficher_courses_existantes()
        # Mettre à jour les statistiques
        self.afficher_statistiques()

    def sauvegarder_carriere(self):
        """Sauvegarde et met à jour l'affichage de la carrière."""
        nom_pilote = self.nom_pilote_entry.get()
        equipe = self.equipe_entry.get()
        voiture = self.voiture_entry.get()

        if not self.carriere:
            self.carriere = Carriere(nom_pilote, equipe, voiture)
        else:
            self.carriere.nom_pilote = nom_pilote
            self.carriere.equipe = equipe
            self.carriere.voiture_preferee = voiture

        self.carriere.enregistrer()

        # Message de confirmation
        confirmation = f"✅ Carrière mise à jour !\n\n"
        confirmation += f"Pilote: {nom_pilote}\n"
        confirmation += f"Équipe: {equipe}\n"
        confirmation += f"Voiture: {voiture}\n"

        if hasattr(self, 'carriere_textbox'):
            self.carriere_textbox.delete('1.0', 'end')
            self.carriere_textbox.insert('1.0', confirmation)

    def afficher_reglages_existants(self):
        """Affiche les réglages existants dans la textbox."""
        if not hasattr(self, 'reglages_textbox'):
            return

        self.reglages_textbox.configure(state="normal")
        self.reglages_textbox.delete("1.0", "end")
        
        if not hasattr(self.carriere, 'reglages') or not self.carriere.reglages:
            self.reglages_textbox.insert("1.0", "Aucun réglage enregistré.")
            self.reglages_textbox.configure(state="disabled")
            return

        for reglage in self.carriere.reglages:
            info_reglage = (
                f"🔧 Réglages pour {reglage.voiture} sur {reglage.circuit} :\n"
                f"Aileron avant : {reglage.aileron_avant}°\n"
                f"Aileron arrière : {reglage.aileron_arriere}°\n"
                f"Pressions pneus AV : {reglage.pression_pneus_av_gauche}/{reglage.pression_pneus_av_droit} bars\n"
                f"Pressions pneus AR : {reglage.pression_pneus_ar_gauche}/{reglage.pression_pneus_ar_droit} bars\n"
                f"Suspensions : {reglage.suspension_avant}/{reglage.suspension_arriere}\n"
                f"Hauteur : {reglage.hauteur_caisse}mm\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            )
            self.reglages_textbox.insert("end", info_reglage)
        
        self.reglages_textbox.configure(state="disabled")

    def afficher_courses_existantes(self):
        """Affiche les courses existantes dans la textbox."""
        self.courses_textbox.delete("1.0", "end")
        if not hasattr(self.carriere, 'courses') or not self.carriere.courses:
            self.courses_textbox.insert("1.0", "Aucune course enregistrée.")
            return

        for course in self.carriere.courses:
            info_course = (
                f"🏁 Course à {course.circuit}\n"
                f"Position : {course.classement}e\n"
                f"Meilleur tour : {course.meilleur_temps}s\n"
                f"Type : {course.type_course}\n"
                f"Distance : {course.duree_ou_tours}\n"
                f"Voiture : {course.voiture_utilisee}\n"
                f"Date : {course.date or 'Non spécifiée'}\n"
                f"Météo : {course.meteo or 'Non spécifiée'}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            )
            self.courses_textbox.insert("end", info_course)

    def afficher_statistiques(self):
        """Affiche les statistiques calculées dans la zone dédiée."""
        if not self.carriere:
            self.stats_textbox.configure(state="normal")
            self.stats_textbox.delete("1.0", tk.END)
            self.stats_textbox.insert(tk.END, "Aucune carrière chargée.")
            self.stats_textbox.configure(state="disabled")
            return

        stats = Statistiques(self.carriere)
        self.stats_textbox.configure(state="normal")
        self.stats_textbox.delete("1.0", tk.END)
        
        # En-tête
        self.stats_textbox.insert(tk.END, f"📊 Statistiques pour {self.carriere.nom_pilote}\n")
        self.stats_textbox.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n")
        
        # Statistiques générales
        self.stats_textbox.insert(tk.END, "🏁 Statistiques générales :\n")
        self.stats_textbox.insert(tk.END, f"Nombre total de courses : {len(self.carriere.courses)}\n")

        # Calcul des victoires, podiums et abandons
        victoires = sum(1 for course in self.carriere.courses if self._convertir_classement(course.classement) == 1)
        podiums = sum(1 for course in self.carriere.courses if self._convertir_classement(course.classement) <= 3)
        abandons = sum(1 for course in self.carriere.courses if self._convertir_classement(course.classement) == 0)

        self.stats_textbox.insert(tk.END, f"🏆 Victoires : {victoires}\n")
        self.stats_textbox.insert(tk.END, f"🥇 Podiums : {podiums}\n")
        self.stats_textbox.insert(tk.END, f"⚠️ Abandons : {abandons}\n\n")

        # Meilleurs temps au tour
        self.stats_textbox.insert(tk.END, "⏱️ Meilleurs temps par circuit :\n")
        
        # Création d'un dictionnaire pour stocker les meilleurs temps par circuit
        meilleurs_temps = {}
        for course in self.carriere.courses:
            temps = self._convertir_temps(course.meilleur_temps)
            if temps is None:
                continue
                
            circuit = course.circuit
            if circuit not in meilleurs_temps or temps < meilleurs_temps[circuit]['temps']:
                meilleurs_temps[circuit] = {
                    'temps': temps,
                    'date': course.date or 'Date non spécifiée',
                    'meteo': course.meteo or 'Météo non spécifiée'
                }

        # Affichage des meilleurs temps triés par circuit
        for circuit in sorted(meilleurs_temps.keys()):
            info = meilleurs_temps[circuit]
            temps_formatte = f"{info['temps']:.3f}"
            self.stats_textbox.insert(tk.END, 
                f"  📍 {circuit}:\n"
                f"     → Temps: {temps_formatte}s\n"
                f"     → Date: {info['date']}\n"
                f"     → Météo: {info['meteo']}\n"
                f"     ―――――――――――――――――\n"
            )

        self.stats_textbox.configure(state="disabled")

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