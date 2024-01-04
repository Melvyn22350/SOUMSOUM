import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de connexion")

        # Comptes dédiés (utilisateurs pré-enregistrés pour l'exemple)
        self.comptes_utilisateurs = [
            {'nom_utilisateur': 'log', 'mot_de_passe': 'log'},
            {'nom_utilisateur': 'prod', 'mot_de_passe': 'prod'}
        ]

        # Chargement de l'image
        image_path = "/home/user/Documents/sousoumlogo.png"
        image = Image.open(image_path)
        image = image.resize((182, 120), Image.ANTIALIAS)  # Redimensionner l'image si nécessaire
        self.photo = ImageTk.PhotoImage(image)


        # Création des widgets
        self.label_utilisateur = tk.Label(root, text="Nom d'utilisateur:")
        self.label_mot_de_passe = tk.Label(root, text="Mot de passe:")
        self.entry_utilisateur = tk.Entry(root)
        self.entry_mot_de_passe = tk.Entry(root, show="*")
        self.bouton_connexion = tk.Button(root, text="Se connecter", command=self.gestion_connexion)

        # Placement des widgets
        self.label_utilisateur.grid(row=0, column=0, sticky=tk.E)
        self.label_mot_de_passe.grid(row=1, column=0, sticky=tk.E)
        self.entry_utilisateur.grid(row=0, column=1)
        self.entry_mot_de_passe.grid(row=1, column=1)
        self.bouton_connexion.grid(row=2, column=1, pady=10)

        # Affichage de l'image dans un Label
        self.label_image = tk.Label(root, image=self.photo)
        self.label_image.grid(row=0, column=2, rowspan=3, padx=10)  # Ajustez la position de l'image
    
        # Calcul de la position pour centrer la fenêtre
        window_width = 300  # Largeur de la fenêtre
        window_height = 150  # Hauteur de la fenêtre

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def gestion_connexion(self):
        nom_utilisateur = self.entry_utilisateur.get()
        mot_de_passe = self.entry_mot_de_passe.get()

        for compte_utilisateur in self.comptes_utilisateurs:
            if nom_utilisateur == compte_utilisateur['nom_utilisateur'] and mot_de_passe == compte_utilisateur['mot_de_passe']:
                messagebox.showinfo("Connexion réussie", "Bienvenue, " + nom_utilisateur + "!")
                return  # Sortir de la fonction après la connexion réussie

        messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect")

if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.geometry("480x120")  # Définir une taille pour la fenêtre (largeur x hauteur)
    root.update()  # Forcer la mise à jour de la fenêtre pour appliquer la nouvelle géométrie
    root.mainloop()

