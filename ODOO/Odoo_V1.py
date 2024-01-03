import tkinter as tk
from tkinter import messagebox

class ApplicationLogistique:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de connexion")

        # Comptes dédiés (utilisateurs pré-enregistrés pour l'exemple)
        self.comptes_utilisateurs = [
            {'nom_utilisateur': 'log', 'mot_de_passe': 'log'},
            {'nom_utilisateur': 'prod', 'mot_de_passe': 'prod'}
        ]

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
    app = ApplicationLogistique(root)
    root.deiconify()  # Ajout de cette ligne pour afficher la fenêtre
    root.mainloop()
