import xmlrpc.client
import tkinter as tk
from tkinter import ttk

class OdooAPI:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        self.uid = self.authenticate()
        self.models = None

    def authenticate(self):
        try:
            uid = self.common.authenticate(self.db, self.username, self.password, {})
            return uid
        except Exception as e:
            print(f"Erreur d'authentification : {e}")
            return None

    def get_order_ids(self):
        try:
            order_ids = self.models.execute_kw(
                self.db, self.uid, self.password,
                'mrp.production', 'search',
                [[['name', 'ilike', 'PA%']]]
            )

            return order_ids
        except Exception as e:
            print(f"Erreur lors de la récupération des numéros d'ordre de fabrication : {e}")
            return []

    def get_order_info(self, order_id):
        try:
            order_info = self.models.execute_kw(
                self.db, self.uid, self.password,
                'mrp.production', 'search_read',
                [[['id', '=', order_id]]],
                {'fields': ['name', 'product_id', 'date_planned_start', 'product_qty', 'qty_produced']}
            )

            return order_info
        except Exception as e:
            print(f"Erreur lors de la récupération de l'ordre de fabrication : {e}")
            return []

    def update_quantity_produced(self, order_id, new_quantity_produced, root):
        try:
            order_id = int(order_id)
            new_quantity_produced = float(new_quantity_produced)

            if new_quantity_produced >= 0:
                self.models.execute_kw(
                    self.db, self.uid, self.password,
                    'mrp.production', 'write',
                    [[order_id], {'qty_produced': new_quantity_produced}]
                )
                print(f"Quantité produite de l'OF {order_id} mise à jour avec succès : {new_quantity_produced}")

                # Planifier le redémarrage de l'application après 2 secondes
                root.after(2000, lambda: self.display_and_modify_orders(root))
            else:
                print("La quantité produite doit être un nombre positif.")
        except ValueError:
            print("Veuillez entrer un nombre valide pour la quantité produite.")
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la quantité produite : {e}")

    def display_and_modify_orders(self, previous_root=None):
        # Création de la connexion à Odoo
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        uid = common.authenticate(self.db, self.username, self.password, {})

        if uid is not None:
            self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))

            if previous_root:
                previous_root.destroy()

            root = tk.Tk()
            root.title("Informations et Modification des Ordres de Fabrication - Odoo")
            root.geometry("1100x500")

            tree = ttk.Treeview(root, columns=("Order ID", "Product Name", "Date Planned", "Quantity", "Qty Produced"), show="headings")
            tree.heading("Order ID", text="Order ID")
            tree.heading("Product Name", text="Product Name")
            tree.heading("Date Planned", text="Date Planned")
            tree.heading("Quantity", text="Quantity")
            tree.heading("Qty Produced", text="Qty Produced")

            order_ids = self.get_order_ids()
            for order_id in order_ids:
                order_info = self.get_order_info(order_id)
                if order_info:
                    order_info = order_info[0]
                    product_name = order_info.get('product_id', '')
                    date_planned = order_info.get('date_planned_start', '')
                    quantity = order_info.get('product_qty', '')
                    qty_produced = order_info.get('qty_produced', '')
                    tree.insert("", "end", values=(order_id, product_name, date_planned, quantity, qty_produced))

            tree.pack(pady=10)

            id_label = tk.Label(root, text="Rentrez l'ordre de fabrication afin de modifier la quantité produite :")
            id_label.pack(pady=10)

            id_entry = tk.Entry(root)
            id_entry.pack(pady=10)

            def open_update_interface():
                order_id = id_entry.get()
                order_info = self.get_order_info(order_id)

                if order_info:
                    if isinstance(order_info, list):
                        order_info = order_info[0]

                    # Fermer la fenêtre principale
                    root.destroy()

                    # Création de l'interface graphique pour la modification de la quantité produite
                    update_root = tk.Tk()
                    update_root.title(f"Modifier Quantité Produite - OF {order_info['name']}")
                    update_root.geometry("400x200")

                    quantity_produced_label = tk.Label(update_root, text="Quantité produite actuelle :")
                    quantity_produced_label.pack(pady=10)

                    quantity_produced_entry = tk.Entry(update_root)
                    quantity_produced_entry.pack(pady=10)
                    quantity_produced_entry.insert(0, str(order_info['qty_produced']))  # Pré-remplir le champ avec la quantité produite actuelle

                    def update_quantity_produced():
                        new_quantity_produced = quantity_produced_entry.get()
                        self.update_quantity_produced(order_info['id'], new_quantity_produced, update_root)

                    update_button = tk.Button(update_root, text="Mettre à jour la quantité produite", command=update_quantity_produced)
                    update_button.pack(pady=10)

                    update_root.mainloop()
                else:
                    print(f"Aucune information trouvée pour l'ordre de fabrication avec l'ID {order_id}")

            submit_button = tk.Button(root, text="Soumettre", command=open_update_interface)
            submit_button.pack(pady=10)

            root.mainloop()
        else:
            print("Échec de l'authentification.")

if __name__ == "__main__":
    odoo_api = OdooAPI('http://localhost:8069', 'demo', 'melvyn.dupas@gmail.com', '123456789')
    odoo_api.display_and_modify_orders()
