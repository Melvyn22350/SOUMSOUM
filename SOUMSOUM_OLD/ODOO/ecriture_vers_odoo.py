import tkinter as tk
from xmlrpc import client

# Informations de connexion à Odoo
url = 'http://localhost:8069'
db = 'demo'
username = 'melvyn.dupas@gmail.com'
password = '123456789'

# Création de la connexion à Odoo
common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

# Création de l'objet pour les opérations sur les OF
models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def modifier_quantite():
    nouvelle_quantite = entry_quantite.get()

    # ID de l'Ordre de Fabrication à mettre à jour
    of_id = 45  # Remplacez par l'ID de votre OF

    # Mise à jour de la quantité de fabrication de l'OF
    models.execute_kw(db, uid, password, 'mrp.production', 'write', [[of_id], {'': float(nouvelle_quantite)}])

    # Exemple : Affichage de la nouvelle quantité dans la console
    print("Nouvelle quantité à fabriquer :", nouvelle_quantite)

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Modifier Quantité OF")

# Libellé et champ de saisie pour la nouvelle quantité
label_quantite = tk.Label(fenetre, text="Nouvelle quantité à fabriquer :")
label_quantite.pack(pady=10)

entry_quantite = tk.Entry(fenetre)
entry_quantite.pack(pady=10)

# Bouton pour valider la modification de quantité
bouton_valider = tk.Button(fenetre, text="Valider", command=modifier_quantite)
bouton_valider.pack(pady=20)

# Lancement de la boucle principale
fenetre.mainloop()