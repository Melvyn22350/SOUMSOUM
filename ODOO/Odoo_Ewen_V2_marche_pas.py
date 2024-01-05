import os
import base64
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import xmlrpc.client

def Connect(ip="172.31.10.204", password="123456789"):
    # Paramètres de connexion à Odoo
    url = "http://%s:8069" % ip
    db = "demo"
    username = "melvyn.dupas@gmail.com"

    try:
        # Connexion à Odoo en utilisant XML-RPC
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})

        if uid:
            print("Connexion réussie à Odoo")
            print("Adresse URL de connexion:", url)
            print("Identifiant de l'utilisateur (uid):", uid)

            # Récupérer la version d'Odoo
            version = common.version()

            if version:
                print("Version de Odoo:", version.get('server_version'))
            else:
                print("Impossible de récupérer la version d'Odoo")

            # Retourner l'objet models
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            print("Connexion OK")
            return models, uid, url, db
        else:
            print("Échec de la connexion à Odoo. Vérifiez les informations d'identification.")
            return None
    except Exception as e:
        print(f"Échec de la connexion à Odoo. Erreur : {e}")
        return None

def SaveProductImage(models, db, uid, password, product_id, image_name, destination_folder):
    try:
        # Rechercher le produit dans la table product.template
        product_info = models.execute_kw(db, uid, password,
                                         'product.template', 'read',
                                         [product_id],
                                         {'fields': ['image_1920']})

        if product_info and 'image_1920' in product_info[0]:
            # Récupérer l'image encodée en base64 depuis le champ image_1920
            image_data = product_info[0]['image_1920']

            # Convertir l'image de base64 à bytes
            image_bytes = base64.b64decode(image_data)

            # Sauvegarder l'image au format '.png' dans le dossier spécifié
            image_path = os.path.join(destination_folder, image_name)
            with open(image_path, 'wb') as f:
                f.write(image_bytes)

            print(f"Image du produit {product_id} sauvegardée avec succès.")
            return image_path
        else:
            print(f"Produit {product_id} sans image.")
            return None

    except Exception as e:
        print(f"Erreur lors de la sauvegarde de l'image : {e}")
        return None

class PageProduit(tk.Toplevel):
    def __init__(self, root, models, db, uid, password, product_id, product_name, image_path):
        super().__init__(root)
        self.title(f"Produit: {product_name}")

        # Afficher l'image dans la nouvelle fenêtre
        try:
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(self, image=photo)
            label.image = photo  # Garantit que la référence à l'image est conservée

            label.pack(padx=10, pady=10)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir l'image : {e}")

        # Ajouter un bouton pour quitter la fenêtre
        self.bouton_quitter = tk.Button(self, text="Quitter", command=self.destroy)
        self.bouton_quitter.pack(side=tk.RIGHT)

class PageArticlesOdoo(tk.Toplevel):
    def __init__(self, root, models, db, uid, password):
        super().__init__(root)
        self.title("Page des Articles Odoo")

        # Conservez la référence à l'objet models
        self.models = models
        self.db = db
        self.uid = uid
        self.password = password

        # Utiliser la fonction Product pour récupérer les informations sur les produits
        self.liste_articles = tk.Listbox(self, height=10, width=50)
        self.populate_articles()
        self.liste_articles.pack(pady=20)

        # Ajout du bouton de modification des quantités
        self.bouton_modifier_quantite = tk.Button(self, text="Modifier les quantités", command=self.modifier_quantites)
        self.bouton_modifier_quantite.pack(side=tk.LEFT)

        # Ajout de la gestion du double clic sur la liste des articles
        self.liste_articles.bind("<Double-Button-1>", self.afficher_image_article)

        # Ajout du bouton quitter
        self.bouton_quitter = tk.Button(self, text="Quitter", command=self.quitter)
        self.bouton_quitter.pack(side=tk.LEFT)

    def populate_articles(self):
        try:
            # Utiliser la fonction Product pour récupérer les informations sur les produits
            product_ids = self.models.execute_kw(self.db, self.uid, self.password,
                                                 'product.template', 'search',
                                                 [[]])

            if product_ids:
                for product_id in product_ids:
                    product_data = self.models.execute_kw(self.db, self.uid, self.password,
                                                          'product.template', 'read',
                                                          [product_id],
                                                          {'fields': ['name', 'list_price']})

                    product_info = f"{product_data[0]['name']} - Prix: {product_data[0]['list_price']}"
                    self.liste_articles.insert(tk.END, (product_id, product_info))

            else:
                self.liste_articles.insert(tk.END, "Aucun produit trouvé dans Odoo")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des produits depuis Odoo : {e}")

    def afficher_image_article(self, event):
        selected_item = self.liste_articles.curselection()
        if not selected_item:
            return

        product_id, product_info = self.liste_articles.get(selected_item[0])
        image_name_to_save = f"product_image_{product_id}.png"

        # Spécifiez le dossier complet où vous souhaitez sauvegarder les images
        destination_folder = "/home/user/Documents/Test1/Test1"

        # Utiliser la fonction SaveProductImage pour sauvegarder l'image du produit
        image_path = SaveProductImage(self.models, self.db, self.uid, self.password, product_id, image_name_to_save, destination_folder)

        if image_path:
            # Changer le chemin d'accès à l'image dans la fenêtre d'affichage
            self.afficher_image(product_id, product_info, image_path)
        else:
            messagebox.showerror("Erreur", f"Impossible de récupérer l'image pour le produit {product_id}")

    def afficher_image(self, product_id, product_info, image_path):
        # Afficher la nouvelle page pour le produit
        page_produit = PageProduit(self, self.models, self.db, self.uid, self.password, product_id, product_info, image_path)

    def quitter(self):
        self.destroy()

    def modifier_quantites(self):
        selected_item = self.liste_articles.curselection()
        if not selected_item:
            messagebox.showinfo("Sélection requise", "Veuillez sélectionner un article.")
            return

        product_id, _ = self.liste_articles.get(selected_item[0])
        modification_quantite = PageModifierQuantites(self, self.models, self.db, self.uid, self.password, product_id)

class PageModifierQuantites(tk.Toplevel):
    def __init__(self, root, models, db, uid, password, product_id):
        super().__init__(root)
        self.title("Modifier les quantités")

        self.models = models
        self.db = db
        self.uid = uid
        self.password = password
        self.product_id = product_id

        # Label et Entry pour saisir la nouvelle quantité
        self.label_quantite = tk.Label(self, text="Nouvelle quantité:")
        self.entry_quantite = tk.Entry(self)
        self.label_quantite.grid(row=0, column=0, padx=10, pady=10)
        self.entry_quantite.grid(row=0, column=1, padx=10, pady=10)

        # Bouton de validation
        self.bouton_valider = tk.Button(self, text="Valider", command=self.valider_quantite)
        self.bouton_valider.grid(row=1, column=0, columnspan=2, pady=10)

    def valider_quantite(self):
        try:
            nouvelle_quantite = int(self.entry_quantite.get())
            if nouvelle_quantite < 0:
                raise ValueError("La quantité doit être un nombre entier positif ou nul.")

            # Mettre à jour la quantité dans Odoo
            self.models.execute_kw(self.db, self.uid, self.password,
                       'stock.quant', 'write',
                       [[self.product_id], {'quantity': nouvelle_quantite}])

            messagebox.showinfo("Succès", "Quantité modifiée avec succès.")
            self.destroy()

        except ValueError as e:
            messagebox.showerror("Erreur", f"Erreur de saisie : {e}")

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de connexion")

        # Comptes dédiés (utilisateurs pré-enregistrés pour l'exemple)
        self.comptes_utilisateurs = [
            {'nom_utilisateur': 'log', 'mot_de_passe': 'log'},
        ]

        # Création des widgets
        self.label_utilisateur = tk.Label(root, text="Nom d'utilisateur:")
        self.label_mot_de_passe = tk.Label(root, text="Mot de passe:")
        self.entry_utilisateur = tk.Entry(root)
        self.entry_mot_de_passe = tk.Entry(root, show="*")
        self.bouton_connexion = tk.Button(root, text="Se connecter", command=self.gestion_connexion)

        # Paramètres Odoo
        self.models = None
        self.uid = None
        self.url = None
        self.db = None

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
                if nom_utilisateur == 'log':
                    self.ouvrir_page_articles_odoo()
                else:
                    messagebox.showinfo("Connexion réussie", "Bienvenue, " + nom_utilisateur + "!")
                return  # Sortir de la fonction après la connexion réussie

        messagebox.showerror("Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect")

    def ouvrir_page_articles_odoo(self):
        print("Tentative de connexion à Odoo...")
        if not self.models:
            print("Connexion à Odoo...")
            connection_result = Connect()
            if connection_result:
                self.models, self.uid, self.url, self.db = connection_result
            else:
                print("Échec de la connexion à Odoo")
                messagebox.showerror("Erreur", "Impossible de se connecter à Odoo")
                return

        print("Ouverture de la page des articles Odoo...")
        fenetre_articles_odoo = PageArticlesOdoo(self.root, self.models, self.db, self.uid, "123456789")

        print("Fenêtre des articles Odoo ouverte avec succès.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Login(root)
    root.deiconify()
    root.mainloop()
