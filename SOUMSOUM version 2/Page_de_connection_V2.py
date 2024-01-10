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
        self.set_icon()
        self.center_window()
        self.create_widgets()
        self.set_dark_theme()


#=====================================================================
#=====================================================================
    def set_icon(self):
        icon = Image.open("/home/user/Documents/SOURCE/Application_SOUMSOUM/SOUMSOUM Version 2/Image/SOUMSOUM_icon.png")
        icon_tk = ImageTk.PhotoImage(icon)
        self.master.iconphoto(True, icon_tk)
#=====================================================================
#=====================================================================
        

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - self.master.winfo_reqwidth()) / 2
        y = (screen_height - self.master.winfo_reqheight()) / 2
        self.master.geometry("+%d+%d" % (x, y))

    def set_dark_theme(self):
        self.master.configure(bg='#333333')

    def create_widgets(self):
        self.label_username = ttk.Label(self.master, text="Nom d'utilisateur:")
        self.label_username.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_username = ttk.Entry(self.master)
        self.entry_username.grid(row=1, column=1, padx=10, pady=10)

        self.label_password = ttk.Label(self.master, text="Mot de passe:")
        self.label_password.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_password = ttk.Entry(self.master, show="*")
        self.entry_password.grid(row=2, column=1, padx=10, pady=10)

        # Bouton Déconnexion
        self.button_logout = ttk.Button(self.master, text="Quitter", command=self.logout)
        self.button_logout.grid(row=3, column=0, columnspan=2, pady=20, sticky=tk.W)

        # Bouton Se Connecter
        self.button_login = ttk.Button(self.master, text="Se Connecter", command=self.login)
        self.button_login.grid(row=3, column=1, columnspan=2, pady=20, sticky=tk.E)


#=====================================================================
#=====================================================================
        # Ajout du widget Label pour l'image avec redimensionnement
        image_path = "/home/user/Documents/SOURCE/Application_SOUMSOUM/SOUMSOUM Version 2/Image/Logo_SOUMSOUM.png"
        original_image = Image.open(image_path)
        resized_image = original_image.resize((200, 50))
        photo = ImageTk.PhotoImage(resized_image)
        self.label_image = ttk.Label(self.master, image=photo)
        self.label_image.image = photo  # Stocke la référence à l'image
        self.label_image.grid(row=0, column=0, columnspan=2, pady=10)
#=====================================================================
#=====================================================================
        

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()


#=====================================================================
#=====================================================================
        url = "http://localhost:8069"
        db = "SOUMSOUM"
#=====================================================================
#=====================================================================
        

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})

        if uid:
            print("Connexion réussie!")
            if 'prod' in username:
                print("Connexion production réussie.")
                self.master.destroy()
#=====================================================================
#=====================================================================
                subprocess.Popen([sys.executable, '/home/user/Documents/SOURCE/Application_SOUMSOUM/SOUMSOUM Version 2/Application_Production_V2.py'])
#=====================================================================
#=====================================================================
            elif 'log' in username:
                print("Connexion logistique réussie.")
                self.master.destroy()
#=====================================================================
#=====================================================================
                subprocess.Popen([sys.executable, '/home/user/Documents/SOURCE/Application_SOUMSOUM/SOUMSOUM Version 2/Application_Logistique_V2.py'])
#=====================================================================
#=====================================================================
            else:
                print("Type de connexion non reconnu.")
        else:
            print("Échec de la connexion. Veuillez vérifier vos identifiants.")

    def logout(self):
        # Ajoutez le code de fermeture ici
        print("Déconnexion réussie.")
        self.master.destroy()  # Fermer la fenêtre principale

def main():
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
