import xmlrpc.client
import tkinter as tk
import asyncio

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

def GetProductId(models, db, uid, password, product_name):
    try:
        # Rechercher l'identifiant du produit dans la table product.template
        product_id = models.execute_kw(db, uid, password,
                                       'product.template', 'search',
                                       [[['name', '=', product_name]]])

        if product_id:
            product_data = models.execute_kw(db, uid, password,
                                             'product.template', 'read',
                                             [product_id[0]],
                                             {'fields': ['id', 'name']})
            
            if product_data:
                print(f"Product name = {product_data[0]['name']} => #{product_data[0]['id']}")
            else:
                print(f"Produit {product_name} non trouvé dans la base de données")
        else:
            print(f"Produit {product_name} non trouvé dans la base de données")

    except Exception as e:
        print(f"Erreur lors de la recherche de l'identifiant du produit : {e}")

def create_blank_page(product_data):
    root = tk.Tk()
    root.title("Nouvelle Page")

    # Définir la taille de la fenêtre
    root.geometry("800x600")

    # Ajoutez ici le contenu de votre nouvelle page
    label = tk.Label(root, text="Articles à produire :")
    label.pack()

    any_order_found = False
    for product_info in product_data:
        order_info = product_info.get('order', 'Aucun ordre de fabrication en cours')
        if order_info != 'Aucun ordre de fabrication':
            any_order_found = True
            product_label = tk.Label(root, text=f"Réf: {product_info['reference']} - {product_info['name']} - Ordre: {order_info}")
            product_label.pack()

    if not any_order_found:
        no_order_label = tk.Label(root, text="Aucun ordre de fabrication en cours")
        no_order_label.pack()

    root.mainloop()


async def open_blank_page(product_data):
    # Exécute create_blank_page dans un événement asyncio
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: create_blank_page(product_data))


def ProductNames(models, db, uid, password):
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

            product_names = []
            if product_ids:
                for product_id in product_ids:
                    product_data = models.execute_kw(db, uid, password,
                                                     'product.template', 'read',
                                                     [product_id],
                                                     {'fields': ['name']})
                    
                    product_names.append(product_data[0]['name'])
            return product_names
        else:
            print("La table product.template n'a pas été trouvée")

    except Exception as e:
        print(f"Erreur lors de la recherche des noms des produits : {e}")
        return []

def ProductData(models, db, uid, password):
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

            product_data = []
            if product_ids:
                for product_id in product_ids:
                    # Lire les informations du produit
                    product_info = models.execute_kw(db, uid, password,
                                                     'product.template', 'read',
                                                     [product_id],
                                                     {'fields': ['name', 'list_price', 'default_code']})
                    
        def get_manufacturing_orders(self):
            if self.uid is not None:
                models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
            try:
                # Recherche des ordres de fabrication
                orders = models.execute_kw(self.db, self.uid, self.password,
                                           'mrp.production', 'search_read',
                                           [[]],
                                           {'fields': ['name']})

                return orders
            except Exception as e:
                print(f"Erreur lors de la récupération des ordres de fabrication : {e}")
                return []


    except Exception as e:
        print(f"Erreur lors de la recherche des informations des produits : {e}")
        return []


# Exemple d'utilisation des fonctions Connect, Company, Product et GetProductId
if __name__ == "__main__":
    models, uid, url, db = Connect()

    if models:
        Company(models, db, uid, "123456789", "SOUMSOUM")
        Product(models, db, uid, "123456789")
        GetProductId(models, db, uid, "123456789", "Storage Box")
        product_data = ProductData(models, db, uid, "123456789")
        asyncio.run(open_blank_page(product_data))
    else:
        print("Echec Connexion")