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

# Exemple d'utilisation des fonctions Connect, Company, Product et GetProductId
if __name__ == "__main__":
    models, uid, url, db = Connect()

    if models:
        Company(models, db, uid, "123456789", "SOUMSOUM")
        Product(models, db, uid, "123456789")
        GetProductId(models, db, uid, "123456789", "Storage Box")
    else:
        print("Echec Connexion")
