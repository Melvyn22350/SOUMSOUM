from xmlrpc import client

# Informations de connexion à Odoo
url = 'http://localhost:8069'
db = 'demo'
username = 'melvyn.dupas@gmail.com'
password = '123456789'

# Création de la connexion à Odoo
common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Création de l'objet pour les opérations sur les objets Odoo
models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# ID de l'ordre de fabrication (à remplacer par l'ID de votre ordre de fabrication)
order_id = 11  # Remplacez par l'ID de votre ordre de fabrication

# Nouvelle quantité de fabrication
nouvelle_quantite = 11  # Remplacez par la nouvelle quantité souhaitée

# Mise à jour de la quantité de fabrication
try:
    models.execute_kw(db, uid, password, 'mrp.production', 'write', [[order_id], {'product_qty': float(nouvelle_quantite)}])
    print("Quantité de fabrication mise à jour avec succès.")
except Exception as e:
    print("Une erreur s'est produite :", str(e))