import xmlrpc.client
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import base64
import sys
from io import BytesIO
import platform
import ctypes
from ctypes import wintypes


# Obtenir le nom du système d'exploitation
os_name = platform.system()

# Vérifier le système d'exploitation
if os_name == "Windows":
    print("Le systeme d'exploitation est Windows.")
elif os_name == "Linux":
    print("Le systeme d'exploitation est Linux.")
else:
    print(f"Le systeme d'exploitation est {os_name}.")


class LoginPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Page de Connexion")
        self.set_icon()
        self.center_window()
        self.create_widgets()
        self.set_dark_theme()

    

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - self.master.winfo_reqwidth()) / 2
        y = (screen_height - self.master.winfo_reqheight()) / 2
        self.master.geometry("+%d+%d" % (x, y))

    def set_dark_theme(self):
        dark_gray = '#333333'
        self.master.configure(bg=dark_gray)

    def create_widgets(self):
        bold_font = ("Helvetica", 12, "bold")
        button_style = "TButton"
        cursor_style = "hand2"

        # Create a ttk style
        style = ttk.Style()

        # Configure the style to change background color on hover
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
        
        username = "melvyndupas01@gmail.com"
        password = "123456789"
        url = "http://172.31.11.79:8069"
        db = "SOUMSOUM"

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


    def set_icon(self):
        url = "http://172.31.11.79:8069"
        db = "SOUMSOUM"
        username = "melvyndupas01@gmail.com"
        password = "123456789"

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

        

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        url = "http://172.31.11.79:8069"
        db = "SOUMSOUM"

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})

        if uid:

            if 'prod' in username:
                print("Connexion production reussie.")
                self.master.destroy()
                if os_name=="Windows":
                    subprocess.Popen([sys.executable, 'Application_Production.py'])
                else:         
                    subprocess.Popen([sys.executable, '/home/user/Documents/SOURCE/SOUMSOUM/SOUMSOUM Version 4/Application_Production.py'])
                
            elif 'log' in username:
                print("Connexion logistique reussie.")
                self.master.destroy()
                if os_name=="Windows":
                    subprocess.Popen([sys.executable, 'Application_Logistique.py'])
                else:         
                    subprocess.Popen([sys.executable, '/home/user/Documents/SOURCE/SOUMSOUM/SOUMSOUM Version 4/Application_Logistique.py'])
            else:
                print("Type de connexion non reconnu.")
        else:
            print("Echec de la connexion. Veuillez verifier vos identifiants.")

    def logout(self):
        print("Deconnexion reussie.")
        self.master.destroy()

def main():
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
