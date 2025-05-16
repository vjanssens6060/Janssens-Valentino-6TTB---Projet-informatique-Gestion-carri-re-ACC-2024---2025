import tkinter as tk
import customtkinter as ctk
import ui
import sys
import os
import traceback

def main():
    try:
        # Création du dossier data si nécessaire
        os.makedirs('data', exist_ok=True)
        
        # Création/vérification du fichier JSON
        if not os.path.exists('data/carrieres_data.json'):
            with open('data/carrieres_data.json', 'w', encoding='utf-8') as f:
                f.write('{"carrieres": [], "carriere_active": null}')
        
        # Configuration de base
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Lancement de l'application
        app = ui.Application()
        app.mainloop()

    except Exception as e:
        print(f"Erreur critique : {str(e)}")
        print(traceback.format_exc())
        input("Appuyez sur Entrée pour fermer...")
        sys.exit(1)

if __name__ == "__main__":
    main()