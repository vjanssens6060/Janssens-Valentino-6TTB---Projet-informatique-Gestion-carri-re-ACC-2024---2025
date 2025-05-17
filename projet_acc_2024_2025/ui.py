import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from carriere import Carriere
from reglage import Reglage
from course import Course
from statistiques import Statistiques
from objectif import Objectif  # Ajout de l'import
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime


class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuration de la fenêtre
        self.title("Gestionnaire de Carrière - ACC")
        self.geometry("1200x900")

        # Définition des styles
        self.label_style = {
            "font": ("Helvetica", 14, "bold"),
            "text_color": "#ffffff"
        }
        
        # Correction du style entry pour éviter la duplication du paramètre width
        self.entry_style = {
            "font": ("Helvetica", 14),
            "corner_radius": 6,
            "border_width": 2,
            "border_color": "#2b2b2b",
            "height": 40
        }
        
        self.button_style = {
            "font": ("Helvetica", 14, "bold"),
            "corner_radius": 8,
            "border_width": 2,
            "border_color": "#2b2b2b",
            "hover_color": "#144870",
            "height": 50
        }
        
        self.delete_button_style = {
            **self.button_style,
            "fg_color": "#ff4444",
            "hover_color": "#cc3333"
        }

        # Création du Canvas pour le défilement
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
        
        # Charger toutes les carrières
        self.carrieres, carriere_active_id = Carriere.charger_carrieres()
        if not self.carrieres:
            nouvelle_carriere = Carriere("Nom par défaut", "Équipe par défaut", "Voiture par défaut")
            self.carrieres = [nouvelle_carriere]
            carriere_active_id = nouvelle_carriere.id
        
        # Définir la carrière active
        self.carriere = next((c for c in self.carrieres if c.id == carriere_active_id), self.carrieres[0])

        # Ajouter un menu pour gérer les carrières
        self.creer_menu_carrieres()

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
            "height": 40
        }
        self.button_style = {
            "font": ("Helvetica", 14, "bold"),
            "corner_radius": 8,
            "border_width": 2,
            "border_color": "#2b2b2b",
            "hover_color": "#144870",
            "height": 50
        }
        
        # Style spécifique pour les boutons de suppression
        self.delete_button_style = {
            **self.button_style,
            "fg_color": "#ff4444",
            "hover_color": "#cc3333"
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

        # Ajout des onglets dans le nouvel ordre
        self.carriere_tab = self.tabview.add("👤 Carrière")
        self.reglages_tab = self.tabview.add("⚙️ Réglages")
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

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Ajouter cette ligne

    def on_closing(self):
        """Appelé lors de la fermeture de l'application."""
        self.sauvegarder_carrieres()
        self.quit()

    def creer_menu_carrieres(self):
        """Crée un menu pour gérer les carrières."""
        menu_frame = ctk.CTkFrame(self.scrollable_frame)
        menu_frame.pack(fill="x", padx=20, pady=10)

        # Combobox pour sélectionner la carrière active
        self.carriere_combobox = ctk.CTkComboBox(
            menu_frame,
            values=[f"{c.nom_pilote} - {c.equipe}" for c in self.carrieres],
            command=self.changer_carriere
        )
        self.carriere_combobox.pack(side="left", padx=10)
        
        # Boutons pour gérer les carrières
        ctk.CTkButton(
            menu_frame,
            text="➕ Nouvelle carrière",
            command=self.nouvelle_carriere,
            width=150,
            **self.button_style
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            menu_frame,
            text="🗑️ Supprimer carrière",
            command=self.supprimer_carriere,
            width=150,
            **self.delete_button_style
        ).pack(side="left", padx=5)

    def nouvelle_carriere(self):
        """Crée une nouvelle carrière."""
        nouvelle_carriere = Carriere("Nouveau pilote", "Nouvelle équipe", "Nouvelle voiture")
        self.carrieres.append(nouvelle_carriere)
        self.carriere = nouvelle_carriere
        self.mettre_a_jour_interface_carriere()
        self.sauvegarder_carrieres()

    def supprimer_carriere(self):
        """Supprime la carrière active."""
        if len(self.carrieres) > 1:
            self.carrieres.remove(self.carriere)
            self.carriere = self.carrieres[0]
            self.mettre_a_jour_interface_carriere()
            self.sauvegarder_carrieres()
        else:
            print("⚠️ Impossible de supprimer la dernière carrière")

    def changer_carriere(self, selection):
        """Change la carrière active."""
        if not selection:
            return
            
        # Sauvegarder la carrière actuelle avant de changer
        if hasattr(self, 'carriere'):
            self.sauvegarder_carrieres()
        
        # Trouver la nouvelle carrière sélectionnée
        nom_pilote = selection.split(" - ")[0]
        nouvelle_carriere = next(
            (c for c in self.carrieres if c.nom_pilote == nom_pilote),
            None
        )
        
        if nouvelle_carriere:
            self.carriere = nouvelle_carriere
            self.mettre_a_jour_interface_carriere()
            # Mettre à jour les objectifs spécifiques à cette carrière
            self.afficher_objectifs()
        else:
            print("❌ Erreur : Carrière non trouvée")

    def changer_saison(self, selection):
        """Gère le changement de saison et met à jour l'affichage des courses."""
        self.saison_actuelle = selection
        self.afficher_courses_existantes()

    def mettre_a_jour_interface_carriere(self):
        """Met à jour l'interface pour refléter la carrière active."""
        # Mettre à jour la combobox
        self.carriere_combobox.configure(
            values=[f"{c.nom_pilote} - {c.equipe}" for c in self.carrieres]
        )
        self.carriere_combobox.set(f"{self.carriere.nom_pilote} - {self.carriere.equipe}")

        # Mettre à jour les affichages
        self.afficher_reglages_existants()
        self.afficher_courses_existantes()
        self.afficher_statistiques()
        
        # Mettre à jour les champs de la carrière
        if hasattr(self, 'nom_pilote_entry'):
            self.nom_pilote_entry.delete(0, 'end')
            self.nom_pilote_entry.insert(0, self.carriere.nom_pilote)
            self.equipe_entry.delete(0, 'end')
            self.equipe_entry.insert(0, self.carriere.equipe)
            self.voiture_entry.delete(0, 'end')
            self.voiture_entry.insert(0, self.carriere.voiture_preferee)

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
        title.pack(pady=30)
        
        # Frame pour les entrées
        input_frame = ctk.CTkFrame(frame, fg_color="transparent")
        input_frame.pack(fill="both", padx=30, pady=20)
        
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
            container.grid(row=row, column=col, padx=20, pady=10, sticky="ew")
            
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

        # Créer la listbox AVANT de l'utiliser
        self.reglages_listbox = tk.Listbox(
            frame, 
            bg="#2b2b2b", 
            fg="white",
            selectmode=tk.SINGLE,
            height=5
        )
        self.reglages_listbox.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Zone d'affichage des réglages existants
        self.reglages_textbox = ctk.CTkTextbox(
            frame,
            height=300,
            **self.textbox_style
        )
        self.reglages_textbox.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Bouton pour supprimer un réglage
        self.delete_reglage_button = ctk.CTkButton(
            frame, 
            text="🗑️ Supprimer Réglage", 
            command=self.supprimer_reglage,
            **self.delete_button_style
        )
        self.delete_reglage_button.pack(fill="x", padx=20, pady=10)

        # Bouton pour modifier un réglage
        self.modify_reglage_button = ctk.CTkButton(
            frame, 
            text="✏️ Modifier Réglage", 
            command=self.modifier_reglage,
            **self.button_style
        )
        self.modify_reglage_button.pack(fill="x", padx=20, pady=10)
        
        # Afficher les réglages existants (maintenant que la listbox est créée)
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
        
        # Ajouter une section pour l'historique
        historique_frame = ctk.CTkFrame(frame, fg_color="#232323", corner_radius=10)
        historique_frame.pack(fill="both", expand=True, padx=15, pady=15)

        historique_label = ctk.CTkLabel(
            historique_frame,
            text="📜 Historique de la carrière",
            font=("Helvetica", 16, "bold"),
            text_color="#ffffff"
        )
        historique_label.pack(pady=10)

        self.historique_textbox = ctk.CTkTextbox(
            historique_frame,
            height=200,
            **self.textbox_style
        )
        self.historique_textbox.pack(fill="both", expand=True, padx=10, pady=10)

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

        # Mettre à jour l'affichage de l'historique
        self.afficher_historique()

        # Ajouter une section pour les objectifs
        objectifs_frame = ctk.CTkFrame(frame, fg_color="#232323", corner_radius=10)
        objectifs_frame.pack(fill="both", expand=True, padx=15, pady=15)

        objectifs_label = ctk.CTkLabel(
            objectifs_frame,
            text="🎯 Objectifs de carrière",
            font=("Helvetica", 16, "bold"),
            text_color="#ffffff"
        )
        objectifs_label.pack(pady=10)

        # Frame pour ajouter un nouvel objectif
        nouvel_objectif_frame = ctk.CTkFrame(objectifs_frame, fg_color="transparent")
        nouvel_objectif_frame.pack(fill="x", padx=10, pady=5)

        # Combobox pour le type d'objectif
        self.type_objectif_combobox = ctk.CTkComboBox(
            nouvel_objectif_frame,
            values=["Victoires", "Podiums", "Classement", "Temps"],
            width=150
        )
        self.type_objectif_combobox.pack(side="left", padx=5)

        # Entry pour la valeur cible
        self.valeur_objectif_entry = ctk.CTkEntry(
            nouvel_objectif_frame,
            placeholder_text="Valeur cible",
            width=100,
            **self.entry_style
        )
        self.valeur_objectif_entry.pack(side="left", padx=5)

        # Entry pour la description
        self.description_objectif_entry = ctk.CTkEntry(
            nouvel_objectif_frame,
            placeholder_text="Description de l'objectif",
            width=200,
            **self.entry_style
        )
        self.description_objectif_entry.pack(side="left", padx=5)

        # Combobox pour la saison
        annee_actuelle = datetime.now().year
        saisons = [str(year) for year in range(annee_actuelle - 1, annee_actuelle + 3)]
        self.saison_objectif_combobox = ctk.CTkComboBox(
            nouvel_objectif_frame,
            values=saisons,
            width=100
        )
        self.saison_objectif_combobox.pack(side="left", padx=5)

        # Bouton pour ajouter l'objectif
        ctk.CTkButton(
            nouvel_objectif_frame,
            text="➕ Ajouter",
            command=self.ajouter_objectif,
            width=100,
            **self.button_style
        ).pack(side="left", padx=5)

        # Listbox pour afficher les objectifs
        self.objectifs_listbox = tk.Listbox(
            objectifs_frame,
            bg="#2b2b2b",
            fg="white",
            selectmode=tk.SINGLE,
            height=5
        )
        self.objectifs_listbox.pack(fill="both", expand=True, padx=10, pady=5)

        # Bouton pour supprimer l'objectif sélectionné
        ctk.CTkButton(
            objectifs_frame,
            text="🗑️ Supprimer objectif",
            command=self.supprimer_objectif,
            **self.delete_button_style
        ).pack(fill="x", padx=10, pady=5)

        # Mettre à jour l'affichage des objectifs
        self.afficher_objectifs()

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
        
        # Ajouter le sélecteur de saison
        saison_frame = ctk.CTkFrame(frame, fg_color="transparent")
        saison_frame.pack(fill="x", padx=20, pady=5)
        
        saison_label = ctk.CTkLabel(
            saison_frame,
            text="📅 Saison :",
            **self.label_style
        )
        saison_label.pack(side="left", padx=5)
        
        # Année actuelle
        annee_actuelle = datetime.now().year
        
        # Liste des saisons (5 ans avant et après l'année actuelle)
        self.saisons = [str(year) for year in range(annee_actuelle - 5, annee_actuelle + 6)]
        
        self.saison_combobox = ctk.CTkComboBox(
            saison_frame,
            values=self.saisons,
            command=self.changer_saison,
            width=150
        )
        self.saison_combobox.pack(side="left", padx=10)
        self.saison_combobox.set(str(annee_actuelle))
        
        # Frame pour les entrées
        input_frame = ctk.CTkFrame(frame, fg_color="transparent")
        input_frame.pack(fill="both", padx=20, pady=10)
        
        # Création des champs de saisie
        fields = [
            ("🏎️ Circuit", "circuit"),
            ("🏆 Classement", "classement"),
            ("⏱️ Meilleur Temps (mm:ss.ms)", "meilleur_temps"),
            ("📅 Date (YYYY-MM-DD)", "date"),
            ("🌤️ Météo", "meteo"),
            ("📋 Stratégie", "strategie")
        ]
        
        for label_text, field_name in fields:
            # Label
            label = ctk.CTkLabel(
                input_frame, 
                text=label_text, 
                **self.label_style
            )
            label.pack(anchor="w", padx=10, pady=5)
            
            # Entry
            entry = ctk.CTkEntry(
                input_frame, 
                **self.entry_style
            )
            entry.pack(fill="x", padx=10, pady=(0, 10))
            setattr(self, f"{field_name}_entry", entry)
        
        # Bouton d'ajout
        self.add_course_button = ctk.CTkButton(
            input_frame, 
            text="➕ Ajouter Course", 
            command=self.ajouter_course, 
            **self.button_style
        )
        self.add_course_button.pack(fill="x", padx=30, pady=20)
        
        # Création de la listbox AVANT son utilisation
        self.courses_listbox = tk.Listbox(
            frame, 
            bg="#2b2b2b", 
            fg="white",
            selectmode=tk.SINGLE,
            height=5
        )
        self.courses_listbox.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Zone d'affichage des courses
        self.courses_textbox = ctk.CTkTextbox(
            frame,
            height=300,
            **self.textbox_style
        )
        self.courses_textbox.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Bouton de suppression
        self.delete_course_button = ctk.CTkButton(
            frame, 
            text="🗑️ Supprimer Course", 
            command=self.supprimer_course,
            **self.delete_button_style
        )
        self.delete_course_button.pack(fill="x", padx=20, pady=10)
        
        # Bouton pour modifier une course
        self.modify_course_button = ctk.CTkButton(
            frame, 
            text="✏️ Modifier Course", 
            command=self.modifier_course,
            **self.button_style
        )
        self.modify_course_button.pack(fill="x", padx=20, pady=10)
        
        # Afficher les courses existantes APRÈS création de tous les widgets
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
            height=400,
            **self.textbox_style
        )
        self.stats_textbox.pack(fill="both", expand=True, padx=30, pady=20)
        
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

        # Mettre à jour l'historique après la sauvegarde
        self.afficher_historique()

    def sauvegarder_carrieres(self):
        """Sauvegarde l'état actuel de toutes les carrières."""
        try:
            Carriere.sauvegarder_carrieres(self.carrieres, self.carriere)
            print("✅ Carrières sauvegardées avec succès")
        except Exception as e:
            print(f"⚠️ Erreur lors de la sauvegarde : {str(e)}")

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

        # Mettre à jour la listbox des réglages
        self.reglages_listbox.delete(0, tk.END)
        for i, reglage in enumerate(self.carriere.reglages):
            self.reglages_listbox.insert(tk.END, f"{reglage.voiture} - {reglage.circuit}")

    def afficher_courses_existantes(self):
        """Affiche les courses existantes dans la listbox."""
        if not hasattr(self, 'courses_listbox'):
            return
            
        # Effacer la liste existante
        self.courses_listbox.delete(0, tk.END)
        
        if not hasattr(self.carriere, 'courses') or not self.carriere.courses:
            return
            
        # Filtrer les courses par saison
        courses_saison = [
            course for course in self.carriere.courses 
            if course.date and course.date.startswith(self.saison_combobox.get())
        ]

        # Mettre à jour la listbox avec les nouvelles courses
        for course in courses_saison:
            self.courses_listbox.insert(
                tk.END, 
                f"{course.circuit} - Position: {course.classement}"
            )

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
        """Convertit le temps en float, ou retourne None si le format est invalide."""
        try:
            if ":" in temps:  # Format mm:ss.ms
                minutes, seconds = temps.split(":")
                return float(minutes) * 60 + float(seconds)
            return float(temps)  # Format en secondes
        except (ValueError, TypeError, AttributeError):
            return None  # Retourne None si le format est invalide

    def supprimer_reglage(self):
        """Supprime le réglage sélectionné dans la listbox."""
        if not hasattr(self, 'reglages_listbox'):
            print("⚠️ La listbox des réglages n'existe pas.")
            return

        selection = self.reglages_listbox.curselection()
        if not selection:
            print("⚠️ Aucun réglage sélectionné.")
            return

        index = selection[0]
        if self.carriere.supprimer_reglage(index):
            self.afficher_reglages_existants()
            print("✅ Réglage supprimé avec succès.")
        else:
            print("⚠️ Erreur lors de la suppression du réglage.")

    def supprimer_course(self):
        """Supprime la course sélectionnée dans la listbox."""
        if not hasattr(self, 'courses_listbox'):
            print("⚠️ La listbox des courses n'existe pas.")
            return

        selection = self.courses_listbox.curselection()
        if not selection:
            print("⚠️ Aucune course sélectionnée.")
            return

        index = selection[0]
        if index >= len(self.carriere.courses):
            print("⚠️ Index de course invalide.")
            return

        # Récupérer l'ID de la course à supprimer
        course_id = self.carriere.courses[index].id
        
        # Supprimer la course
        self.carriere.supprimer_course(course_id)
        self.carriere.enregistrer()
        
        # Mettre à jour l'interface
        self.afficher_courses_existantes()
        self.afficher_statistiques()
        print("✅ Course supprimée avec succès.")

    def modifier_reglage(self):
        """Modifie le réglage sélectionné."""
        if not hasattr(self, 'reglages_listbox'):
            print("⚠️ La listbox des réglages n'existe pas.")
            return

        selection = self.reglages_listbox.curselection()
        if not selection:
            print("⚠️ Aucun réglage sélectionné.")
            return

        index = selection[0]
        reglage = self.carriere.reglages[index]

        # Pré-remplir les champs avec les valeurs actuelles
        self.voiture_entry.delete(0, 'end')
        self.voiture_entry.insert(0, reglage.voiture)
        
        self.circuit_entry.delete(0, 'end')
        self.circuit_entry.insert(0, reglage.circuit)
        
        # Pré-remplir tous les autres champs
        fields = {
            'aileron_avant': reglage.aileron_avant,
            'aileron_arriere': reglage.aileron_arriere,
            'pression_av_gauche': reglage.pression_pneus_av_gauche,
            'pression_av_droit': reglage.pression_pneus_av_droit,
            'pression_ar_gauche': reglage.pression_pneus_ar_gauche,
            'pression_ar_droit': reglage.pression_pneus_ar_droit,
            'suspension_avant': reglage.suspension_avant,
            'suspension_arriere': reglage.suspension_arriere,
            'hauteur_caisse': reglage.hauteur_caisse
        }
        
        for field, value in fields.items():
            entry = getattr(self, f'{field}_entry')
            entry.delete(0, 'end')
            entry.insert(0, str(value))

        # Créer un bouton de mise à jour
        self.update_reglage_button = ctk.CTkButton(
            self.frames[self.reglages_tab],
            text="✅ Mettre à jour le réglage",
            command=lambda: self._sauvegarder_modification_reglage(index),
            **self.button_style
        )
        self.update_reglage_button.pack(fill="x", padx=20, pady=10)

    def _sauvegarder_modification_reglage(self, index):
        """Sauvegarde les modifications d'un réglage."""
        try:
            # Créer un nouveau réglage avec les valeurs modifiées
            reglage_modifie = Reglage(
                voiture=self.voiture_entry.get(),
                circuit=self.circuit_entry.get(),
                aileron_avant=float(self.aileron_avant_entry.get()),
                aileron_arriere=float(self.aileron_arriere_entry.get()),
                pression_pneus_av_gauche=float(self.pression_av_gauche_entry.get()),
                pression_pneus_av_droit=float(self.pression_av_droit_entry.get()),
                pression_pneus_ar_gauche=float(self.pression_ar_gauche_entry.get()),
                pression_pneus_ar_droit=float(self.pression_ar_droit_entry.get()),
                suspension_avant=float(self.suspension_avant_entry.get()),
                suspension_arriere=float(self.suspension_arriere_entry.get()),
                hauteur_caisse=float(self.hauteur_caisse_entry.get())
            )

            # Mettre à jour le réglage dans la carrière
            self.carriere.reglages[index] = reglage_modifie
            self.carriere.enregistrer()

            # Mettre à jour l'affichage
            self.afficher_reglages_existants()
            
            # Supprimer le bouton de mise à jour
            if hasattr(self, 'update_reglage_button'):
                self.update_reglage_button.destroy()

            print("✅ Réglage mis à jour avec succès!")

        except ValueError as e:
            print(f"⚠️ Erreur de conversion: {str(e)}")
        except Exception as e:
            print(f"⚠️ Erreur lors de la modification du réglage: {str(e)}")

    def modifier_course(self):
        """Modifie la course sélectionnée."""
        if not hasattr(self, 'courses_listbox'):
            print("⚠️ La listbox des courses n'existe pas.")
            return

        selection = self.courses_listbox.curselection()
        if not selection:
            print("⚠️ Aucune course sélectionnée.")
            return

        index = selection[0]
        if index >= len(self.carriere.courses):
            print("⚠️ Index de course invalide.")
            return

        course = self.carriere.courses[index]

        # Pré-remplir les champs avec les valeurs actuelles
        fields = {
            'circuit': course.circuit,
            'classement': course.classement,
            'meilleur_temps': course.meilleur_temps,
            'date': course.date or '',
            'meteo': course.meteo or '',
            'strategie': course.strategie or ''
        }
        
        for field, value in fields.items():
            entry = getattr(self, f'{field}_entry')
            entry.delete(0, 'end')
            entry.insert(0, str(value))

        # Créer un bouton de mise à jour
        self.update_course_button = ctk.CTkButton(
            self.frames[self.courses_tab],
            text="✅ Mettre à jour la course",
            command=lambda: self._sauvegarder_modification_course(course.id),
            **self.button_style
        )
        self.update_course_button.pack(fill="x", padx=20, pady=10)

    def _sauvegarder_modification_course(self, course_id):
        """Sauvegarde les modifications d'une course."""
        try:
            # Récupérer les nouvelles valeurs
            nouvelles_donnees = {
                'circuit': self.circuit_entry.get(),
                'classement': self.classement_entry.get(),
                'meilleur_temps': self.meilleur_temps_entry.get(),
                'date': self.date_entry.get(),
                'meteo': self.meteo_entry.get(),
                'strategie': self.strategie_entry.get()
            }

            # Mettre à jour la course dans la carrière
            self.carriere.modifier_course(course_id, nouvelles_donnees)
            self.carriere.enregistrer()

            # Mettre à jour l'affichage
            self.afficher_courses_existantes()
            self.afficher_statistiques()
            
            # Supprimer le bouton de mise à jour
            if hasattr(self, 'update_course_button'):
                self.update_course_button.destroy()

            print("✅ Course mise à jour avec succès!")

        except ValueError as e:
            print(f"⚠️ Erreur de conversion: {str(e)}")
        except Exception as e:
            print(f"⚠️ Erreur lors de la modification de la course: {str(e)}")

    def ajouter_objectif(self):
        """Ajoute un nouvel objectif à la carrière active."""
        type_obj = self.type_objectif_combobox.get()
        valeur = self.valeur_objectif_entry.get()
        description = self.description_objectif_entry.get()
        saison = self.saison_objectif_combobox.get()

        if not all([type_obj, valeur, description, saison]):
            print("❌ Erreur : Tous les champs sont obligatoires")
            return

        if not hasattr(self, 'carriere') or not self.carriere:
            print("❌ Erreur : Aucune carrière active")
            return

        try:
            nouvel_objectif = Objectif(description, type_obj, valeur, saison)
            self.carriere.ajouter_objectif(nouvel_objectif)
            self.carriere.enregistrer()
            self.sauvegarder_carrieres()  # Sauvegarder toutes les carrières
            self.afficher_objectifs()
            
            # Effacer les champs
            self.valeur_objectif_entry.delete(0, 'end')
            self.description_objectif_entry.delete(0, 'end')
            
            print("✅ Objectif ajouté avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout de l'objectif : {str(e)}")

    def supprimer_objectif(self):
        """Supprime l'objectif sélectionné."""
        if not hasattr(self, 'objectifs_listbox'):
            return

        selection = self.objectifs_listbox.curselection()
        if not selection:
            print("⚠️ Aucun objectif sélectionné")
            return

        if self.carriere.supprimer_objectif(selection[0]):
            self.carriere.enregistrer()
            self.afficher_objectifs()
            print("✅ Objectif supprimé avec succès")

    def afficher_objectifs(self):
        """Affiche les objectifs de la carrière active."""
        if not hasattr(self, 'objectifs_listbox'):
            return
        
        self.objectifs_listbox.delete(0, tk.END)
        
        if not hasattr(self.carriere, 'objectifs'):
            return
        
        # Vérifier si la carrière a des objectifs
        if not self.carriere.objectifs:
            self.objectifs_listbox.insert(tk.END, "Aucun objectif défini pour cette carrière")
            return

        # Afficher les objectifs de la carrière active uniquement
        for obj in self.carriere.objectifs:
            status_emoji = "🔄" if obj.statut == "En cours" else "✅" if obj.statut == "Réussi" else "❌"
            objectif_text = f"{status_emoji} {obj.description} ({obj.type_objectif}: {obj.valeur_cible}, Saison {obj.saison})"
            self.objectifs_listbox.insert(tk.END, objectif_text)

    def afficher_historique(self):
        """Affiche l'historique de la carrière."""
        if not hasattr(self, 'historique_textbox'):
            return

        self.historique_textbox.configure(state="normal")
        self.historique_textbox.delete("1.0", "end")

        if not self.carriere or not self.carriere.historique.changements:
            self.historique_textbox.insert("1.0", "Aucun changement dans l'historique.")
            self.historique_textbox.configure(state="disabled")
            return

        for changement in self.carriere.historique.changements:
            info_changement = (
                f"📅 Date : {changement['date']}\n"
                f"🔄 Changement de {changement['type']}\n"
                f"Ancien : {changement['ancienne_valeur']}\n"
                f"Nouveau : {changement['nouvelle_valeur']}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            )
            self.historique_textbox.insert("end", info_changement)

        self.historique_textbox.configure(state="disabled")