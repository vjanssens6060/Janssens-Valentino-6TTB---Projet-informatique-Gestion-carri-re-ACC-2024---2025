import tkinter as tk  # Ajout de l'import de tkinter
import customtkinter as ctk  # Ajout de l'import de customtkinter
import ui  # Importation du module contenant la classe Application

if __name__ == "__main__":
    # Configuration initiale de customtkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    # Lancer l'application correctement
    app = ui.Application()  # ✅ On crée une instance de l'application
    app.mainloop()  # ✅ On démarre l'application avec la méthode correcte