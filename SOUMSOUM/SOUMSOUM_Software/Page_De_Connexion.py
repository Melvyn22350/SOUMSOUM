import xmlrpc.client
import tkinter as tk
import subprocess
import base64
import sys
import platform
import ctypes
import os
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
from ctypes import wintypes


#===========================================================================================================
#====================== Application de Connexion ===========================================================
#===========================================================================================================


# Obtenir le nom du système d'exploitation
os_name = platform.system()

# Vérifier le système d'exploitation
if os_name == "Windows":
    print("Le systeme d'exploitation est Windows.")
elif os_name == "Linux":
    print("Le systeme d'exploitation est Linux.")
else:
    print(f"Le systeme d'exploitation est {os_name}.")

# Obtenir le chemin complet du script
chemin_script = os.path.abspath(os.path.realpath(__file__))
print(chemin_script)

# Obtenir le chemin du répertoire parent
repertoire_parent = os.path.dirname(chemin_script)
print(repertoire_parent)

class AuthenticationFailedWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Echec de l'authentification")
        self.master.resizable(False, False)

        # Centrer la fenêtre sur l'écran
        self.center_window()

        label_message = ttk.Label(self.master, text="Echec de l'authentification. Veuillez vérifier vos identifiants.", wraplength=250)
        label_message.pack(pady=20)

        button_ok = ttk.Button(self.master, text="OK", command=self.close_window)
        button_ok.pack(pady=10)

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - 300) // 2  # Largeur de la fenêtre est fixée à 300
        y = (screen_height - 100) // 2  # Hauteur de la fenêtre est fixée à 100
        self.master.geometry("+{}+{}".format(x, y))

    def close_window(self):
        self.master.destroy()
        
# Classe représentant la page de connexion
class LoginPage:
    def __init__(self, master):

        # Initialisation de la fenêtre principale
        self.master = master
        self.master.title("Page de Connexion")
        self.set_icon()
        self.center_window()
        self.create_widgets()
        self.set_dark_theme()

    
    # Méthode pour centrer la fenêtre
    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - self.master.winfo_reqwidth()) / 2
        y = (screen_height - self.master.winfo_reqheight()) / 2
        self.master.geometry("+%d+%d" % (x, y))

    # Méthode pour appliquer un thème sombre
    def set_dark_theme(self):
        dark_gray = '#333333'
        self.master.configure(bg=dark_gray)

    # Méthode pour créer les widgets
    def create_widgets(self):
        bold_font = ("Helvetica", 12, "bold")
        button_style = "TButton"
        cursor_style = "hand2"

        # Création d'un style ttk
        style = ttk.Style()

        # Configuration du style pour changer la couleur de fond au survol
        style.map(button_style,
                background=[('active', '#333333')],
                foreground=[('active', 'white')])

        self.label_username = ttk.Label(self.master, text="Nom d'utilisateur:", background='#333333', foreground='white', font=bold_font)
        self.label_username.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_username = ttk.Entry(self.master)
        self.entry_username.grid(row=1, column=1, padx=10, pady=10)

        self.label_password = ttk.Label(self.master, text="Mot de passe:", background='#333333', foreground='white', font=bold_font)
        self.label_password.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        self.entry_password = ttk.Entry(self.master, show="*")
        self.entry_password.grid(row=2, column=1, padx=10, pady=10)

        self.button_logout = ttk.Button(self.master, text="Quitter", command=self.logout, style=button_style, cursor=cursor_style)
        self.button_logout.grid(row=3, column=0, columnspan=2, pady=20, padx=20, sticky=tk.W)

        self.button_login = ttk.Button(self.master, text="Se connecter", command=self.login, style=button_style, cursor=cursor_style)
        self.button_login.grid(row=3, column=1, columnspan=2, pady=20, padx=20, sticky=tk.E)


        # Ajout du widget Label pour l'image
        self.label_image = ttk.Label(self.master, borderwidth=0, relief="flat")
        self.label_image.grid(row=0, column=0, columnspan=2, pady=10)


#===========================================================================================================
#=== Paramètre pour la connexion Odoo (ne pas modifier sauf si votre serveur à un addressage différents) ===
#===========================================================================================================   
        url = "http://172.31.10.158:8069"
        db = "SOUMSOUM"
        username = "melvyndupas01@gmail.com"
        password = "123456789"
#===========================================================================================================
#===========================================================================================================
        

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        uid = common.authenticate(db, username, password, {})
        user_data = models.execute_kw(db, uid, password,'res.users', 'read',[uid], {'fields': ['image_1920']})
        if user_data and user_data[0].get('image_1920'):
            image_data = user_data[0]['image_1920']
            try:
                decoded_image_data = base64.b64decode(image_data)
                image = Image.open(BytesIO(decoded_image_data))
                resized_image = image.resize((200, 50))
                tk_image = ImageTk.PhotoImage(resized_image)

                # Mettre à jour l'image de l'étiquette existante
                self.label_image.configure(image=tk_image)
                self.label_image.image = tk_image
            except Exception as e:
                print(f"Erreur lors du traitement de l'image : {e}")


#===========================================================================================================
#=== Paramètre pour la connexion Odoo (ne pas modifier sauf si votre serveur à un addressage différents) ===
#===========================================================================================================
    
    # Méthode pour définir l'icône de la fenêtre principale
    def set_icon(self):
        url = "http://172.31.10.158:8069"
        db = "SOUMSOUM"
        username = "melvyndupas01@gmail.com"
        password = "123456789"

#===========================================================================================================
#===========================================================================================================
        

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        
        if uid:
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            company_data = models.execute_kw(db, uid, password,
                                            'res.company', 'read',
                                            [1], {'fields': ['logo']})
            if company_data and company_data[0].get('logo'):
                logo_data = company_data[0]['logo']
                try:
                    decoded_logo_data = base64.b64decode(logo_data)
                    logo_image = Image.open(BytesIO(decoded_logo_data))
                    logo_tk = ImageTk.PhotoImage(logo_image)

                    # Mettre à jour l'icône de la fenêtre principale
                    self.master.iconphoto(True, logo_tk)
                except Exception as e:
                    print(f"Erreur lors du traitement du logo : {e}")
            else:
                print("Logo non trouve pour la societe.")
        else:
            print("Echec de l'authentification. Veuillez verifier vos identifiants.")

        
    # Méthode de gestion de la connexion
    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

#===========================================================================================================
#=== Paramètre pour la connexion Odoo (ne pas modifier sauf si votre serveur à un addressage différents) ===
#===========================================================================================================
        url = "http://172.31.10.158:8069"
        db = "SOUMSOUM"
#===========================================================================================================
#===========================================================================================================
        
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})

        if uid:

            if 'prod' in username:
                print("Connexion production reussie.")
                self.master.destroy()
                if os_name=="Windows":
                    subprocess.Popen([sys.executable, f'{repertoire_parent}//Application_Production.py'])
                else:                            
                    subprocess.Popen([sys.executable, f'{repertoire_parent}//Application_Production.py'])
            elif 'log' in username:
                print("Connexion logistique reussie.")
                self.master.destroy()
                if os_name=="Windows":
                    subprocess.Popen([sys.executable, f'{repertoire_parent}//Application_Logistique.py'])
                else:         
                    subprocess.Popen([sys.executable, f'{repertoire_parent}//Application_Logistique.py'])
            else:
                print("Type de connexion non reconnu.")
        else:
            print("Echec de la connexion. Veuillez verifier vos identifiants.")
            self.show_authentication_failed_window()

    def show_authentication_failed_window(self):
        auth_failed_window = tk.Toplevel()
        app = AuthenticationFailedWindow(auth_failed_window)

    # Méthode de gestion de la déconnexion
    def logout(self):
        print("Deconnexion reussie.")
        self.master.destroy()

# Fonction principale
def main():
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()

# Exécution de la fonction principale
if __name__ == "__main__":
    main()
