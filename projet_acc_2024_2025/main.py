import tkinter as tk
import customtkinter as ctk
import ui
import sys
import os
import traceback
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='debug.log'
)

def initialiser_donnees():
    """Initialise les fichiers nécessaires."""
    try:
        # Création du dossier data
        os.makedirs('data', exist_ok=True)
        logging.info("Dossier data créé/vérifié")
        
        # Vérification/création du fichier JSON
        if not os.path.exists('data/carrieres_data.json'):
            with open('data/carrieres_data.json', 'w', encoding='utf-8') as f:
                f.write('{"carrieres": [], "carriere_active": null}')
            logging.info("Fichier JSON initialisé")
        return True
    except Exception as e:
        logging.error(f"Erreur d'initialisation : {str(e)}")
        return False

def main():
    try:
        # Initialisation des données
        if not initialiser_donnees():
            print("❌ Erreur lors de l'initialisation des données")
            sys.exit(1)

        # Initialisation de la fenêtre racine Tk
        root = tk.Tk()
        root.withdraw()  # Cache la fenêtre Tk principale
        logging.info("Fenêtre racine Tk créée")

        # Configuration de customtkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        logging.info("CustomTkinter configuré")

        # Création et démarrage de l'application
        app = ui.Application()
        
        # Configuration de la fermeture propre
        def on_closing():
            try:
                app.on_closing()  # Sauvegarde les données
                root.destroy()    # Ferme la fenêtre racine
            except Exception as e:
                logging.error(f"Erreur lors de la fermeture : {str(e)}")
                sys.exit(1)

        app.protocol("WM_DELETE_WINDOW", on_closing)
        logging.info("Application créée et configurée")

        # Lancement de la boucle principale
        app.mainloop()

    except Exception as e:
        logging.error(f"Erreur critique : {str(e)}")
        logging.error(traceback.format_exc())
        print(f"❌ Une erreur critique s'est produite : {str(e)}")
        print("Consultez le fichier debug.log pour plus de détails")
        input("Appuyez sur Entrée pour fermer...")
        sys.exit(1)

if __name__ == "__main__":
    main()