import xmlrpc.client
import tkinter as tk
import io
import base64
import sys
import subprocess
import ctypes
import platform
import os
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import StringVar
from ctypes import wintypes
import tkinter.messagebox as messagebox


#===========================================================================================================
#====================== Application de Logistique ==========================================================
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


# Class représentant l'interface utilisateur de mise à jour du stock
class StockUpdaterGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Mise à jour du stock")
        self.set_icon()
        self.create_widgets()
        self.tree.bind("<ButtonRelease-1>", self.show_selected_article_image)
        self.center_window()

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
                print("Logo non trouvé pour la sociéte.")
        else:
            print("Échec de l'authentification. Veuillez verifier vos identifiants.")

    # Méthode pour créer les widgets
    def create_widgets(self):
        # Création du Treeview pour afficher les articles
        self.tree = ttk.Treeview(self.master, columns=("Nom", "Référence", "Prix", "Quantité en stock"))
        self.tree.heading("#0", text="ID")
        self.tree.heading("Nom", text="Nom de l'article", anchor=tk.CENTER)
        self.tree.heading("Référence", text="Référence", anchor=tk.CENTER)
        self.tree.heading("Prix", text="Prix", anchor=tk.CENTER)
        self.tree.heading("Quantité en stock", text="Quantité en stock", anchor=tk.CENTER)
        self.tree.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        # Centrer le texte dans chaque colonne
        for col in ("Nom", "Référence", "Prix", "Quantité en stock"):
            self.tree.column(col, anchor=tk.CENTER)


#===========================================================================================================
#=== Paramètre pour la connexion Odoo (ne pas modifier sauf si votre serveur à un addressage différents) ===
#===========================================================================================================
        url = "http://172.31.10.158:8069"
        db = "SOUMSOUM"
        username = "melvyndupas01@gmail.com"
        password = "123456789"
#===========================================================================================================
#===========================================================================================================
        
        # Connexion au serveur Odoo et récupération des données d'articles
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        articles = models.execute_kw(db, uid, password, 'product.template', 'search_read', [], {'fields': ['id', 'name', 'default_code', 'list_price', 'qty_available']})

        # Insertion des articles dans le Treeview
        for article in articles:
            self.tree.insert("", tk.END, text=article['id'], values=(article['name'], article['default_code'], "${:.2f}".format(article['list_price']), article['qty_available']))

        # Création des labels et entry pour la référence et la quantité
        self.label_ref = ttk.Label(self.master, text="Référence de l'article:", font=("Helvetica", 10, "bold"), foreground="white", background="#3498db")
        self.label_ref.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)

        self.entry_ref = ttk.Entry(self.master)
        self.entry_ref.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

        self.label_quantity = ttk.Label(self.master, text="Nouvelle quantité:", font=("Helvetica", 10, "bold"), foreground="white", background="#3498db")
        self.label_quantity.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)

        self.entry_quantity = ttk.Entry(self.master)
        self.entry_quantity.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

        # Créer un style pour les boutons
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12, "bold"))

        # Définition du style pour le bouton de déconnexion (rouge)
        style.map("Red.TButton",
                  foreground=[('pressed', 'white'), ('active', 'white')],
                  background=[('pressed', 'red'), ('active', 'red')])

        # Définition du style pour le bouton de mise à jour (vert)
        style.map("Green.TButton",
                  foreground=[('pressed', 'white'), ('active', 'white')],
                  background=[('pressed', 'green'), ('active', 'green')])

        # Création des boutons de mise à jour et de déconnexion
        self.button_update = ttk.Button(self.master, text="Mettre à jour le stock", command=self.update_stock, style="Green.TButton", cursor="hand2")
        self.button_update.grid(row=3, column=0, columnspan=2, pady=20)

        quit_button = ttk.Button(self.master, text="Déconnexion", command=self.quit_program, style="Red.TButton", cursor="hand2")
        quit_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Initialiser le texte de l'étiquette de l'image
        self.selected_reference_text = StringVar(value="Sélectionner une référence")
        self.image_label = tk.Label(self.master, textvariable=self.selected_reference_text)
        self.image_label.grid(row=0, column=2, rowspan=4, padx=10, pady=10)


        # Bouton Actualiser
        self.button_refresh = ttk.Button(self.master, text="Actualiser", command=self.refresh_data, cursor="hand2")
        self.button_refresh.grid(row=5, column=0, columnspan=2, pady=10)

    def refresh_data(self):
        # Réexécuter la requête pour obtenir les articles mis à jour
        url = "http://172.31.10.158:8069"
        db = "SOUMSOUM"
        username = "melvyndupas01@gmail.com"
        password = "123456789"

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        articles = models.execute_kw(db, uid, password, 'product.template', 'search_read', [], {'fields': ['id', 'name', 'default_code', 'list_price', 'qty_available']})

        # Mettre à jour le Treeview avec les nouvelles données
        self.tree.delete(*self.tree.get_children())  # Effacer les anciennes données
        for article in articles:
            self.tree.insert("", tk.END, text=article['id'], values=(article['name'], article['default_code'], "${:.2f}".format(article['list_price']), article['qty_available']))

        # Réinitialiser les champs de texte ou d'autres widgets si nécessaire
        self.entry_ref.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)

        print("Les données ont été actualisées !")


    # Méthode pour mettre à jour le stock
    def update_stock(self):
        # Récupération de la référence de l'article et de la nouvelle quantité
        article_default_code = self.entry_ref.get()
        new_quantity = int(self.entry_quantity.get())  
        
        if new_quantity < 0:
            # Afficher un message d'erreur
            messagebox.showerror("Erreur", "La quantité ne peut pas être négative.")
            return


#===========================================================================================================
#=== Paramètre pour la connexion Odoo (ne pas modifier sauf si votre serveur à un addressage différents) ===
#===========================================================================================================
        url = "http://172.31.10.158:8069"
        db = "SOUMSOUM"
        username = "melvyndupas01@gmail.com"
        password = "123456789"
#===========================================================================================================
#===========================================================================================================
        
        # Connexion au serveur Odoo et récupération des données
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        # Recherche de l'article par la référence
        article_id = models.execute_kw(db, uid, password, 'product.template', 'search', [[('default_code', '=', article_default_code)]])
        
        if article_id:
            # Recherche des entrées de stock pour l'article
            stock_entries = models.execute_kw(db, uid, password, 'stock.quant', 'search_read', [
                [('product_id', '=', article_id[0])]
            ])

            if stock_entries:

                # Mise à jour de la quantité en stock avec la nouvelle quantité
                new_stock_quantity = new_quantity

                models.execute_kw(db, uid, password, 'stock.quant', 'write', [stock_entries[0]['id'], {'quantity': new_stock_quantity}])
                print("Quantite en stock mise à jour avec succes.")

                # Fermeture de la fenêtre actuelle et création d'une nouvelle instance de l'application
                self.master.destroy()
                root = tk.Tk()
                app = StockUpdaterGUI(root)
                app.configure_bg_color('#3498db')  # Ajouter cette ligne pour restaurer la couleur de fond
                root.mainloop()
            else:
                print("Aucune entree stock.quant trouvee pour l'article.")
        else:
            print("Article non trouve.")

    # Méthode pour afficher l'image de l'article sélectionné
    def show_selected_article_image(self, event):
        # Récupération de l'ID et de la référence de l'article sélectionné dans le Treeview
        selected_item_id = self.tree.item(self.tree.selection())['text']
        selected_item_ref = self.tree.item(self.tree.selection())['values'][1]

        # Effacement du contenu actuel de l'entrée et insertion de la référence sélectionnée
        self.entry_ref.delete(0, tk.END)  # Effacer le contenu actuel
        self.entry_ref.insert(0, selected_item_ref)  # Insérer la référence sélectionnée


#===========================================================================================================
#=== Paramètre pour la connexion Odoo (ne pas modifier sauf si votre serveur à un addressage différents) ===
#===========================================================================================================
        url = "http://172.31.10.158:8069"
        db = "SOUMSOUM"
        username = "melvyndupas01@gmail.com"
        password = "123456789"
#===========================================================================================================
#===========================================================================================================

        # Connexion au serveur Odoo et récupération de l'image de l'article sélectionné
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        article_image = models.execute_kw(db, uid, password, 'product.template', 'read', [int(selected_item_id)], {'fields': ['image_1920']})

        # Affichage de l'image s'il y en a une, sinon réinitialisation du texte
        if article_image and 'image_1920' in article_image[0]:
            image_data = article_image[0]['image_1920']
            image = Image.open(io.BytesIO(base64.b64decode(image_data)))
            image.thumbnail((500, 500))
            tk_image = ImageTk.PhotoImage(image)

            self.selected_reference_text.set("")  # Réinitialiser le texte
            self.image_label.configure(image=tk_image)
            self.image_label.image = tk_image
        else:
            self.selected_reference_text.set("Sélectionner une référence")
            self.image_label.configure(image=None)

    # Méthode pour centrer la fenêtre principale
    def center_window(self):
        # Mettre à jour les tâches en attente et récupérer la largeur et la hauteur de l'écran
        self.master.update_idletasks()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculer les positions X et Y pour centrer la fenêtre        
        x_position = (screen_width - self.master.winfo_reqwidth()) // 2
        y_position = (screen_height - self.master.winfo_reqheight()) // 2
        
        # Appliquer les nouvelles positions        
        self.master.geometry("+{}+{}".format(x_position, y_position))

    # Méthode pour configurer la couleur de fond de la fenêtre principale
    def configure_bg_color(self, color):
        self.master.configure(bg=color)

    # Méthode pour quitter le programme
    def quit_program(self):
        print("Programme ferme.")
        self.redirect_to_login()

    # Méthode pour rediriger vers la page de connexion et fermer la fenêtre actuelle
    def redirect_to_login(self):
        print("Redirection vers page de connexion.")
        self.master.destroy()  # Fermez la fenêtre actuelle
        if os_name == "Windows":
            subprocess.Popen([sys.executable, f'{repertoire_parent}//Page_De_Connexion.py'])
        else:      
            subprocess.Popen([sys.executable, f'{repertoire_parent}//Page_De_Connexion.py'])

# Fonction principale            
def main():
    root = tk.Tk()    # Créer la fenêtre principale Tkinter
    app = StockUpdaterGUI(root)     # Créer une instance de l'interface utilisateur du gestionnaire de stocks
    app.configure_bg_color('#3498db')    # Changer la couleur de fond en bleu
    root.mainloop()    # Lancer la boucle principale de l'interface utilisateur

# Exécution de la fonction principale
if __name__ == "__main__":
    main()
