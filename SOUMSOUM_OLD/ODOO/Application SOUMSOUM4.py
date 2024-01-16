import xmlrpc.client

# Informations de connexion à votre instance Odoo
url = "http://localhost:8069"
db = "SOUMSOUMv2"
username = "melvyndupas01@gmail.com"
password = "123456789"

# Établir la connexion XML-RPC avec Odoo
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Connexion à l'objet models pour effectuer des opérations
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# Rechercher l'ID de l'article que vous souhaitez mettre à jour par la référence interne
article_default_code = '100'
article_id = models.execute_kw(db, uid, password, 'product.template', 'search', [[('default_code', '=', article_default_code)]])

if article_id:
    print("ID de l'article trouvé :", article_id)

    # Rechercher les entrées du modèle stock.quant associées à l'article
    stock_entries = models.execute_kw(db, uid, password, 'stock.quant', 'search_read', [
        [('product_id', '=', article_id[0])]
    ])

    if stock_entries:
        # Mettre à jour la quantité en ajoutant la nouvelle quantité
        new_stock_quantity = stock_entries[0]['quantity'] + 10

        # Mettre à jour la stock.quant associée à l'article
        models.execute_kw(db, uid, password, 'stock.quant', 'write', [stock_entries[0]['id'], {'quantity': new_stock_quantity}])
        print("Quantité en stock mise à jour avec succès.")
    else:
        print("Aucune entrée stock.quant trouvée pour l'article.")
else:
    print("Article non trouvé.")
