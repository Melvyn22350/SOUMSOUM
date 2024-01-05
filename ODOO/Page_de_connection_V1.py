import xmlrpc.client
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import sys

class LoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Page de Connexion")
        self.set_icon()  # Ajoutez cette ligne pour définir l'icône
        self.center_window()
        self.create_widgets()
        self.set_dark_theme()

    def set_icon(self):
        # Charger l'icône avec Pillow
        icon = Image.open("/home/user/Téléchargements/SOUMSOUM.png")
        # Convertir l'icône en format Tkinter
        icon_tk = ImageTk.PhotoImage(icon)
        # Définir l'icône de la fenêtre
        self.master.iconphoto(True, icon_tk)

    def center_window(self):
        # Obtenez les dimensions de l'écran
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculez les coordonnées x, y pour centrer la fenêtre
        x = (screen_width - self.master.winfo_reqwidth()) / 2
        y = (screen_height - self.master.winfo_reqheight()) / 2

        # Définissez les nouvelles coordonnées de la fenêtre
        self.master.geometry("+%d+%d" % (x, y))

    def set_dark_theme(self):
        # Définissez la couleur de fond sur foncé
        self.master.configure(bg='#333333')  # Remplacez '#333333' par la couleur souhaitée

    def create_widgets(self):
        self.label_username = ttk.Label(self.master, text="Nom d'utilisateur:")
        self.label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_username = ttk.Entry(self.master)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)

        self.label_password = ttk.Label(self.master, text="Mot de passe:")
        self.label_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_password = ttk.Entry(self.master, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.button_login = ttk.Button(self.master, text="Se Connecter", command=self.login)
        self.button_login.grid(row=2, column=0, columnspan=2, pady=20)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Connexion à Odoo
        url = "http://localhost:8069"
        db = "SOUMSOUMv2"

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})

        if uid:
            print("Connexion réussie!")

            # Vérifier si l'adresse e-mail contient "prod" ou "log"
            if 'prod' in username:
                print("Connexion production réussie.")
                self.master.destroy()  # Fermer la fenêtre de connexion

                # Ouvrir un fichier Python lorsque la connexion "prod" réussit
                subprocess.Popen([sys.executable, '/home/user/Documents/SOURCE/Test1/ODOO/Application_Production_V1.py'])
            elif 'log' in username:
                print("Connexion logistique réussie.")
                self.master.destroy()  # Fermer la fenêtre de connexion

                # Ouvrir un fichier Python lorsque la connexion "log" réussit
                subprocess.Popen([sys.executable, '/home/user/Documents/SOURCE/Test1/ODOO/Application_Logistique_V1.py'])
            else:
                print("Type de connexion non reconnu.")
        else:
            print("Échec de la connexion. Veuillez vérifier vos identifiants.")

def main():
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
