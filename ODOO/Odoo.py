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

def Company(models, db, uid, password, company_name):
    try:
        # Rechercher la compagnie dans la table res.company
        company_id = models.execute_kw(db, uid, password,
                                       'res.company', 'search',
                                       [[['name', '=', company_name]]])

        if company_id:
            company_data = models.execute_kw(db, uid, password,
                                             'res.company', 'read',
                                             [company_id[0]],
                                             {'fields': ['name', 'phone', 'website']})

            if company_data:
                print("Informations de la compagnie", company_data[0]['name'])
                print("Numéro de téléphone:", company_data[0]['phone'])
                print("Site Web:", company_data[0]['website'])
            else:
                print("Compagnie inexistante")
        else:
            print("Compagnie inexistante")

    except Exception as e:
        print(f"Erreur lors de la recherche des informations de la compagnie : {e}")

def Product(models, db, uid, password):
    try:
        # Rechercher l'identifiant de la table product.template
        product_template_id = models.execute_kw(db, uid, password,
                                                'ir.model', 'search',
                                                [[['model', '=', 'product.template']]])

        if product_template_id:
            # Lire tous les produits dans la table product.template
            product_ids = models.execute_kw(db, uid, password,
                                            'product.template', 'search',
                                            [[]])

            if product_ids:
                print("Produits trouvés dans la base de données:")
                for product_id in product_ids:
                    product_data = models.execute_kw(db, uid, password,
                                                     'product.template', 'read',
                                                     [product_id],
                                                     {'fields': ['id', 'name', 'list_price']})

                    product_info = f"#{product_data[0]['id']} – {product_data[0]['name']} = {product_data[0]['list_price']}"
                    print(product_info)
            else:
                print("Aucun produit trouvé dans la base de données")
        else:
            print("La table product.template n'a pas été trouvée")

    except Exception as e:
        print(f"Erreur lors de la recherche des produits : {e}")

class PageArticlesOdoo(tk.Toplevel):
    def __init__(self, root, models, db, uid, password):
        super().__init__(root)
        self.title("Page des Articles Odoo")

        # Utiliser la fonction Product pour récupérer les informations sur les produits
        self.liste_articles = tk.Listbox(self, height=10, width=50)
        self.populate_articles(models, db, uid, password)
        self.liste_articles.pack(pady=20)

        self.bouton_quitter = tk.Button(self, text="Quitter", command=self.quitter)
        self.bouton_quitter.pack()

    def populate_articles(self, models, db, uid, password):
        try:
            # Utiliser la fonction Product pour récupérer les informations sur les produits
            product_ids = models.execute_kw(db, uid, password,
                                            'product.template', 'search',
                                            [[]])

            if product_ids:
                for product_id in product_ids:
                    product_data = models.execute_kw(db, uid, password,
                                                     'product.template', 'read',
                                                     [product_id],
                                                     {'fields': ['name', 'list_price']})

                    product_info = f"{product_data[0]['name']} - Prix: {product_data[0]['list_price']}"
                    self.liste_articles.insert(tk.END, product_info)

            else:
                self.liste_articles.insert(tk.END, "Aucun produit trouvé dans Odoo")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des produits depuis Odoo : {e}")

    def quitter(self):
        self.destroy()

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
    root.deiconify()  # Ajout de cette ligne pour afficher la fenêtre
    root.mainloop()