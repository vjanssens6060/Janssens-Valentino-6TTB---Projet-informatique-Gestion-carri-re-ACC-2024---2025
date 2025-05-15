import tkinter as tk
import customtkinter as ctk
import ui
import sys
import os

def main():
    try:
        # Vérifier que le dossier data existe
        if not os.path.exists('data'):
            os.makedirs('data')
            
        # Vérifier que le fichier de données existe
        if not os.path.exists('data/carrieres_data.json'):
            with open('data/carrieres_data.json', 'w') as f:
                f.write('{"carrieres": [], "carriere_active": null}')

        # Configuration de l'interface graphique
        root = tk.Tk()
        root.withdraw()  # Cache la fenêtre principale tk
        
        # Configuration de customtkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Création et lancement de l'application
        app = ui.Application()
        app.protocol("WM_DELETE_WINDOW", lambda: (app.on_closing(), root.destroy()))
        app.mainloop()

    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()